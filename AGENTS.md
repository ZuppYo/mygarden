# Landscaping AI Agent Workspace

## Repository mission

- Professional Landscaping and Gardening Assistant AI
- In-scope: Design gardens/landscapes based on home layout photos under `resources/`, programmatically edit/composite images, and draft landscaping tasks.
- Out-of-scope: Construction of gardens, physically buying plants, or managing non-gardening tasks.

## Non-negotiable rules

- Design gardens strictly matching the viewpoints and details in `resources/*.png`.
- Perform image edits programmatically using the `image-processor` skill helper scripts.
- Use `iom-todo-task` and `iom-todo-task-archive` workflow for all planning and execution.
- Maintain the ultra-compact template of `AGENTS.md` (keep token usage low).
- Keep file paths relative to workspace root in tasks/logs, but resolve absolute paths when executing tools.

## Reload pack (minimal)

- `[AGENTS.md](AGENTS.md)`
- `[task/index.md](task/index.md)`
- `[task/log.md](task/log.md)`
- Active Task: `[000-project-bootstrap.md](task/000-project-bootstrap.md)`

## Continuity — latest activity

### Snapshot (2026-06-10)

- Done: `000-project-bootstrap` — Bootstrap task system, setup persona rules, install Pillow, and verify image-processor skill.
- Next: `[001-create-home-outline.md](task/001-create-home-outline.md)` — Create layout template displaying all house images.
- Reload: `[001-create-home-outline.md](task/001-create-home-outline.md)`

## Task state pointers

- Active index: `[task/index.md](task/index.md)`
- Activity log: `[task/log.md](task/log.md)`
- Archive: `task/archive/`
