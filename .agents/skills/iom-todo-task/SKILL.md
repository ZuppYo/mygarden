---
name: iom-todo-task
version: "1.2.0"
description: >-
  Creates or executes IOM task markdown under task/: YAML frontmatter, markdown links,
  task/index.md, and task/log.md. On create, allocates NNN-slug, updates index and log; or
  instantiate from task/template/{set}/{file}.md (Mode A-template), including master-task
  ({NNN}-master-task-{scope}) and sub-task ({NNN}-{NN}-sub-task-{scope}) under a parent master.
  On execute, reads Task Requirement then - [ ] items ([N]/[U]), writes - [x] and bumps updated/log/index.
  Use for iom-todo-task, new task checklists, task templates, master/sub-task hierarchy, or running task/*.md sequentially.
disable-model-invocation: false
---

# IOM Todo Task

**Create** planning/execution tasks under `task/`, or **execute** an existing task file. Templates: [reference.md](reference.md).

**Related skills:** [iom-todo-task-archive](../iom-todo-task-archive/SKILL.md) — move finished tasks to `task/archive/{created}/` · [iom-todo-handoff](../iom-todo-handoff/SKILL.md) — session handoff without archiving · [iom-todo-task-knowledge](../iom-todo-task-knowledge/SKILL.md) — refresh Requirement knowledge / gate draft before create (invoke separately)

## Standards (portable v1)

- Canonical task paths: `task/`, `task/index.md`, `task/log.md`, `task/archive/{YYYY-MM-DD}/`, `task/template/{set}/`
- Numbered task filename patterns:
  - **Standalone:** `{NNN}-{kebab-summary}.md` — `{NNN}` = global family id (zero-padded recommended)
  - **Master:** `{NNN}-master-task-{scope}.md` — see [reference.md § Master tasks](reference.md#master-tasks)
  - **Sub-task:** `{NNN}-{NN}-sub-task-{scope}.md` — reuses master `{NNN}`; `{NN}` = `01`–`99` under that master
- Required frontmatter fields: `title`, `type`, `detail`, `tags`, `created`, `updated`
- Link default: Markdown links (`[label](path-or-file.md)`); Obsidian wikilinks are optional only when user explicitly requests
- Log: **prepend** new events at top of `task/log.md` (newest first) — see [reference.md § Log ordering](reference.md#tasklogmd--ordering-policy) and [§ Log event catalog](reference.md#log-event-catalog)

**Agent context (before any work):**

1. Read [`task/index.md`](../../../task/index.md) for active vs archived tasks
2. Read recent entries from `task/log.md` only (**head ~30 lines**, ~10 event headings); avoid shell-specific commands when possible

---

## Mode 0 — Bootstrap project task system

Use when starting a new project or when `AGENTS.md` / `task/` baseline is missing.

### 0.1 Detect baseline

1. Check whether `AGENTS.md` exists at repo root
2. Check whether `task/index.md` and `task/log.md` exist
3. If missing, create them from templates (see [reference.md](reference.md))

### 0.2 Initialize AGENTS.md (compact)

1. Create or update `AGENTS.md` using compact template:
   - `.agents/skills/iom-todo-task-archive/references/AGENTS_ULTRA_COMPACT_TEMPLATE.md`
2. Keep only one latest continuity snapshot (do not append history)
3. Keep AGENTS focused on pointers; move deep history to `task/archive/` or dedicated docs

### 0.3 Create bootstrap task

1. Create first numbered task for project bootstrap (e.g. `000-project-bootstrap.md` or next available id)
2. Include checklist for:
   - mission + hard constraints finalized in `AGENTS.md`
   - reload pack paths validated
   - task workflow verified (`create`, `execute`, `archive`)
3. **Prepend** `created` event to `task/log.md` and add active row in `task/index.md`

### 0.4 Confirmation

Report created/updated files and ask user to continue execution:

`go` | `1,3` | `go + <detail>` | `stop`

---

## Mode A — Create task

Use when the user asks to **create**, **plan**, or **add** a new task under `task/`.

For repeatable work, use **Mode A-template** instead of writing from scratch.

### A1. Allocate slug

1. Scan `task/` and `task/archive/**/` for files matching `^[0-9]{3,}-.*\.md$` — **exclude** `task/template/**`
2. **Family id** `{NNN}` = leading numeric prefix only (before first `-`); next global `{NNN}` = max family + 1
3. Slug = `{NNN}-{kebab-summary}.md` (e.g. `{NNN}-example-task.md`)

Sub-tasks and masters use **Mode A-template** slug rules (A1c) — do not allocate a new global `{NNN}` for sub-tasks.

### A2. Write task file

1. Create `task/{slug}.md` with YAML frontmatter (`title`, `type`, `detail`, `tags`, `created`, `updated`) — see [reference.md](reference.md)
2. Validate minimum frontmatter:
   - `title` non-empty string
   - `type` one of `planning|improvement|execution|continuity|handoff`
   - `detail` non-empty one line
   - `tags` non-empty array
   - `created`, `updated` in `YYYY-MM-DD`
3. Body: `# title`, related markdown links, `## Task Requirement`, `## Checklist` with `- [ ]` items
4. Set `created` and `updated` to today (`YYYY-MM-DD`)

### A3. Ensure `task/index.md` and `task/log.md`

If missing, create from [reference.md](reference.md) skeletons.

### A4. Update index and log

1. **index.md** — add row under **Active** (`Status: open`)
2. **log.md** — **prepend** at top:

```markdown
## [YYYY-MM-DD HH:MM] created | {slug-without-.md}
- type: <type>
- note: <one line from user request>
```

When created via **Mode A-template**, add:

```markdown
- template: {set}/{file}
- note: instantiated from task/template/{set}/{file}.md
```

For **sub-task**, also add:

```markdown
- parent: {master-slug}
```

3. Present path and markdown link to the new task; **do not** execute checklist unless user says **go**

---

## Mode A-template — Create from task template

Use when the user asks to **create from template**, **instantiate template**, or names `task/template/{set}/{file}`.

See [reference.md § Task templates](reference.md#task-templates).

### A1b. Resolve template

1. Path = `task/template/{set}/{file}.md` (`.md` optional on `{file}` — normalize)
2. If missing → stop; list available files under `task/template/{set}/` if directory exists
3. Optional: read `task/template/{set}/README.md` for placeholder table

### A1c. Collect placeholders

1. Determine output slug by template set:
   - **`master-task`** — require `{scope}` (user or prompt). Slug = `{NNN}-master-task-{scope}.md`. Run **A1** for global `{NNN}`.
   - **`sub-task`** — require `parent={master-slug}` (basename without `.md`). Read parent file; derive `{NNN}` from parent basename; `{scope}` from parent or user override. Allocate `{NN}` = next two-digit sub-sequence under that `{NNN}` (scan `^{NNN}-[0-9]{2}-sub-task-`). Slug = `{NNN}-{NN}-sub-task-{scope}.md`. **Do not** run global A1 for a new `{NNN}`.
   - **Other sets** — run **A1**; user summary → `{NNN}-{kebab-summary}.md`; if omitted derive from template filename + `{scope}` if present; else `{NNN}-{file-kebab}.md`
2. Auto-fill: `{NNN}`, `{NN}` (sub-task only), `{CREATED}`, `{UPDATED}` = today, `{slug}` / `{SLUG}` = kebab summary without numeric prefix, `{PARENT}` = master slug (sub-task), `{MASTER_TITLE}` = parent frontmatter `title` (sub-task)
3. Merge user values from prompt or `go + KEY=value` pairs
4. For any remaining `{TOKEN}` in template → **ask** before write (do not guess secrets or production ids)

### A1d. Post-create (sub-task only)

After writing a sub-task file:

1. Add or update row in parent master `## Children` table (`NN`, slug, type, status `open`, template note)
2. Prepend parent `## Activity` optional `created` note when scope warrants
3. Log `created` includes `parent: {master-slug}`

### A2t. Substitute and write

1. Global replace each `{TOKEN}` in template content
2. Scan output for unreplaced `\{[A-Za-z0-9_]+\}` → **block** write; report missing tokens
3. Validate frontmatter per Mode A2
4. If no template-source link in body, add after title:

   `> Template: [task/template/{set}/{file}.md](../../../task/template/{set}/{file}.md)`

5. Write `task/{slug}.md` (full basename from A1c — includes `master-task` / `sub-task` segments)

### A3t / A4t

Same as Mode A3 and A4 (index + log with `template:` field).

**One file per run** — multi-file template sets (e.g. phase 1 → 2 → 3) require separate instantiate calls.

---

## Mode B — Execute task

Use when the user provides a task file path or asks to **run** / **execute** a checklist.

### B0. Context

1. Read task frontmatter; if `updated` stale after edits, bump at end of session
2. Optional: skim `task/index.md` row for this slug

### B1. Read Task File

1. Read the specified markdown file
2. **Task Requirement** — Find heading **Task Requirement** (or Thai equivalents / `Requirements` when clearly document-level). Read from heading through next same-or-higher-level heading **before** any `- [ ]` work.
   - Missing section → note `No "Task Requirement" section found — proceeding from checklist only`
   - Empty section → ask user to fill or confirm
3. Parse unchecked `- [ ]`; skip `- [x]`
4. Confirm with user (**STOP** until **go**, **1,3**, **go + …**, **stop**, or clarification):

```
📋 Task File: <filename>
Found <N> pending tasks:
…
---
🔲 Your turn: go | 1,3 | go + <detail> | stop | <clarification>
```

### B2. Execute Tasks

For each pending item:

0. **Task Requirement wins** over conflicting checkbox text
1. **`[N]`** — new work; **`[U]`** — read prior result/output first, patch only; no flag = `[N]`
2. Follow links/paths in the task line for context
3. Mark `- [x]` with `  - ✅ <result>` (or `  - ⚠️ <reason>` if failed; leave unchecked on hard failure)

After each completed item (or end of batch): bump frontmatter `updated`; **prepend** **log.md** `executed | {slug}` with completed ids; set index **Status** to `done` only when **all** checklist items are `[x]`.

**When to prepend other events:** see [reference.md § Log event catalog](reference.md#log-event-catalog) — e.g. `updated` on scope change, `handoff` on session close (optional per project).

### B3. Report

```
📋 Task Execution Complete
✅ Completed: <N>
…
Updated: <filename>, task/log.md, task/index.md (if status changed)
```

---

## Task Requirement section (document-level)

```markdown
## Task Requirement

- Goal: …
- In scope / out of scope: …
- References: [other-task](../task/{NNN}-other-task.md), paths …
```

Mandatory read when present — see Mode B1.

---

## Checklist format

| Flag | Meaning |
|------|---------|
| `[N]` | New — create/overwrite as needed |
| `[U]` | Update — preserve existing output; patch only |
| (none) | Treat as `[N]` |

```markdown
- [ ] T001 [N] Create [task/index.md](../../../task/index.md)
- [ ] T002 [U] Update [{NNN}-prior-task](../../../task/{NNN}-prior-task.md) per review
```

Completed:

```markdown
- [x] T001 [N] …
  - ✅ <result>
```

---

## Behavioral rules

- **Index + log:** On create and on material execute progress, update `task/index.md` and **prepend** `task/log.md`
- **Frontmatter:** Never remove YAML; keep `title`/`detail` in sync with index row when title changes
- **Links:** Use markdown links by default; allow wikilinks only when user explicitly requests
- **Language:** Match task file (Thai/English)
- **Order:** Execute checklist top to bottom
- **Safety:** No destructive ops without explicit confirmation; `go +` user text overrides task text where applicable
- **Scope:** Do not edit files outside checklist intent except index/log/frontmatter updates above
- **Archive:** Do not move files to `task/archive/` — use **iom-todo-task-archive**
- **Portability:** Skill examples use placeholders only — see [reference.md § Portability](reference.md#portability)

---

## Error handling

| Case | Action |
|------|--------|
| Task file missing | Stop; report |
| Template file missing | Stop; list `task/template/{set}/` if present |
| Unreplaced `{TOKEN}` after substitute | Block write; list missing tokens |
| Referenced file missing | Note in result; continue if possible |
| `[U]` with no prior result | Treat as `[N]`; note in result |

---

## Examples

**Create:** User: "create task to improve skill" → `{NNN}-example-task.md`, index row, log `created`, show task path/link.

**Create from template (master):** User: `create from template master-task/skeleton scope=ai-research` → `039-master-task-ai-research.md`, `role: master`, log `created` + `template: master-task/skeleton`.

**Create from template (sub-task):** User: `create from template sub-task/skeleton parent=039-master-task-ai-research` → `039-01-sub-task-ai-research.md`, update master Children table, log `created` + `parent:`.

**Create from template (generic):** User: `create from template example-task/skeleton scope=demo-run` → read `task/template/example-task/skeleton.md`, substitute placeholders, `{NNN}-demo-run-example.md`, log `created` + `template: example-task/skeleton`.

**Execute:** User: `@task/{NNN}-example-task.md go` → Task Requirement → checkboxes → log `executed`.

**Context reload:** `@AGENTS.md` first (§ Reload playbook in iom-todo-handoff reference) → handoff-close if Continuity points there → primary `@task/{slug}.md`.
