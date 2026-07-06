# Dispatch profiles — master/worker orchestration

Portable **dispatch contract** and **runtime profiles** for the SDD pipeline template. Skill procedures stay in `.agents/skills/`; this file defines how **master** invokes **worker** across AI runtimes.

Related: [README](./README.md) · [PIPELINE_TESTING.md](../../../.agents/skills/iom-sdd-init/references/PIPELINE_TESTING.md)

---

## Portable dispatch contract (every runtime)

Master **MUST** complete these steps before marking worker checklist items `[x]`:

| Step | Action |
|------|--------|
| 1 | Write **`WORKER_HANDOFF.md`** at the worker `cwd` (from phase template or skill template) — all placeholders resolved |
| 2 | Write **`DISPATCH.json`** next to the handoff (schema below) |
| 3 | Invoke worker per **`{DISPATCH_METHOD}`** (profile appendix) |
| 4 | Collect **`WORKER_REPORT.md`** or equivalent sub-agent return — master verifies artifacts before `[x]` |

**Forbidden (all profiles):** master marks worker steps `[x]` without dispatch record + worker report (unless documented `⚠️` override in `task/log.md`).

**Worker obligation:** read and execute `WORKER_HANDOFF.md` end-to-end; write `WORKER_REPORT.md` at `{expected_report}` before session end.

---

## DISPATCH.json schema

Minimal audit trail — keep flat; do not add vendor-specific fields here.

```json
{
  "master_runtime": "cursor",
  "worker_runtime": "kiro-cli",
  "dispatch_method": "async-handoff",
  "phase": 1,
  "cwd": "src/resource/cm-account-service/",
  "handoff": "WORKER_HANDOFF.md",
  "expected_report": "WORKER_REPORT.md",
  "init_agent": "Kiro",
  "cross_runtime": true,
  "dispatched_at": "2026-06-11T21:00:00+07:00"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `master_runtime` | yes | Runtime executing master checklist |
| `worker_runtime` | yes | Runtime executing worker handoff |
| `dispatch_method` | yes | Profile id (see appendix) |
| `phase` | yes | `1` \| `2` \| `3` |
| `cwd` | yes | Worker working directory (repo-relative) |
| `handoff` | yes | Path to handoff file relative to `cwd` or absolute |
| `expected_report` | yes | Path worker must write (typically `WORKER_REPORT.md`) |
| `init_agent` | Phase 3 only | `{INIT_AGENT}` branch for `iom-sdd-init` |
| `specify_init_ai` | Phase 3 only | `kiro` \| `cursor-agent` — must match `worker_runtime` |
| `speckit_procedures_root` | Phase 3 only | `.kiro/prompts/` \| `.cursor/skills/` |
| `speckit_invoke_style` | Phase 3 optional | `dot` \| `hyphen` |
| `cross_runtime` | yes | `true` when `master_runtime` ≠ `worker_runtime` |
| `dispatched_at` | yes | ISO-8601 timestamp |

---

## WORKER_REPORT.md (worker return)

Worker writes this file at `expected_report` from `DISPATCH.json`. Master reads it before verify/closeout.

```markdown
## Worker report — Phase {N}

- dispatch_method: {DISPATCH_METHOD}
- worker_runtime: {WORKER_RUNTIME}
- cwd: …

### Checklist status
- T020: …
- T021: …

### Artifacts
- paths, validator exit codes, blockers

### Phase 3 only (if applicable)
- INIT_VERIFY attempt N/3
- Speckit setup-script exit codes
- implement provenance: generated | partial-resource-copy | resource-copy
- go build / go test exit codes
```

Phase 3 may extend with sections from [WORKER_HANDOFF.template.md](../../../.agents/skills/iom-sdd-init/assets/WORKER_HANDOFF.template.md) — **Return report** block.

---

## Cross-runtime exception

When `{MASTER_RUNTIME}` ≠ `{WORKER_RUNTIME}`:

| Rule | Detail |
|------|--------|
| **Allowed** | User or master opens a **separate** worker session/terminal in the worker runtime |
| **Required** | `DISPATCH.json` with `cross_runtime: true` |
| **Required** | `WORKER_REPORT.md` on disk before master marks worker items `[x]` |
| **Required** | `task/log.md` entry: `cross-runtime dispatch` with both runtimes + `dispatch_method` |

**Same-runtime:** prefer `cursor-task-tool` or vendor-native sub-agent when available; manual session still needs `DISPATCH.json` + report.

---

## Compatibility matrix

| Profile | Phase 1–2 | Phase 3 Speckit | Status |
|---------|-----------|-----------------|--------|
| `cursor-task-tool` | ✅ tested (runs 4–5) | ✅ tested (runs 4–5) | **production** |
| `async-handoff` | ✅ feasible | ⚠️ manual worker session | **supported** |
| `kiro-cli-spawn` | ✅ run-6 Ph1–2 | ⚠️ run-6 Ph3 — use `--ai kiro` not `cursor-agent` | **supported** |
| `gemini-cli-spawn` | ⚠️ illustrative CLI | ❓ `{SPECKIT_SKILLS_ROOT}` TBD | **draft** |

Verify vendor CLI syntax against current docs before production use. Draft profiles are contract-compliant but not E2E-proven in this repo.

---

## Profile appendix

### `cursor-task-tool` — production

**When:** `{MASTER_RUNTIME}` = `cursor` and `{WORKER_RUNTIME}` = `cursor` (or Cursor sub-agent).

```text
Task tool · subagent_type: generalPurpose
prompt: Read and execute @{cwd}/{handoff} end-to-end.
       Write report to @{cwd}/{expected_report}.
cwd = {cwd}
Return: checklist status, artifact paths, validator exit codes, blockers.
```

Set `dispatch_method`: `cursor-task-tool`, `cross_runtime`: `false` when master and worker are both Cursor.

---

### `async-handoff` — supported (cross-runtime default)

**When:** `{MASTER_RUNTIME}` ≠ `{WORKER_RUNTIME}`, or no programmatic spawn API.

1. Master writes `WORKER_HANDOFF.md` + `DISPATCH.json` (`cross_runtime: true`).
2. Master (or user) starts worker session in `{WORKER_RUNTIME}` with prompt:

   ```text
   cwd = {cwd}
   Read and execute WORKER_HANDOFF.md end-to-end.
   Write WORKER_REPORT.md before finishing.
   ```

3. Master polls for `WORKER_REPORT.md` or user confirms worker done.
4. Master runs verify checklist; append `task/log.md`: `cross-runtime dispatch`.

**Best first pilot** for master Cursor + worker kiro-cli / Gemini.

---

### `kiro-cli-spawn` — supported

**When:** `{WORKER_RUNTIME}` = `kiro-cli` and CLI spawn is available.

Verify against [Kiro CLI](https://kiro.dev/docs) current syntax:

```text
cd {cwd}
# Master Phase 3 T003 first:
#   specify init . --force --ai kiro
# Then spawn worker:
kiro-cli chat --no-interactive "Read and execute WORKER_HANDOFF.md end-to-end. Write WORKER_REPORT.md."
```

| Phase 3 setting | Value |
|-----------------|-------|
| `{INIT_AGENT}` | `Kiro` — `.kiro/steering/` from `iom-sdd-init` |
| `{SPECIFY_INIT_AI}` | `kiro` — **not** `cursor-agent` when worker is kiro-cli |
| `{SPECKIT_PROCEDURES_ROOT}` | `.kiro/prompts/` (`speckit.specify.md`, …) |
| Speckit slash | `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement` (dot) |

Full resolver: [SPECKIT_INTEGRATION.md](../../../.agents/skills/iom-sdd-init/references/SPECKIT_INTEGRATION.md).

**Run-6 lesson:** `specify init --ai cursor-agent` + kiro worker left Speckit in `.cursor/skills/` with no Kiro native commands — **avoid**.

---

### `gemini-cli-spawn` — draft

**When:** `{WORKER_RUNTIME}` = `gemini-cli`.

Illustrative only — verify against Gemini CLI docs:

```text
cd {cwd}
gemini -p "Read and execute WORKER_HANDOFF.md end-to-end. Write WORKER_REPORT.md."
```

Set `{INIT_AGENT}` = `Gemini` for Phase 3 (workspace needs `.gemini/`).

After init: worker may need `/memory reload` per `iom-sdd-init` Gemini branch.

---

## Log entry template (`task/log.md`)

```markdown
## [YYYY-MM-DD HH:MM] cross-runtime dispatch | {task-slug}
- master_runtime: {MASTER_RUNTIME}
- worker_runtime: {WORKER_RUNTIME}
- dispatch_method: {DISPATCH_METHOD}
- phase: {1|2|3}
- cwd: {cwd}
- report: {expected_report} received yes|no
```

---

## Phase template wiring

Phase templates [phase-1-context.md](./phase-1-context.md), [phase-2-spec.md](./phase-2-spec.md), [phase-3-speckit.md](./phase-3-speckit.md) reference this file for dispatch — set `{DISPATCH_METHOD}` when instantiating a pipeline run.
