"""V17 finite-search controller. Does not execute or modify V16 algorithms."""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import json
import math
from pathlib import Path
import sqlite3
import uuid


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


@dataclass(frozen=True)
class Space:
    """Finite Cartesian space, indexed lazily; no materialized trillion-row grid."""
    axes: tuple

    @classmethod
    def create(cls, axes):
        normalized = []
        for key, values in sorted(axes.items()):
            unique = {}
            for value in values:
                unique.setdefault(canonical(value), value)
            if not unique:
                raise ValueError(f"Empty axis: {key}")
            normalized.append((key, tuple(unique.values())))
        if not normalized:
            raise ValueError("An explicit search space is required")
        return cls(tuple(normalized))

    @property
    def total(self):
        return math.prod(len(values) for _, values in self.axes)

    def candidate(self, index):
        if not 0 <= index < self.total:
            raise IndexError(index)
        result = {}
        for key, values in reversed(self.axes):
            index, remainder = divmod(index, len(values))
            result[key] = values[remainder]
        return result


class RunStore:
    """One isolated experiment database, used by one coordinator, not workers.

    A result is committed once. After a crash a RUNNING task can be recovered,
    so execution is at-least-once, but committed results are never rerun.
    All workers must have stopped before recover_interrupted() is called.
    """
    def __init__(self, path, space, context):
        required = {"version", "run_id", "dataset_sha256", "engine", "evaluation"}
        if not required <= context.keys() or any(not context[k] for k in required):
            raise ValueError("Full version/run/data/engine/evaluation identity required")
        self.space = space
        self.context = json.loads(canonical(context))
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS tasks(
                idx TEXT PRIMARY KEY, parameters TEXT NOT NULL,
                status TEXT NOT NULL, token TEXT, result TEXT, net REAL, error TEXT);
            CREATE INDEX IF NOT EXISTS task_status ON tasks(status);
            CREATE INDEX IF NOT EXISTS task_ranking ON tasks(status,net);
        ''')
        identity = canonical({"context": context, "axes": space.axes})
        try:
            with self.transaction():
                stored = self.get("identity")
                if stored is None:
                    for key, value in {"identity": identity, "cursor": "0", "paused": "0"}.items():
                        self.set(key, value)
                elif stored != identity:
                    raise ValueError("Checkpoint belongs to different data, version or search space")
        except Exception:
            self.db.close()
            raise

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
        except BaseException:
            self.db.execute("ROLLBACK")
            raise
        else:
            self.db.execute("COMMIT")

    def get(self, key):
        row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row[0] if row else None

    def set(self, key, value):
        self.db.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (key, str(value)))

    def enqueue(self, index):
        parameters = canonical(self.space.candidate(index))
        self.db.execute("INSERT OR IGNORE INTO tasks(idx,parameters,status) VALUES (?,?,'PENDING')",
                        (str(index), parameters))

    def prioritize(self, indices):
        """Adaptive proposals may only reorder existing finite-space members."""
        with self.transaction():
            for index in indices:
                self.enqueue(index)

    def claim(self, block_size=1000):
        if not isinstance(block_size, int) or block_size < 1:
            raise ValueError("Positive block size required")
        with self.transaction():
            if self.get("paused") == "1":
                return []
            pending = self.db.execute("SELECT count(*) FROM tasks WHERE status='PENDING'").fetchone()[0]
            cursor = int(self.get("cursor"))
            while pending < block_size and cursor < self.space.total:
                before = self.db.total_changes
                self.enqueue(cursor)
                pending += self.db.total_changes - before
                cursor += 1
            self.set("cursor", cursor)
            rows = self.db.execute("SELECT idx,parameters FROM tasks WHERE status='PENDING' ORDER BY rowid LIMIT ?",
                                   (block_size,)).fetchall()
            result = []
            for idx, parameters in rows:
                token = uuid.uuid4().hex
                self.db.execute("UPDATE tasks SET status='RUNNING',token=? WHERE idx=?", (token, idx))
                result.append({"index": int(idx), "token": token, "parameters": json.loads(parameters)})
            return result

    def finish(self, task, result=None, error=None):
        if (result is None) == (error is None):
            raise ValueError("Provide exactly a completed result or an error")
        encoded, net = None, None
        if result is not None:
            if result.get("context") != self.context:
                raise ValueError("Result identity mismatch")
            if result.get("parameters") != task["parameters"]:
                raise ValueError("Result parameters mismatch")
            net = result["net"]
            if isinstance(net, bool) or not isinstance(net, (int, float)) or not math.isfinite(net):
                raise ValueError("NET must be finite")
            encoded = canonical(result)
        with self.transaction():
            row = self.db.execute("SELECT parameters FROM tasks WHERE idx=? AND status='RUNNING' AND token=?",
                                  (str(task["index"]), task["token"])).fetchone()
            if row is None or row[0] != canonical(task["parameters"]):
                raise ValueError("Stale, duplicate or invalid completion")
            self.db.execute("UPDATE tasks SET status=?,result=?,net=?,error=?,token=NULL WHERE idx=?",
                            ("DONE" if result is not None else "ERROR", encoded, net, error, str(task["index"])))

    def pause(self):
        with self.transaction():
            self.set("paused", "1")

    def resume(self):
        with self.transaction():
            self.set("paused", "0")

    def recover_interrupted(self):
        with self.transaction():
            self.db.execute("UPDATE tasks SET status='PENDING',token=NULL WHERE status='RUNNING'")

    def progress(self, block_size=1000):
        if block_size < 1:
            raise ValueError("Positive block size required")
        counts = dict(self.db.execute("SELECT status,count(*) FROM tasks GROUP BY status"))
        done, errors = counts.get("DONE", 0), counts.get("ERROR", 0)
        resolved = done + errors
        finished = resolved == self.space.total
        state = ("COMPLETED_WITH_ERRORS" if errors else "COMPLETED") if finished else (
            "PAUSED" if self.get("paused") == "1" else "IN_PROGRESS")
        return {"state": state, "total": self.space.total, "completed": done, "errors": errors,
                "running": counts.get("RUNNING", 0), "queued": counts.get("PENDING", 0),
                "unplanned": self.space.total - sum(counts.values()),
                "resolved_percent": resolved * 100 / self.space.total,
                "block_size": block_size,
                "nominal_blocks": (self.space.total + block_size - 1) // block_size}

    def best(self):
        # No archive fallback; all records in this database have the same identity.
        row = self.db.execute("SELECT result FROM tasks WHERE status='DONE' ORDER BY net DESC,rowid ASC LIMIT 1").fetchone()
        return json.loads(row[0]) if row else None

    def close(self):
        self.db.close()

