#!/usr/bin/env python3
import argparse
import calendar
import datetime
import json
import re
import sys

MONTHS = {name.lower(): i for i, name in enumerate(calendar.month_abbr) if name}
MONTHS["sept"] = 9
DAYS = {name.lower(): i for i, name in enumerate(calendar.day_abbr)}
NTH = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5}
SECTIONS = ("chores", "work", "tasks")


def easter(year):
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return datetime.date(year, month, day + 1)


def month_day(month_name, day_text):
    if month_name not in MONTHS or not day_text.isdigit():
        raise ValueError("wants a month and a day, such as Jan 5")
    month, day = MONTHS[month_name], int(day_text)
    if not 1 <= day <= calendar.monthrange(2000, month)[1]:
        raise ValueError(f"{month_name} has no day {day}")
    return month, day


def on_day(date, month, day):
    return date.month == month and date.day == min(day, calendar.monthrange(date.year, month)[1])


def rule(when):
    words = when.lower().split()
    if not words:
        raise ValueError("When is empty")
    if len(words) == 1 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", words[0]):
        try:
            once = datetime.date.fromisoformat(words[0])
        except ValueError:
            raise ValueError(f"{words[0]} is not a real date")
        return "once", once
    match = re.fullmatch(r"easter([+-]\d+)?", "".join(words))
    if match:
        offset = datetime.timedelta(days=int(match.group(1) or 0))
        return "rule", lambda d: d - offset == easter((d - offset).year)
    if words[0] == "every":
        if len(words) != 6 or not words[1].isdigit() or words[2] not in ("month", "months") or words[3] != "from":
            raise ValueError("wants every N months from Mon DD")
        step = int(words[1])
        if not 1 <= step <= 12:
            raise ValueError("N must be 1 to 12")
        month, day = month_day(words[4], words[5])
        return "rule", lambda d: (d.month - month) % step == 0 and on_day(d, d.month, day)
    if words[0] in NTH:
        if len(words) not in (2, 3) or words[1] not in DAYS or (len(words) == 3 and words[2] not in MONTHS):
            raise ValueError("wants Nth Day, or Nth Day Mon, such as 2nd Sun May")
        nth, weekday = NTH[words[0]], DAYS[words[1]]
        month = MONTHS[words[2]] if len(words) == 3 else None
        return "rule", lambda d: d.weekday() == weekday and (d.day - 1) // 7 + 1 == nth and month in (None, d.month)
    if words[0] in MONTHS:
        if len(words) != 2:
            raise ValueError("wants a month and a day, such as Jan 5")
        month, day = month_day(words[0], words[1])
        return "rule", lambda d: on_day(d, month, day)
    parity = None
    if words[-1] in ("even", "odd"):
        parity = 0 if words.pop() == "even" else 1
    if words and all(w in DAYS for w in words):
        days = {DAYS[w] for w in words}
        return "rule", lambda d: d.weekday() in days and parity in (None, d.isocalendar()[1] % 2)
    raise ValueError(f"cannot read When: {when.strip()}")


def cells(line):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", body)]


def is_separator(line):
    return line.strip().startswith("|") and all(re.fullmatch(r":?-+:?", c) for c in cells(line))


def read(text, date):
    out = {"date": date.isoformat(), "daily": [], "due": {s: [] for s in SECTIONS}, "errors": [], "past": []}
    lines = text.split("\n")
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    heading = None
    for i in range(start, len(lines)):
        line = lines[i].rstrip("\r")
        number = i + 1
        if line.startswith("## "):
            heading = line[3:].strip().lower()
            continue
        if not line.strip():
            continue
        if heading == "daily":
            out["daily"].append(line.rstrip())
            continue
        if heading is None or not line.strip().startswith("|") or is_separator(line):
            continue
        if i + 1 < len(lines) and is_separator(lines[i + 1]):
            continue
        row = cells(line)
        error = None
        if len(row) != 3:
            error = f"row has {len(row)} cells, wants 3: Item, When, Section"
        else:
            item, when, section = row
            section = section.lower() or "chores"
            if section not in SECTIONS:
                error = f"Section {row[2]} is not chores, work, or tasks"
            else:
                try:
                    kind, test = rule(when)
                except ValueError as e:
                    error = str(e)
        if error:
            out["errors"].append({"line": number, "row": line.strip(), "why": error})
            continue
        if kind == "once":
            if test == date:
                out["due"][section].append(item)
            elif test < date:
                out["past"].append({"line": number, "item": item, "when": when, "section": section})
        elif test(date):
            out["due"][section].append(item)
    return out


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--date", type=datetime.date.fromisoformat, default=datetime.date.today())
    args = parser.parse_args(argv)
    try:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError) as e:
        print(f"cannot read {args.file}: {e}", file=sys.stderr)
        return 2
    json.dump(read(text, args.date), sys.stdout, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
