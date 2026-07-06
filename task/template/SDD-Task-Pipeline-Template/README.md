# SDD Task Pipeline Template

Reusable **master/worker** pipeline templates to test skills `iom-sdd-context` → `iom-sdd-spec` → Speckit SDD (`iom-sdd-init`).

Derived from executed SDD pipeline tasks in **iom-ai-skill** (`014`–`016`, archived).

## Files

| File | Phase | Skill under test |
|------|-------|------------------|
| [phase-1-context.md](./phase-1-context.md) | 1 | `iom-sdd-context` |
| [phase-2-spec.md](./phase-2-spec.md) | 2 | `iom-sdd-spec` |
| [phase-3-speckit.md](./phase-3-speckit.md) | 3 | `iom-sdd-init` + Speckit chain |
| [dispatch-profiles.md](./dispatch-profiles.md) | all | Master/worker dispatch contract + runtime profiles |

## Placeholders (replace when creating a new task)

| Token | Example | Use |
|-------|---------|-----|
| `{NNN}` | `017` | Next task id (`iom-todo-task` allocate) |
| `{RUN_SLUG}` | `cm-account-service-run-2` | Short label for this pipeline run |
| `{BASENAME}` | `cm-account-service` | FM module basename |
| `{QUEUE}` | `ccbs.create_new_account` | Active queue spec stem |
| `{RESOURCE_SANDBOX}` | `src/resource/cm-account-service` | **Context scan only** (Phase 1); Speckit implement **ห้าม copy** |
| `{JUNCTION_TARGET}` | `E:\SRC\iom\fm\cm-account-service` | Optional junction target |
| `{CONFLUENCE_PAGE_ID}` | `1302429778` | Confluence page for `{QUEUE}` |
| `{CONFLUENCE_URL}` | `https://trueomx.atlassian.net/wiki/spaces/I/pages/1302429778/...` | Full wiki URL |
| `{INIT_AGENT}` | `Cursor` | `iom-sdd-init` agent branch — **workspace layout** (`.cursor/`, `.kiro/`, `.gemini/`, …) |
| `{MASTER_RUNTIME}` | `cursor` | AI runtime running **master** checklist |
| `{WORKER_RUNTIME}` | `kiro-cli` | AI runtime running **worker** handoff |
| `{DISPATCH_METHOD}` | `async-handoff` | Profile id — see [dispatch-profiles.md](./dispatch-profiles.md) |
| `{SPECIFY_INIT_AI}` | `kiro` \| `cursor-agent` | `specify init --ai` — **must match `{WORKER_RUNTIME}`** — see [SPECKIT_INTEGRATION](../../../.agents/skills/iom-sdd-init/references/SPECKIT_INTEGRATION.md) |
| `{SPECKIT_PROCEDURES_ROOT}` | `.kiro/prompts/` \| `.cursor/skills/` | Speckit procedure files after init (Kiro: `speckit.*.md` · Cursor: `speckit-*/SKILL.md`) |
| `{SPECKIT_INVOKE_STYLE}` | `dot` \| `hyphen` | Kiro: `/speckit.specify` · Cursor: `/speckit-specify` |
| `{SPECKIT_SKILLS_ROOT}` | *(legacy alias)* | Same as `{SPECKIT_PROCEDURES_ROOT}` — prefer new name in new runs |
| `{PRIOR_PHASE_1}` | `017-iom-sdd-pipeline-context-…` | Slug link after Phase 1 created |
| `{PRIOR_PHASE_2}` | `018-iom-sdd-pipeline-spec-…` | Slug link after Phase 2 created |
| `{CREATED}` / `{UPDATED}` | `YYYY-MM-DD` | Frontmatter dates |
| `{COMPARE_ARTIFACT}` | `src/PIPELINE_COMPARE.md` | Master compare report (per run) |

### `{INIT_AGENT}` vs `{WORKER_RUNTIME}` (do not conflate)

| Concept | Placeholder | Answers |
|---------|-------------|---------|
| **Who runs the worker handoff?** | `{WORKER_RUNTIME}` | Shell/IDE executing `WORKER_HANDOFF.md` (`cursor`, `kiro-cli`, `gemini-cli`, …) |
| **Which init branch writes workspace agent folders?** | `{INIT_AGENT}` | `iom-sdd-init` branch: `Cursor`, `Kiro`, `Gemini`, … — see [INIT_VERIFY](../../../.agents/skills/iom-sdd-init/references/INIT_VERIFY.md) |
| **How master starts worker?** | `{DISPATCH_METHOD}` | `cursor-task-tool`, `async-handoff`, `kiro-cli-spawn`, `gemini-cli-spawn` |

They are **independent**. Phase 3 often sets `{INIT_AGENT}` from the **workspace target**, not from `{MASTER_RUNTIME}`.

| Example run | `{MASTER_RUNTIME}` | `{WORKER_RUNTIME}` | `{INIT_AGENT}` | Notes |
|-------------|-------------------|-------------------|----------------|-------|
| All Cursor (runs 4–5) | `cursor` | `cursor` | `Cursor` | `cursor-task-tool`; `cross_runtime: false` |
| Cursor master, Kiro worker | `cursor` | `kiro-cli` | `Kiro` | `async-handoff`; `specify init --ai kiro` → `.kiro/prompts/`; `/speckit.specify` |
| Gemini master + worker | `gemini-cli` | `gemini-cli` | `Gemini` | `.gemini/` + `/memory reload` |
| Cursor master, Gemini worker | `cursor` | `gemini-cli` | `Gemini` | `async-handoff`; init branch = Gemini |

Full dispatch rules: [dispatch-profiles.md](./dispatch-profiles.md).

## How to create a new pipeline run

1. Use **`iom-todo-task` Mode A-template** — one phase file per run:

   ```text
   create from template SDD-Task-Pipeline-Template/phase-1-context RUN_SLUG={RUN_SLUG} BASENAME=… MASTER_RUNTIME=… WORKER_RUNTIME=… DISPATCH_METHOD=…
   ```

   Provide placeholders from the table above (or `go + KEY=value`). The skill allocates `{NNN}`, substitutes tokens, writes `task/{NNN}-….md`, and updates index + log.

2. Execute Phase 1 (`go`) → archive or mark **done**.
3. Repeat for **phase-2-spec.md** (prerequisite: Phase 1 done) and **phase-3-speckit.md** (prerequisite: Phase 1 + 2 done).
4. Each run: new task ids — **do not reuse** completed checklists from a prior run.

Manual copy still works if Mode A-template is unavailable; prefer Mode A-template for consistent placeholders and logging.

## Rerun / clean workspace

Before a fresh pipeline:

- Keep `src/resource/` (context scan source — do not delete).
- Clear or confirm incremental: `src/docs/`, `src/.specify/`, `src/.cursor/`, `src/.kiro/prompts/` (re-init with correct `--ai`), implement artifacts under `src/` (except `resource/`).
- Create **new** numbered tasks from these templates.

## Orchestration (all phases)

- **master** (`{MASTER_RUNTIME}`) — env prep, `WORKER_HANDOFF.md`, `DISPATCH.json`, dispatch, verify, closeout.
- **worker** (`{WORKER_RUNTIME}`) — executes handoff; writes `WORKER_REPORT.md`.
- **Dispatch profiles:** [dispatch-profiles.md](./dispatch-profiles.md) — contract + `{DISPATCH_METHOD}` appendix.
- **Forbidden:** master marks worker steps `[x]` without `DISPATCH.json` + worker report (or documented `⚠️` override in `task/log.md`).
- **Cross-runtime exception:** when `{MASTER_RUNTIME}` ≠ `{WORKER_RUNTIME}`, separate worker session is **allowed** — requires `cross_runtime: true` in `DISPATCH.json` + `cross-runtime dispatch` log entry.
- **Same-runtime default:** `{DISPATCH_METHOD}` = `cursor-task-tool` when both runtimes are `cursor`.
- **Phase 3 only — Forbidden:** simulate Speckit or hand-write `spec.md`/`plan.md`/`tasks.md` without `{SPECKIT_PROCEDURES_ROOT}` procedures + setup scripts; **Forbidden:** kiro worker + `specify init --ai cursor-agent` (run-6 anti-pattern).

## Pipeline conventions

Skill rules stay **generic** (rotate `{BASENAME}` each run): [PIPELINE_TESTING.md](../../../.agents/skills/iom-sdd-init/references/PIPELINE_TESTING.md). Service-specific values live **only** in placeholders below and in workspace outputs.

### From run 016+ improvements

| Topic | Phase | Rule |
|-------|-------|------|
| **Legacy spec sync** | 2 | No Change History → full §1–§14 export; omit Sync mode metadata |
| **Test infra** | 3 | Handoff includes Redis LOV + wiremock policy ([WORKER_HANDOFF.template.md](../../../.agents/skills/iom-sdd-init/assets/WORKER_HANDOFF.template.md)) |
| **Baseline test gate** | 3 | Master runs `go test` in `{RESOURCE_SANDBOX}/` before failing on red implement tests |
| **No copy from resource** | 3 | `{RESOURCE_SANDBOX}/` = context scan only; implement from `docs/` only — **including** `backend/`, `tests/testutils/`, adapter harness |
| **Implement provenance** | 3 | Worker reports `generated` \| `partial-resource-copy` \| `resource-copy`; master **byte-hash + line-overlap** gate (T030b) — not worker self-report alone |
| **Provenance gate (run 019+)** | 3 | Master T030b: per-file SHA256 + substantive-line overlap %; ≥50% overlap or byte-identical on any key Go file → **provenance fail** |
| **Speckit procedure mandatory (run 4+)** | 3 | Worker runs specify → plan → tasks → implement via `{SPECKIT_PROCEDURES_ROOT}` + setup scripts; native slash when supported; **no simulation**; master T030c artifact gate |
| **Speckit init aligns worker (run 7+)** | 3 | `{SPECIFY_INIT_AI}` matches `{WORKER_RUNTIME}` — kiro → `.kiro/prompts/` + `/speckit.*`; cursor → `.cursor/skills/` + `/speckit-*` |

### Provenance labels (Phase 3 master verdict)

| Label | When | Pipeline verdict |
|-------|------|------------------|
| **generated** | All key Go files &lt;15% substantive-line overlap vs `{RESOURCE_SANDBOX}/`; no resource reads during implement | **Pass** (if structure/pattern conform) |
| **partial-resource-copy** | Any key file 15–49% overlap, or transcription in `backend/` / `tests/testutils/` without byte-match | **Fail** — skill violation |
| **resource-copy** | Byte-identical **or** ≥50% substantive-line overlap on any key Go file | **Fail** — skill violation |
