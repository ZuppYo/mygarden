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

- Done: `000–006` archived; garden design unchanged (Lamsam + Makhom in `design/placements.json`).
- Done: `007–010` quotation work — PDF `178,750` THB; plan.jpg v2 gravel `93.3` / grass `306.6` sqm; plan-2 qt-v1 areas grass `177.3`, gravel `83.7`, paving `38.6`, concrete `102.0`, carport `36.5` sqm.
- qt-v1: benchmark `121,266` THB vs vendor plan areas `438,818` THB; vendor alt back-gravel `235,965` THB (`12.88×12.35` → stone).
- Active Task: none; `007–010` done, not archived.
- Reload: `[task/index.md](task/index.md)`, `[task/log.md](task/log.md)`, `[resources/quotation/qt-v1/](resources/quotation/qt-v1/)`, `[resources/quotation/plan-2.jpg](resources/quotation/plan-2.jpg)`

## Task state pointers

- Active index: `[task/index.md](task/index.md)`
- Activity log: `[task/log.md](task/log.md)`
- Archive: `task/archive/2026-06-10/`
