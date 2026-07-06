# Sub-task template

Child work unit under a **master task**. Shares the master's `{NNN}` prefix and `{scope}`.

## Naming (required)

```text
{NNN}-{NN}-sub-task-{scope}.md
```

| Part | Example | Rule |
|------|---------|------|
| `{NNN}` | `037` | Same as parent master — **not** a new global id |
| `{NN}` | `01`, `02` | Zero-padded 2 digits; next = max existing + 1 under that master |
| `{scope}` | `ai-research` | Same kebab as parent master unless user overrides |

**Parent master:** `{NNN}-master-task-{scope}.md`

Example family:

```text
037-master-task-ai-research.md
037-01-sub-task-ai-research.md
037-02-sub-task-ai-research.md
```

## Placeholders

| Token | On instantiate |
|-------|----------------|
| `{NNN}` | From parent master basename |
| `{NN}` | Next sub-sequence (01–99) under `{NNN}` |
| `{scope}` | From parent or user |
| `{PARENT}` | Master slug without `.md` |
| `{MASTER_TITLE}` | `title` from parent master frontmatter |
| `{SUB_TITLE}` | Display title (optional) |
| `{CREATED}`, `{UPDATED}` | Today |

## Instantiate

```text
create from template sub-task/skeleton parent=037-master-task-ai-research
```

Or: `parent={master-slug}` + same `{scope}` as master.

**Requires** an existing master file. On instantiate, read parent `title` → `{MASTER_TITLE}`. Updates master `## Children` table after create.

### Body (required)

Sub-task files must show parent in **both** places:

1. **Frontmatter** — `role: child`, `parent: {master-slug}`, `master_nnn`, `sub_nn`
2. **Body** (visible) — blockquote `Parent master:` with human title + link, not slug alone

## When not to use

Single-session work → checklist inside master or standalone `{NNN}-{kebab}.md` (Mode A).
