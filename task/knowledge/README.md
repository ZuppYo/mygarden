# Task knowledge

Generated patterns from archived tasks — improves **Requirement** quality for new tasks.

| File | Purpose |
|------|---------|
| [requirements-playbook.md](requirements-playbook.md) | Global should do / should not do |
| [by-type/planning.md](by-type/planning.md) | Planning-task guidance |
| [by-type/execution.md](by-type/execution.md) | Execution-task guidance |
| [refresh-manifest.yaml](refresh-manifest.yaml) | Ingest tracking for incremental refresh |

## Refresh

```text
refresh knowledge           # incremental (new/changed archive only)
refresh knowledge full      # full rebuild
```

Invoke **iom-todo-task-knowledge** skill. Not in AGENTS reload pack — load on demand.

## Gate before create

```text
gate requirement type={planning|execution|improvement}

Goal: …
In scope: …
Out of scope: …
```

Then invoke **iom-todo-task** Mode A to create the task.
