#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import sys

START = re.compile(r"^<!-- managed: ([\w-]+) -->$")
END = "<!-- end managed -->"
PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")
HEADING = re.compile(r"^(#+) ")
HEADER_KEYS = ("replaces", "lists")


class Fail(Exception):
    pass


def load_sections(directory):
    sections = {}
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".md"):
            continue
        with open(os.path.join(directory, filename)) as f:
            lines = f.read().splitlines(keepends=True)
        meta = {key: [] for key in HEADER_KEYS}
        i = 0
        while i < len(lines):
            key, sep, rest = lines[i].partition(": ")
            if not sep or key not in meta:
                break
            meta[key].append(rest.rstrip("\r\n"))
            i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        body = "".join(lines[i:])
        if not body.endswith("\n"):
            body += "\n"
        sections[filename[:-3]] = {"body": body, **meta}
    return sections


def render(sections, values, hydrate_note):
    missing = []
    for name, section in sections.items():
        for key in PLACEHOLDER.findall(section["body"]):
            if key not in values:
                missing.append((name, key))
    if missing:
        raise Fail(
            "\n".join(
                f"missing value `{key}` for section `{name}`: see its entry in {hydrate_note}"
                for name, key in missing
            )
        )
    return {
        name: PLACEHOLDER.sub(lambda m: str(values[m.group(1)]), section["body"])
        for name, section in sections.items()
    }


def parse(text, known):
    items = []
    buffer = []
    open_name = None
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        start = START.match(stripped)
        if open_name is None and start:
            if start.group(1) not in known:
                raise Fail(f"unknown managed block `{start.group(1)}`")
            if buffer:
                items.append(["text", "".join(buffer)])
            buffer = []
            open_name = start.group(1)
        elif open_name is not None and start:
            raise Fail(f"managed block `{open_name}` has no end marker")
        elif stripped == END:
            if open_name is None:
                raise Fail("end marker with no start marker")
            items.append(["block", open_name])
            open_name = None
        elif open_name is None:
            buffer.append(line)
    if open_name is not None:
        raise Fail(f"managed block `{open_name}` has no end marker")
    if buffer:
        items.append(["text", "".join(buffer)])
    return items


def find_heading(lines, heading):
    for index, line in enumerate(lines):
        if line.rstrip() == heading:
            return index
    return None


def section_end(lines, start):
    level = len(HEADING.match(lines[start]).group(1))
    for index in range(start + 1, len(lines)):
        m = HEADING.match(lines[index])
        if m and len(m.group(1)) <= level:
            return index
    return len(lines)


def block_text(name, body):
    return f"<!-- managed: {name} -->\n{body}{END}\n"


def install(target, values_path, sections_dir, drops):
    sections = load_sections(sections_dir)
    for name in drops:
        if name not in sections or not sections[name]["replaces"]:
            raise Fail(f"cannot drop `{name}`: no section of that name replaces an old heading")
    values = {}
    if os.path.exists(values_path):
        with open(values_path) as f:
            values = json.load(f)
    rendered = render(sections, values, "HYDRATE.md")

    original = None
    if os.path.exists(target):
        with open(target, "rb") as f:
            original = f.read().decode()
    items = parse(original or "", sections)
    report = []

    for name, section in sections.items():
        line_no = 1
        for item in items:
            if item[0] == "block":
                line_no += 2 + rendered[item[1]].count("\n")
                continue
            lines = item[1].splitlines(keepends=True)
            for heading in section["replaces"]:
                index = find_heading(lines, heading)
                if index is None:
                    continue
                if name in drops:
                    end = section_end(lines, index)
                    report.append(f"DROPPED {name}: `{heading}` ({end - index} lines)")
                    lines = lines[:index] + lines[end:]
                else:
                    end = section_end(lines, index)
                    report.append(
                        f"OLD {name}: line {line_no + index}: `{heading}` ({end - index} lines)"
                    )
            for needle in section["lists"]:
                for index, line in enumerate(lines):
                    if needle in line:
                        report.append(
                            f"EDIT {name}: line {line_no + index}: {line.rstrip()}"
                        )
            item[1] = "".join(lines)
            line_no += len(lines)

    present = {item[1] for item in items if item[0] == "block"}
    head = [block_text(n, rendered[n]) for n in sections if n not in present]
    out = "\n".join(head)
    rest = "".join(
        block_text(item[1], rendered[item[1]]) if item[0] == "block" else item[1]
        for item in items
    )
    result = out + ("\n" if out and rest else "") + rest

    if original is None:
        os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
        status = "created"
    elif result == original:
        status = "unchanged"
    else:
        shutil.copyfile(target, target + ".bak")
        status = "updated (backup: AGENTS.md.bak)"
    if status != "unchanged":
        with open(target, "wb") as f:
            f.write(result.encode())
    return status, report


def main():
    home = os.path.expanduser("~/.claude")
    here = os.path.dirname(os.path.abspath(__file__))
    p = argparse.ArgumentParser()
    p.add_argument("--target", default=os.path.join(home, "AGENTS.md"))
    p.add_argument("--values", default=os.path.join(home, "agents-md.values.json"))
    p.add_argument("--sections", default=os.path.join(here, "..", "sections"))
    p.add_argument("--drop", action="append", default=[])
    args = p.parse_args()
    try:
        status, report = install(args.target, args.values, args.sections, args.drop)
    except Fail as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    print(status)
    for line in report:
        print(line)


if __name__ == "__main__":
    main()
