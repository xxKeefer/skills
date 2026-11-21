#!/usr/bin/env python3
"""Write or update an HTML report. Usage: write_report.py <report path> <run json path>"""
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "template.html")
BLOCK = re.compile(r'(<script type="application/json" id="runs">)(.*?)(</script>)', re.S)


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def read_block(text, label):
    match = BLOCK.search(text)
    if not match:
        fail(f"{label}: no runs block found.")
    try:
        return json.loads(match.group(2))
    except ValueError as error:
        fail(f"{label}: the runs block does not parse: {error}")


def main():
    if len(sys.argv) != 3:
        fail("Usage: write_report.py <report path> <run json path>")
    report = os.path.abspath(sys.argv[1])
    with open(sys.argv[2], encoding="utf-8") as f:
        try:
            given = json.load(f)
        except ValueError as error:
            fail(f"run json does not parse: {error}")
    new_run = given.get("run")
    if not isinstance(new_run, dict):
        fail("run json has no run object.")

    earlier = []
    if os.path.exists(report):
        with open(report, encoding="utf-8") as f:
            earlier = read_block(f.read(), "runs block in the report").get("runs", [])

    new_run = dict(new_run)
    new_run["run"] = max([r["run"] for r in earlier], default=0) + 1
    new_run.setdefault("date", datetime.date.today().isoformat())
    for n, row in enumerate(new_run.get("rows", []), start=1):
        row.setdefault("id", f"r{new_run['run']}.{n}")

    data = {"title": given.get("title", "Report"), "path": report, "skill": given.get("skill", "")}
    if "track" in given:
        data["track"] = given["track"]
    data["runs"] = sorted([new_run] + earlier, key=lambda r: r["run"], reverse=True)

    body = json.dumps(data, indent=1, ensure_ascii=False).replace("</", "<\\/")
    with open(TEMPLATE, encoding="utf-8") as f:
        template = f.read()
    text = BLOCK.sub(lambda m: m.group(1) + "\n" + body + "\n" + m.group(3), template, count=1)

    with open(report, "w", encoding="utf-8") as f:
        f.write(text)

    folder = os.path.dirname(report)
    names = [n for n in os.listdir(folder) if n.endswith(".html")]
    names.sort(key=lambda n: os.path.getmtime(os.path.join(folder, n)), reverse=True)
    with open(os.path.join(folder, "reports.js"), "w", encoding="utf-8") as f:
        f.write("window.REPORTS = " + json.dumps(names) + ";\n")

    print("file://" + report)


main()
