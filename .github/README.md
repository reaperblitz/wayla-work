# Video task queue (Remotion MP4 edition)

Schedule: **08:00 and 15:00 UTC daily** (`0 8,15 * * *`).
Queue-gated: if `queue/*.txt` is empty at that time, the run exits successfully with no work.
One TXT per run (oldest first). Each run renders **one 9:16 MP4 (1080x1920, 15s, h264)**
with Remotion, uploads it to **Actions Artifacts with 2-day retention** (auto-deleted
after ~2 days), posts a **Discord webhook** message, moves the TXT to `completed/`,
and stops. **MP4s are never committed to the repo.**

Weekly: `weekly-cleanup.yml` runs **Sundays 00:00 UTC** and deletes all
`completed/*.txt` (keeps `.gitkeep`).

## Folders

- `queue/` — one `.txt` per video task. Runner consumes the oldest.
- `completed/` — finished queue files land here; purged weekly.
- `render/` — local/CI render scratch (git-ignored, never committed).
- `remotion/` — Remotion 9:16 project (`WaylaShort`, 1080x1920, 30fps, 450 frames).
- `output/<task>-<timestamp>/` — tiny `plan.md` / `task.json` / `STATUS.txt` records only.
- `prompts/make_video.md` — exact prompt for `opencode run` (writes `remotion/props.json`).
- `scripts/make_props.py` — deterministic props fallback. `scripts/build_task.py` — record builder.

## Secrets (Settings > Secrets and variables > Actions)

- `OPENCODE_API_KEY` **or** `ANTHROPIC_API_KEY` (optional) — enables the `opencode run` copy step.
  Without either, the run still renders via the deterministic props builder.
- `DISCORD_WEBHOOK_URL` (required for alerts) — Discord channel webhook. Each completed
  video posts task name, MP4 size, artifact name (2-day expiry), and run link.
  Without it, the run succeeds but skips the Discord step with a log notice.

`GITHUB_TOKEN` (automatic) pushes the queue move + records.

## Manual run

Actions > video-task-queue > Run workflow. Optional `task` input picks a file,
e.g. `queue/IDEA3-burning-bridges-dinner.txt`. Empty = oldest.
Download MP4s from the run's **Artifacts** section within 2 days.

## GitHub TOS compliance

- Twice-daily cron + weekly cleanup only; `timeout-minutes` set; single job;
  `concurrency` groups prevent overlaps. No sleep loops, no runner persistence.
- Least-privilege `permissions: contents: write` (queue move + records).
- Pinned marketplace actions by major version (`checkout@v4`, `setup-python@v5`,
  `setup-node@v4`, `upload-artifact@v4`).
- opencode via `npm install -g @opencode/cli` (auditable); non-interactive
  `opencode --standalone run` with bounded prompt; failures never block the queue.
- Remotion via `npm ci` on a pinned `package-lock.json`; no `curl | bash` in CI.
- No mining, no secret exfiltration (webhook URL only ever used as POST target),
  one commit per consumed task, binaries excluded from git via `.gitignore`.
- Scheduled workflows may be delayed and auto-disabled after 60 days of repo
  inactivity — re-enable in Actions if needed. Cron times are UTC.
