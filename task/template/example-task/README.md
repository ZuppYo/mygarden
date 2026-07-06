# Example task template

Generic **Mode A-template** sample for documentation and smoke tests. Not a numbered task.

## Files

| File | Use |
|------|-----|
| [skeleton.md](./skeleton.md) | Minimal instantiate target |

## Placeholders

| Token | On instantiate |
|-------|----------------|
| `{NNN}` | Allocated task id (zero-padded) |
| `{CREATED}`, `{UPDATED}` | Today `YYYY-MM-DD` |
| `{scope}` | Short label for this run (user-provided) |
| `{slug}`, `{SLUG}` | Kebab summary (auto from scope if omitted) |

## How to instantiate

1. **iom-todo-task** Mode A-template — `create from template example-task/skeleton scope={scope}`
2. Agent allocates `{NNN}`, substitutes tokens, writes `task/{NNN}-{scope}-example.md`
3. Execute with `go` when ready

One file per instantiate call. For multi-step pipelines, add phase files under a separate `{set}/` in the consumer repo.
