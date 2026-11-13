"""Adds a screenshots visual to the latest run of a /write-report HTML report.

Usage: python3 -I add-report-screenshots.py <report.html> <items.json>

items.json is a list of {"id", "heading", "files": [...]} or {"id", "heading", "skip": "<reason>"}.
File paths are relative to the report folder. A second call replaces the earlier screenshots visual.
"""

import html
import json
import re
import sys

QUESTION = "Screenshots from the QA run. Open an item to see its images."
BLOCK = re.compile(r'(<script[^>]*type="application/json"[^>]*>)(.*?)(</script>)', re.S)


def item_html(item):
    label = f'{html.escape(item["id"])} · {html.escape(item["heading"])}'
    if "skip" in item:
        return f'<p class="font-mono text-xs text-muted">{label}. Skipped: {html.escape(item["skip"])}</p>'
    images = "".join(
        f'<a href="{html.escape(f)}" target="_blank">'
        f'<img src="{html.escape(f)}" alt="{html.escape(f)}" class="border-2 border-paper max-w-full"></a>'
        for f in item["files"]
    )
    return (
        f'<details><summary class="cursor-pointer font-mono text-xs text-mag">{label}</summary>'
        f'<div class="mt-2 space-y-2">{images}</div></details>'
    )


def main(report_path, items_path):
    items = json.load(open(items_path))
    page = open(report_path).read()
    match = BLOCK.search(page)
    data = json.loads(match.group(2))
    run = data["runs"][-1]
    visuals = [v for v in run.get("visuals", []) if v.get("question") != QUESTION]
    body = '<div class="space-y-2">' + "".join(item_html(i) for i in items) + "</div>"
    run["visuals"] = visuals + [{"question": QUESTION, "html": body}]
    block = "\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n    "
    page = page[: match.start(2)] + block + page[match.end(2) :]
    open(report_path, "w").write(page)
    print(f'runs: {len(data["runs"])}, details: {body.count("<details>")}')


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
