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
    for name, section in sections.items():
        for key in PLACEHOLDER.findall(section["body"]):
            if key not in values:
                print(
                    f"warning: missing value `{key}` for section `{name}`, rendered as `none`: see its entry in {hydrate_note}",
                    file=sys.stderr,
                )
    return {
        name: PLACEHOLDER.sub(lambda m: str(values.get(m.group(1), "none")), section["body"])
        for name, section in sections.items()
    }


def parse(text, known):
    items = []
    buffer = []
    buffer_start = 1
    open_name = None
    open_start = 0
    for number, line in enumerate(text.splitlines(keepends=True), start=1):
        stripped = line.strip()
        start = START.match(stripped)
        if open_name is None and start:
            if start.group(1) not in known:
                raise Fail(f"unknown managed block `{start.group(1)}`")
            if buffer:
                items.append(("text", "".join(buffer), buffer_start))
            buffer = []
            open_name = start.group(1)
            open_start = number
        elif open_name is not None and start:
            raise Fail(f"managed block `{open_name}` has no end marker")
        elif stripped == END:
            if open_name is None:
                raise Fail("end marker with no start marker")
            items.append(("block", open_name, open_start))
            open_name = None
            buffer_start = number + 1
        elif open_name is None:
            if not buffer:
                buffer_start = number
            buffer.append(line)
    if open_name is not None:
        raise Fail(f"managed block `{open_name}` has no end marker")
    if buffer:
        items.append(("text", "".join(buffer), buffer_start))
    return items


def heading_lines(lines):
    in_fence = False
    for index, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
        elif not in_fence:
            yield index, line


def find_heading(lines, heading):
    for index, line in heading_lines(lines):
        if line.rstrip() == heading:
            return index
    return None


def section_end(lines, start):
    level = len(HEADING.match(lines[start]).group(1))
    for index, line in heading_lines(lines[start + 1:]):
        m = HEADING.match(line)
        if m and len(m.group(1)) <= level:
            return start + 1 + index
    return len(lines)


def block_text(name, body):
    return f"<!-- managed: {name} -->\n{body}{END}\n"


def scan(items, sections, drops):
    cleaned = []
    report = []
    found = set()
    for kind, value, first_line in items:
        if kind == "block":
            cleaned.append((kind, value))
            continue
        lines = value.splitlines(keepends=True)
        original = list(lines)
        for name, section in sections.items():
            for heading in section["replaces"]:
                while (index := find_heading(lines, heading)) is not None:
                    end = section_end(lines, index)
                    found.add(name)
                    where = first_line + original.index(lines[index])
                    if name in drops:
                        report.append(f"DROPPED {name}: `{heading}` ({end - index} lines)")
                        lines = lines[:index] + lines[end:]
                    else:
                        report.append(
                            f"OLD {name}: line {where}: `{heading}` ({end - index} lines)"
                        )
                        break
            for needle in section["lists"]:
                for index, line in enumerate(original):
                    if needle in line:
                        report.append(
                            f"EDIT {name}: line {first_line + index}: {line.rstrip()}"
                        )
        cleaned.append((kind, "".join(lines)))
    for name in drops:
        if name not in found:
            report.append(f"NOT FOUND {name}: no old heading to drop")
    return cleaned, report


def assemble(items, sections, rendered):
    present = {value for kind, value in items if kind == "block"}
    head = "\n".join(block_text(n, rendered[n]) for n in sections if n not in present)
    rest = "".join(
        block_text(value, rendered[value]) if kind == "block" else value
        for kind, value in items
    )
    return head + ("\n" if head and rest else "") + rest


def write_target(target, original, result):
    if original is None:
        os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
        status = "created"
    elif result == original:
        return "unchanged"
    else:
        shutil.copyfile(target, target + ".bak")
        status = "updated (backup: AGENTS.md.bak)"
    with open(target, "wb") as f:
        f.write(result.encode())
    return status


def load_values(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise Fail(f"values file {path} is not valid JSON: {e}")


def install(target, values_path, sections_dir, drops):
    sections = load_sections(sections_dir)
    for name in drops:
        if name not in sections or not sections[name]["replaces"]:
            raise Fail(f"cannot drop `{name}`: no section of that name replaces an old heading")
    rendered = render(sections, load_values(values_path), "HYDRATE.md")
    original = None
    if os.path.exists(target):
        with open(target, "rb") as f:
            original = f.read().decode()
    items, report = scan(parse(original or "", sections), sections, drops)
    status = write_target(target, original, assemble(items, sections, rendered))
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
