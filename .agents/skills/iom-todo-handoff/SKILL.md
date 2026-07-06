---
name: iom-todo-handoff
version: "1.2.0"
description: >-
  Produces session handoff for IOM task workflows: AGENTS.md-first entry,
  summarizes Active tasks from task/index.md, writes handoff markdown (no duplicate
  reload pack), patches AGENTS continuity and canonical reload pack, prepends task/log.md.
  Separate from archive — no file moves. Use for iom-todo-handoff, session close, or next-agent reload.
disable-model-invocation: true
---

# IOM Todo Handoff

Prepare **next-session continuity** when ending a work session. **Entry point:** [`AGENTS.md`](../../../AGENTS.md) — then task control plane per [reference.md § Reload playbook](reference.md#reload-playbook).

**Related skills:** [iom-todo-task](../iom-todo-task/SKILL.md) · [iom-todo-task-archive](../iom-todo-task-archive/SKILL.md) (archive is separate; do not move task files here) · [iom-todo-task-knowledge](../iom-todo-task-knowledge/SKILL.md) (Requirement knowledge — separate; not on session reload)

Templates: [reference.md](reference.md)

---

## Quick start

1. Read **`AGENTS.md`** (mission, IOM task skills, reload pack, continuity)
2. Read [`task/index.md`](../../../task/index.md) — collect **every Active row** (non-archived; any `Status`)
3. Read [`task/log.md`](../../../task/log.md) — **head ~30 lines** only
4. For each Active numbered task, read `task/{slug}.md` (Task Requirement + checklist + `✅`/`⚠️` results)
5. Determine **primary task:** lowest `NNN` with unchecked `- [ ]`; if none, lowest `NNN` in Active
6. Build handoff plan (below) → **STOP** until user **go**
7. On **go**: write handoff file, patch AGENTS, prepend log, update index pointer

---

## Task scope

| Include | Exclude |
|---------|---------|
| Every **Active** row in `task/index.md` (not yet archived) | Archived tasks under `task/archive/` |
| Checklist state (`- [ ]` / `- [x]`) and result lines | Full task body paste into AGENTS |
| Recent log context (head ~30 lines) | Moving or archiving task files |
| Duplicate `@` reload lists in handoff file | Whole `@.agents/skills/{name}/` folders in reload pack |

Summarize each active task in **1–3 lines**. See [reference.md § Token budget](reference.md#token-budget).

---

## Handoff filename

| Case | File |
|------|------|
| Default (session end) | `task/session.handoff-close.md` |
| User specifies `{scope}` | `task/{scope}.handoff-close.md` |
| Single active task + user requests task-scoped | `task/{NNN}.handoff.md` |

Use YAML `created` = today (`YYYY-MM-DD`) on new handoff files. On re-handoff same session, **overwrite** the same file and bump `updated`.

---

## Handoff plan (STOP)

```
📋 Handoff plan

Active tasks (<N>):
1. {slug} — {title} — {open|done} — pending: T00x, …
Primary: {primary-slug}

Handoff file: task/session.handoff-close.md
Will update: AGENTS.md (§ IOM task skills, § Reload pack, § Continuity), task/log.md, task/index.md
Handoff file: Reload chain only (no duplicate @ list)

Reply "go" to write handoff, or "go + {scope}" for custom scope, or "stop".
```

---

## On go — outputs

### 1. Handoff markdown

Create or overwrite per [reference.md § Handoff body](reference.md#handoff-body-skeleton). Required: status line, **Reload chain** (link to AGENTS — not a duplicate `@` block), one-line summary, per-active-task bullets, next-session steps.

### 2. `AGENTS.md`

Patch **only**:

- **`## IOM task skills`** — ensure discovery table (skill paths to `SKILL.md` only); see [reference.md § AGENTS reload pack template](reference.md#agents-reload-pack-template)
- **`## Reload pack (minimal)`** — canonical list: `@task/index.md`, `@task/log.md` (head ~30), **one `@task/{slug}.md` per Active row**; mark **Primary:** line for primary task; **do not** list skill folders
- **`## Continuity — latest activity`** — **replace** with one snapshot (date = today):
  - **Done:** up to 2–3 bullets
  - **Next:** primary task slug + one line, or `none`
  - **Reload:** `@task/session.handoff-close.md` (or handoff basename written)

Never append old continuity snapshots. Never duplicate reload pack inside handoff file.

### 3. `task/log.md`

**Prepend** at top:

```markdown
## [YYYY-MM-DD HH:MM] handoff | session.handoff-close
- note: {one line — active task count + primary next step}
- related: {comma-separated active slugs}
```

### 4. `task/index.md`

Under **Active**, add or update handoff line:

```markdown
Handoff: [session.handoff-close](./session.handoff-close.md)
```

---

## Behavioral rules

- **AGENTS first:** Always read `AGENTS.md` before `task/`; next agent follows [Reload playbook](reference.md#reload-playbook)
- **No duplicate reload pack** in handoff markdown
- **No archive:** Do not move files to `task/archive/` — use **iom-todo-task-archive**
- **Skills:** Discovery via AGENTS § IOM task skills; load full `SKILL.md` on invoke only
- **Portability:** Placeholders (`{NNN}`, `{slug}`, `{scope}`) only
- **Language:** Match project/task file language
- **Safety:** No writes until user **go**
- **Links:** Markdown links by default

---

## Errors

| Case | Action |
|------|--------|
| No Active tasks in index | Offer session summary handoff; confirm with user |
| Missing `task/index.md` / `task/log.md` | Stop; suggest **iom-todo-task** bootstrap |
| Missing `AGENTS.md` | Stop; suggest bootstrap, install script, or minimal AGENTS |

---

## Examples

**Session close:** User: "handoff" → AGENTS + Active tasks → plan → **go** → `session.handoff-close.md` (Reload chain only) + AGENTS patched.

**Custom scope:** User: `go + release-prep` → `task/release-prep.handoff-close.md`.
