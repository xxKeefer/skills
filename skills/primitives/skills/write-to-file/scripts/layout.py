"""Parse and check the YAML header and the `## ` sections that check_plan.py and check_spec.py share."""
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


def check_header(header, err, doctype, keys, statuses):
    """Report each missing or empty key, a wrong doctype, and a status not in statuses."""
    for key in keys:
        if key not in header or header[key].value == "":
            err(1, f"header has no `{key}`", f"add `{key}:` to the YAML header")
    if "doctype" in header and header["doctype"].value not in ("", doctype):
        value, line = header["doctype"]
        err(line, f"doctype `{value}` is not `{doctype}`", f"set `doctype: {doctype}`")
    if "status" in header and header["status"].value not in [""] + statuses:
        value, line = header["status"]
        err(line, f"status `{value}` is not valid", "set it to one of " + ", ".join(statuses))
