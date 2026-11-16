"""Parse the YAML header and the `## ` sections that check_plan.py and check_spec.py share."""
import re
from typing import NamedTuple


class Field(NamedTuple):
    value: str
    line: int


def read_header(lines):
    """Return ({key: Field}, end index) or (None, 0) when there is no header."""
    if not lines or lines[0].strip() != "---":
        return None, 0
    header = {}
    for i in range(1, len(lines)):
        line = lines[i]
        if line.strip() == "---":
            return header, i + 1
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            header[m.group(1)] = Field(m.group(2).strip().strip("\"'"), i + 1)
    return None, 0


def sections(lines, start):
    """Map each `## ` heading to its (first body index, end index)."""
    found = {}
    name, begin = None, None
    for i in range(start, len(lines)):
        if lines[i].startswith("## "):
            if name is not None:
                found[name] = (begin, i)
            name, begin = lines[i][3:].strip(), i + 1
    if name is not None:
        found[name] = (begin, len(lines))
    return found
