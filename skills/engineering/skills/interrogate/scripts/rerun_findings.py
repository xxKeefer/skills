#!/usr/bin/env python3
import argparse
import json
import os
import signal
import subprocess
import sys


def rerun(f, timeout):
    command = (f.get("command") or "").strip()
    evidence = (f.get("evidence") or "").strip()
    cwd = f.get("cwd") or os.getcwd()
    if not command:
        return None, "no command"
    if not evidence:
        return None, "no evidence"
    if not os.path.isdir(cwd):
        return None, "cwd not found"
    proc = subprocess.Popen(
        command, shell=True, cwd=cwd, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True,
    )
    try:
        output, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.communicate()
        return None, "timed out"
    if proc.returncode == 0:
        return None, "passed on re-run"
    if evidence not in output:
        return None, "evidence not in output"
    return {"output": output, "exit": proc.returncode}, None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("findings")
    p.add_argument("--timeout", type=float, default=120)
    args = p.parse_args()
    try:
        with open(args.findings) as fh:
            findings = json.load(fh)
    except (OSError, ValueError) as e:
        print(f"cannot read {args.findings}: {e}")
        return 1
    if not isinstance(findings, list):
        print("findings file must hold a JSON list")
        return 1
    for i, f in enumerate(findings, 1):
        if not isinstance(f, dict):
            print(f"finding {i} is not an object")
            return 1
    kept, dropped = [], []
    for f in findings:
        proof, reason = rerun(f, args.timeout)
        if proof:
            kept.append({**f, **proof})
        else:
            dropped.append({**f, "reason": reason})
    print(json.dumps({"kept": kept, "dropped": dropped}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
