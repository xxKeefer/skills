#!/usr/bin/env python3
"""Print the functions whose lizard numbers differ between two refs. Usage: complexity.py <base> <head> <file>..."""
import csv
import io
import os
import shutil
import subprocess
import sys
import tempfile

HEADER = ["file", "function", "line", "base_ccn", "head_ccn", "base_nloc", "head_nloc"]


def snapshot(ref, files, folder):
    for path in files:
        shown = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True)
        if shown.returncode != 0:
            continue
        target = os.path.join(folder, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as f:
            f.write(shown.stdout)


def measure(folder):
    result = subprocess.run(["lizard", "--csv", "."], cwd=folder, capture_output=True, text=True)
    found = {}
    for row in csv.reader(io.StringIO(result.stdout)):
        if len(row) < 11:
            continue
        path = os.path.normpath(row[6])
        found[(path, row[7])] = {"ccn": row[1], "nloc": row[0], "line": row[9]}
    return found


def main(argv):
    if len(argv) < 4:
        print(__doc__.strip(), file=sys.stderr)
        return 1
    if not shutil.which("lizard"):
        print("lizard not found. Install it with: pipx install lizard", file=sys.stderr)
        return 2
    base_ref, head_ref, files = argv[1], argv[2], argv[3:]
    with tempfile.TemporaryDirectory() as base_dir, tempfile.TemporaryDirectory() as head_dir:
        snapshot(base_ref, files, base_dir)
        snapshot(head_ref, files, head_dir)
        base, head = measure(base_dir), measure(head_dir)
    out = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    out.writerow(HEADER)
    for key in sorted(set(base) | set(head)):
        old, new = base.get(key), head.get(key)
        if old and new and (old["ccn"], old["nloc"]) == (new["ccn"], new["nloc"]):
            continue
        dash = {"ccn": "-", "nloc": "-", "line": "-"}
        old, new = old or dash, new or dash
        out.writerow([key[0], key[1], new["line"], old["ccn"], new["ccn"], old["nloc"], new["nloc"]])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
