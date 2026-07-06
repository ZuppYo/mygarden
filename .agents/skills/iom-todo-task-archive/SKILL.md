---
name: iom-todo-task-archive
version: "1.2.0"
description: >-
  Archives completed IOM task markdown files from task/ into task/archive/{created-date}/,
  using task/index.md and task/log.md. Moves tasks whose checklists are fully done and whose
  created date is at least one calendar day old. Updates index, log, and AGENTS.md continuity.
  Use when the user asks to archive tasks, run iom-todo-task-archive, or tidy the task folder.
disable-model-invocation: true
---

# IOM Todo Task Archive

Move **finished** numbered tasks from `task/` to `task/archive/{created}/`, then refresh index, log, and **`AGENTS.md`** continuity.

**Prerequisites:** [`task/index.md`](../../../task/index.md) and [`task/log.md`](../../../task/log.md) exist (created by **iom-todo-task**). Read [`../iom-todo-task/reference.md`](../iom-todo-task/reference.md) for frontmatter, slug, handoff, and log rules.

**Related skills:** [iom-todo-handoff](../iom-todo-handoff/SKILL.md) — session handoff without archiving · [iom-todo-task-knowledge](../iom-todo-task-knowledge/SKILL.md) — optional `refresh knowledge` after archive

---

## Quick start

1. Read `task/index.md` and only recent entries from `task/log.md` (**head ~30 lines**, ~10 event headings)
2. List candidates in `task/[0-9]{3,}-*.md` (exclude `index.md`, `log.md`, `prompt.md`)
3. For each candidate, apply **eligibility** (below)
4. Move eligible files → `task/archive/{created}/`
5. Update `task/index.md`, **prepend** `task/log.md`, patch **`AGENTS.md`** § Continuity

**STOP** after presenting the move plan; wait for user **go** before moving files (same guardrail as task execution).

---

## Eligibility

Archive a numbered task file when **all** are true:

| Rule | Check |
|------|--------|
| **Done** | Every checklist `- [ ]` is absent OR all items are `- [x]` (ignore `Task Requirement` prose) |
| **Age** | Frontmatter `created` ≤ **yesterday** (calendar date using current system date in `YYYY-MM-DD`; if date context is unavailable, ask user to confirm today's date before archiving) |
| **Location** | File is directly under `task/`, not already under `task/archive/` |

**Also move** (same archive folder = task file’s YAML `created` date):

- `task/{NNN}.handoff.md` if present for the same numeric prefix `{NNN}`
- Session handoffs (`task/{scope}.handoff.md`, `task/{scope}.handoff-close.md`) when user confirms or log references them — destination **`task/archive/{created}/`** where `{created}` is the handoff file’s YAML `created` (must match folder name)
- Other `task/{NNN}-*` siblings created as part of the same task when user confirms

**Archive path validation:** destination folder name MUST equal frontmatter `created`. Do not archive into a date folder that disagrees with YAML.

**Do not archive:** `task/index.md`, `task/log.md`, `task/prompt.md`, or any file with open `- [ ]` items (unless user explicitly cancels — see project cancel workflow outside this skill’s default eligibility).

---

## Archive path

Destination: `task/archive/{created}/` where `{created}` is the task file’s YAML `created` value (`YYYY-MM-DD`).

Example: `task/{NNN}-example-task.md` with `created: YYYY-MM-DD` → `task/archive/YYYY-MM-DD/{NNN}-example-task.md`

Create the date folder if missing.

---

## After move

### 1. `task/log.md`

**Prepend** at top (newest first — see [reference.md § Log ordering](../iom-todo-task/reference.md#tasklogmd--ordering-policy)):

```markdown
## [YYYY-MM-DD HH:MM] archived | {slug}
- moved: task/{file} → task/archive/{created}/
- related: {handoff or siblings if any}
```

Full event catalog: [reference.md § Log event catalog](../iom-todo-task/reference.md#log-event-catalog).

### 2. `task/index.md`

- Remove row from **Active**
- Add row under **Archived → {created}** (create `### YYYY-MM-DD` if needed)
- Set status `done` on archived rows
- When no active tasks remain, use [zero-active template](../iom-todo-task/reference.md#index-zero-active-state)

### 3. `AGENTS.md` — Continuity block (required in this standard)

Update **only** the `## Continuity — latest activity` section:

- Replace with **one** recent snapshot (date = today), never append old snapshots
- **Done:** up to 2-3 bullets max; each one line only
- **Next:** one highest-priority active task, or `none` when no active tasks
- **Reload:** `@task/session.handoff-close.md` when present (AGENTS-first; canonical `@` list stays in § Reload pack)
- Keep continuity concise; avoid embedding long implementation details (link to task/archive instead)

Use compact structure from: `.agents/skills/iom-todo-task-archive/references/AGENTS_ULTRA_COMPACT_TEMPLATE.md`

---

## Confirmation message

```
📦 Archive plan

Candidates (eligible):
1. {NNN}-example-task — created YYYY-MM-DD, all [x]
…

Skipped:
- {NNN}-other — open checklist items
- {NNN}-today — created today (age rule)

Destinations:
- task/archive/YYYY-MM-DD/{NNN}-example-task.md
…

Will update: task/index.md, task/log.md, AGENTS.md § Continuity

Reply "go" to archive, or "1,3" for subset, or "stop".

After successful archive: suggest invoking **iom-todo-task-knowledge** — `refresh knowledge` (incremental; reads only new/changed tasks per `task/knowledge/refresh-manifest.yaml`).
```

---

## Errors

- Missing frontmatter `created` → ask user to fix or set from file mtime; do not archive until valid
- `created` ≠ destination folder date → fix frontmatter or pick correct folder before move
- Archive folder collision (file already exists) → skip and report
- No eligible files → report and suggest running **iom-todo-task** to close checklists first

---

## Minimum test scenarios

- Create a numbered task with valid frontmatter, then verify it appears in `task/index.md` as `open`
- Execute task checklist until all items are `[x]`, then verify `task/log.md` head has `executed` entry
- Archive success: done task with `created <= yesterday` moves to `task/archive/{created}/`, and index/log/AGENTS continuity are updated
- Archive skip: task still has `- [ ]` or `created` is today; report as skipped without moving files
