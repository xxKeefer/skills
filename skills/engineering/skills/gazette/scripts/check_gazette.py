#!/usr/bin/env python3
"""Checks a gazette page. Prints ok and exits 0, or prints each problem and exits 1."""
import re
import sys
from html.parser import HTMLParser

SECTIONS = ["masthead", "lead", "weather", "your-desk", "around-the-repos", "the-board", "honour-roll"]
TICKET = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")
PR = re.compile(r"(?<![\w&])#\d+\b")
GROUPED = {"your-desk", "around-the-repos", "the-board"}
PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.problems = []
        self.sections = set()
        self.link_depth = 0
        self.code_depth = 0
        self.skip_depth = 0
        self.in_body = False
        self.card = None
        self.section = None
        self.divs = []
        self.in_label = False
        self.in_headline = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for _, value in attrs:
            for found in PLACEHOLDER.findall(value or ""):
                self.problems.append(f"placeholder {found} is still on the page")
        if tag == "body":
            self.in_body = True
        if tag in ("style", "script"):
            self.skip_depth += 1
        if tag in ("code", "pre"):
            self.code_depth += 1
        if a.get("id") in SECTIONS:
            self.sections.add(a["id"])
        if self.in_body and "style" in a:
            self.problems.append(f'<{tag}> has an inline style. Use a class from the template: style="{a["style"]}"')
        if tag == "section" and a.get("id"):
            self.section = a["id"]
        classes = (a.get("class") or "").split()
        if tag == "div":
            self.divs.append({"tagline": False} if "group" in classes else None)
        if "tagline" in classes:
            for group in reversed(self.divs):
                if group:
                    group["tagline"] = True
                    break
        if tag == "article":
            self.card = {"label": "", "headline": "", "headline_hrefs": [], "desk": self.section == "your-desk", "done": False}
        if self.card is not None and tag == "input" and a.get("type") == "checkbox" and "done" in (a.get("class") or "").split():
            self.card["done"] = True
        if self.card is not None and tag == "span" and "label" in (a.get("class") or "").split():
            self.in_label = True
        if self.card is not None and tag in ("h3", "h4"):
            self.in_headline = True
        if tag == "a" and self.in_headline:
            self.card["headline_hrefs"].append(a.get("href", ""))
        if tag == "a":
            self.link_depth += 1
            href = a.get("href", "")
            if a.get("target") != "_blank":
                self.problems.append(f'link {href} has no target="_blank"')
            if "noopener" not in (a.get("rel") or ""):
                self.problems.append(f'link {href} has no rel="noopener"')

    def handle_endtag(self, tag):
        if tag == "span":
            self.in_label = False
        if tag in ("h3", "h4"):
            self.in_headline = False
        if tag == "div" and self.divs:
            group = self.divs.pop()
            if group and not group["tagline"]:
                self.problems.append(f"#{self.section}: a group with no tagline")
        if tag == "article" and self.card is not None:
            label = self.card["label"].strip()
            if "review" in label.lower() and not any("/pull/" in h for h in self.card["headline_hrefs"]):
                self.problems.append(f'review card "{label}" does not link its headline to the PR')
            if self.section in GROUPED and not any(self.divs):
                self.problems.append(f'#{self.section}: card "{self.card["headline"].strip()}" is not in a group')
            if self.card["desk"] and not self.card["done"]:
                self.problems.append(f'your-desk card "{self.card["headline"].strip()}" has no done checkbox')
            self.card = None
        if tag == "section":
            self.section = None
        if tag == "a":
            self.link_depth -= 1
        if tag in ("code", "pre"):
            self.code_depth -= 1
        if tag in ("style", "script"):
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.in_label:
            self.card["label"] += data
        if self.in_headline:
            self.card["headline"] += data
        for found in PLACEHOLDER.findall(data):
            self.problems.append(f"placeholder {found} is still on the page")
        if self.skip_depth or self.link_depth or self.code_depth:
            return
        for found in TICKET.findall(data):
            self.problems.append(f"ticket key {found} is not a link")
        for found in PR.findall(data):
            self.problems.append(f"PR {found} is not a link")


def main(path):
    page = Page()
    with open(path) as f:
        page.feed(f.read())
    problems = page.problems + [f"section #{s} is missing" for s in SECTIONS if s not in page.sections]
    for problem in problems:
        print(problem)
    if problems:
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
