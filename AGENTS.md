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

### Snapshot (2026-07-03)

- Done: `000–006` archived; garden design state unchanged (Lamsam + Makhom in `design/placements.json`).
- Done: `007` analyzed `resources/quotation/quotation.pdf`; actual quote `178,750` THB; grass line suspicious.
- Done: `008` created `resources/quotation/benchmark-quotation.html`; benchmark `120,120` THB (+48.8% vs actual).
- Done: `009` analyzed `resources/quotation/plan.jpg`; created `resources/quotation/benchmark-quotation-v2.html` (v1 untouched); red-box gravel `93.3` sqm, grass `306.6` sqm; v2 total `64,782` THB (grass+gravel vs actual `78,750` THB).
- Active Task: none; `007–009` done but not archived.
- Reload: `[task/index.md](task/index.md)`, `[task/log.md](task/log.md)`, `[resources/quotation/benchmark-quotation-v2.html](resources/quotation/benchmark-quotation-v2.html)`, `[resources/quotation/plan.jpg](resources/quotation/plan.jpg)`

## Task state pointers

- Active index: `[task/index.md](task/index.md)`
- Activity log: `[task/log.md](task/log.md)`
- Archive: `task/archive/2026-06-10/`
