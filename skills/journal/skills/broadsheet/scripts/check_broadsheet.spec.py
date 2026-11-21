#!/usr/bin/env python3
"""Run: python3 check_broadsheet.spec.py"""
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "check_broadsheet.py")
SECTIONS = ["masthead", "lead", "compass", "weather", "chores", "gaps", "the-ledger", "letters", "stale-shelf",
            "the-morgue", "editorial", "floor-plan", "honour-roll", "the-board", "back-pages"]
ROW = ('<li class="action" data-id="{id}"><span>A row</span>'
       '<select class="choice" aria-label="Choice"><option value="">-</option><option>archive</option></select>'
       '<details><summary>Comment</summary><textarea class="comment" aria-label="Comment"></textarea></details></li>')
PROMPT_SCRIPT = "<script>document.querySelectorAll('.action');</script>"


def page(sections=SECTIONS, rows=(ROW.format(id="ledger-1"),), scripts=(PROMPT_SCRIPT,)):
    body = "".join(f'<section id="{s}"><h2>{s}</h2></section>' for s in sections)
    body = body.replace("<h2>the-ledger</h2>", "<h2>The ledger</h2><ul>" + "".join(rows) + "</ul>")
    body = body.replace("<h2>editorial</h2>", "<h2>Editorial</h2>")
    return "<html><head><style>p{}</style></head><body>" + body + "".join(scripts) + "</body></html>"


def filled():
    return page()


TEMPLATE = os.path.join(os.path.dirname(HERE), "template.html")
SAMPLE_ROW = ('<li class="action" data-id="{id}">{text} '
              '<select class="choice" aria-label="Choice for {id}"></select>'
              '<details><summary>Comment</summary><textarea class="comment" aria-label="Comment on {id}"></textarea></details></li>')
SAMPLE = {
    "accent": "#8b1e3f",
    "ledger_body": ('<table><tr><th>Goal</th><th>State</th><th>Choice</th></tr>'
                    '<tr class="action" data-id="ledger-run"><td>Run twice a week</td><td>served</td><td>'
                    '<select class="choice" aria-label="Choice for ledger-run"></select>'
                    '<details><summary>Comment</summary><textarea class="comment" aria-label="Comment on ledger-run"></textarea></details>'
                    '</td></tr></table>'),
    "letters_body": "<ul>" + SAMPLE_ROW.format(id="letters-idea", text="Idea, 12 days old: file to the knowledge folder") + "</ul>",
    "stale_body": "<ul>" + SAMPLE_ROW.format(id="stale-old", text="Old note, 200 days, no backlinks: archive") + "</ul>",
    "morgue_body": "<ul>" + SAMPLE_ROW.format(id="morgue-gone", text="Gone note, 400 days, no links: delete") + "</ul>",
    "editorial_body": "<ul>" + SAMPLE_ROW.format(id="editorial-hours", text="Most writing is after 21:00") + "</ul>",
    "floor_plan_body": "<ul>" + SAMPLE_ROW.format(id="floor-loose", text="Loose notes beside subfolders") + "</ul>",
    "board_body": "<ul>" + SAMPLE_ROW.format(id="board-garden", text="Garden: next card is Buy seeds") + "</ul>",
}


def fill(template):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: SAMPLE.get(m.group(1), f"Sample {m.group(1)}"), template)


def check(html):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
    try:
        p = subprocess.run([sys.executable, SCRIPT, f.name], capture_output=True, text=True)
        return p.returncode, p.stdout
    finally:
        os.unlink(f.name)


class Check(unittest.TestCase):
    def test_the_template_filled_with_sample_data_is_ok(self):
        with open(TEMPLATE) as f:
            html = fill(f.read())
        self.assertEqual(check(html), (0, "ok\n"))
        self.assertIn('id="copy-prompt"', html)

    def test_a_good_page_is_ok(self):
        self.assertEqual(check(filled()), (0, "ok\n"))

    def test_names_a_placeholder_left_on_the_page(self):
        code, out = check(filled().replace("<h2>The ledger</h2>", "<h2>{{ledger}}</h2>"))
        self.assertEqual(code, 1)
        self.assertIn("placeholder {{ledger}} is still on the page", out)

    def test_names_a_missing_section(self):
        code, out = check(filled().replace('id="the-morgue"', 'id="gone"'))
        self.assertEqual(code, 1)
        self.assertIn("section #the-morgue is missing", out)

    def test_names_an_inline_style(self):
        code, out = check(filled().replace('<section id="gaps"', '<section style="color: red" id="gaps"'))
        self.assertEqual(code, 1)
        self.assertIn("has an inline style", out)

    def test_names_a_note_path_that_is_not_a_link(self):
        code, out = check(filled().replace("<h2>Editorial</h2>", "<h2>Editorial</h2><p>See 02-research/old note.md now.</p>"))
        self.assertEqual(code, 1)
        self.assertIn("note 02-research/old note.md is not a link", out)

    def test_a_linked_note_path_is_fine(self):
        link = '<a href="obsidian://open?vault=notes&amp;file=02-research%2Fa" target="_blank" rel="noopener">02-research/a.md</a>'
        self.assertEqual(check(filled().replace("<h2>Editorial</h2>", "<h2>Editorial</h2>" + link))[0], 0)

    def test_names_a_link_without_target_and_rel(self):
        code, out = check(filled().replace("<h2>Editorial</h2>", '<h2>Editorial</h2><a href="obsidian://x">x</a>'))
        self.assertEqual(code, 1)
        self.assertIn('link obsidian://x has no target="_blank"', out)
        self.assertIn('link obsidian://x has no rel="noopener"', out)

    def test_wants_compass_and_chores(self):
        code, out = check(page(sections=[s for s in SECTIONS if s not in ("compass", "chores")]))
        self.assertEqual(code, 1)
        self.assertIn("section #compass is missing", out)
        self.assertIn("section #chores is missing", out)

    def test_rejects_carried_over_and_link_health(self):
        code, out = check(page(sections=SECTIONS + ["carried-over", "link-health"]))
        self.assertEqual(code, 1)
        self.assertIn("section #carried-over must not be on the page", out)
        self.assertIn("section #link-health must not be on the page", out)

    def test_names_an_action_row_with_no_data_id(self):
        for row in (ROW.replace(' data-id="{id}"', ""), ROW.format(id="")):
            code, out = check(page(rows=(row,)))
            self.assertEqual(code, 1)
            self.assertIn("action row has no data-id", out)

    def test_names_an_action_row_with_no_choice_control(self):
        row = re.sub(r"<select.*?</select>", "", ROW.format(id="letters-2"))
        code, out = check(page(rows=(row,)))
        self.assertEqual(code, 1)
        self.assertIn("action row letters-2 has no choice control", out)

    def test_names_an_action_row_with_no_comment(self):
        row = re.sub(r"<details>.*?</details>", "", ROW.format(id="morgue-3"))
        code, out = check(page(rows=(row,)))
        self.assertEqual(code, 1)
        self.assertIn("action row morgue-3 has no comment", out)

    def test_a_text_input_comment_is_fine(self):
        row = re.sub(r"<details>.*?</details>", '<input class="comment" type="text" aria-label="Comment">', ROW.format(id="a"))
        self.assertEqual(check(page(rows=(row,))), (0, "ok\n"))

    def test_a_control_outside_the_row_does_not_count(self):
        row = '<li class="action" data-id="b">bare</li><select class="choice"></select><textarea class="comment"></textarea>'
        code, out = check(page(rows=(row,)))
        self.assertEqual(code, 1)
        self.assertIn("action row b has no choice control", out)
        self.assertIn("action row b has no comment", out)

    def test_names_a_data_id_used_twice(self):
        code, out = check(page(rows=(ROW.format(id="dup"), ROW.format(id="dup"))))
        self.assertEqual(code, 1)
        self.assertIn("action row id dup is used twice", out)

    def test_one_script_is_allowed_and_two_fail(self):
        self.assertEqual(check(page())[0], 0)
        code, out = check(page(scripts=(PROMPT_SCRIPT, PROMPT_SCRIPT)))
        self.assertEqual(code, 1)
        self.assertIn("the page has 2 script blocks; only 1 is allowed", out)

    def test_an_inline_style_still_fails_with_the_script(self):
        code, out = check(page().replace('<section id="gaps"', '<section style="color: red" id="gaps"'))
        self.assertEqual(code, 1)
        self.assertIn("has an inline style", out)


if __name__ == "__main__":
    unittest.main()
