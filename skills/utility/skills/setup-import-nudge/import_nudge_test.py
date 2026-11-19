#!/usr/bin/env python3
import json
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).parent
CONFIG = json.loads((HERE / "import-nudge.example.json").read_text())
ROOT = pathlib.Path(tempfile.mkdtemp())


def spec(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return str(path)


LEGACY = spec("apps/web/src/a/Legacy.spec.ts", "import { render } from '@testing-library/vue'\n")
LEGACY_UTILS = spec("apps/web/src/a/Utils.spec.ts", "import { render } from '@/legacy/src/utils/testUtils'\n")
MODERN = spec("apps/web/src/a/Modern.spec.ts", "import { shallowMount } from '@acme/test-utils'\n")
SOURCE = spec("apps/web/src/a/Thing.ts", "import { render } from '@testing-library/vue'\n")
LIB = spec("libs/ui/src/a/Lib.spec.ts", "import { render } from '@testing-library/vue'\n")


def run(payload, config_text):
    with tempfile.TemporaryDirectory() as tmp:
        hook = pathlib.Path(tmp) / "import_nudge.py"
        hook.write_text((HERE / "import_nudge.py").read_text())
        (pathlib.Path(tmp) / "import-nudge.config.json").write_text(config_text)
        out = subprocess.run([sys.executable, str(hook)], input=payload, capture_output=True, text=True)
    return out.returncode, out.stdout.strip()


def call(path, tool="Edit"):
    return json.dumps({"hook_event_name": "PostToolUse", "tool_name": tool, "tool_input": {"file_path": path}})


CASES = [
    ("legacy import gets the message", call(LEGACY), json.dumps(CONFIG), "legacy test harness"),
    ("legacy utils path gets the message", call(LEGACY_UTILS, "Write"), json.dumps(CONFIG), "legacy test harness"),
    ("modern spec gets nothing", call(MODERN), json.dumps(CONFIG), ""),
    ("non-spec file gets nothing", call(SOURCE), json.dumps(CONFIG), ""),
    ("spec outside the path rule gets nothing", call(LIB), json.dumps(CONFIG), ""),
    ("empty config gets nothing", call(LEGACY), '{ "rules": [] }', ""),
    ("broken config gets nothing", call(LEGACY), "{not json", ""),
    ("broken payload gets nothing", "not json", json.dumps(CONFIG), ""),
    ("missing file gets nothing", call(str(ROOT / "apps/web/src/Gone.spec.ts")), json.dumps(CONFIG), ""),
]

failed = 0
for name, payload, config_text, expected in CASES:
    code, out = run(payload, config_text)
    if expected:
        ok = code == 0 and expected in out and json.loads(out)["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
    else:
        ok = code == 0 and out == ""
    if not ok:
        failed += 1
        print(f"FAIL {name}: code={code} out={out!r}")
print(f"{len(CASES) - failed}/{len(CASES)} passed")
sys.exit(1 if failed else 0)
