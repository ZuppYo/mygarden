# AGENTS Ultra-Compact Template

Use this template for long-running projects to reduce startup token usage across sessions.

## Project initialization (day 0)

Recommended startup via IOM skills:

1. Use `iom-todo-task` to bootstrap task system (`task/index.md`, `task/log.md`) if missing
2. Create first task: `000-project-bootstrap.md` (or `001-...` if numbering already used)
3. Fill AGENTS using this template with only:
   - Mission (1 line)
   - Hard constraints (5-10 bullets)
   - IOM task skills (discovery paths only)
   - Reload pack (minimal pointers only — **canonical** `@` list)
   - Continuity snapshot (one block only)
4. Run `iom-todo-task` execution on bootstrap task until done
5. Use `iom-todo-task-archive` only when checklist is done and age rule passes

Day-0 deliverables:
- `AGENTS.md` (compact)
- `task/index.md`
- `task/log.md`
- `task/000-project-bootstrap.md` (or next numbered task)

Install skills: `scripts/install.ps1` or `install.sh` — creates or patches `AGENTS.md` with IOM block when missing.

## Repository mission

- One-line scope of this repo
- In-scope vs out-of-scope in 3-6 bullets total

## Non-negotiable rules

- 5-10 bullets only (hard constraints)
- Keep each bullet one line

## IOM task skills

Load `SKILL.md` on **invoke** only; frontmatter suffices for discovery.

| Skill | Path |
|-------|------|
| iom-todo-task | `.agents/skills/iom-todo-task/SKILL.md` |
| iom-todo-task-archive | `.agents/skills/iom-todo-task-archive/SKILL.md` |
| iom-todo-handoff | `.agents/skills/iom-todo-handoff/SKILL.md` |

Reload playbook: [iom-todo-handoff reference § Reload playbook](.agents/skills/iom-todo-handoff/reference.md#reload-playbook).

## Reload pack (minimal)

Canonical list — handoff files do not duplicate this block.

- `@task/index.md`
- `@task/log.md` (head ~30 lines only)
- `@task/{slug}.md` — one pointer per **Active** row (all non-archived tasks)
- Primary: `@task/{primary-slug}.md`

Continuity § Reload → `@task/session.handoff-close.md` when session handoff exists.

## Continuity — latest activity

Keep this section short and replace old snapshot each time (do not append history).

### Snapshot (YYYY-MM-DD)

- Done: `<task-slug>` — one-line outcome
- Done: `<task-slug>` — one-line outcome
- Next: `<primary-slug>` — one-line action
- Reload: `@task/session.handoff-close.md`

## Task state pointers

- Active index: `task/index.md`
- Activity log: `task/log.md` (read **head** ~30 lines)
- Archive: `task/archive/YYYY-MM-DD/`

## Token hygiene policy

- Keep `AGENTS.md` under ~250 lines
- Keep Continuity section under ~50 lines
- Never duplicate old continuity snapshots
- Never paste long task details into AGENTS; link instead
- Prefer pointers over prose
- Never list `@.agents/skills/{name}/` whole folders — `SKILL.md` on invoke only
- Handoff files: Reload chain link to AGENTS, not duplicate `@` lists

## Optional deep context (link-only)

- `docs/history/` or `task/archive/` for full history
- Long implementation notes stay outside AGENTS
