"""Convert a hand-written test set from its one-line-per-case text form to JSONL.

The text form is what a person writes (see data/test_hand5.txt):

    C | request | tool arg=value arg?=value arg~=[word, word]
    A | request          (ambiguous: the right answer is to ask, no call)
    N | request          (no tool needed)
    U | request          (no tool can do it)

Values: `a|b` is any_of; `~=[...]` is contains_all; `?=` marks the argument
optional; `"..."` is an exact string; digits are integers. A path value is
expanded to the spellings that name the same place (`x`, `x/`, `./x`), so the
writer does not have to list them. Nothing else is interpreted: the text file
is the source of truth and the JSONL is regenerated from it byte for byte.

    python -m toolcall.handset data/test_hand5.txt   # writes data/test_hand5.jsonl
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NO_CALL = {"A": "ambiguous", "N": "no_tool", "U": "unsupported"}
_ARG = re.compile(r'(\w+)(\?=|~=|=)(\[[^\]]*\]|"[^"]*"|\S+)')
_ROOTS = (".", "/")


class HandSetError(ValueError):
    pass


def _path_spellings(value: str, is_dir: bool) -> list[str]:
    if value in _ROOTS:
        return [value]
    base = value.removeprefix("./").rstrip("/")
    return [base, f"{base}/", f"./{base}"] if is_dir else [base, f"./{base}"]


def _value(tool: str, key: str, op: str, raw: str) -> object:
    if op == "~=":
        if not (raw.startswith("[") and raw.endswith("]")):
            raise HandSetError(f"{key}~= needs [word, word]: {raw}")
        words = [w.strip() for w in raw[1:-1].split(",") if w.strip()]
        if not words:
            raise HandSetError(f"{key}~= has no words")
        return {"contains_all": words}
    if raw.startswith('"') and raw.endswith('"') and len(raw) >= 2:
        return raw[1:-1]
    alternatives = raw.split("|")
    if key == "path":
        is_dir = tool == "fs_list" or raw.endswith("/")
        spellings = [s for a in alternatives for s in _path_spellings(a, is_dir)]
        return {"any_of": list(dict.fromkeys(spellings))}
    values = [int(a) if a.isdigit() else a for a in alternatives]
    return values[0] if len(values) == 1 else {"any_of": values}


def _expected(spec: str) -> dict:
    tool, _, rest = spec.strip().partition(" ")
    if not tool:
        raise HandSetError("a C case needs a tool")
    leftover = _ARG.sub("", rest).strip()
    if leftover:
        raise HandSetError(f"unparsed argument text: {leftover!r}")
    arguments, optional = {}, []
    for key, op, raw in _ARG.findall(rest):
        if key in arguments:
            raise HandSetError(f"argument {key} given twice")
        arguments[key] = _value(tool, key, op, raw)
        if op == "?=":
            optional.append(key)
    expected = {"name": tool, "arguments": arguments}
    if optional:
        expected["optional"] = optional
    return expected


def _row(kind: str, fields: list[str]) -> tuple[str, dict | None]:
    if kind == "C":
        if len(fields) != 3:
            raise HandSetError("C needs: C | request | call")
        expected = _expected(fields[2])
        return expected["name"], expected
    if kind in NO_CALL:
        if len(fields) != 2:
            raise HandSetError(f"{kind} needs: {kind} | request")
        return NO_CALL[kind], None
    raise HandSetError(f"unknown type {kind!r}")


def convert(text: str, split: str) -> list[dict]:
    rows = []
    for number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = [f.strip() for f in line.split(" | ")]
        try:
            intent, expected = _row(fields[0], fields)
        except HandSetError as e:
            raise HandSetError(f"line {number}: {e}") from None
        rows.append({"id": f"{split}-{len(rows):03d}", "split": split, "intent": intent,
                     "family": -1, "request": fields[1], "expected": expected, "reply": None})
    return rows


def to_jsonl(rows: list[dict]) -> str:
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def main(argv: list[str]) -> None:
    if len(argv) != 1:
        raise SystemExit("usage: python -m toolcall.handset data/<split>.txt")
    source = Path(argv[0])
    rows = convert(source.read_text(encoding="utf-8"), source.stem)
    target = source.with_suffix(".jsonl")
    target.write_text(to_jsonl(rows), encoding="utf-8")
    print(f"{len(rows)} cases -> {target}")


if __name__ == "__main__":
    main(sys.argv[1:])
