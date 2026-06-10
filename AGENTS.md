# Landscaping AI Agent Workspace

## Repository mission

- Professional Landscaping and Gardening Assistant AI
- In-scope: Design gardens/landscapes based on home layout photos under `resources/`, programmatically edit/composite images, and draft landscaping tasks.
- Out-of-scope: Construction of gardens, physically buying plants, or managing non-gardening tasks.

## Non-negotiable rules

- Design gardens strictly matching the viewpoints and details in `resources/*.png`.
- Perform image edits using hybrid pipeline: `place --guide-dir` (position) then `generate_image` (blend into CGI style).
- Never use `place` without guide-dir as final output on 3D renders; never use text-only `generate_image` without placement guide.
- Use `iom-todo-task` and `iom-todo-task-archive` workflow for all planning and execution.
- Maintain the ultra-compact template of `AGENTS.md` (keep token usage low).
- Keep file paths relative to workspace root in tasks/logs, but resolve absolute paths when executing tools.

## Reload pack (minimal)

- `[AGENTS.md](AGENTS.md)`
- `[task/index.md](task/index.md)`
- `[task/log.md](task/log.md)`
- Active Task: none (await next task)

## Continuity — latest activity

### Snapshot (2026-06-10)

- Done: `000-project-bootstrap` — Bootstrap task system, setup persona rules, install Pillow, and verify image-processor skill.
- Done: `001-create-home-outline` — Create layout template displaying all house images.
- Done: `002-implement-3d-360-view` — Research and implement 3D pseudo-360 viewpoint switcher.
- Done: `003-add-front-right-lamsam-tree` — Add front-right Lamsam tree with Japanese grass on low/high front views.
- Done: `004-improve-multi-view-plant-placement` — Placement registry, `place` command, 5-view compositing, Placement Picker UI.
- Done: `005-hybrid-generative-blend` — 2-phase place guide + generate_image blend for all 5 front-yard views.
- Reload: `[task/index.md](task/index.md)`

## Task state pointers

- Active index: `[task/index.md](task/index.md)`
- Activity log: `[task/log.md](task/log.md)`
- Archive: `task/archive/`
