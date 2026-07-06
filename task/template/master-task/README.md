# Master task template

Standard template for an **initiative control plane** (Jira Story–like). One master per topic; spawn **sub-task** children for executable work.

## Naming (required)

```text
{NNN}-master-task-{scope}.md
```

| Part | Example |
|------|---------|
| `{NNN}` | `037` — global allocated id |
| `{scope}` | `ai-research` — short kebab label |

Example: `037-master-task-ai-research.md`

Children use [sub-task template](../sub-task/README.md): `037-01-sub-task-ai-research.md`, `037-02-sub-task-ai-research.md`.

## When to use

| Use master-task | Use sub-task | Use checklist only |
|-----------------|--------------|-------------------|
| New initiative spanning multiple sessions | Plannable child in `task/index.md` | Single session, one owner |
| Need Activity (comment) trail on scope | Instantiate from `sub-task/` or other template | Steps fit one master file |

## Placeholders

| Token | On instantiate |
|-------|----------------|
| `{NNN}` | Global allocated id |
| `{CREATED}`, `{UPDATED}` | Today `YYYY-MM-DD` |
| `{scope}` | Short kebab (e.g. `ai-research`) |
| `{MASTER_TITLE}` | Human title (optional; default from scope) |

Output slug: **`{NNN}-master-task-{scope}.md`** (not `{NNN}-master-{scope}`).

## Instantiate

```text
create from template master-task/skeleton scope=ai-research MASTER_TITLE="AI research — master"
```

## Hierarchy (iom-todo)

```text
Master  {NNN}-master-task-{scope}.md
  └── Sub-task  {NNN}-{NN}-sub-task-{scope}.md   (NN = 01, 02, …)
        └── Checklist items                      (no deeper files)
```

## Sections

| Section | Role | Jira analog |
|---------|------|-------------|
| `## Task Requirement` | Stable goal, scope, acceptance | Description |
| `## Children` | Table: NN, slug, status | Linked issues |
| `## Activity` | Prepend decisions / blockers | Comments |

**Do not** use `task/prompts.md` as source of truth when a master exists — add Activity on the master instead.

## Spawn sub-task

```text
create from template sub-task/skeleton parent={NNN}-master-task-{scope}
```

Set `{scope}` same as master unless intentional fork. Add row to master `## Children` after create.
