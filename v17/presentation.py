"""Presentation rules independent of the engine and historical archive format."""
import math

PALETTE = dict(background="#101113", panel="#191B1F", text="#ECEDEF",
               muted="#A5ABB5", accent="#F0B90B", positive="#2EBD85", negative="#F6465D")
COLUMNS = ("id", "version", "net", "trades", "windows", "status", "date")


def archive_rows(rows, version=None, minimum_net=0.20, column="net", descending=True):
    if column not in COLUMNS:
        raise ValueError("Unknown sorting column")
    selected = []
    for row in rows:
        if version is not None and str(row.get("version")) != str(version):
            continue
        net = row.get("net")
        if minimum_net is not None and (not isinstance(net, (int, float)) or
                                        not math.isfinite(net) or net < minimum_net):
            continue
        selected.append(row)

    def value(row):
        item = row.get(column)
        if column in ("net", "trades", "windows"):
            if isinstance(item, bool) or not isinstance(item, (int, float)) or not math.isfinite(item):
                return None
            return item
        return str(item) if item is not None else None

    # Missing values always last; stable ties preserve identity/selection.
    valid = [r for r in selected if value(r) is not None]
    missing = [r for r in selected if value(r) is None]
    return sorted(valid, key=value, reverse=descending) + missing


def current_leader(rows, context):
    valid = [row for row in rows if row.get("context") == context
             and row.get("status") == "DONE"
             and isinstance(row.get("net"), (int, float))
             and not isinstance(row["net"], bool) and math.isfinite(row["net"])]
    return max(valid, key=lambda row: row["net"], default=None)


def progress_text(progress):
    return (f"Всего в плане: {progress['total']:,} · Готово: {progress['completed']:,} · "
            f"Ошибки: {progress['errors']:,}\n"
            f"В работе: {progress['running']:,} · Порция: до {progress['block_size']:,} вариантов · "
            f"Состояние: {progress['state']}")

