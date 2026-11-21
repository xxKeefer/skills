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

    def scan(self, *extra):
        p = subprocess.run(
            [sys.executable, SCRIPT, self.root, "--journal", os.path.join(self.root, "01-journal"),
             "--today", TODAY, *extra],
            capture_output=True, text=True,
        )
        if p.returncode:
            raise AssertionError(p.stderr)
        return json.loads(p.stdout)


def base(v):
    v.write("01-journal/occasions.md", "## Chores\n- [ ] **Kitchen**\n\t- [ ] 🧼 Dishes On\n| Sunday | 🧹 Vacuum |\n",
            date="2026-01-01")


class Ages(unittest.TestCase):
    def test_age_comes_from_the_last_commit_not_the_file_time(self):
        v = Vault(self)
        base(v)
        v.write("02-research/old.md", "old", date="2026-08-23")
        out = v.scan()
        self.assertEqual(out["dates_from"], "git")
        stale = {s["path"]: s for s in out["stale"]}
        self.assertEqual(stale["02-research/old.md"]["age_days"], 90)

    def test_a_file_changed_since_its_last_commit_takes_its_file_time(self):
        v = Vault(self)
        base(v)
        v.write("02-research/edited.md", "v1", date="2026-01-10")
        v.write("02-research/edited.md", "v2")
        out = v.scan()
        self.assertNotIn("02-research/edited.md", [s["path"] for s in out["stale"]])
        self.assertEqual(out["activity"]["edits_by_folder"], {"02-research": 1})

    def test_without_git_age_comes_from_the_file_time(self):
        v = Vault(self, git=False)
        base(v)
        v.write("02-research/new.md", "new")
        self.assertEqual(v.scan()["dates_from"], "mtime")


class Links(unittest.TestCase):
    def test_finds_broken_links_and_skips_template_placeholders(self):
        v = Vault(self)
        base(v)
        v.write("03-reference/a.md", "See [[b]], [[b#Part|alias]], [[gone]], [[{{date}}]], `[[in code]]`.")
        v.write("03-reference/b.md", "Back to [[03-reference/a]] and ![[pic.png]] and ![[missing.png]].")
        v.write("99-meta/assets/pic.png", "x", date="2026-11-01")
        out = v.scan()
        self.assertEqual(out["links"]["broken"], [
            {"target": "gone", "count": 1, "from": ["03-reference/a.md"]},
            {"target": "missing.png", "count": 1, "from": ["03-reference/b.md"]},
        ])

    def test_groups_broken_links_by_target_with_the_most_linked_first(self):
        v = Vault(self)
        base(v)
        v.write("07-omen/a.md", "[[Ella]] [[Rose]]")
        v.write("07-omen/b.md", "[[Ella]]")
        v.write("CLAUDE.md", "[[root example]]")
        broken = v.scan()["links"]["broken"]
        self.assertEqual([(b["target"], b["count"]) for b in broken], [("Ella", 2), ("Rose", 1)])

    def test_orphans_are_notes_with_no_backlinks_outside_the_journal(self):
        v = Vault(self)
        base(v)
        v.write("03-reference/a.md", "[[b]]")
        v.write("03-reference/b.md", "no links")
        v.write("01-journal/2026-wk47-fri.md", daily("2026-11-20", "- [ ] x"), date="2026-11-20")
        out = v.scan()
        self.assertEqual(out["links"]["orphans"], ["03-reference/a.md"])


class Stale(unittest.TestCase):
    def test_stale_lists_old_notes_and_their_recent_backlinks(self):
        v = Vault(self)
        base(v)
        v.write("02-research/old.md", "old", date="2026-01-10")
        v.write("02-research/linked.md", "old", date="2026-01-10")
        v.write("02-research/fresh.md", "new [[linked]]", date="2026-11-20")
        out = v.scan("--stale", "90")
        stale = {s["path"]: s for s in out["stale"]}
        self.assertEqual(set(stale), {"02-research/old.md", "02-research/linked.md"})
        self.assertEqual(stale["02-research/linked.md"]["recent_backlinks"], 1)
        self.assertEqual(stale["02-research/old.md"]["recent_backlinks"], 0)

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
        v.write("03-reference/r.md", "[[kept]]", date="2026-11-01")
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

    def test_broken_nav_names_each_up_prev_next_that_does_not_resolve(self):
        v = Vault(self)
        base(v)
        v.write("01-journal/2026-wk47-week.md", "---\ntype: journal/weekly\n---\n")
        v.write("01-journal/2026-11-20.md", daily("2026-11-20", "- [x] a").replace(
            "up: '[[2026-wk47-week]]'", "up: '[[2026-wk47-week]]'\nprev: '[[2026-wk47-thu]]'"))
        nav = v.scan()["journal"]["broken_nav"]
        self.assertEqual(nav, [{"path": "01-journal/2026-11-20.md", "key": "prev", "target": "2026-wk47-thu"}])


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
        v.write("07-omen/old.md", "x", date="2026-01-01")
        v.write("07-omen/session.md", "one two", date="2026-11-18")
        v.write("06-lessons/vim.md", "x", date="2026-11-20")
        v.write("01-journal/2026-11-20.md", daily("2026-11-20", "- [x] a"), date="2026-11-20")
        self.assertEqual(v.scan("--window", "7")["recent"], [
            {"path": "06-lessons/vim.md", "age_days": 1, "words": 1},
            {"path": "07-omen/session.md", "age_days": 3, "words": 2},
        ])


class Limits(unittest.TestCase):
    def test_caps_each_long_list_and_gives_its_total(self):
        v = Vault(self)
        base(v)
        for i in range(5):
            v.write(f"02-research/n{i}.md", f"[[gone{i}]]", date="2026-01-10")
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
        v.write("02-research/a.md", "---\ntags: [rust, ideas]\n---\nx", date="2026-11-18")
        v.write("02-research/b.md", "---\ntags:\n  - rust\n---\nx", date="2026-11-19")
        v.write("03-reference/old.md", "x", date="2026-01-01")
        act = v.scan("--window", "7")["activity"]
        self.assertEqual(act["edits_by_folder"], {"02-research": 2})
        self.assertEqual(act["hours"][10], 2)
        self.assertEqual(act["tags"][0], ["rust", 2])


if __name__ == "__main__":
    unittest.main()
