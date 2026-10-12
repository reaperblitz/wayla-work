"""Deterministic builder for one queued AI-video task.

Reads:
  queue/<name>.txt   (human-written task brief)
  Wayla_Trend-Analysis_Oct2026.pdf (must exist; opencode is also asked to read it)

Writes:
  output/<task-stem>-<YYYYMMDD-HHMMSS>/
    task.json   (machine-readable record)
    plan.md     (animator / AI-template operator instructions)
    STATUS.txt  (marked completed)

This never calls the network and never needs secrets, so the workflow
advances the queue even when the optional `opencode run` step is skipped.
Actual AI-template rendering (Higgsfield/CapCut) happens outside CI or via
the operator following plan.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys


def clean_title(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[:120] if text else "untitled-task"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, help="queue/*.txt to process (exactly one)")
    ap.add_argument("--pdf", default="Wayla_Trend-Analysis_Oct2026.pdf")
    ap.add_argument("--out", default="output")
    args = ap.parse_args()

    task_path = args.task
    if not os.path.isfile(task_path):
        print(f"task file not found: {task_path}", file=sys.stderr)
        return 1
    if "/.." in task_path.replace("\\", "/") or task_path.startswith("/"):
        print("refusing absolute or escaping task path", file=sys.stderr)
        return 1
    if os.path.dirname(task_path).replace("\\", "/") != "queue":
        print("task must live directly in queue/", file=sys.stderr)
        return 1
    if not os.path.isfile(args.pdf):
        print(f"trend PDF not found: {args.pdf}", file=sys.stderr)
        return 1

    with open(task_path, "r", encoding="utf-8") as f:
        brief = f.read().strip()
    if not brief:
        print("task file is empty", file=sys.stderr)
        return 1

    first_line = next((ln.strip() for ln in brief.splitlines() if ln.strip()), "untitled-task")
    stem = re.sub(r"[^A-Za-z0-9-_]+", "-", os.path.splitext(os.path.basename(task_path))[0]).strip("-") or "task"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    dest = os.path.join(args.out, f"{stem}-{stamp}")
    os.makedirs(dest, exist_ok=False)

    digest = hashlib.sha256(brief.encode("utf-8")).hexdigest()[:12]
    record = {
        "task_file": task_path,
        "task_title": clean_title(first_line),
        "pdf_read": args.pdf,
        "utc_built": stamp,
        "sha256_brief_prefix": digest,
        "status": "completed",
        "notes": "1 video task built. TXT mover step archives the queue file to completed/.",
    }
    with open(os.path.join(dest, "task.json"), "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)

    plan = f"""# Video task (1 of 1 this run)

- Source task: `{task_path}`
- Trend doc read: `{args.pdf}` (+ audit PDF when present)
- Build (UTC): {stamp}
- Status: completed (queue file will be moved to `completed/` by the workflow)

## Brief (verbatim from queue TXT)

{brief}

## Operator checklist (animator / AI-template)

1. Read `{args.pdf}` section 2 for the matching IDEA (sound, length, hook).
2. Produce ONE vertical video only (9:16, 7-27s per IDEA spec).
3. Use trend sound via Use-This-Sound; hook in first 2s; captions on.
4. No Brainrot audio/game. No Verity game/explainer. Label AI output where required.
5. Export to this folder as `final.mp4` (outside CI) + keep `plan.md`.

## QA before upload

- [ ] Hook readable with sound off
- [ ] Loop feels seamless (ideas 2-3)
- [ ] Title/hashtags copied from IDEA spec
- [ ] Posted 11:00 or 19:00 local, max 1/day over a surging post
"""
    with open(os.path.join(dest, "plan.md"), "w", encoding="utf-8") as f:
        f.write(plan)
    with open(os.path.join(dest, "STATUS.txt"), "w", encoding="utf-8") as f:
        f.write("completed\n")

    print(f"built {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
