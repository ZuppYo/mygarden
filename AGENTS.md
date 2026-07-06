# Landscaping AI Agent Workspace

## Repository mission

- Professional Landscaping and Gardening Assistant AI
- In-scope: Design gardens/landscapes based on home layout photos under `resources/`, programmatically edit/composite images, and draft landscaping tasks.
- Out-of-scope: Construction of gardens, physically buying plants, or managing non-gardening tasks.

## Non-negotiable rules

- Design gardens strictly matching the viewpoints and details in `resources/*.png`.
- Perform image edits using hybrid pipeline: `place --guide-dir` (position) then `generate_image` (blend into CGI style).
- Never use `place` without guide-dir as final output on 3D renders; never use text-only `generate_image` without placement guide.
- Partial views with roof/structure occlusion: run `composite-foreground --view <viewId>` after blend (see `design/occluders.json`).
- Use `iom-todo-task` and `iom-todo-task-archive` workflow for all planning and execution.
- Maintain the ultra-compact template of `AGENTS.md` (keep token usage low).
- Keep file paths relative to workspace root in tasks/logs, but resolve absolute paths when executing tools.

## Reload pack (minimal)

- `[AGENTS.md](AGENTS.md)`
- `[task/index.md](task/index.md)`
- `[task/log.md](task/log.md)`
- `[design/WORKFLOW.md](design/WORKFLOW.md)`
- Active Task: none (await next task)

## Continuity — latest activity

### Snapshot (2026-07-06)

- Done: `007–010` quotation; `summary.html` (self-contained, plan-2 embedded base64, ~421 KB) at `resources/quotation/summary.html`.
- qt-v1: benchmark `121,266` THB; vendor plan `438,818` THB; back-gravel alt vendor `235,965` / benchmark `~149,904` THB.
- Clarified: benchmark = **market estimate** (task 007 web research, task 008 mid-range picks) — **not** สรท./ราชการ; task 007 has ranges but **no URLs saved in repo**.
- Active Task: none; `007–010` done, not archived.
- **Next session:** add price **source citations** (URLs) to `summary.html` and/or `task/007`; optional `benchmark-back-gravel.html`.
- Reload: `[summary.html](resources/quotation/summary.html)`, `[task/007-analyze-landscaping-quotation.md](task/007-analyze-landscaping-quotation.md)`, `[qt-v1/](resources/quotation/qt-v1/)`, `[plan-2.jpg](resources/quotation/plan-2.jpg)`

## Task state pointers

- Active index: `[task/index.md](task/index.md)`
- Activity log: `[task/log.md](task/log.md)`
- Archive: `task/archive/2026-06-10/`
