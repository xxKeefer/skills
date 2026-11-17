#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time

HOME = os.path.expanduser("~")
DIR = os.path.join(HOME, ".cache", "babysit")
STATE = os.path.join(DIR, "state.json")
PID = os.path.join(DIR, "run.pid")
VALUES = os.path.join(HOME, ".claude", "agents-md.values.json")
FIELDS = "state,headRefName,baseRefName,mergeStateStatus,reviewDecision,statusCheckRollup"
QUERY = (
    "query($owner:String!,$name:String!,$number:Int!){repository(owner:$owner,name:$name)"
    "{pullRequest(number:$number){reviewThreads(first:100){nodes{isResolved}}}}}"
)
BAD = {"FAILURE", "ERROR", "TIMED_OUT", "CANCELLED", "STARTUP_FAILURE", "ACTION_REQUIRED"}


def gh(*args):
    out = subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def load():
    try:
        with open(STATE) as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save(prs):
    os.makedirs(DIR, exist_ok=True)
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(prs, f)
    os.replace(tmp, STATE)


def classify(view, threads):
    checks = view.get("statusCheckRollup") or []
    if view["state"] in ("MERGED", "CLOSED"):
        return "done"
    if any((c.get("conclusion") or c.get("state")) in BAD for c in checks):
        return "failed"
    if view["mergeStateStatus"] in ("BEHIND", "DIRTY"):
        return "stale"
    if threads:
        return "threads"
    if any(c.get("status", "COMPLETED") != "COMPLETED" or c.get("state") in ("PENDING", "EXPECTED") for c in checks):
        return "pending"
    if view.get("reviewDecision") in ("APPROVED", "", None):
        return "ready"
    return "pending"


def notify(title, body):
    try:
        with open(VALUES) as f:
            cmd = json.load(f).get("notifier_command")
    except (FileNotFoundError, ValueError):
        return
    if cmd and cmd != "none":
        subprocess.run(["sh", "-c", cmd + ' "$1" "$2"', "sh", title, body])


def add(repo, number):
    if any(p["repo"] == repo and p["number"] == number for p in load()):
        return
    view = gh("pr", "view", str(number), "-R", repo, "--json", FIELDS)
    prs = load()
    prs.append({"repo": repo, "number": number, "head": view["headRefName"],
                "base": view["baseRefName"], "state": None, "threads": 0, "done_at": None})
    save(prs)


def poll():
    prs = load()
    live = [p for p in prs if p["state"] != "done"]
    heads = {(p["repo"], p["head"]) for p in live}
    for p in live:
        if (p["repo"], p["base"]) in heads:
            continue
        owner, name = p["repo"].split("/")
        try:
            view = gh("pr", "view", str(p["number"]), "-R", p["repo"], "--json", FIELDS)
            data = gh("api", "graphql", "-f", "query=" + QUERY, "-F", "owner=" + owner,
                      "-F", "name=" + name, "-F", "number=%d" % p["number"])
        except (subprocess.CalledProcessError, OSError, ValueError):
            continue
        nodes = data["data"]["repository"]["pullRequest"]["reviewThreads"]["nodes"]
        p["threads"] = sum(1 for n in nodes if not n["isResolved"])
        new = classify(view, p["threads"])
        old = p["state"]
        p["head"], p["base"], p["state"] = view["headRefName"], view["baseRefName"], new
        if new == "done":
            p["done_at"] = int(time.time())
        if old is not None and old != new:
            notify("babysit", "%s#%d is %s" % (p["repo"], p["number"], new))
        fresh = load()
        for q in fresh:
            if q["repo"] == p["repo"] and q["number"] == p["number"]:
                q.update(head=p["head"], base=p["base"], state=p["state"],
                         threads=p["threads"], done_at=p["done_at"])
        save(fresh)
        prs = fresh
    return any(p["state"] != "done" for p in load())


def alive(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def run(interval):
    try:
        with open(PID) as f:
            if alive(int(f.read())):
                return
    except (FileNotFoundError, ValueError):
        pass
    os.makedirs(DIR, exist_ok=True)
    with open(PID, "w") as f:
        f.write(str(os.getpid()))
    try:
        while poll():
            time.sleep(interval)
    finally:
        os.remove(PID)


def main(argv):
    if argv[0] == "add":
        add(argv[1], int(argv[2]))
    elif argv[0] == "poll":
        poll()
    elif argv[0] == "run":
        run(float(argv[2]) if argv[1:2] == ["--interval"] else 60)


if __name__ == "__main__":
    main(sys.argv[1:])
