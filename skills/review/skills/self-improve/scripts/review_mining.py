#!/usr/bin/env python3
"""Get the review threads and failed CI runs of a window for /review:self-improve, and rate the themes.

  fetch   Writes threads.jsonl, runs.jsonl, the miner chunks, and meta.json to the cache folder.
          When meta.json is there, it makes no call and prints meta.json.
  themes  Counts and rates each theme of a draft, compares it with the last run, and writes
          themes.json to the cache folder.

Run: python3 review_mining.py fetch --repo <owner/repo> --since <date> --until <date> --cache <folder>
     python3 review_mining.py themes --cache <folder> --draft <file> [--prior <file>]
"""
import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone

# GitHub gives at most this many results for one filtered query.
CAP = 1000
PR_PAGE = 25
RUN_PAGE = 100
BODY_MAX = 500
TREND = 1.5
SECOND = timedelta(seconds=1)

SEARCH = """
query($q: String!, $first: Int!, $after: String) {
  search(query: $q, type: ISSUE, first: $first, after: $after) {
    issueCount
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on PullRequest {
        number
        reviewThreads(first: 100) {
          nodes {
            isResolved
            isOutdated
            path
            comments(first: 1) { nodes { author { __typename login } body url } }
          }
        }
      }
    }
  }
}
"""


def gh(args):
    """Returns the parsed JSON output of one gh call."""
    out = subprocess.run(["gh", *args], check=True, stdout=subprocess.PIPE, text=True).stdout
    return json.loads(out)


def parse_time(text):
    form = "%Y-%m-%dT%H:%M:%SZ" if "T" in text else "%Y-%m-%d"
    return datetime.strptime(text, form).replace(tzinfo=timezone.utc)


def stamp(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def halves(since, until):
    """Returns two windows that do not overlap and together cover the window."""
    middle = (since + (until - since) / 2).replace(microsecond=0)
    return (since, middle), (middle + SECOND, until)


def merged_prs(repo, since, until):
    """Returns the PRs merged in the window, and halves the window while the search passes the cap."""
    query = f"repo:{repo} is:pr is:merged merged:{stamp(since)}..{stamp(until)}"
    args = ["api", "graphql", "-f", f"query={SEARCH}", "-F", f"first={PR_PAGE}", "-f", f"q={query}"]
    page = gh(args)["data"]["search"]
    if page["issueCount"] > CAP:
        first, second = halves(since, until)
        return merged_prs(repo, *first) + merged_prs(repo, *second)
    prs = page["nodes"]
    while page["pageInfo"]["hasNextPage"]:
        page = gh(args + ["-f", f"after={page['pageInfo']['endCursor']}"])["data"]["search"]
        prs += page["nodes"]
    return prs


def failed_runs(repo, since, until):
    """Returns the failed runs of the window, and halves the window while the list passes the cap."""
    args = ["api", f"repos/{repo}/actions/runs", "-X", "GET", "-f", f"created={stamp(since)}..{stamp(until)}",
            "-f", "status=failure", "-f", f"per_page={RUN_PAGE}"]
    page = gh(args + ["-f", "page=1"])
    if page["total_count"] > CAP:
        first, second = halves(since, until)
        return failed_runs(repo, *first) + failed_runs(repo, *second)
    runs, number = page["workflow_runs"], 1
    while len(page["workflow_runs"]) == RUN_PAGE:
        number += 1
        page = gh(args + ["-f", f"page={number}"])
        runs += page["workflow_runs"]
    return runs


def failed_steps(repo, run_id):
    """Returns each failed job of a run, with its first failed step."""
    jobs = gh(["api", f"repos/{repo}/actions/runs/{run_id}/jobs", "-X", "GET", "-f", "per_page=100"])["jobs"]
    failed = []
    for job in jobs:
        if job["conclusion"] == "failure":
            step = next((s["name"] for s in job.get("steps", []) if s["conclusion"] == "failure"), None)
            failed.append({"job": job["name"], "step": step})
    return failed


def passed_workflows(repo, sha):
    """Returns the IDs of the workflows that passed on a commit."""
    args = ["api", f"repos/{repo}/actions/runs", "-X", "GET", "-f", f"head_sha={sha}", "-f", "status=success",
            "-f", f"per_page={RUN_PAGE}"]
    return {run["workflow_id"] for run in gh(args)["workflow_runs"]}


def author(who):
    """Returns the login of a bot, else human. A deleted account is human."""
    if who and (who["__typename"] == "Bot" or who["login"].endswith("[bot]")):
        return who["login"]
    return "human"


def outcome(thread):
    """Returns changed when the code at the line changed after the comment, else closed or open."""
    if thread["isOutdated"]:
        return "changed"
    return "closed" if thread["isResolved"] else "open"


def thread_records(prs):
    records = []
    for pr in prs:
        for thread in pr["reviewThreads"]["nodes"]:
            first = thread["comments"]["nodes"][0]
            records.append({"id": f"t{len(records) + 1}", "pr": pr["number"], "author": author(first["author"]),
                            "outcome": outcome(thread), "path": thread["path"], "url": first["url"],
                            "body": first["body"][:BODY_MAX]})
    return records


def run_record(run):
    return {"id": f"r{run['id']}", "run": run["id"], "workflow": run["name"], "event": run["event"],
            "branch": run["head_branch"], "sha": run["head_sha"], "created": run["created_at"],
            "url": run["html_url"]}


def surfaces(sampled):
    """Returns the sampled runs grouped by workflow, failed job, and failed step, largest group first."""
    groups = {}
    for run in sampled:
        for failure in run["failed"] or [{"job": None, "step": None}]:
            key = (run["workflow"], failure["job"], failure["step"])
            group = groups.setdefault(key, {"workflow": key[0], "job": key[1], "step": key[2], "runs": 0,
                                            "flaky": 0, "ids": []})
            group["runs"] += 1
            group["flaky"] += int(run["flaky"])
            group["ids"].append(run["id"])
    return sorted(groups.values(), key=lambda g: -g["runs"])


def review_counts(threads):
    counts = {}
    for source in ("human", "bot"):
        group = [t for t in threads if (t["author"] == "human") == (source == "human")]
        outcomes = Counter(t["outcome"] for t in group)
        counts[source] = {"threads": len(group), "changed": outcomes["changed"], "closed": outcomes["closed"],
                          "open": outcomes["open"]}
    counts["bots"] = dict(Counter(t["author"] for t in threads if t["author"] != "human"))
    return counts


def chunk_line(thread):
    body = " ".join(thread["body"].split())
    return f"[{thread['id']}|{thread['author']}|{thread['outcome']}|{thread['path']}] {body}\n"


def write_chunks(cache, threads, size):
    """Writes the human and bot threads to chunk files of at most size lines, and returns their paths."""
    os.makedirs(os.path.join(cache, "chunks"), exist_ok=True)
    paths = []
    for name in ("human", "bot"):
        group = [t for t in threads if (t["author"] == "human") == (name == "human")]
        for number, start in enumerate(range(0, len(group), size), 1):
            path = f"chunks/{name}-{number:02d}.txt"
            with open(os.path.join(cache, path), "w") as f:
                f.writelines(chunk_line(t) for t in group[start:start + size])
            paths.append(path)
    return paths


def write_json(cache, name, data):
    with open(os.path.join(cache, name), "w") as f:
        json.dump(data, f, indent=2)


def write_lines(cache, name, records):
    with open(os.path.join(cache, name), "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in records)


def read_lines(cache, name):
    with open(os.path.join(cache, name)) as f:
        return [json.loads(line) for line in f]


def fetch(repo, since, until, cache, sample=150, chunk=150):
    """Writes the threads, the failed runs, and the chunks of the window to the cache, and returns meta."""
    meta_path = os.path.join(cache, "meta.json")
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            return json.load(f)
    since, until = parse_time(since), parse_time(until)
    prs = merged_prs(repo, since, until)
    threads = thread_records(prs)
    default = gh(["api", f"repos/{repo}"])["default_branch"]
    runs = sorted(failed_runs(repo, since, until), key=lambda r: r["created_at"], reverse=True)
    records = [run_record(r) for r in runs]
    passed = {}
    for record, run in zip(records[:sample], runs[:sample]):
        record["failed"] = failed_steps(repo, run["id"])
        if run["head_sha"] not in passed:
            passed[run["head_sha"]] = passed_workflows(repo, run["head_sha"])
        record["flaky"] = run["workflow_id"] in passed[run["head_sha"]]
    os.makedirs(cache, exist_ok=True)
    write_lines(cache, "threads.jsonl", threads)
    write_lines(cache, "runs.jsonl", records)
    sampled = records[:sample]
    meta = {
        "repo": repo,
        "window": f"{stamp(since)}..{stamp(until)}",
        "defaultBranch": default,
        "mergedPrs": len(prs),
        "review": review_counts(threads),
        "ci": {
            "failedRuns": len(records),
            "byWorkflow": dict(Counter(r["workflow"] for r in records).most_common()),
            "byEvent": dict(Counter(r["event"] for r in records).most_common()),
            "onDefaultBranch": sum(r["branch"] == default for r in records),
            "sample": len(sampled),
            "flaky": sum(r["flaky"] for r in sampled),
            "surfaces": surfaces(sampled),
        },
        "chunks": write_chunks(cache, threads, chunk),
    }
    # Write meta.json last, so that a fetch that stops early gets the window again.
    write_json(cache, "meta.json", meta)
    return meta


def meets_floor(count, corpus):
    """Returns whether a group is a theme: the larger of 2 items and 1 per 100 items of its source."""
    return count >= 2 and count * 100 >= corpus


def trend(rate, last, has_prior):
    if not has_prior:
        return "baseline"
    if last is None:
        return "new"
    if rate >= last["rate"] * TREND:
        return "rising"
    if rate * TREND <= last["rate"]:
        return "declining"
    return "steady"


def themes(cache, draft, prior=None):
    """Counts and rates each draft theme, compares it with the last run, and writes themes.json."""
    threads = {t["id"]: t for t in read_lines(cache, "threads.jsonl")}
    runs = {r["id"]: r for r in read_lines(cache, "runs.jsonl") if "failed" in r}
    items = {**threads, **runs}
    unknown = [i for theme in draft for i in theme["ids"] if i not in items]
    if unknown:
        sys.exit(f"These IDs are not in the cache: {', '.join(unknown)}")
    humans = sum(t["author"] == "human" for t in threads.values())
    corpus = {"human": humans, "bot": len(threads) - humans, "ci": len(runs)}
    last = {t["slug"]: t for t in prior["themes"]} if prior else {}
    rows = []
    for theme in draft:
        picked = [items[i] for i in theme["ids"]]
        row = dict(theme, count=len(picked))
        if theme["source"] == "ci":
            row["flaky"] = sum(r["flaky"] for r in picked)
        else:
            outcomes = Counter(t["outcome"] for t in picked)
            row.update(changed=outcomes["changed"], closed=outcomes["closed"], open=outcomes["open"],
                       mostlyIgnored=outcomes["changed"] * 2 < len(picked))
        size = corpus[theme["source"]]
        row["rate"] = round(100 * len(picked) / size, 1)
        row["floor"] = meets_floor(len(picked), size)
        row["trend"] = trend(row["rate"], last.get(theme["slug"]), prior is not None)
        rows.append(row)
    slugs = {t["slug"] for t in draft}
    dropped = [t for t in prior["themes"] if t["slug"] not in slugs] if prior else []
    with open(os.path.join(cache, "meta.json")) as f:
        window = json.load(f)["window"]
    result = {"window": window, "corpus": corpus, "themes": rows, "dropped": dropped}
    write_json(cache, "themes.json", result)
    return result


def load(path):
    with open(path) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Review and CI mining for /review:self-improve.")
    commands = parser.add_subparsers(dest="command", required=True)
    get = commands.add_parser("fetch", help="Get the threads and failed runs of a window.")
    get.add_argument("--repo", required=True, help="owner/repo")
    get.add_argument("--since", required=True, help="YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ")
    get.add_argument("--until", required=True, help="YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ")
    get.add_argument("--cache", required=True, help="The cache folder of this window")
    get.add_argument("--sample", type=int, default=150, help="The newest failed runs to drill")
    get.add_argument("--chunk", type=int, default=150, help="Threads in each miner chunk")
    rate = commands.add_parser("themes", help="Count, rate, and compare the draft themes.")
    rate.add_argument("--cache", required=True)
    rate.add_argument("--draft", required=True, help="A JSON list of {slug, source, ids, ...}")
    rate.add_argument("--prior", help="The last run's themes.json. A missing file means no last run.")
    args = parser.parse_args()
    if args.command == "fetch":
        result = fetch(args.repo, args.since, args.until, args.cache, args.sample, args.chunk)
    else:
        prior = load(args.prior) if args.prior and os.path.exists(args.prior) else None
        result = themes(args.cache, load(args.draft), prior)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
