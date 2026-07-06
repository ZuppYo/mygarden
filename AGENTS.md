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
- Active Task: [011-southern-benchmark-pricing](task/011-southern-benchmark-pricing.md)

## Continuity — latest activity

### Snapshot (2026-07-06)

- Done: task 011 — สำรวจราคากลางภาคใต้; ภาคใต้**ไม่ครบ** (หญ้าครบ, หิน/ปู/คอนกรีตบางส่วน, ทรายล้าง+carport ไม่พบ); อัปเดต `summary.html` ข้อ 3+10
- Active Task: [011-southern-benchmark-pricing](task/011-southern-benchmark-pricing.md) — done; archive optional
- Reload: `[resources/quotation/summary.html](resources/quotation/summary.html)`

## Task state pointers

- Active index: `[task/index.md](task/index.md)`
- Activity log: `[task/log.md](task/log.md)`
- Archive: `task/archive/2026-06-10/`
