#!/usr/bin/env python3
"""Run: python3 install_fonts.spec.py"""
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "install_fonts.py")
REAL_FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")

MANIFEST = {
    "roles": {
        "body": ["Body Face", "sans-serif"],
        "mono": ["Mono Face", "monospace"],
    },
    "faces": [
        {"family": "Body Face", "dir": "Body", "file": "BodyFace", "style": "normal", "weight": "200 800"},
        {"family": "Body Face", "dir": "Body", "file": "BodyFace-Italic", "style": "italic", "weight": "200 800",
         "stretch": "62.5% 100%"},
        {"family": "Mono Face", "dir": "Mono", "file": "MonoFace", "style": "normal", "weight": "100 800"},
    ],
}


class Env:
    def __init__(self, tc):
        self.dir = tempfile.mkdtemp()
        tc.addCleanup(lambda: shutil.rmtree(self.dir, ignore_errors=True))
        self.fonts = os.path.join(self.dir, "fonts")
        for face in MANIFEST["faces"]:
            d = os.path.join(self.fonts, face["dir"])
            os.makedirs(d, exist_ok=True)
            for ext in ("ttf", "woff2"):
                with open(os.path.join(d, face["file"] + "." + ext), "w") as f:
                    f.write(face["file"] + ext)
            with open(os.path.join(d, "OFL.txt"), "w") as f:
                f.write("licence " + face["dir"])
        with open(os.path.join(self.fonts, "manifest.json"), "w") as f:
            json.dump(MANIFEST, f)
        self.dest = os.path.join(self.dir, "dest")
        self.project = os.path.join(self.dir, "repo", "public", "fonts")
        self.bin = os.path.join(self.dir, "bin")
        os.makedirs(self.bin)
        self.cache_log = os.path.join(self.dir, "fc-cache.log")

    def fake_fc_cache(self):
        path = os.path.join(self.bin, "fc-cache")
        with open(path, "w") as f:
            f.write('#!/bin/sh\necho "$@" >> "%s"\n' % self.cache_log)
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)

    def run(self, *extra):
        env = dict(os.environ, PATH=self.bin + os.pathsep + "/usr/bin" + os.pathsep + "/bin")
        p = subprocess.run([sys.executable, SCRIPT, "--fonts", self.fonts, *extra],
                           capture_output=True, text=True, env=env)
        return p.returncode, p.stdout, p.stderr

    def read(self, *parts):
        with open(os.path.join(*parts)) as f:
            return f.read()


class MachineInstall(unittest.TestCase):
    def test_copies_every_ttf_into_dest(self):
        e = Env(self)
        code, out, _ = e.run("--dest", e.dest)
        self.assertEqual(code, 0)
        self.assertEqual(sorted(os.listdir(e.dest)), ["BodyFace-Italic.ttf", "BodyFace.ttf", "MonoFace.ttf"])
        self.assertEqual(e.read(e.dest, "BodyFace.ttf"), "BodyFacettf")
        self.assertIn("copied BodyFace.ttf", out)

    def test_second_run_reports_unchanged(self):
        e = Env(self)
        e.run("--dest", e.dest)
        _, out, _ = e.run("--dest", e.dest)
        self.assertNotIn("copied", out)
        self.assertIn("unchanged MonoFace.ttf", out)

    def test_refreshes_the_font_cache_when_fc_cache_exists(self):
        e = Env(self)
        e.fake_fc_cache()
        e.run("--dest", e.dest)
        self.assertIn(e.dest, e.read(e.cache_log))

    def test_runs_without_fc_cache(self):
        e = Env(self)
        code, _, _ = e.run("--dest", e.dest)
        self.assertEqual(code, 0)
        self.assertFalse(os.path.exists(e.cache_log))


class ProjectInstall(unittest.TestCase):
    def test_copies_woff2_and_one_licence_per_family(self):
        e = Env(self)
        code, _, _ = e.run("--project", e.project)
        self.assertEqual(code, 0)
        self.assertEqual(sorted(os.listdir(e.project)), [
            "Body-OFL.txt", "BodyFace-Italic.woff2", "BodyFace.woff2",
            "Mono-OFL.txt", "MonoFace.woff2", "fonts.css",
        ])
        self.assertEqual(e.read(e.project, "Mono-OFL.txt"), "licence Mono")

    def test_writes_one_font_face_per_face_with_relative_urls(self):
        e = Env(self)
        e.run("--project", e.project)
        css = e.read(e.project, "fonts.css")
        self.assertEqual(css.count("@font-face"), 3)
        self.assertIn('src: url("./BodyFace-Italic.woff2") format("woff2");', css)
        self.assertIn('font-family: "Body Face";', css)
        self.assertIn("font-style: italic;", css)
        self.assertIn("font-weight: 200 800;", css)
        self.assertIn("font-stretch: 62.5% 100%;", css)
        self.assertEqual(css.count("font-stretch"), 1)
        self.assertIn("font-display: swap;", css)

    def test_writes_a_custom_property_per_role(self):
        e = Env(self)
        e.run("--project", e.project)
        css = e.read(e.project, "fonts.css")
        self.assertIn(":root {", css)
        self.assertIn('--font-body: "Body Face", sans-serif;', css)
        self.assertIn('--font-mono: "Mono Face", monospace;', css)

    def test_does_not_touch_the_machine(self):
        e = Env(self)
        e.fake_fc_cache()
        e.run("--project", e.project, "--dest", e.dest)
        self.assertFalse(os.path.exists(e.dest))
        self.assertFalse(os.path.exists(e.cache_log))

    def test_second_run_reports_unchanged(self):
        e = Env(self)
        e.run("--project", e.project)
        _, out, _ = e.run("--project", e.project)
        self.assertNotIn("copied", out)
        self.assertNotIn("wrote", out)
        self.assertIn("unchanged fonts.css", out)


class RealFonts(unittest.TestCase):
    def test_every_manifest_face_ships_a_ttf_and_a_woff2(self):
        with open(os.path.join(REAL_FONTS, "manifest.json")) as f:
            manifest = json.load(f)
        for face in manifest["faces"]:
            for ext in ("ttf", "woff2"):
                self.assertTrue(os.path.isfile(os.path.join(REAL_FONTS, face["dir"], face["file"] + "." + ext)))
            self.assertTrue(os.path.isfile(os.path.join(REAL_FONTS, face["dir"], "OFL.txt")))


if __name__ == "__main__":
    unittest.main()
