# iom-todo-task — templates and conventions

## Portability

These skills are **agent-agnostic** and **workspace-agnostic**:

- Use placeholder examples only (`{NNN}`, `{slug}`, `{scope}`, `{YYYY-MM-DD}`) — never embed real completed-task slugs from a specific repo in skill text.
- Core workflow (`create`, `execute`, `archive`) applies to any project type.
- **Optional** log events (`handoff`, `cancelled`, `corrected`, …) extend the catalog when a project needs them — not required in every workspace.
- Cross-link between **iom-todo-task**, **iom-todo-task-archive**, **iom-todo-handoff**, and **iom-todo-task-knowledge**; do not couple to domain templates or other skills in skill core text.

---

## Task templates

Reusable work patterns live under **`task/template/{set}/`** — **not** numbered tasks. Instantiate via **Mode A-template** in [SKILL.md](SKILL.md) to produce `task/{NNN}-{kebab-summary}.md`.

### Layout

```text
task/template/
└── {set}/
    ├── README.md          # optional — placeholder table, how to instantiate
    ├── {file}.md          # template body (may use {TOKEN} placeholders)
    └── …                  # supporting docs (project-specific)
```

| Rule | Detail |
|------|--------|
| **Path** | `task/template/{set}/{file}.md` only — no flat `task/template/{file}.md` |
| **Not in index** | Template files never get Active rows in `task/index.md` |
| **Not numbered** | Exclude `task/template/**` from NNN allocation scan |
| **Not archived** | Never move template files to `task/archive/` |
| **Reload** | Do not list `task/template/**` in AGENTS reload pack — load on demand when creating |
| **One file** | Instantiate **one** template file per Mode A-template run (batch = out of scope) |
| **Domain** | Domain-specific template sets live in consumer repos; skill core stays generic |

### Placeholder syntax

Tokens use curly braces: `{TOKEN}` (uppercase recommended in templates).

| Token | On instantiate |
|-------|----------------|
| `{NNN}` | Allocated global family id (zero-padded, same width as project convention) |
| `{NN}` | Sub-sequence under a master (`01`–`99`; sub-task template only) |
| `{PARENT}` | Master slug without `.md` (sub-task template) |
| `{MASTER_TITLE}` | Parent master `title` from frontmatter (sub-task template) |
| `{CREATED}`, `{UPDATED}` | Today `YYYY-MM-DD` |
| `{slug}`, `{SLUG}` | Kebab summary from user or derived filename (see SKILL Mode A-template) |
| Other `{TOKEN}` | User-provided via prompt or `go + KEY=value`; **ask** if missing |
| Unreplaced `{…}` | **Block** write; list missing tokens |

Optional: read `task/template/{set}/README.md` for a placeholder table before asking the user.

### Instantiate algorithm

1. Resolve `task/template/{set}/{file}.md` — stop if missing
2. Allocate slug:
   - **`master-task`** → global `{NNN}` + `{scope}` → `{NNN}-master-task-{scope}.md`
   - **`sub-task`** → `{NNN}` from `parent=` master; next `{NN}` under that family → `{NNN}-{NN}-sub-task-{scope}.md`
   - **default** → global `{NNN}` + `{kebab-summary}` (Numbering rules — templates excluded)
3. Collect placeholder values: auto-fill `{NNN}`, `{NN}` (sub-task), `{CREATED}`, `{UPDATED}`, `{slug}`/`{SLUG}`, `{PARENT}`; merge user map
4. Substitute all `{TOKEN}` in template body (global replace per token)
5. Validate frontmatter (real dates, no remaining `{…}` in YAML values used for index)
6. Ensure body links back to template source (blockquote or Related) if not already present
7. Write `task/{slug}.md`; update index + log per Mode A4; sub-task → update parent master `## Children`

### Template file skeleton

```markdown
---
title: "{scope} — example work unit"
type: planning
detail: "Instantiated from template for {scope}"
tags: [template, example]
created: {CREATED}
updated: {UPDATED}
---

# {scope} — example work unit

> Template: [example-task](./README.md) · [skeleton](./skeleton.md)

## Task Requirement

- Goal: …
- In scope: …
- Out of scope: …

## Checklist

- [ ] T001 [N] …
```

### Generic example (this repo)

`task/template/example-task/` — README + `skeleton.md` for smoke and documentation only.

`task/template/master-task/` — **standard** initiative control plane; instantiate `{NNN}-master-task-{scope}.md`.

`task/template/sub-task/` — child under a master; instantiate `{NNN}-{NN}-sub-task-{scope}.md`.

---

## Master tasks

Initiative **control plane** — one master per topic; **sub-task** children for executable work. Replaces ad-hoc `task/prompts.md` inboxes.

### Naming patterns (required)

| Role | Filename pattern | Example |
|------|------------------|---------|
| **Master** | `{NNN}-master-task-{scope}.md` | `037-master-task-ai-research.md` |
| **Sub-task** | `{NNN}-{NN}-sub-task-{scope}.md` | `037-01-sub-task-ai-research.md` |
| **Standalone** | `{NNN}-{kebab-summary}.md` | `036-iom-todo-task-template-instantiate.md` |

- `{NNN}` — global family id (zero-padded, 3+ digits recommended)
- `{NN}` — sub-sequence under that master (`01`–`99`, zero-padded)
- `{scope}` — shared kebab label within a master family (same across master + sub-tasks unless intentionally forked)

Regex:

- Master: `^[0-9]{3,}-master-task-[a-z0-9-]+\.md$`
- Sub-task: `^([0-9]{3,})-([0-9]{2})-sub-task-[a-z0-9-]+\.md$` — group 1 = `{NNN}`, group 2 = `{NN}`

Legacy slugs (e.g. `{NNN}-master-{scope}` without `-task-`) may exist in archive; **new** masters use `-master-task-`.

### Hierarchy

```text
Master  task/{NNN}-master-task-{scope}.md       role: master
  └── Sub-task  task/{NNN}-{NN}-sub-task-{scope}.md   role: child
        └── Checklist - [ ] items                     (no deeper task files)
```

| Level | Template source |
|-------|-----------------|
| Master | `task/template/master-task/skeleton.md` |
| Sub-task | `task/template/sub-task/skeleton.md` |

### Frontmatter (master / sub-task)

```yaml
role: master | child
parent: null | {master-slug-without-.md}
master_nnn: "{NNN}"      # optional but recommended
sub_nn: "{NN}"           # sub-task only
```

Core fields (`title`, `type`, `detail`, `tags`, `created`, `updated`) remain required.

### Master body sections

| Section | Purpose | Update style |
|---------|---------|--------------|
| `## Task Requirement` | Stable goal, scope, master acceptance | Patch when scope changes |
| `## Children` | Table: **NN**, slug, status, template | Update when spawning/closing sub-tasks |
| `## Activity` | Decisions, blockers, scope notes | **Prepend** newest first (Jira comment style) |

### Children table columns

| NN | Slug | Type | Status | Template / note |
|----|------|------|--------|-----------------|
| 01 | `{NNN}-01-sub-task-{scope}` | improvement | open | `sub-task/skeleton` |

### Sub-task numbering

Given parent master `{NNN}-master-task-{scope}.md`:

1. Scan `task/` and `task/archive/**/` for `^{NNN}-[0-9]{2}-sub-task-.*\.md$`
2. Extract `{NN}` (two digits after first hyphen group); next = max + 1, zero-pad to 2 digits
3. If none exist → `01`
4. Slug = `{NNN}-{NN}-sub-task-{scope}.md` — **do not** allocate a new global `{NNN}` for sub-tasks

### Global numbering (masters and standalone)

1. Scan `task/` and `task/archive/**/` for `^[0-9]{3,}-.*\.md$` (exclude `task/template/**`)
2. Extract **family** `{NNN}` = leading numeric prefix only (first `3+` digit group)
   - `037-master-task-x` → family `037`
   - `037-01-sub-task-x` → family `037` (same family, not a new global id)
3. Next global `{NNN}` = max family + 1

### Spawn sub-task

1. Confirm parent master exists
2. Mode A-template `sub-task/skeleton` with `parent={master-slug}` (and `scope=` if overriding)
3. Allocate `{NN}` per rules above; write `task/{NNN}-{NN}-sub-task-{scope}.md`
4. Set `role: child`, `parent`, `master_nnn`, `sub_nn` in frontmatter; set `detail` to include parent title (e.g. `Sub-task 01 · master: {title}`)
5. Body blockquote **Parent master:** with `[{title}](./{parent}.md)` — human title, not slug-only
6. Add row to master `## Children`; prepend log `created` with optional `parent:` field

**Do not** duplicate master Requirement in `task/prompts.md` — stub/redirect only when master model is adopted.

### Activity entry format

```markdown
### [YYYY-MM-DD HH:MM] {kind} | {author}
- note: …
- change: … (optional)
- affects: {slug}, … (optional)
```

Kinds: `decision`, `blocker`, `scope`, `migrated`, `created` (examples — project may extend).

### Spawn child (deprecated label)

Use **Spawn sub-task** above. “Child” in prose means sub-task file under a master.

---

## Task file frontmatter

Every **numbered** task file (`task/{NNN}-*.md`, not `prompt.md` or `index.md`) MUST start with:

```yaml
---
title: "<short human title>"
type: <planning|improvement|execution|continuity|handoff>
detail: "<one line for index tables — no markdown>"
tags: [<tag1>, <tag2>]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

| Field | Use |
|-------|-----|
| `title` | Display name |
| `type` | Index grouping (`improvement`, `planning`, …) |
| `detail` | Copied into `task/index.md` active table |
| `tags` | Filter keys for index/search |
| `created` | Archive folder date (`task/archive/YYYY-MM-DD/`) — **must match** destination folder when archived |
| `updated` | Bump on every create, execute, or material edit |

**Slug** = basename without `.md` (e.g. `{NNN}-example-task`). Use markdown links by default: `[{NNN}-example-task](../../../task/{NNN}-example-task.md)`.

**Archive path rule:** a file with `created: YYYY-MM-DD` MUST land in `task/archive/YYYY-MM-DD/`. If `created` and folder disagree, fix frontmatter or move file before archiving.

---

## Task Requirement quality

Before **Mode A** create (especially `type: improvement`), invoke [iom-todo-task-knowledge](../iom-todo-task-knowledge/SKILL.md) to refresh or **gate** the draft Requirement against [`task/knowledge/requirements-playbook.md`](../../../task/knowledge/requirements-playbook.md). Separate skill — not auto-run on create.

---

## Task body skeleton

```markdown
---
title: "…"
type: planning
detail: "…"
tags: [skill]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <same as title>

Related: [{NNN}-prior-task](../../../task/{NNN}-prior-task.md) · [requirements knowledge](../../../task/knowledge/requirements-playbook.md) · [iom-todo-task](SKILL.md)

## Task Requirement

- Goal: …
- In scope / out of scope: …
- References: …

## Checklist

- [ ] T001 [N] …
```

---

## Bootstrap task skeleton (project day 0)

```markdown
---
title: "Project bootstrap"
type: planning
detail: "Initialize AGENTS/task baseline for new project"
tags: [bootstrap, task-management]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Project bootstrap

Related: [AGENTS](../../../AGENTS.md)

## Task Requirement

- Goal: Initialize AGENTS + task workflow for a new repo
- In scope: AGENTS compact baseline, task index/log, first execution flow
- Out of scope: implementation features

## Checklist

- [ ] T001 [N] Create/update `AGENTS.md` from ultra-compact template
- [ ] T002 [N] Ensure `task/index.md` and `task/log.md` exist
- [ ] T003 [N] Validate reload pack pointers and active task flow
```

---

## `task/index.md` skeleton

```markdown
# Task index

Read for **active** vs **archived** tasks. Use recent entries from `task/log.md` only (head ~30 lines).

## Active (`task/`)

| Slug | Title | Type | Tags | Updated | Status |
|------|-------|------|------|---------|--------|
| [{NNN}-example-task](./{NNN}-example-task.md) | … | improvement | skill | YYYY-MM-DD | open |

## Archived (`task/archive/`)

### YYYY-MM-DD

| Slug | Title | Type | Tags | Created |
|------|-------|------|------|---------|
| [{NNN}-example-task](./archive/YYYY-MM-DD/{NNN}-example-task.md) | … | improvement | example | YYYY-MM-DD |
```

**Status:** `open` = any `- [ ]` in checklist; `done` = all checklist items `- [x]` (or no checklist); `cancelled` = user cancelled (optional).

### Index zero-active state

When no numbered tasks remain under `task/`, replace the active table with short prose pointers:

```markdown
## Active (`task/`)

*No active tasks.*

Handoff: [{scope}.handoff-close](./archive/YYYY-MM-DD/{scope}.handoff-close.md)

Reload: `@task/{NNN}-next-task.md` · `@task/archive/YYYY-MM-DD/{scope}.handoff-close.md`
```

Use generic `{scope}` / `{NNN}` in skill text; each project fills real paths in its own `task/index.md`.

---

## Handoff files

Handoff markdown captures session continuity. Two naming patterns:

| Pattern | Filename | Scope |
|---------|----------|-------|
| Task-scoped | `{NNN}.handoff.md` | Same numeric prefix as a numbered task |
| Session-scoped | `{scope}.handoff.md` | Planning / mid-session (any `{scope}` label) |
| Session close | `{scope}.handoff-close.md` | End-of-session summary when tasks archived or paused |

**Frontmatter (session handoffs):**

```yaml
---
title: "Handoff — {one-line summary}"
type: handoff
detail: "{one line for index if listed}"
tags: [handoff]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Body should include:** one-line status, **Reload chain** (link to `AGENTS.md` § Reload pack — no duplicate `@` list), optional next-step bullets. Playbook: [iom-todo-handoff reference § Reload playbook](../iom-todo-handoff/reference.md#reload-playbook).

**Archive:** move handoffs to `task/archive/{created}/` where `{created}` is YAML `created`. Session handoffs without `NNN` prefix follow the same rule.

**Also move (numbered task archive):** `task/{NNN}.handoff.md` when present for the same prefix.

---

## `task/log.md` — ordering policy

| Rule | Detail |
|------|--------|
| **Write** | **Prepend** each new event block at the **top** of `task/log.md` (newest first) |
| **Read** | Inspect only the **head ~30 lines** (~10 event headings); do not load the full log unless debugging history |
| **Reorder** | If blocks are out of order, sort entire file by timestamp descending; do not edit fields inside blocks |
| **Same timestamp** | Keep original relative order among blocks sharing the same minute |

---

## Log event catalog

Heading format: `## [{timestamp}] {event} | {subject}`

`{timestamp}` = `YYYY-MM-DD HH:MM` · `{subject}` = slug without `.md`, handoff basename, or short label.

### Core events (always available)

| Event | When to prepend | `{subject}` | Suggested fields |
|-------|-----------------|-------------|------------------|
| `created` | Mode A, Mode A-template — new numbered task | `{slug}` | `type`, `note`; optional `template:`, `parent:` |
| `executed` | Mode B — material checklist progress | `{slug}` | `completed`, `note` |
| `archived` | Archive skill — file moved | `{slug}` | `moved`, `related` |

**Templates:**

```markdown
## [{timestamp}] created | {slug}
- type: {type}
- note: {one line}

## [{timestamp}] created | {slug}
- type: {type}
- template: {set}/{file}
- parent: {master-slug}
- note: instantiated sub-task under master

## [{timestamp}] executed | {slug}
- completed: T001, T002
- note: {one line}

## [{timestamp}] archived | {slug}
- moved: task/{file} → task/archive/{created}/
- related: {handoff or siblings if any}
```

### Optional extension events

Use when the project needs richer audit trails. Not required in minimal setups.

| Event | When | `{subject}` | Suggested fields |
|-------|------|-------------|------------------|
| `updated` | Task file scope/requirement changed without execute | `{slug}` | `note` |
| `handoff` | Session handoff written or referenced | `{scope}.handoff` or `{scope}.handoff-close` | `note` |
| `cancelled` | User cancels task(s) | `{slug}` or batch label | `note` |
| `corrected` | Post-execute fix to task or artifacts | `{slug}` | `note`, `updated` (paths) |
| `confirmed` | User locked scope before `go` | `{slug}` | `note` |
| `renamed` | Slug renumbered | `{old-slug}` → `{new-slug}` | `note` |

Projects may add domain-specific events (e.g. dispatch, resume) in their own docs — keep **iom-todo-task** core limited to the table above.

---

## Numbering

### Global family `{NNN}`

- Scan `task/[0-9]{3,}-*.md` and `task/archive/**/[0-9]{3,}-*.md`
- **Family id** = leading numeric prefix only (before first `-`)
  - `037-master-task-ai-research` → `037`
  - `037-01-sub-task-ai-research` → `037` (same family)
  - `038-standalone-task` → `038`
- Next global `{NNN}` = max family + 1 (zero-padded recommended)

### Sub-sequence `{NN}` (under one master)

- Pattern: `{NNN}-{NN}-sub-task-{scope}.md`
- Next `{NN}` = max existing two-digit segment for that `{NNN}` + 1, zero-padded (`01`–`99`)
- Sub-tasks **reuse** master `{NNN}` — never bump global id when spawning sub-tasks

### Exclusions

- Skip: `prompt.md`, `index.md`, `log.md`, **`task/template/**`**, unnumbered `*.handoff.md` unless tied to `{NNN}-` prefix.

---

## Frontmatter validation (minimum)

- `title`: non-empty string
- `type`: `planning|improvement|execution|continuity|handoff`
- `detail`: one-line non-empty string
- `tags`: non-empty array
- `created`, `updated`: `YYYY-MM-DD`

---

## Special files (never archive)

| File | Role |
|------|------|
| `task/index.md` | Agent index |
| `task/log.md` | Activity log |
| `task/prompt.md` | Scratch / prompts — not a numbered task |
| `task/prompts.md` | **Deprecated inbox** — redirect to active master; scratch only |
| `task/template/**` | Reusable task templates — instantiate via Mode A-template; never archive |

`{NNN}-session-continuity-compact.md` — archive like other numbered tasks when done + age rule passes.
