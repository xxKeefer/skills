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
ROW = ('<li class="action" data-id="{id}"><input type="checkbox" class="done" aria-label="Done"><span>A row</span>'
       '<select class="choice" aria-label="Choice"><option value="">-</option><option>archive</option></select>'
       '<details><summary>Comment</summary><textarea class="comment" aria-label="Comment"></textarea></details></li>')
PROMPT_SCRIPT = "<script>document.querySelectorAll('.action');</script>"


LEGEND = '<dl class="legend"><dt>do</dt><dd>Apply it.</dd><dt>done</dt><dd>You did it.</dd></dl>'
PROMPTS = ('<textarea id="prompt-vault" aria-label="Vault prompt"></textarea>'
           '<textarea id="prompt-suite" aria-label="Suite prompt"></textarea>')


def page(sections=SECTIONS, rows=(ROW.format(id="ledger-1"),), scripts=(PROMPT_SCRIPT,), ledger_open=None,
         suite_rows=(), prompts=PROMPTS, legend=LEGEND):
    body = "".join(f'<section id="{s}"><h2>{s}</h2></section>' for s in sections)
    opening = ledger_open or '<section id="the-ledger" data-prompt="vault" data-choices="do done">'
    body = body.replace('<section id="the-ledger">', opening)
    body = body.replace("<h2>the-ledger</h2>", "<h2>The ledger</h2>" + legend + "<ul>" + "".join(rows) + "</ul>")
    body = body.replace('<section id="editorial">',
                        '<section id="editorial" data-prompt="suite" data-choices="do done">' if suite_rows else '<section id="editorial">')
    body = body.replace("<h2>editorial</h2>", "<h2>Editorial</h2>" + (legend + "<ul>" + "".join(suite_rows) + "</ul>" if suite_rows else ""))
    return "<html><head><style>p{}</style></head><body>" + body + prompts + "".join(scripts) + "</body></html>"


def filled():
    return page()


TEMPLATE = os.path.join(os.path.dirname(HERE), "template.html")
SAMPLE_ROW = ('<li class="action" data-id="{id}"><input type="checkbox" class="done" aria-label="Done">{text} '
              '<select class="choice" aria-label="Choice for {id}"></select>'
              '<details><summary>Comment</summary><textarea class="comment" aria-label="Comment on {id}"></textarea></details></li>')
SAMPLE = {
    "accent": "#8b1e3f",
    "ledger_body": ('<table><tr><th>Goal</th><th>State</th><th>Choice</th></tr>'
                    '<tr class="action" data-id="ledger-run"><td><input type="checkbox" class="done" aria-label="Done">Run twice a week</td><td>served</td><td>'
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
        self.assertIn('id="prompt-vault"', html)
        self.assertIn('id="prompt-suite"', html)

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
        code, out = check(filled().replace("<h2>Editorial</h2>", "<h2>Editorial</h2><p>See 02-knowledge/old note.md now.</p>"))
        self.assertEqual(code, 1)
        self.assertIn("note 02-knowledge/old note.md is not a link", out)

    def test_a_linked_note_path_is_fine(self):
        link = '<a href="obsidian://open?vault=notes&amp;file=02-knowledge%2Fa" target="_blank" rel="noopener">02-knowledge/a.md</a>'
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

    def test_names_an_action_row_with_no_done_checkbox(self):
        row = ROW.format(id="stale-4").replace('<input type="checkbox" class="done" aria-label="Done">', "")
        code, out = check(page(rows=(row,)))
        self.assertEqual(code, 1)
        self.assertIn("stale-4 has no done checkbox", out)

    def test_names_a_card_that_is_not_in_a_group(self):
        for section in ("floor-plan", "the-board", "back-pages"):
            html = page().replace(f'<h2>{section}</h2>', f'<h2>{section}</h2><div class="three"><article><h3>Loose card</h3></article></div>')
            code, out = check(html)
            self.assertEqual(code, 1, section)
            self.assertIn('"Loose card" is not in a group', out)

    def test_names_a_group_with_no_tagline(self):
        html = page().replace('<h2>back-pages</h2>', '<h2>back-pages</h2><div class="three"><div class="group"><article><h4>A story</h4></article></div></div>')
        code, out = check(html)
        self.assertEqual(code, 1)
        self.assertIn("group with no tagline", out)

    def test_cards_grouped_under_taglines_are_fine(self):
        html = page().replace('<h2>back-pages</h2>', '<h2>back-pages</h2><div class="three"><div class="group"><h3 class="tagline">The kitchen had a big week</h3>'
                              '<article><h4>Pho</h4><p>Good.</p></article><article><h4>Bread</h4><p>Flat.</p></article></div></div>')
        code, out = check(html)
        self.assertEqual(code, 0, out)

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

    def test_names_a_section_with_rows_and_no_prompt_kind(self):
        code, out = check(page(ledger_open='<section id="the-ledger" data-choices="do done">'))
        self.assertEqual(code, 1)
        self.assertIn("section #the-ledger has action rows but data-prompt is not vault or suite", out)
        code, out = check(page(ledger_open='<section id="the-ledger" data-prompt="both" data-choices="do done">'))
        self.assertIn("section #the-ledger has action rows but data-prompt is not vault or suite", out)

    def test_names_a_section_with_rows_and_no_valid_choices(self):
        code, out = check(page(ledger_open='<section id="the-ledger" data-prompt="vault">'))
        self.assertEqual(code, 1)
        self.assertIn("section #the-ledger has action rows but data-choices is empty or holds a value other than do, veto, snooze, or done", out)
        code, out = check(page(ledger_open='<section id="the-ledger" data-prompt="vault" data-choices="do maybe">'))
        self.assertIn("data-choices is empty or holds a value other than", out)

    def test_names_a_choice_the_legend_does_not_explain(self):
        code, out = check(page(ledger_open='<section id="the-ledger" data-prompt="vault" data-choices="do veto done">'))
        self.assertEqual(code, 1)
        self.assertIn("section #the-ledger: the legend does not explain veto", out)

    def test_names_a_legend_entry_for_a_choice_the_section_drops(self):
        code, out = check(page(ledger_open='<section id="the-ledger" data-prompt="vault" data-choices="do">'))
        self.assertEqual(code, 1)
        self.assertIn("section #the-ledger: the legend explains done, which the section does not offer", out)

    def test_names_a_section_with_rows_and_no_legend(self):
        code, out = check(page(legend=""))
        self.assertEqual(code, 1)
        self.assertIn("section #the-ledger: the legend does not explain do", out)

    def test_a_suite_row_can_point_at_a_vault_row(self):
        row = ROW.format(id="editorial-1").replace('data-id="editorial-1"', 'data-id="editorial-1" data-relates="ledger-1"')
        self.assertEqual(check(page(suite_rows=(row,))), (0, "ok\n"))

    def test_names_a_relation_to_a_row_that_is_not_on_the_page(self):
        row = ROW.format(id="editorial-1").replace('data-id="editorial-1"', 'data-id="editorial-1" data-relates="gone"')
        code, out = check(page(suite_rows=(row,)))
        self.assertEqual(code, 1)
        self.assertIn("action row editorial-1 relates to gone, which is not a vault row on the page", out)

    def test_names_a_relation_to_a_suite_row(self):
        first = ROW.format(id="editorial-1")
        second = ROW.format(id="editorial-2").replace('data-id="editorial-2"', 'data-id="editorial-2" data-relates="editorial-1"')
        code, out = check(page(suite_rows=(first, second)))
        self.assertEqual(code, 1)
        self.assertIn("action row editorial-2 relates to editorial-1, which is not a vault row on the page", out)

    def test_names_a_relation_on_a_vault_row(self):
        row = ROW.format(id="ledger-1").replace('data-id="ledger-1"', 'data-id="ledger-1" data-relates="ledger-1"')
        code, out = check(page(rows=(row,)))
        self.assertEqual(code, 1)
        self.assertIn("action row ledger-1 relates to ledger-1, but only a suite row can relate to a vault row", out)

    def test_a_row_can_override_the_section_prompt_kind(self):
        row = ROW.format(id="editorial-1").replace('data-id="editorial-1"', 'data-id="editorial-1" data-prompt="vault"')
        first = ROW.format(id="editorial-2").replace('data-id="editorial-2"', 'data-id="editorial-2" data-relates="editorial-1"')
        self.assertEqual(check(page(suite_rows=(row, first))), (0, "ok\n"))

    def test_names_a_row_with_a_bad_prompt_kind(self):
        row = ROW.format(id="editorial-1").replace('data-id="editorial-1"', 'data-id="editorial-1" data-prompt="both"')
        code, out = check(page(suite_rows=(row,)))
        self.assertEqual(code, 1)
        self.assertIn("action row editorial-1 has no data-prompt of vault or suite", out)

    def test_wants_the_two_prompt_boxes_when_the_page_has_rows(self):
        code, out = check(page(prompts=""))
        self.assertEqual(code, 1)
        self.assertIn("the page has no textarea #prompt-vault", out)
        self.assertIn("the page has no textarea #prompt-suite", out)

    def test_names_a_prompt_box_that_is_read_only(self):
        code, out = check(page(prompts=PROMPTS.replace('id="prompt-vault"', 'id="prompt-vault" readonly')))
        self.assertEqual(code, 1)
        self.assertIn("textarea #prompt-vault is read-only; the user must be able to edit the prompt", out)


if __name__ == "__main__":
    unittest.main()
