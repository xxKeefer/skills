#!/usr/bin/env python3
import re
import sys
from pathlib import Path

HASH = ("#",)
SLASH = ("//",)
C_BLOCK = ("/*", "*/")
HTML_BLOCK = ("<!--", "-->")
ROWS = (
    ("py sh bash zsh nix yaml yml toml rb pl r", HASH, ()),
    ("ts tsx js jsx mjs cjs java kt go rs c h cpp cs swift scala php scss", SLASH, (C_BLOCK,)),
    ("css", (), (C_BLOCK,)),
    ("vue", SLASH, (C_BLOCK, HTML_BLOCK)),
    ("html", (), (HTML_BLOCK,)),
    ("sql lua hs", ("--",), ()),
)
LANGS = {ext: (lines, blocks) for exts, lines, blocks in ROWS for ext in exts.split()}

HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)")
ESCAPES = {"a": 7, "b": 8, "t": 9, "n": 10, "v": 11, "f": 12, "r": 13, '"': 34, "\\": 92}


def unquote(path):
    if not (len(path) > 1 and path[0] == path[-1] == '"'):
        return path
    body = path[1:-1]
    out = bytearray()
    i = 0
    while i < len(body):
        c = body[i]
        if c == "\\" and i + 1 < len(body):
            nxt = body[i + 1]
            if nxt in "0123":
                out.append(int(body[i + 1:i + 4], 8))
                i += 4
                continue
            if nxt in ESCAPES:
                out.append(ESCAPES[nxt])
                i += 2
                continue
        out.extend(c.encode())
        i += 1
    return out.decode("utf-8", "replace")


def closes(text, i, quote):
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == quote:
            return True
        i += 1
    return False


def scan(text, lines, blocks):
    quote = None
    i = 0
    while i < len(text):
        c = text[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c == '"' and text[i - 1:i] == "'" and text[i + 1:i + 2] == "'":
            i += 1
            continue
        if c in "\"`" and closes(text, i + 1, c):
            quote = c
            i += 1
            continue
        for tok in lines:
            if text.startswith(tok, i) and (tok != "#" or text[i - 1:i] not in ("$", "{")):
                return i, None, len(text)
        for open_, close in blocks:
            if text.startswith(open_, i):
                end = text.find(close, i + len(open_))
                if end < 0:
                    return i, close, len(text)
                return i, None, end + len(close)
        i += 1
    return None


def comments(diff):
    path = None
    lang = None
    num = 0
    close = None
    for raw in diff.split("\n"):
        if raw.startswith("diff "):
            lang = None
            close = None
            continue
        if raw.startswith("+++ "):
            path = unquote(raw[4:].strip())
            if path.startswith("b/"):
                path = path[2:]
            lang = LANGS.get(path.rsplit(".", 1)[-1])
            close = None
            continue
        m = HUNK.match(raw)
        if m:
            num = int(m.group(1))
            close = None
            continue
        if raw.startswith("-") or raw.startswith("\\"):
            continue
        added = raw.startswith("+")
        text = raw[1:]
        here = num
        num += 1
        if not lang:
            continue
        if close:
            end = text.find(close)
            if end >= 0:
                close = None
            if added:
                yield path, here, text.strip()
            continue
        if added and here == 1 and text.startswith("#!"):
            continue
        found = scan(text, *lang)
        if found:
            start, close, stop = found
            if added:
                yield path, here, text[start:stop].strip()
        elif added and text.lstrip().startswith("*") and C_BLOCK in lang[1]:
            yield path, here, text.strip()


def main():
    diff = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else sys.stdin.read()
    for path, line, text in comments(diff):
        print("%s:%d: %s" % (path, line, text))


if __name__ == "__main__":
    main()
