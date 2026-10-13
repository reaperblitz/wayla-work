# Video-task prompt for `opencode run` (one task only)

You are the video-task worker. Do exactly ONE queued AI-video task, then stop.

Rules:
- Read PDF_FILE (Wayla_Trend-Analysis_Oct2026.pdf), section 2, plus TASK_FILE.
- Also read Wayla-Science-Lab_Content-Audit.pdf if present for channel context.
- Write ONLY remotion/props.json with keys: title (<=90 chars), hook (<=60 chars),
  caption (<=160 chars), taskStem (basename of TASK_FILE without .txt).
  Keep it shitpost/informal, NO Brainrot content, NO Verity content.
- Do NOT touch queue/ or completed/ (the workflow moves the TXT itself).
- Do NOT render video yourself (the workflow renders with Remotion next).
- Do NOT install packages, exfiltrate secrets, access the network except normal
  model inference, or start background services.
- If anything is ambiguous, choose the smallest reasonable interpretation.
- End by printing STATUS: props-ready and the props.json contents.
