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

## IOM task skills

| Skill | Path |
|-------|------|
| iom-todo-task | `.agents/skills/iom-todo-task/SKILL.md` |
| iom-todo-task-archive | `.agents/skills/iom-todo-task-archive/SKILL.md` |
| iom-todo-handoff | `.agents/skills/iom-todo-handoff/SKILL.md` |
| iom-todo-task-knowledge | `.agents/skills/iom-todo-task-knowledge/SKILL.md` |

## Reload pack (minimal)

- `[AGENTS.md](AGENTS.md)`
- `[task/session.handoff-close.md](task/session.handoff-close.md)` — **Primary context**
- `[task/index.md](task/index.md)`
- `[task/log.md](task/log.md)` (head ~30 lines)
- `[task/011-southern-benchmark-pricing.md](task/011-southern-benchmark-pricing.md)`
- `[task/012-master-task-quotation-v2-analysis.md](task/012-master-task-quotation-v2-analysis.md)`
- `[task/012-01-sub-task-compare-v1-v2.md](task/012-01-sub-task-compare-v1-v2.md)`
- `[task/012-02-sub-task-v2-benchmark.md](task/012-02-sub-task-v2-benchmark.md)`
- `[resources/quotation/qt-v2/cut-packages.html](resources/quotation/qt-v2/cut-packages.html)`
- `[resources/quotation/qt-v2/contractor-message.md](resources/quotation/qt-v2/contractor-message.md)`

## Continuity — latest activity

### Snapshot (2026-07-19)

- Done: สีเทา plan **61.2** · ชุดตัดงาน A/B (`cut-packages.html`) · sync qt-v2/summary/qt-v1 · กลาง×แผน **102,906**
- Active Task: none (all `done`) — **next:** เลือกชุดตัดจาก cut-packages หรือต่อรองบริษัท (12cm / overlay / มัดจำ) หรือ archive 011+012
- Reload: `[task/session.handoff-close.md](task/session.handoff-close.md)` · `[resources/quotation/qt-v2/cut-packages.html](resources/quotation/qt-v2/cut-packages.html)`

## Task state pointers

- Active index: `[task/index.md](task/index.md)`
- Activity log: `[task/log.md](task/log.md)`
- Archive: `task/archive/2026-06-10/`
