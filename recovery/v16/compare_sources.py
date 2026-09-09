"""Compare local sources against recovered code, ignoring locations only."""
import json
import marshal
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "Pump.exe" / "src"

def signature(code):
    return (code.co_code, code.co_names, code.co_varnames,
            code.co_freevars, code.co_cellvars, code.co_argcount,
            code.co_posonlyargcount, code.co_kwonlyargcount, code.co_flags,
            code.co_exceptiontable,
            tuple(signature(c) if isinstance(c, types.CodeType) else c
                  for c in code.co_consts))

rows = []
for path in sorted((ROOT / "compiled").rglob("*.pyc")):
    source = SOURCE / path.relative_to(ROOT / "compiled").with_suffix(".py")
    saved = marshal.loads(path.read_bytes()[16:])
    status = "SOURCE_MISSING"
    if source.exists():
        current = compile(source.read_bytes(), saved.co_filename, "exec", optimize=0)
        status = "MATCH_EXECUTABLE_STRUCTURE" if signature(saved) == signature(current) else "DIFFERENT"
    rows.append({"source": str(source), "status": status})
(ROOT / "source_comparison.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
for status in sorted({r["status"] for r in rows}):
    print(status, sum(r["status"] == status for r in rows))
for row in rows:
    print(row["status"], Path(row["source"]).name)

