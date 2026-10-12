# Video task queue

Schedule: **08:00 and 15:00 UTC daily** (`0 8,15 * * *`).
Queue-gated: if `queue/*.txt` is empty at that time, the run exits successfully with no work.
One TXT per run (oldest first), then the workflow moves it to `completed/` and stops.

## Folders

- `queue/` — put one `.txt` per AI-video task here. The runner consumes the oldest.
- `completed/` — finished queue files land here (via `git mv` + push).
- `output/<task>-<timestamp>/` — `plan.md`, `task.json`, `STATUS.txt` per completed task.
- `prompts/make_video.md` — exact prompt given to `opencode run`.
- `scripts/build_task.py` — deterministic builder (no network, no secrets).

## Secrets (optional but recommended)

Settings > Secrets and variables > Actions > New repository secret:

- `OPENCODE_API_KEY` **or** `ANTHROPIC_API_KEY` — lets the `opencode run` step call a model.
- Without either key, the workflow skips `opencode run` and still builds the artifact + advances the queue.

No other secrets needed. `GITHUB_TOKEN` (automatic) is used to push the queue move + output.

## Manual run

Actions > video-task-queue > Run workflow. Optional input `task` picks a specific file,
e.g. `queue/IDEA2-mandem-attack-shrug.txt`. Empty = oldest.

## GitHub TOS compliance

- Twice-daily cron only, `timeout-minutes: 20`, single job, `concurrency` group so runs never overlap.
- Least-privilege `permissions: contents: write` (needed to archive queue + save output).
- Pinned marketplace actions by major version (`checkout@v4`, `setup-python@v5`, `setup-node@v4`).
- opencode installed via `npm install -g @opencode/cli` (auditable registry install, no `curl | bash` in CI).
- Non-interactive `opencode --standalone run` with a bounded prompt; failure never blocks queue progress.
- No mining, no sleep loops, no runner persistence, no secret exfiltration, no spam commits (one commit per consumed task).
- Note: GitHub may delay scheduled runs and auto-disable schedules after 60 days of repo inactivity — re-enable in Actions if needed.
- Times are UTC (GitHub cron is always UTC). 08:00/15:00 local = convert to UTC cron if you need local time.
