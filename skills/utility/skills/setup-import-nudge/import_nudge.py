#!/usr/bin/env python3
import json
import pathlib
import re
import sys

CONFIG_PATH = pathlib.Path(__file__).parent / "import-nudge.config.json"


def messages(path, text, rules):
    """Returns the message of each rule whose path and content patterns both match the file."""
    return [
        rule["message"]
        for rule in rules
        if re.search(rule["path"], path) and re.search(rule["content"], text)
    ]


def main():
    try:
        payload = json.load(sys.stdin)
        rules = json.loads(CONFIG_PATH.read_text())["rules"]
        path = payload["tool_input"]["file_path"]
        text = pathlib.Path(path).read_text()
        found = messages(path, text, rules)
    except (OSError, ValueError, KeyError, TypeError, re.error):
        return
    if found:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"{path}: " + " ".join(found),
            }
        }))


if __name__ == "__main__":
    main()
