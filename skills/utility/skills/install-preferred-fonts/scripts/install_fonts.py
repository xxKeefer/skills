#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")


def machine_dest():
    if sys.platform == "darwin":
        return os.path.expanduser("~/Library/Fonts")
    if sys.platform.startswith("linux"):
        data = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
        return os.path.join(data, "fonts", "preferred-fonts")
    sys.exit("install-preferred-fonts: no machine install for " + sys.platform)


def same(src, dst):
    if not os.path.isfile(dst):
        return False
    with open(src, "rb") as a, open(dst, "rb") as b:
        return a.read() == b.read()


def copy(src, dest, name):
    dst = os.path.join(dest, name)
    if same(src, dst):
        print("unchanged " + name)
        return
    shutil.copyfile(src, dst)
    print("copied " + name)


def font_face(face):
    lines = [
        "@font-face {",
        '  font-family: "%s";' % face["family"],
        '  src: url("./%s.woff2") format("woff2");' % face["file"],
        "  font-style: %s;" % face["style"],
        "  font-weight: %s;" % face["weight"],
    ]
    if "stretch" in face:
        lines.append("  font-stretch: %s;" % face["stretch"])
    lines += ["  font-display: swap;", "}"]
    return "\n".join(lines)


def stack(names):
    return ", ".join('"%s"' % n if " " in n else n for n in names)


def css(manifest):
    faces = "\n\n".join(font_face(f) for f in manifest["faces"])
    roles = "\n".join("  --font-%s: %s;" % (role, stack(names)) for role, names in manifest["roles"].items())
    return faces + "\n\n:root {\n" + roles + "\n}\n"


def install_machine(fonts, manifest, dest):
    os.makedirs(dest, exist_ok=True)
    for face in manifest["faces"]:
        name = face["file"] + ".ttf"
        copy(os.path.join(fonts, face["dir"], name), dest, name)
    if sys.platform != "darwin" and shutil.which("fc-cache"):
        subprocess.run(["fc-cache", "-f", dest], check=True)
        print("refreshed font cache")


def install_project(fonts, manifest, dest):
    os.makedirs(dest, exist_ok=True)
    for face in manifest["faces"]:
        name = face["file"] + ".woff2"
        copy(os.path.join(fonts, face["dir"], name), dest, name)
    for d in sorted({f["dir"] for f in manifest["faces"]}):
        copy(os.path.join(fonts, d, "OFL.txt"), dest, d + "-OFL.txt")
    path = os.path.join(dest, "fonts.css")
    text = css(manifest)
    if os.path.isfile(path) and open(path).read() == text:
        print("unchanged fonts.css")
        return
    with open(path, "w") as f:
        f.write(text)
    print("wrote fonts.css")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fonts", default=FONTS)
    p.add_argument("--dest")
    p.add_argument("--project")
    args = p.parse_args()
    with open(os.path.join(args.fonts, "manifest.json")) as f:
        manifest = json.load(f)
    if args.project:
        install_project(args.fonts, manifest, args.project)
    else:
        install_machine(args.fonts, manifest, args.dest or machine_dest())


if __name__ == "__main__":
    main()
