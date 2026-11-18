#!/usr/bin/env python3
"""Check the runs block of an HTML report. Usage: check_report.py <report path>"""
import json
import re
import sys

BLOCK = re.compile(r'(<script type="application/json" id="runs">)(.*?)(</script>)', re.S)


def problems(data):
    found = []

    def need(ok, problem, fix):
        if not ok:
            found.append((problem, fix))

    if not isinstance(data, dict):
        return [("the runs block is not an object", "write an object with title, path, skill, and runs")]
    for key in ("title", "path", "skill"):
        need(isinstance(data.get(key), str), f"top key `{key}` is missing or not a string", f"set `{key}` to a string")
    runs = data.get("runs")
    if not isinstance(runs, list):
        need(False, "top key `runs` is missing or not a list", "set `runs` to a list of runs")
        return found
    numbers = []
    seen = set()
    for run in runs:
        if not isinstance(run, dict):
            need(False, "a run is not an object", "make each run an object")
            continue
        number = run.get("run")
        ok = isinstance(number, int) and not isinstance(number, bool)
        need(ok, "a run has no integer `run`", "set `run` to an integer")
        if ok:
            numbers.append(number)
        label = f"run {number}"
        for key in ("title", "date", "answer"):
            need(isinstance(run.get(key), str), f"{label}: `{key}` is missing or not a string", f"set `{key}` to a string")
        rows = run.get("rows")
        if rows:
            columns = run.get("columns")
            good = isinstance(columns, list) and columns and all(
                isinstance(c, dict) and "key" in c and "label" in c for c in columns
            )
            need(good, f"{label}: rows have no valid `columns`", "give `columns` a list of objects with `key` and `label`")
            for row in rows:
                if not isinstance(row, dict):
                    need(False, f"{label}: a row is not an object", "make each row an object")
                    continue
                row_id = row.get("id")
                need(isinstance(row_id, str), f"{label}: a row has no string `id`", "set `id` to a string")
                if isinstance(row_id, str):
                    need(row_id not in seen, f"duplicate row id `{row_id}`", "give each row a unique `id`")
                    seen.add(row_id)
                need(isinstance(row.get("cells"), dict), f"{label}: row `{row_id}` has no `cells` object", "set `cells` to an object")
                ticks = row.get("ticks")
                need(
                    ticks is None or (isinstance(ticks, list) and all(isinstance(t, str) for t in ticks)),
                    f"{label}: row `{row_id}` has bad `ticks`",
                    "make `ticks` a list of strings",
                )
    need(
        len(set(numbers)) == len(numbers) and numbers == sorted(numbers, reverse=True),
        "run numbers are not unique and in falling order",
        "number the runs, newest first",
    )
    return found


def main():
    if len(sys.argv) != 2:
        print("Usage: check_report.py <report path>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        text = f.read()
    match = BLOCK.search(text)
    if not match:
        print(f"{path}: no runs block found. Fix: write the file with write_report.py.")
        sys.exit(1)
    try:
        data = json.loads(match.group(2))
    except ValueError as error:
        print(f"{path}: the runs block does not parse: {error}. Fix: correct the JSON in the block.")
        sys.exit(1)
    found = problems(data)
    for problem, fix in found:
        print(f"{path}: {problem}. Fix: {fix}.")
    if found:
        sys.exit(1)
    print("ok")


main()
