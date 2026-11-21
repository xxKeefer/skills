#!/usr/bin/env python3
"""Run: python3 scan_vault.spec.py"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_vault.py")
TODAY = "2026-11-21"


def daily(date, tasks, summary="A quiet day.", up="[[2026-wk47-week]]"):
    return (f"---\ntype: journal/daily\ndate: {date}\ntags: [journal, journal/daily]\nup: '{up}'\n---\n\n"
            f"# Day\n\n> {summary}\n\n## Today\n\n{tasks}\n")


class Vault:
    def __init__(self, tc, git=True):
        self.root = tempfile.mkdtemp()
        tc.addCleanup(lambda: shutil.rmtree(self.root, ignore_errors=True))
        os.makedirs(os.path.join(self.root, ".obsidian"))
        self.git = git
        if git:
            self.sh("git", "init", "-q")
            self.sh("git", "config", "user.email", "t@t")
            self.sh("git", "config", "user.name", "t")

    def sh(self, *args, date=None):
        env = dict(os.environ)
        if date:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date + "T10:00:00+00:00"
        subprocess.run(args, cwd=self.root, check=True, capture_output=True, env=env)

    def write(self, rel, text, date=None):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)
        if self.git and date:
            self.sh("git", "add", "-A")
            self.sh("git", "commit", "-q", "-m", rel, date=date)

    def move(self, old, new, date, text=None):
        os.makedirs(os.path.dirname(os.path.join(self.root, new)), exist_ok=True)
        self.sh("git", "mv", old, new)
        if text is not None:
            with open(os.path.join(self.root, new), "w") as f:
                f.write(text)
        self.sh("git", "add", "-A")
        self.sh("git", "commit", "-q", "-m", new, date=date)

    def scan(self, *extra):
        p = subprocess.run(
            [sys.executable, SCRIPT, self.root, "--journal", os.path.join(self.root, "01-journal"),
             "--today", TODAY, *extra],
            capture_output=True, text=True,
        )
        if p.returncode:
            raise AssertionError(p.stderr)
        return json.loads(p.stdout)


OCCASIONS = ("## Daily\n\n- [ ] **Kitchen**\n\t- [ ] 🧼 Dishes On\n\n## Weekly\n\n| Item | When | Section |\n"
             "| --- | --- | --- |\n| 🧹 Vacuum | Sun | chores |\n| Timesheet | Fri | work |\n")


def base(v, occasions=OCCASIONS):
    v.write("01-journal/occasions.md", occasions, date="2026-01-01")


class Ages(unittest.TestCase):
    def test_age_comes_from_the_last_commit_not_the_file_time(self):
        v = Vault(self)
        base(v)
        v.write("03-work/old.md", "old", date="2026-08-23")
        out = v.scan()
        self.assertEqual(out["dates_from"], "git")
        stale = {s["path"]: s for s in out["stale"]}
        self.assertEqual(stale["03-work/old.md"]["age_days"], 90)

    def test_a_file_changed_since_its_last_commit_takes_its_file_time(self):
        v = Vault(self)
        base(v)
        v.write("03-work/edited.md", "v1", date="2026-01-10")
        v.write("03-work/edited.md", "v2")
        out = v.scan()
        self.assertNotIn("03-work/edited.md", [s["path"] for s in out["stale"]])
        self.assertEqual(out["activity"]["edits_by_folder"], {"03-work": 1})

    def test_a_pure_rename_keeps_the_age_and_is_not_an_edit(self):
        v = Vault(self)
        base(v)
        v.write("03-work/old.md", "a long note body that git can match\n" * 5, date="2026-08-23")
        v.move("03-work/old.md", "06-omen/moved.md", date="2026-11-20")
        out = v.scan()
        stale = {s["path"]: s for s in out["stale"]}
        self.assertEqual(stale["06-omen/moved.md"]["age_days"], 90)
        self.assertEqual(out["activity"]["edits_by_folder"], {})
        rows = {r["days"]: r for r in out["compass"]}
        self.assertEqual((rows[7]["edits"], rows[365]["edits"]), (0, 2))
        self.assertEqual(rows[365]["busiest"], [["01-journal", 1], ["06-omen", 1]])

    def test_a_note_renamed_twice_keeps_the_age_of_its_first_content_commit(self):
        v = Vault(self)
        base(v)
        v.write("03-work/a.md", "a long note body that git can match\n" * 5, date="2026-08-23")
        v.move("03-work/a.md", "03-work/b.md", date="2026-10-01")
        v.move("03-work/b.md", "06-omen/c.md", date="2026-11-20")
        out = v.scan()
        stale = {s["path"]: s for s in out["stale"]}
        self.assertEqual(stale["06-omen/c.md"]["age_days"], 90)
        self.assertEqual({r["days"]: r for r in out["compass"]}[365]["busiest"], [["01-journal", 1], ["06-omen", 1]])

    def test_a_rename_with_a_content_change_is_an_edit(self):
        v = Vault(self)
        base(v)
        v.write("03-work/old.md", "a long note body that git can match\n" * 5, date="2026-08-23")
        v.move("03-work/old.md", "06-omen/moved.md", date="2026-11-20",
               text="a long note body that git can match\n" * 5 + "one more line\n")
        out = v.scan()
        self.assertNotIn("06-omen/moved.md", [s["path"] for s in out["stale"]])
        self.assertEqual(out["activity"]["edits_by_folder"], {"06-omen": 1})

    def test_without_git_age_comes_from_the_file_time(self):
        v = Vault(self, git=False)
        base(v)
        v.write("02-knowledge/new.md", "new")
        self.assertEqual(v.scan()["dates_from"], "mtime")


class Links(unittest.TestCase):
    def test_finds_broken_links_and_skips_template_placeholders(self):
        v = Vault(self)
        base(v)
        v.write("02-knowledge/a.md", "See [[b]], [[b#Part|alias]], [[gone]], [[{{date}}]], `[[in code]]`.")
        v.write("02-knowledge/b.md", "Back to [[02-knowledge/a]] and ![[pic.png]] and ![[missing.png]].")
        v.write("99-meta/assets/pic.png", "x", date="2026-11-01")
        out = v.scan()
        self.assertEqual(out["links"]["broken"], [
            {"target": "gone", "count": 1, "from": ["02-knowledge/a.md"]},
            {"target": "missing.png", "count": 1, "from": ["02-knowledge/b.md"]},
        ])

    def test_groups_broken_links_by_target_with_the_most_linked_first(self):
        v = Vault(self)
        base(v)
        v.write("06-omen/a.md", "[[Ella]] [[Rose]]")
        v.write("06-omen/b.md", "[[Ella]]")
        v.write("CLAUDE.md", "[[root example]]")
        broken = v.scan()["links"]["broken"]
        self.assertEqual([(b["target"], b["count"]) for b in broken], [("Ella", 2), ("Rose", 1)])

    def test_orphans_are_notes_with_no_backlinks_outside_the_journal(self):
        v = Vault(self)
        base(v)
        v.write("02-knowledge/a.md", "[[b]]")
        v.write("02-knowledge/b.md", "no links")
        v.write("01-journal/2026-wk47-fri.md", daily("2026-11-20", "- [ ] x"), date="2026-11-20")
        out = v.scan()
        self.assertEqual(out["links"]["orphans"], ["02-knowledge/a.md"])


class Stale(unittest.TestCase):
    def test_stale_lists_old_notes_and_their_recent_backlinks(self):
        v = Vault(self)
        base(v)
        v.write("03-work/old.md", "old", date="2026-01-10")
        v.write("03-work/linked.md", "old", date="2026-01-10")
        v.write("03-work/fresh.md", "new [[linked]]", date="2026-11-20")
        out = v.scan("--stale", "90")
        stale = {s["path"]: s for s in out["stale"]}
        self.assertEqual(set(stale), {"03-work/old.md", "03-work/linked.md"})
        self.assertEqual(stale["03-work/linked.md"]["recent_backlinks"], 1)
        self.assertEqual(stale["03-work/old.md"]["recent_backlinks"], 0)

    def test_stale_skips_notes_in_the_knowledge_folder(self):
        v = Vault(self)
        base(v)
        v.write("02-knowledge/kept.md", "x", date="2026-01-10")
        v.write("03-work/old.md", "x", date="2026-01-10")
        out = v.scan("--stale", "90")
        self.assertEqual([s["path"] for s in out["stale"]], ["03-work/old.md"])
        self.assertEqual(out["totals"]["stale"], 1)

    def test_stale_skips_the_journal_inbox_archive_and_meta(self):
        v = Vault(self)
        base(v)
        for rel in ("00-notes/a.md", "98-archive/a.md", "99-meta/a.md", "01-journal/a.md"):
            v.write(rel, "x", date="2026-01-10")
        self.assertEqual(v.scan()["stale"], [])


class Archive(unittest.TestCase):
    def test_old_unlinked_archive_notes_are_delete_candidates(self):
        v = Vault(self)
        base(v)
        v.write("98-archive/dead.md", "x", date="2026-03-01")
        v.write("98-archive/kept.md", "x", date="2026-03-01")
        v.write("98-archive/young.md", "x", date="2026-11-01")
        v.write("02-knowledge/r.md", "[[kept]]", date="2026-11-01")
        out = v.scan("--archive-days", "180")
        archive = {a["path"]: a["delete_candidate"] for a in out["archive"]}
        self.assertEqual(archive, {"98-archive/dead.md": True, "98-archive/kept.md": False,
                                   "98-archive/young.md": False})

    def test_links_from_inside_the_archive_do_not_keep_a_note(self):
        v = Vault(self)
        base(v)
        v.write("98-archive/a.md", "[[b]]", date="2026-03-01")
        v.write("98-archive/b.md", "[[a]]", date="2026-03-01")
        out = v.scan("--archive-days", "180")
        self.assertEqual([a["delete_candidate"] for a in out["archive"]], [True, True])


class Inbox(unittest.TestCase):
    def test_lists_each_inbox_note_with_age_and_words(self):
        v = Vault(self)
        base(v)
        v.write("00-notes/idea.md", "one two three", date="2026-11-14")
        self.assertEqual(v.scan()["inbox"], [{"path": "00-notes/idea.md", "age_days": 7, "words": 3}])


class Journal(unittest.TestCase):
    def test_missing_days_in_the_window_skip_today(self):
        v = Vault(self)
        base(v)
        for d in ("2026-11-14", "2026-11-15", "2026-11-17", "2026-11-19", "2026-11-20"):
            v.write(f"01-journal/{d}.md", daily(d, "- [x] done"))
        out = v.scan("--window", "7")
        self.assertEqual(out["journal"]["missing_days"], ["2026-11-16", "2026-11-18"])
        self.assertEqual(out["journal"]["summaries"][-1], {"date": "2026-11-20", "path": "01-journal/2026-11-20.md",
                                                            "summary": "A quiet day."})

    def test_carried_counts_the_run_of_dailies_a_leaf_task_stays_open(self):
        v = Vault(self)
        base(v)
        open_leaf = "- [ ] **Work**\n\t- [ ] Port QA walk\n\t- [x] standup"
        done_leaf = "- [x] **Work**\n\t- [x] Port QA walk\n\t- [x] standup"
        v.write("01-journal/a.md", daily("2026-11-16", done_leaf))
        for d in ("2026-11-17", "2026-11-18", "2026-11-19", "2026-11-20"):
            v.write(f"01-journal/{d}.md", daily(d, open_leaf))
        out = v.scan()
        self.assertEqual(out["journal"]["carried"], [{"task": "Port QA walk", "days": 4, "first": "2026-11-17",
                                                       "last": "2026-11-20"}])

    def test_carried_keeps_a_task_that_rolled_then_dropped(self):
        v = Vault(self)
        base(v)
        for d in ("2026-11-16", "2026-11-17", "2026-11-18"):
            v.write(f"01-journal/{d}.md", daily(d, "- [ ] bank statements"))
        v.write("01-journal/2026-11-19.md", daily("2026-11-19", "- [x] other"))
        out = v.scan()
        self.assertEqual(out["journal"]["carried"], [{"task": "bank statements", "days": 3, "first": "2026-11-16",
                                                       "last": "2026-11-18"}])

    def test_checklists_give_the_tick_rate_of_recurring_leaf_tasks(self):
        v = Vault(self)
        base(v)
        days = ["2026-11-17", "2026-11-18", "2026-11-19", "2026-11-20"]
        ticks = ["x", "x", " ", "x"]
        for d, t in zip(days, ticks):
            v.write(f"01-journal/{d}.md", daily(d, f"- [ ] **Kitchen**\n\t- [{t}] 🧼 Dishes On\n- [ ] bank statements"))
        rows = v.scan()["journal"]["checklists"]
        self.assertEqual(rows, [{"task": "🧼 Dishes On", "ticked": 3, "seen": 4, "rate": 0.75}])

    def test_checklists_count_only_the_items_that_occasions_says_are_due_that_day(self):
        v = Vault(self)
        base(v)
        tasks = "- [x] 🧹 Vacuum\n- [x] Dishes\n- [x] Timesheet\n- [ ] 🧼 Dishes On"
        v.write("01-journal/2026-11-15.md", daily("2026-11-15", tasks))
        v.write("01-journal/2026-11-20.md", daily("2026-11-20", tasks))
        rows = v.scan()["journal"]["checklists"]
        self.assertEqual(rows, [
            {"task": "🧼 Dishes On", "ticked": 0, "seen": 2, "rate": 0.0},
            {"task": "🧹 Vacuum", "ticked": 1, "seen": 1, "rate": 1.0},
        ])

    def test_an_old_layout_occasions_file_gives_its_errors_and_no_chores(self):
        v = Vault(self)
        base(v, "## Chores\n| Sunday | 🧹 Vacuum |\n")
        v.write("01-journal/2026-11-15.md", daily("2026-11-15", "- [x] 🧹 Vacuum"))
        out = v.scan()
        self.assertEqual(out["journal"]["checklists"], [])
        self.assertEqual(out["journal"]["occasions_errors"], [
            {"line": 2, "row": "| Sunday | 🧹 Vacuum |", "why": "row has 2 cells, wants 3: Item, When, Section"}])
        self.assertIsNone(out["compass"][0]["chore_rate"])

    def test_no_occasions_file_gives_no_errors_and_no_chores(self):
        v = Vault(self)
        v.write("01-journal/2026-11-20.md", daily("2026-11-20", "- [x] 🧼 Dishes On"))
        out = v.scan()
        self.assertEqual((out["journal"]["checklists"], out["journal"]["occasions_errors"]), ([], []))

    def test_broken_nav_names_each_up_prev_next_that_does_not_resolve(self):
        v = Vault(self)
        base(v)
        v.write("01-journal/2026-wk47-week.md", "---\ntype: journal/weekly\n---\n")
        v.write("01-journal/2026-11-20.md", daily("2026-11-20", "- [x] a").replace(
            "up: '[[2026-wk47-week]]'", "up: '[[2026-wk47-week]]'\nprev: '[[2026-wk47-thu]]'"))
        nav = v.scan()["journal"]["broken_nav"]
        self.assertEqual(nav, [{"path": "01-journal/2026-11-20.md", "key": "prev", "target": "2026-wk47-thu"}])

    def test_broken_nav_leaves_out_files_in_chronicles(self):
        v = Vault(self)
        base(v)
        v.write("01-journal/chronicles/2026/2026-04-chronicle.md",
                "---\ntype: journal/chronicle\nprev: '[[2026-03-chronicle]]'\n---\n", date="2026-11-20")
        self.assertEqual(v.scan()["journal"]["broken_nav"], [])


class Folders(unittest.TestCase):
    def test_reports_each_folder_with_counts_and_loose_notes_beside_subfolders(self):
        v = Vault(self)
        base(v)
        v.write("01-journal/year-2026/2026-wk13-fri.md", "x", date="2026-03-27")
        v.write("01-journal/2026-wk47-fri.md", "x", date="2026-11-20")
        folders = {f["path"]: f for f in v.scan()["folders"]}
        j = folders["01-journal"]
        self.assertEqual((j["md"], j["subfolders"], j["loose_md"], j["newest_days"]), (3, 1, 2, 1))
        self.assertEqual(folders["01-journal/year-2026"]["md"], 1)
        self.assertNotIn(".obsidian", folders)

    def test_skips_every_dot_folder(self):
        v = Vault(self)
        base(v)
        v.write(".ai/plan.md", "[[nowhere]]")
        out = v.scan()
        self.assertNotIn(".ai", [f["path"] for f in out["folders"]])
        self.assertEqual(out["links"]["broken"], [])


class Recent(unittest.TestCase):
    def test_lists_notes_outside_the_journal_edited_in_the_window_newest_first(self):
        v = Vault(self)
        base(v)
        v.write("06-omen/old.md", "x", date="2026-01-01")
        v.write("06-omen/session.md", "one two", date="2026-11-18")
        v.write("05-lessons/vim.md", "x", date="2026-11-20")
        v.write("01-journal/2026-11-20.md", daily("2026-11-20", "- [x] a"), date="2026-11-20")
        self.assertEqual(v.scan("--window", "7")["recent"], [
            {"path": "05-lessons/vim.md", "age_days": 1, "words": 1},
            {"path": "06-omen/session.md", "age_days": 3, "words": 2},
        ])


class Limits(unittest.TestCase):
    def test_caps_each_long_list_and_gives_its_total(self):
        v = Vault(self)
        base(v)
        for i in range(5):
            v.write(f"03-work/n{i}.md", f"[[gone{i}]]", date="2026-01-10")
        out = v.scan("--limit", "2")
        self.assertEqual(len(out["stale"]), 2)
        self.assertEqual(len(out["links"]["broken"]), 2)
        self.assertEqual(out["totals"]["stale"], 5)
        self.assertEqual(out["totals"]["broken"], 5)
        self.assertEqual(out["totals"]["orphans"], 5)


class Activity(unittest.TestCase):
    def test_counts_edits_by_folder_hour_and_tag_in_the_window(self):
        v = Vault(self)
        base(v)
        v.write("02-knowledge/a.md", "---\ntags: [rust, ideas]\n---\nx", date="2026-11-18")
        v.write("02-knowledge/b.md", "---\ntags:\n  - rust\n---\nx", date="2026-11-19")
        v.write("02-knowledge/old.md", "x", date="2026-01-01")
        act = v.scan("--window", "7")["activity"]
        self.assertEqual(act["edits_by_folder"], {"02-knowledge": 2})
        self.assertEqual(act["hours"][10], 2)
        self.assertEqual(act["tags"][0], ["rust", 2])


class Compass(unittest.TestCase):
    def test_gives_one_row_for_each_of_7_30_90_and_365_days(self):
        v = Vault(self)
        base(v)
        out = v.scan()
        self.assertEqual([r["days"] for r in out["compass"]], [7, 30, 90, 365])
        self.assertEqual(set(out["compass"][0]), {"days", "dailies", "edits", "chore_rate", "busiest", "reflections"})

    def test_a_daily_6_days_back_is_in_the_week_and_one_7_days_back_is_not(self):
        v = Vault(self)
        base(v)
        v.write("01-journal/a.md", daily("2026-11-15", "- [x] a"), date="2026-11-15")
        v.write("01-journal/b.md", daily("2026-11-14", "- [x] a"), date="2026-11-14")
        rows = {r["days"]: r for r in v.scan()["compass"]}
        self.assertEqual((rows[7]["dailies"], rows[30]["dailies"]), (1, 2))

    def test_counts_edits_and_the_busiest_folders_in_each_window(self):
        v = Vault(self)
        base(v)
        v.write("03-work/a.md", "x", date="2026-11-20")
        v.write("03-work/b.md", "x", date="2026-11-19")
        v.write("06-omen/a.md", "x", date="2026-11-01")
        v.write("02-knowledge/a.md", "x", date="2026-03-01")
        rows = {r["days"]: r for r in v.scan()["compass"]}
        self.assertEqual((rows[7]["edits"], rows[7]["busiest"]), (2, [["03-work", 2]]))
        self.assertEqual(rows[30]["busiest"], [["03-work", 2], ["06-omen", 1]])
        self.assertEqual(rows[365]["edits"], 5)

    def test_gives_the_chore_tick_rate_of_each_window_or_none_with_no_chores(self):
        v = Vault(self)
        base(v)
        v.write("01-journal/a.md", daily("2026-11-20", "- [ ] **Kitchen**\n\t- [x] 🧼 Dishes On"))
        v.write("01-journal/b.md", daily("2026-11-01", "- [ ] **Kitchen**\n\t- [ ] 🧼 Dishes On"))
        rows = {r["days"]: r for r in v.scan()["compass"]}
        self.assertEqual((rows[7]["chore_rate"], rows[30]["chore_rate"]), (1.0, 0.5))
        v2 = Vault(self)
        base(v2)
        self.assertIsNone(v2.scan()["compass"][0]["chore_rate"])


REFLECT = "## 🤔 Reflect\n\n### 🧠 What I learned\n\n{learned}\n### ➡️ What is next\n\n{next}\n\n### ⚠️ What caused friction\n\n"


def note(kind, date, body):
    return f"---\ntype: journal/{kind}\ndate: {date}\n---\n\n# Note\n\n## Today\n\n- [x] a\n\n{body}"


class Reflections(unittest.TestCase):
    def test_a_reflect_with_only_sub_headings_and_empty_markers_gives_nothing(self):
        v = Vault(self)
        base(v)
        v.write("01-journal/2026-wk47-fri.md", note("daily", "2026-11-20", REFLECT.format(learned="", next="- ")))
        self.assertEqual(v.scan()["reflections"], [])

    def test_gives_each_filled_sub_heading_with_its_note_level_and_date(self):
        v = Vault(self)
        base(v)
        v.write("01-journal/2026-wk47-fri.md",
                note("daily", "2026-11-20", REFLECT.format(learned="Rust lifetimes\nare fine", next="")))
        v.write("01-journal/2026-wk46-week.md", note("weekly", "2026-11-09", REFLECT.format(learned="", next="- Ship it")))
        v.write("01-journal/2026-10-oct.md", note("monthly", "2026-10-01", REFLECT.format(learned="Slow down", next="")))
        out = v.scan()["reflections"]
        self.assertEqual(out, [
            {"path": "01-journal/2026-wk47-fri.md", "level": "daily", "date": "2026-11-20",
             "sections": [{"heading": "🧠 What I learned", "text": "Rust lifetimes\nare fine"}]},
            {"path": "01-journal/2026-wk46-week.md", "level": "weekly", "date": "2026-11-09",
             "sections": [{"heading": "➡️ What is next", "text": "- Ship it"}]},
            {"path": "01-journal/2026-10-oct.md", "level": "monthly", "date": "2026-10-01",
             "sections": [{"heading": "🧠 What I learned", "text": "Slow down"}]},
        ])

    def test_a_bullet_reflect_gives_each_filled_bullet_and_drops_the_placeholders(self):
        v = Vault(self)
        base(v)
        body = ("## 🤔 Reflect\n\n- 🧠 What I learned\n\t- Rust lifetimes\n\t- are fine\n"
                "- ⚠️ What caused friction\n\t- `Annoyances`\n"
                "- ➡️ What is next\n\t- `things to carry over or push up in the journal`\n"
                "- 📝 Notes\n\t- `anything other reflections`\n")
        v.write("01-journal/2026-wk46-sun.md", note("daily", "2026-11-15", body))
        self.assertEqual(v.scan()["reflections"], [
            {"path": "01-journal/2026-wk46-sun.md", "level": "daily", "date": "2026-11-15",
             "sections": [{"heading": "🧠 What I learned", "text": "- Rust lifetimes\n\t- are fine"}]},
        ])

    def test_a_bullet_reflect_with_only_placeholders_gives_nothing(self):
        v = Vault(self)
        base(v)
        body = ("## 🤔 Reflect\n\n- 🧠 What I learned\n\t- `Learnings`\n"
                "- ⚠️ What caused friction\n\t- `Annoyances`\n")
        v.write("01-journal/2026-wk46-sun.md", note("daily", "2026-11-15", body))
        self.assertEqual(v.scan()["reflections"], [])

    def test_any_level_two_heading_ends_the_reflect_so_a_shopping_list_is_not_quoted(self):
        v = Vault(self)
        base(v)
        body = REFLECT.format(learned="", next="") + "\n## Shopping\n\n- milk\n"
        v.write("01-journal/2026-wk47-fri.md", note("daily", "2026-11-20", body))
        self.assertEqual(v.scan()["reflections"], [])

    def test_reads_the_level_and_date_from_the_file_name_when_frontmatter_has_none(self):
        v = Vault(self)
        base(v)
        v.write("01-journal/2026-wk47-thu.md", REFLECT.format(learned="x", next=""))
        v.write("01-journal/2026-wk46-week.md", REFLECT.format(learned="y", next=""))
        v.write("01-journal/2026-09-sep.md", REFLECT.format(learned="z", next=""))
        out = [(r["level"], r["date"]) for r in v.scan()["reflections"]]
        self.assertEqual(out, [("daily", "2026-11-19"), ("weekly", "2026-11-09"), ("monthly", "2026-09-01")])

    def test_a_sunday_weekly_reflect_is_a_weekly_reflection_dated_to_its_monday(self):
        v = Vault(self)
        base(v)
        body = (REFLECT.format(learned="Day text", next="") +
                "\n## 🗓️ Weekly Reflect (Sundays only)\n\n### ✅ What went well\n\nWeek text\n")
        v.write("01-journal/2026-wk46-sun.md", note("daily", "2026-11-15", body))
        out = v.scan()["reflections"]
        self.assertEqual(out, [
            {"path": "01-journal/2026-wk46-sun.md", "level": "daily", "date": "2026-11-15",
             "sections": [{"heading": "🧠 What I learned", "text": "Day text"}]},
            {"path": "01-journal/2026-wk46-sun.md", "level": "weekly", "date": "2026-11-09",
             "sections": [{"heading": "✅ What went well", "text": "Week text"}]},
        ])

    def test_an_empty_sunday_weekly_reflect_gives_no_weekly_reflection(self):
        v = Vault(self)
        base(v)
        body = (REFLECT.format(learned="Day text", next="") +
                "\n## 🗓️ Weekly Reflect (Sundays only)\n\n### ✅ What went well\n\n- \n")
        v.write("01-journal/2026-wk46-sun.md", note("daily", "2026-11-15", body))
        self.assertEqual([r["level"] for r in v.scan()["reflections"]], ["daily"])

    def test_counts_reflections_in_each_compass_window_and_drops_ones_past_a_year(self):
        v = Vault(self)
        base(v)
        v.write("01-journal/a.md", note("daily", "2026-11-15", REFLECT.format(learned="in", next="")))
        v.write("01-journal/b.md", note("daily", "2026-11-14", REFLECT.format(learned="out", next="")))
        v.write("01-journal/c.md", note("daily", "2025-11-22", REFLECT.format(learned="edge", next="")))
        v.write("01-journal/d.md", note("daily", "2025-11-21", REFLECT.format(learned="old", next="")))
        out = v.scan()
        rows = {r["days"]: r["reflections"] for r in out["compass"]}
        self.assertEqual(rows, {7: 1, 30: 2, 90: 2, 365: 3})
        self.assertEqual([r["path"] for r in out["reflections"]], ["01-journal/a.md", "01-journal/b.md", "01-journal/c.md"])


class Projects(unittest.TestCase):
    def test_reads_status_and_until_from_each_mission(self):
        v = Vault(self)
        base(v)
        v.write("04-projects/house/MISSION.md", "---\nstatus: waiting\nuntil: 2027-01-10\n---\n# House\n",
                date="2026-11-18")
        v.write("04-projects/house/house.kanban.md", "x", date="2026-11-20")
        v.write("04-projects/garden/MISSION.md", "---\nstatus: dormant\n---\n# Garden\n", date="2026-03-01")
        v.write("04-projects/bike/MISSION.md", "# Bike\n", date="2026-11-01")
        self.assertEqual(v.scan()["projects"], [
            {"project": "bike", "path": "04-projects/bike/MISSION.md", "status": "active", "until": None,
             "changed_days": 20},
            {"project": "garden", "path": "04-projects/garden/MISSION.md", "status": "dormant", "until": None,
             "changed_days": 265},
            {"project": "house", "path": "04-projects/house/MISSION.md", "status": "waiting",
             "until": "2027-01-10", "changed_days": 1},
        ])

    def test_gives_no_projects_when_the_vault_has_no_projects_folder(self):
        v = Vault(self)
        base(v)
        self.assertEqual(v.scan()["projects"], [])


if __name__ == "__main__":
    unittest.main()
