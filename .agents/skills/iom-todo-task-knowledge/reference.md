# iom-todo-task-knowledge — reference

## Portability

- Skill text = algorithm + placeholders (`{NNN}`, `{type}`, `{scope}`).
- Repo-specific should/should-not examples live in **`task/knowledge/`** only.
- Cross-link **iom-todo-task**, **iom-todo-task-archive**, **iom-todo-handoff**, **iom-todo-task-knowledge** — no domain/SDD coupling in skill core.

---

## Knowledge layout

```text
task/knowledge/
├── README.md
├── refresh-manifest.yaml
├── requirements-playbook.md
└── by-type/

.agents/skills/iom-todo-task-knowledge/
├── SKILL.md
├── reference.md
└── scripts/
    └── knowledge-manifest.py   # optional diff helper (Python, stdlib) — ships with skill install
```

Repo-root **`scripts/`** (install.ps1, install.sh) is **not** for skill helpers — keep skill scripts inside the skill folder.

| File | Role |
|------|------|
| `refresh-manifest.yaml` | Tracks which archive tasks were ingested; enables incremental refresh |
| `requirements-playbook.md` | Global patterns + meta (`last_refresh`, `last_refresh_mode`, source count) |
| `by-type/*.md` | Type-specific Requirement guidance |
| `README.md` | How to refresh; link to skill |

**Not in reload pack** — load on invoke or before Requirement gate only.

---

## Incremental refresh

### Manifest record (per archived task)

```yaml
tasks:
  {slug}:
    path: "task/archive/YYYY-MM-DD/{slug}.md"
    content_hash: "16-char hex"   # SHA-256 of raw file bytes, first 16 hex digits
    type: "{type}"
    created: "YYYY-MM-DD"
    updated: "YYYY-MM-DD"
    ingested_at: "YYYY-MM-DD"
```

Top-level:

```yaml
version: 1
last_full_refresh: "YYYY-MM-DD"   # null until first full rebuild
```

### Diff algorithm

1. **Glob** numbered tasks: `task/archive/*/[0-9]{3,}-*.md` (exclude `*.handoff*.md`)
2. For each file: `slug` = basename without `.md`; `content_hash` = SHA-256(**raw bytes**).hexdigest()[:16]
3. Compare to `refresh-manifest.yaml` `tasks.{slug}.content_hash`:

| Set | Condition |
|-----|-----------|
| **new** | slug not in manifest |
| **changed** | manifest hash ≠ current hash |
| **skipped** | manifest hash = current hash |
| **removed** | slug in manifest but file gone from archive |

4. **Incremental (default):** read archive **only** for `new ∪ changed`; merge patterns into playbook; update manifest entries; drop **removed** slugs from manifest; prune their patterns on **full** or explicit reconcile
5. **Full (`--full` / `go full`):** read **all** archive tasks; replace playbook synthesis; set `last_full_refresh`; rewrite all manifest entries

### Helper script (optional, this repo)

```bash
python .agents/skills/iom-todo-task-knowledge/scripts/knowledge-manifest.py
python .agents/skills/iom-todo-task-knowledge/scripts/knowledge-manifest.py --write
python .agents/skills/iom-todo-task-knowledge/scripts/knowledge-manifest.py --init
```

Agent may run script or replicate diff logic — manifest file is source of truth. **Python 3** + stdlib only (no pip deps).

### When to skip archive reads

| Condition | Action |
|-----------|--------|
| Incremental + empty new/changed/removed | Report **up to date**; ~0 archive token reads |
| User `go full` | Read all archive files |
| Skill synthesize algorithm changed | Recommend **full** once |

### Merge vs replace (incremental)

| Section | Incremental | Full |
|---------|-------------|------|
| Should do / should not | Add or refine bullets from new/changed tasks; dedupe similar lines | Replace entire lists |
| Patterns by tag | Merge new tag hints | Replace |
| Open follow-ups | Merge; remove stale only on full | Replace |
| Source tasks table | Append new rows; remove **removed** slugs | Replace table |
| `by-type/*.md` | Patch if new/changed tasks affect that `type` | Replace all |

Recommend **full** every **~10 incremental** ingests or when playbook feels noisy.

### Log event

```markdown
## [YYYY-MM-DD HH:MM] knowledge-refresh | requirements-playbook
- note: {incremental|full} — ingested {slug},{slug}; skipped {K}
- related: task/knowledge/requirements-playbook.md
```

---

## Full refresh algorithm (legacy baseline)

1. **Glob** archive numbered tasks
2. **Parse** Requirement, Out of scope, Decisions, checklist lessons, `type`, `tags`
3. **Aggregate** → should/should-not, by-type, by-tag
4. **Write** playbook + by-type + manifest (all tasks ingested)

---

## Requirement gate

Apply when user runs **Mode G** before create.

### Global (all types)

| # | Check | Block if `improvement` |
|---|--------|------------------------|
| G1 | **Goal** — one clear outcome | Yes |
| G2 | **In scope** — explicit bullets | Warn |
| G3 | **Out of scope** — ≥ 2 bullets | Yes |
| G4 | Open questions → **Decisions** table or "ask user in T001" | Warn |
| G5 | No duplicate source of truth (e.g. master exists → no parallel inbox) | Warn |
| G6 | Research inputs labeled "execute only — not in skill output" when reading archive | Warn (skill tasks) |

### By type (see `by-type/{type}.md`)

Load matching file when `type` is set in draft frontmatter or user states type.

### Block vs warn (Q5)

| `type` | Missing Out of scope / Goal |
|--------|----------------------------|
| `improvement` | **Block** — user must revise + confirm |
| `planning`, `execution`, other | **Warn** — list gaps; proceed only on user **go** |

User may say **strict gate** to block any type.

---

## Playbook skeleton

```markdown
---
title: "Requirements knowledge"
type: knowledge
detail: "Generated from task/archive — do not edit by hand without refresh"
last_refresh: YYYY-MM-DD
last_refresh_mode: incremental
source_task_count: N
manifest_tasks: N
---

# Requirements knowledge

> Generated by **iom-todo-task-knowledge**. Refresh: `refresh knowledge` (incremental) · `refresh knowledge full`
```

---

## User guide

Full command reference and workflow: [SKILL.md § User guide](SKILL.md#user-guide).

| User intent | Command | Agent reply |
|-------------|---------|-------------|
| Incremental refresh | `refresh knowledge` | Refresh plan → **go** / **stop** |
| Full rebuild | `refresh knowledge full` | Refresh plan → **go full** / **stop** |
| Gate draft | `gate requirement type={type}` + Requirement body | Gap report → revise or **go** |
| Gate existing file | `gate requirement @task/{NNN}-{slug}.md` | Same |
| Strict gate | `gate requirement strict` + body | Block on any gap until fixed |

**Not in reload pack:** `task/knowledge/**` — invoke this skill or `@` playbook on demand.

---

## Integration points

| Skill | Hook |
|-------|------|
| **iom-todo-task** | User invokes knowledge **before** Mode A; optional Related link to playbook |
| **iom-todo-task-archive** | After archive: suggest `refresh knowledge` (incremental) |
| **iom-todo-handoff** | No automatic refresh |

---

## Token budget

| Operation | Approx. reads |
|-----------|----------------|
| Gate (Mode G) | playbook + one `by-type` (~1.4k tokens) |
| Incremental refresh, 0 diff | manifest only (~0.5k) |
| Incremental refresh, 1 new task | ~1.1k + merge |
| Full refresh | all archive tasks (~1.1k × N) |

Run `python .agents/skills/iom-todo-task-knowledge/scripts/knowledge-manifest.py` before Mode R to avoid reading skipped tasks.
