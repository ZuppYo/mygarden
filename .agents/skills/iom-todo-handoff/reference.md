# iom-todo-handoff — templates and conventions

## Portability

- Placeholder examples only (`{NNN}`, `{slug}`, `{scope}`, `{YYYY-MM-DD}`).
- Agent-agnostic; no consumer-repo paths in skill core text.
- Cross-link **iom-todo-task**, **iom-todo-task-archive**, **iom-todo-handoff**, **iom-todo-task-knowledge** only.

---

## Reload playbook

**Canonical reload list:** `AGENTS.md` § Reload pack only. Handoff files **do not** duplicate `@` path lists.

Session start — follow in order; load on demand, not in parallel from multiple artifacts.

| Step | Load | When |
|------|------|------|
| 1 | `@AGENTS.md` | **Always first** — mission, IOM task skills, reload pack, continuity |
| 2 | `@task/session.handoff-close.md` (or latest handoff-close) | When Continuity § **Reload** points here |
| 3 | `@task/{primary-slug}.md` | Primary active task (see rule below) |
| 4 | `@task/{slug}.md` | Other **Active** rows when working that task |
| 5 | `@task/index.md` | When overview of active vs archived needed |
| 6 | `@task/log.md` | **Head ~30 lines** only — audit or debug |
| 7 | `@.agents/skills/{name}/SKILL.md` | **Invoke only** — user calls skill or playbook step requires execution |
| 8 | Skill `reference.md` | When invoked `SKILL.md` links to it |

**Active tasks (reload pack):** Every numbered task row under **Active** in `task/index.md` (not yet archived) — regardless of `Status` (`open`, `done`, etc.). One `@task/{slug}.md` pointer per row in AGENTS § Reload pack.

**Primary task** (step 3 — start here after handoff summary):

1. Lowest `NNN` among Active tasks with **unchecked** checklist items (`- [ ]`)
2. If none pending → lowest `NNN` among all Active rows

**Do not** list `@.agents/skills/{name}/` (whole folder) in reload pack — see [Skill load policy](#skill-load-policy).

---

## Skill load policy

Progressive disclosure (agent-agnostic):

| Phase | Content |
|-------|---------|
| **Discovery** | YAML frontmatter (`name`, `description`) from each installed `SKILL.md`; paths listed in AGENTS § IOM task skills |
| **Invoke** | Full `@.agents/skills/{name}/SKILL.md` when user runs that skill |
| **Deep** | `reference.md` or `references/` only when invoked skill links to them |

Skills with `disable-model-invocation: true` (handoff, archive, knowledge) load full body **only** on explicit user invoke.

---

## Handoff file frontmatter

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

---

## Handoff body skeleton

No duplicate reload pack — point to AGENTS § Reload pack.

```markdown
---
title: "Handoff — {one-line summary}"
type: handoff
detail: "{one line}"
tags: [handoff]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Handoff — {short title}

**Status:** {N} active task(s) · {optional notes}

---

## Reload chain

Start at [`AGENTS.md`](../AGENTS.md) § Reload pack (canonical `@` list). This file is step 2 when Continuity § Reload points here. Playbook: [iom-todo-handoff reference](../.agents/skills/iom-todo-handoff/reference.md#reload-playbook).

---

## One-line summary

{Single sentence for next agent.}

---

## Active tasks

### {slug} — {title}

- **Status:** {open|done} · **Updated:** YYYY-MM-DD
- **Goal:** {from Task Requirement — one line}
- **Done:** {completed checklist ids or "none"}
- **Pending:** {open checklist ids or "none"}
- **Next:** {one action}

---

## Next session

1. `@AGENTS.md` → follow § Reload pack + Continuity § Reload
2. {concrete step — often primary `@task/{slug}.md` or invoke skill}
```

---

## AGENTS continuity patch template

Replace entire `## Continuity — latest activity` block:

```markdown
## Continuity — latest activity

### Snapshot (YYYY-MM-DD)

- Done: `{slug}` — {one-line outcome}
- Next: `{primary-slug}` — {one-line next action}
- Reload: `@task/session.handoff-close.md`
```

Rules:

- **One snapshot only** — replace, never append
- **Done:** max 2–3 bullets
- **Next:** primary task slug (lowest `NNN` with pending, else lowest Active `NNN`)
- **Reload:** handoff-close file (step 2 in playbook); not a duplicate path list

---

## AGENTS reload pack template

**Single canonical list** — handoff files must not copy this block.

```markdown
## Reload pack (minimal)

- `@task/index.md`
- `@task/log.md` (head ~30 lines only)
- `@task/{slug}.md` — one pointer per **Active** row (all non-archived tasks)
- Primary: `@task/{primary-slug}.md` — {optional one-line why}

Continuity § Reload → `@task/session.handoff-close.md` when session handoff exists.
```

**§ IOM task skills** (separate section in AGENTS — discovery only, not full folder load):

```markdown
## IOM task skills

Load `SKILL.md` **on invoke** only; frontmatter suffices for discovery.

| Skill | Path |
|-------|------|
| iom-todo-task | `.agents/skills/iom-todo-task/SKILL.md` |
| iom-todo-task-archive | `.agents/skills/iom-todo-task-archive/SKILL.md` |
| iom-todo-handoff | `.agents/skills/iom-todo-handoff/SKILL.md` |
| iom-todo-task-knowledge | `.agents/skills/iom-todo-task-knowledge/SKILL.md` |

Reload playbook: [iom-todo-handoff reference § Reload playbook](.agents/skills/iom-todo-handoff/reference.md#reload-playbook).

Requirement quality (invoke before create): `iom-todo-task-knowledge` → `task/knowledge/` — not in reload pack.
```

Update reload pack when Active task set changes.

---

## Token budget

| Artifact | Limit |
|----------|-------|
| Per active task in handoff file | 1–3 lines + bullet list |
| AGENTS § Continuity | ~15 lines total |
| AGENTS § Reload pack | One line per Active task + index/log |
| AGENTS § IOM task skills | Table of paths only — no skill body |
| Handoff file total | Prefer &lt;120 lines; no `@` path block |
| Skill load at session start | Frontmatter / table only until invoke |

Do not paste full checklists into AGENTS. Do not duplicate reload pack in handoff files.

---

## Log event

```markdown
## [YYYY-MM-DD HH:MM] handoff | {basename-without-.md}
- note: {one line}
- related: {slug}, {slug}
```

See [iom-todo-task reference § Log event catalog](../iom-todo-task/reference.md#log-event-catalog).

---

## Index handoff pointer

Under **Active (`task/`)**:

```markdown
Handoff: [session.handoff-close](./session.handoff-close.md)
```

Replace link when handoff basename changes.
