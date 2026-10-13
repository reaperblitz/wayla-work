"""Build render props for the Remotion WaylaShort composition from a queue TXT.

Deterministic fallback so CI can render even when the `opencode run` step
is skipped (no LLM key). opencode may overwrite remotion/props.json with
better copy; this script only fills it in when missing/invalid.
"""

from __future__ import annotations

import argparse
import json
import os
import re


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--props", default="remotion/props.json")
    ap.add_argument("--max-title", type=int, default=90)
    ap.add_argument("--max-hook", type=int, default=60)
    ap.add_argument("--max-caption", type=int, default=160)
    args = ap.parse_args()

    if os.path.isfile(args.props):
        try:
            data = json.load(open(args.props, encoding="utf-8"))
            if all(k in data for k in ("title", "hook", "caption", "taskStem")):
                print(f"props exist, keeping {args.props}")
                return 0
        except Exception as e:  # noqa: BLE001 - fall through and regenerate
            print(f"props invalid ({e}), regenerating")

    with open(args.task, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.read().splitlines()]
    stem = re.sub(r"[^A-Za-z0-9-_]+", "-", os.path.splitext(os.path.basename(args.task))[0]).strip("-")
    content = [ln for ln in lines if ln]
    skip = ("source:", "channel:")
    meaningful = [ln for ln in content if not ln.lower().startswith(skip)] or content or [stem]
    title = (meaningful[1] if len(meaningful) > 1 else meaningful[0])[: args.max_title]
    hook_src = meaningful[0].replace("IDEA", "IDEA ").strip()
    hook = hook_src[: args.max_hook]
    caption = " ".join(meaningful[2:])[: args.max_caption] if len(meaningful) > 2 else "Automated Shorts render"

    os.makedirs(os.path.dirname(args.props), exist_ok=True)
    json.dump(
        {"title": title, "hook": hook, "caption": caption, "taskStem": stem},
        open(args.props, "w", encoding="utf-8"),
        indent=2,
    )
    print(f"wrote {args.props}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
