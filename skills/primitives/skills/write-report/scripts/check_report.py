#!/usr/bin/env python3
"""Check the runs block of an HTML report. Usage: check_report.py <report path>"""
import argparse
import collections
import json
import re
import sys

BLOCK = re.compile(r'(<script type="application/json" id="runs">)(.*?)(</script>)', re.S)


TYPES = ("mermaid", "bars", "table", "html")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def texts(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from texts(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            if key not in ("mermaid", "html"):
                yield from texts(item)


def check_links(run, label):
    return [
        (f"{label}: link `{match.group(0)}` has no web URL", "start the URL with `https://`, or write the text with no link")
        for text in texts(run)
        for match in LINK.finditer(text)
        if not match.group(2).startswith(("https://", "http://"))
    ]


def check_visuals(visuals, label):
    if visuals is None:
        return []
    if not isinstance(visuals, list):
        return [(f"{label} has bad `visuals`", "make `visuals` a list of objects")]
    found = []
    for v in visuals:
        if not isinstance(v, dict):
            found.append((f"{label} has a visual that is not an object", "make each visual an object"))
            continue
        if not isinstance(v.get("question"), str):
            found.append((f"{label} has a visual with no string `question`", "set `question` to the question that the visual answers"))
        if sum(key in v for key in TYPES) != 1:
            found.append((f"{label} has a visual without exactly one of `mermaid`, `bars`, `table`, `html`", "give each visual one type"))
    return found


def check_row(row, label):
    if not isinstance(row, dict):
        return [(f"{label}: a row is not an object", "make each row an object")]
    found = []
    row_id = row.get("id")
    if not isinstance(row_id, str):
        found.append((f"{label}: a row has no string `id`", "set `id` to a string"))
    if not isinstance(row.get("cells"), dict):
        found.append((f"{label}: row `{row_id}` has no `cells` object", "set `cells` to an object"))
    ticks = row.get("ticks")
    if not (ticks is None or (isinstance(ticks, list) and all(isinstance(t, str) for t in ticks))):
        found.append((f"{label}: row `{row_id}` has bad `ticks`", "make `ticks` a list of strings"))
    found.extend(check_visuals(row.get("visuals"), f"{label}: row `{row_id}`"))
    return found


def check_run(run):
    if not isinstance(run, dict):
        return None, [("a run is not an object", "make each run an object")]
    found = []
    number = run.get("run")
    ok = isinstance(number, int) and not isinstance(number, bool)
    if not ok:
        found.append(("a run has no integer `run`", "set `run` to an integer"))
    label = f"run {number}"
    for key in ("title", "date", "answer"):
        if not isinstance(run.get(key), str):
            found.append((f"{label}: `{key}` is missing or not a string", f"set `{key}` to a string"))
    found.extend(check_links(run, label))
    rows = run.get("rows")
    visuals = run.get("visuals")
    shown = isinstance(visuals, list) and any(isinstance(v, dict) and not v.get("fold") for v in visuals)
    found.extend(check_visuals(visuals, label))
    if rows and not shown:
        found.append((f"{label}: has rows but no visual that shows unfolded", "add a visual before the rows, such as `bars` of the rows by status"))
    if rows and not isinstance(rows, list):
        found.append((f"{label}: `rows` is not a list", "set `rows` to a list"))
    elif rows:
        columns = run.get("columns")
        good = isinstance(columns, list) and columns and all(
            isinstance(c, dict) and "key" in c and "label" in c for c in columns
        )
        if not good:
            found.append((f"{label}: rows have no valid `columns`", "give `columns` a list of objects with `key` and `label`"))
        for row in rows:
            found.extend(check_row(row, label))
    return (number if ok else None), found


def problems(data):
    if not isinstance(data, dict):
        return [("the runs block is not an object", "write an object with title, path, skill, and runs")]
    found = []
    for key in ("title", "path", "skill"):
        if not isinstance(data.get(key), str):
            found.append((f"top key `{key}` is missing or not a string", f"set `{key}` to a string"))
    runs = data.get("runs")
    if not isinstance(runs, list):
        found.append(("top key `runs` is missing or not a list", "set `runs` to a list of runs"))
        return found
    numbers = []
    for run in runs:
        number, run_found = check_run(run)
        found.extend(run_found)
        if number is not None:
            numbers.append(number)
    ids = collections.Counter(
        row["id"]
        for run in runs
        if isinstance(run, dict)
        for row in (run.get("rows") if isinstance(run.get("rows"), list) else [])
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    )
    for row_id, count in ids.items():
        if count > 1:
            found.append((f"duplicate row id `{row_id}`", "give each row a unique `id`"))
    if len(set(numbers)) != len(numbers) or numbers != sorted(numbers, reverse=True):
        found.append(("run numbers are not unique and in falling order", "number the runs, newest first"))
    return found


def main(argv):
    parser = argparse.ArgumentParser(prog="check_report.py", description="Check the runs block of an HTML report.")
    parser.add_argument("report")
    path = parser.parse_args(argv[1:]).report
    with open(path, encoding="utf-8") as f:
        text = f.read()
    match = BLOCK.search(text)
    if not match:
        print(f"{path}: no runs block found. Fix: write the file with write_report.py.")
        return 1
    try:
        data = json.loads(match.group(2))
    except ValueError as error:
        print(f"{path}: the runs block does not parse: {error}. Fix: correct the JSON in the block.")
        return 1
    found = problems(data)
    for problem, fix in found:
        print(f"{path}: {problem}. Fix: {fix}.")
    if found:
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
