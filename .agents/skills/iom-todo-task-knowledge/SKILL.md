---
name: iom-todo-task-knowledge
version: "1.1.1"
description: >-
  Refreshes task Requirement quality knowledge from task/archive/** into task/knowledge/,
  with incremental refresh via refresh-manifest.yaml (skip already-ingested tasks).
  Gates draft Requirements before create. Invoke separately from iom-todo-task.
  User commands: refresh knowledge, gate requirement — see SKILL § User guide.
disable-model-invocation: true
---

# IOM Todo Task Knowledge

Extract **should do** / **should not do** patterns from archived tasks and maintain **`task/knowledge/`** so the next task’s **Requirement** improves over time.

**Separate from create:** invoke this skill **before** [iom-todo-task](../iom-todo-task/SKILL.md) Mode A — do not auto-create tasks here.

**Related skills:** [iom-todo-task](../iom-todo-task/SKILL.md) · [iom-todo-task-archive](../iom-todo-task-archive/SKILL.md) (suggest incremental refresh after archive) · [iom-todo-handoff](../iom-todo-handoff/SKILL.md)

Templates, manifest, and gate rules: [reference.md](reference.md)

---

## User guide

Knowledge maintains **`task/knowledge/`** (playbook, by-type, manifest) from **`task/archive/**`**. It does **not** create tasks, archive, or handoff — invoke **separately** from [iom-todo-task](../iom-todo-task/SKILL.md).

| Output | Purpose |
|--------|---------|
| `task/knowledge/requirements-playbook.md` | Global should do / should not do |
| `task/knowledge/by-type/{type}.md` | Guidance per task `type` |
| `task/knowledge/refresh-manifest.yaml` | Which archive tasks were already ingested |

**Optional layer:** create and execute work without refresh/gate. Use knowledge to improve Requirement quality over time.

### When to invoke

| Situation | Mode | User says |
|-----------|------|-----------|
| After archiving tasks | R — refresh | `refresh knowledge` → **go** |
| Playbook feels stale / many incremental ingests | R — full | `refresh knowledge full` → **go full** |
| Before creating a new task | G — gate | `gate requirement` + draft → **go** |
| First project / empty archive | R — refresh | Creates stub playbook; refresh again after first archive |

### User commands — refresh (Mode R)

```text
refresh knowledge                 # incremental (default) — new/changed archive only
refresh knowledge full            # full rebuild — all archive tasks
```

Agent shows a refresh plan → reply **`go`** (incremental), **`go full`** (force full), or **`stop`**.

If already up to date: agent reports 0 new/changed — reply **`go full`** to rebuild anyway, or **`stop`**.

### User commands — gate (Mode G)

**Paste draft Requirement:**

```text
gate requirement type={type}

Goal: …
In scope: …
Out of scope: …
```

**Existing task file:**

```text
gate requirement @task/{NNN}-{slug}.md
```

**Strict (block on any gap, all types):**

```text
gate requirement strict

Goal: …
```

Agent shows Pass / Gap / Warn → reply with revised Requirement, or **`go`** if pass + confirmed. Then invoke **iom-todo-task** to create (Mode G does not write task files).

| `type` | Missing Goal or Out of scope |
|--------|------------------------------|
| `improvement` | **Block** until fixed + **go** |
| `planning`, `execution`, other | **Warn** — proceed on **go** unless **strict gate** |

### Recommended flow (with sibling skills)

```text
1. refresh knowledge          → go          # optional; especially after archive
2. gate requirement type=…    → go          # recommended before create
3. create task to …                         # iom-todo-task Mode A
4. @task/{NNN}-{slug}.md go                 # iom-todo-task Mode B execute
5. handoff                                  # iom-todo-handoff (session end)
6. archive tasks                → go        # iom-todo-task-archive
7. refresh knowledge            → go        # optional; ingest new archive
```

**Session reload** (AGENTS reload pack) does **not** include `task/knowledge/**` — load on invoke only.

### Read playbook without gate

```text
@task/knowledge/requirements-playbook.md summarize should do / should not do
@task/knowledge/by-type/{type}.md
```

Reference only — does not replace Mode G gate before create.

---

## Quick start

### Mode R — Refresh knowledge

**Default: incremental** — read only **new** or **changed** archive tasks (via `task/knowledge/refresh-manifest.yaml`).

**Full rebuild:** user says `refresh knowledge full` or `refresh knowledge --full`.

1. Run diff (agent or helper script):
   - `python .agents/skills/iom-todo-task-knowledge/scripts/knowledge-manifest.py` → JSON `{ newSlugs, changed, skipped, removed, total }`
   - Or manual: compare each archive file **slug** + **content_hash** (SHA-256 raw bytes, first 16 hex) to manifest
2. If **incremental** and `newSlugs`, `changed`, `removed` all empty → report **up to date**; skip archive reads (optional manifest-only touch)
3. **Read archive files** only for `newSlugs ∪ changed`; on **full**, read all numbered archive tasks
4. **Merge** into existing playbook (incremental) or **replace** synthesis (full)
5. Update `refresh-manifest.yaml`, playbook meta, `by-type/` as needed
6. Build refresh plan → **STOP** until user **go**
7. On **go**: write outputs; **prepend** `knowledge-refresh` to `task/log.md` with mode + slugs ingested

See [reference.md § Incremental refresh](reference.md#incremental-refresh).

### Mode G — Gate draft Requirement

1. Read `task/knowledge/requirements-playbook.md` (and matching `by-type/{type}.md` if present)
2. User supplies draft Requirement (paste or `{NNN}` task file path)
3. Run [reference.md § Requirement gate](reference.md#requirement-gate) — report gaps
4. **`type: improvement`:** **BLOCK** until Out of scope + Goal present and user confirms fixes (**go**)
5. Other types: **warn** on gaps; block only if user says **strict gate**

**STOP** after gap report; no task file writes unless user also invokes **iom-todo-task**.

---

## Refresh plan (STOP)

```
📚 Knowledge refresh plan — {incremental|full}

Archive total: {N} numbered tasks
Ingest: {new} new, {changed} changed, {removed} removed from manifest
Skip (already ingested): {skipped}

Read archive files: {list slugs to read, or "all" if full}
Outputs:
- task/knowledge/requirements-playbook.md
- task/knowledge/by-type/*.md (if patterns changed)
- task/knowledge/refresh-manifest.yaml

Will update: task/log.md (knowledge-refresh event)

Reply "go" to refresh, "go full" to force full rebuild, or "stop".
```

If incremental and nothing to ingest:

```
📚 Knowledge up to date — 0 new/changed/removed ({skipped} skipped). Reply "go full" to rebuild anyway, or "stop".
```

---

## Gate report (STOP)

```
📋 Requirement gate — {type}

Pass: {items}
Gap (block for improvement): {items}
Warn: {items}

Reply with revised Requirement, or "go" if pass + user confirms.
Then invoke iom-todo-task to create the task.
```

---

## Behavioral rules

- **Portability:** SKILL.md uses placeholders only; **never** embed archived slugs in skill text
- **Lazy load:** Do not add `task/knowledge/**` to AGENTS reload pack by default
- **Incremental default:** skip archive files whose `content_hash` matches manifest unless **full**
- **No create/archive/handoff:** Do not allocate `{NNN}`, move archive files, or write handoff
- **Replace unbounded history** in playbook — merge incremental into stable sections; periodic **full** reconciles frequency counts
- **Empty archive:** Write minimal playbook + empty manifest; note "refresh after first archive"
- **Skill scripts only:** Optional helpers live under **`.agents/skills/iom-todo-task-knowledge/scripts/`** — do **not** add skill-specific scripts to repo-root `scripts/` (that folder is install/bootstrap for iom-todo repo only)

---

## Errors

| Case | Action |
|------|--------|
| No `task/archive/` | Write stub playbook; suggest bootstrap + archive first |
| Missing manifest on first refresh | `--init` manifest from archive (full ingest) |
| Missing `task/knowledge/` | Create folder + README on refresh |
| Draft missing `type` for gate | Ask user; default gate = warn-only |
