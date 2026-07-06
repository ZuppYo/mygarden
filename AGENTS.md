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

- Done: task 011 — ราคากลางภาคใต้ (ไม่ครบ 6 รายการ); แก้หญ้าบริษัท **100 ตร.ม. @ 157.5 = 15,750** (PDF ใส่ 10 ผิด); อัปเดต `summary.html` ข้อ 3–7, 10.2
- Active Task: none — **next:** sync 157.5/100 ตร.ม. → `benchmark-quotation.html`, `qt-v1/*`; archive task 011 optional
- Reload: `[resources/quotation/summary.html](resources/quotation/summary.html)`

## Task state pointers

- Active index: `[task/index.md](task/index.md)`
- Activity log: `[task/log.md](task/log.md)`
- Archive: `task/archive/2026-06-10/`
