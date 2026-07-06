---
title: "iom-sdd pipeline Phase 3 — Speckit SDD ({RUN_SLUG})"
type: execution
detail: "Phase 3: specify init, iom-sdd-init {INIT_AGENT}, Speckit chain, compare src vs resource"
tags: [iom-sdd, pipeline, speckit, iom-sdd-init, template, execution]
created: {CREATED}
updated: {UPDATED}
---

# iom-sdd pipeline Phase 3 — Speckit SDD

> Template: [SDD-Task-Pipeline-Template](./README.md) · Phase 3 of 3 · ต่อจาก `{PRIOR_PHASE_1}` + `{PRIOR_PHASE_2}`

Related: [iom-sdd-init SKILL](../../../.agents/skills/iom-sdd-init/SKILL.md) · [INIT_VERIFY](../../../.agents/skills/iom-sdd-init/references/INIT_VERIFY.md) · queue `src/docs/specs/{QUEUE}.md`

## Task Requirement

### เป้าหมาย

ทดสอบ **Speckit SDD** — `specify init` → `iom-sdd-init {INIT_AGENT}` → Speckit chain → compare `src/` vs `{RESOURCE_SANDBOX}/`

### ข้อกำหนด

| Rule | ค่า (แก้ตอน instantiate) |
|------|---------------------------|
| Prerequisite | `{PRIOR_PHASE_1}` + `{PRIOR_PHASE_2}` **done** |
| Workspace | `src/` · `{SDD_ROOT}` = `src/docs/` |
| Context scan source | `{RESOURCE_SANDBOX}/` — Phase 1 only; **ห้ามแก้** |
| Implement source | `src/docs/` (project-context + specs + binding) — **ห้าม copy จาก `{RESOURCE_SANDBOX}/`** |
| Queue | `{QUEUE}` |
| Init agent | `{INIT_AGENT}` — workspace layout branch (`Cursor`, `Kiro`, `Gemini`, …) |
| Master / worker | `{MASTER_RUNTIME}` / `{WORKER_RUNTIME}` — see [dispatch-profiles.md](./dispatch-profiles.md) |
| Dispatch | `{DISPATCH_METHOD}` |
| Speckit procedures root | `{SPECKIT_PROCEDURES_ROOT}` — from [SPECKIT_INTEGRATION](../../../.agents/skills/iom-sdd-init/references/SPECKIT_INTEGRATION.md) |
| Specify init | `specify init . --force --ai {SPECIFY_INIT_AI}` — **must match `{WORKER_RUNTIME}`** (kiro worker → `--ai kiro`) |
| Speckit invoke | `{SPECKIT_INVOKE_STYLE}` — `dot` (`/speckit.specify`) for Kiro · `hyphen` (`/speckit-specify`) for Cursor |
| Skills | `src/.agents/skills/iom-sdd-init/` + `iom-sdd-spec/` (paired) |

### ลำดับงาน

1. **master** — `specify init . --force --ai {SPECIFY_INIT_AI}` (script type **ps**)
2. **master** — copy init+spec skills → `src/.agents/skills/` + handoff + `DISPATCH.json` + dispatch
3. **worker** — `iom-sdd-init {INIT_AGENT}` + INIT_VERIFY (≤3 retries)
4. **worker** — Speckit chain via `{SPECKIT_PROCEDURES_ROOT}` (specify → plan → tasks → implement) — native slash or read procedure files
5. **master** — compare + `{COMPARE_ARTIFACT}`

### Speckit chain — **mandatory procedure**

Worker **MUST** execute the Speckit chain using procedures under **`{SPECKIT_PROCEDURES_ROOT}`** — **one step at a time**, in order. See [SPECKIT_INTEGRATION](../../../.agents/skills/iom-sdd-init/references/SPECKIT_INTEGRATION.md).

| Order | Step | Kiro (`--ai kiro`) | Cursor (`--ai cursor-agent`) |
|-------|------|--------------------|------------------------------|
| 1 | specify | `{SPECKIT_PROCEDURES_ROOT}/speckit.specify.md` · `/speckit.specify` | `…/speckit-specify/SKILL.md` · `/speckit-specify` |
| 2 | plan | `speckit.plan.md` · `/speckit.plan` | `speckit-plan/SKILL.md` · `/speckit-plan` |
| 3 | tasks | `speckit.tasks.md` · `/speckit.tasks` | `speckit-tasks/SKILL.md` · `/speckit-tasks` |
| 4 | implement | `speckit.implement.md` · `/speckit.implement` | `speckit-implement/SKILL.md` · `/speckit-implement` |

**Resolver:** `{WORKER_RUNTIME}` = `kiro-cli` → `{SPECIFY_INIT_AI}` = `kiro`, `{SPECKIT_PROCEDURES_ROOT}` = `.kiro/prompts/`. `{WORKER_RUNTIME}` = `cursor` → `cursor-agent`, `.cursor/skills/`.

**Anti-pattern:** kiro worker + `specify init --ai cursor-agent` (run-6) — procedures in `.cursor/skills/` with no Kiro native slash.

**Specify prompt:** *Create project spec by read requirement from `@docs/specs/{QUEUE}.md` and `@docs/specs/{BASENAME}/GV.binding.md`*

### Hard rule — Speckit procedure (no simulation)

| Rule | Detail |
|------|--------|
| **Execute procedures** | Native slash (`{SPECKIT_INVOKE_STYLE}`) **or** read each procedure file under `{SPECKIT_PROCEDURES_ROOT}` **end-to-end** — including setup scripts (`create-new-feature.ps1`, `setup-plan.ps1`, `setup-tasks.ps1`, `check-prerequisites.ps1`) |
| **Forbidden** | “Simulate”, “equivalent to”, hand-write `spec.md`/`plan.md`/`tasks.md`, skip setup scripts, or implement Go **before** speckit-implement completes |
| **Master dispatch** | Handoff + dispatch profile **must not** say simulate — only `WORKER_HANDOFF.md` + Speckit skill procedures |
| **Mark `[x]`** | T021–T024 only when worker report includes **setup-script exit codes** + **required artifacts** (below) |
| **Override** | If Speckit cannot run (no procedures under `{SPECKIT_PROCEDURES_ROOT}` for chosen `--ai`), master records `⚠️` + reason in task — **do not** silently substitute manual implement |

**Required artifacts after Speckit chain (worker report + master T030c):**

| After step | Must exist |
|------------|------------|
| speckit-specify | `.specify/feature.json` · `specs/<feature>/spec.md` · `specs/<feature>/checklists/requirements.md` |
| speckit-plan | `plan.md` · `research.md` · `data-model.md` · `contracts/` · `quickstart.md` |
| speckit-tasks | `tasks.md` (format `[ID] [P?] [Story]` per `.specify/templates/tasks-template.md`) |
| speckit-implement | Go tree per `tasks.md`; worker ran `check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` before implement |

### Master → Worker dispatch

Portable contract: [dispatch-profiles.md](./dispatch-profiles.md) — profile **`{DISPATCH_METHOD}`**, `cwd` = `src/`.

```text
1. Write src/WORKER_HANDOFF.md + DISPATCH.json (phase: 3, init_agent: {INIT_AGENT})
2. Dispatch per {DISPATCH_METHOD}
3. Worker: INIT_VERIFY + Speckit via {SPECKIT_PROCEDURES_ROOT} (native slash or procedure files; no simulation)
4. Worker writes WORKER_REPORT.md; master runs T030b/T030c before [x]
```

### Hard rule — `src/resource/` (context only)

| Phase | `{RESOURCE_SANDBOX}/` |
|-------|------------------------|
| 1 | `iom-sdd-context` scan → `docs/project-context*` |
| 3 worker | **ห้าม** read / attach / copy / transcribe Go จาก resource — **รวม** `backend/`, `tests/testutils/`, adapter harness |
| 3 master | compare-only (structure, parity, baseline `go test`, byte-hash + line-overlap gate) |

Speckit implement ต้อง **generate** จาก `docs/` + `AGENTS.md` เท่านั้น — byte-identical, transcription, หรือ overlap สูงกับ resource = **provenance fail** (ดู rubric ด้านล่าง)

### Pre-clean (master — Phase A, before `specify init`)

**ห้าม** bulk-delete ไฟล์ FM template ที่ git track ไว้ — ใช้ **git discard** แทน

| Action | Allowed |
|--------|---------|
| Restore template | `git restore .` ใน `src/` **หรือ** `git restore` รายการใน [FM_TEMPLATE_MANIFEST.md](../../../src/FM_TEMPLATE_MANIFEST.md) |
| Remove pipeline artifacts | ลบเฉพาะ untracked/ generated (`.specify/`, `.kiro/`, `specs/`, `AGENTS.md`, handoff) เมื่อ user ยืนยัน |
| **Forbidden** | `Remove-Item -Recurse` บน `service/`, `tests/`, `version/`, `main.go` เพื่อ “clean workspace” |

คงไว้เสมอ: `{RESOURCE_SANDBOX}/`, `src/docs/` (หลัง Ph2) — ลบ docs เฉพาะเมื่อ rerun Ph1–2

### Out of scope

- แก้ `{RESOURCE_SANDBOX}/`
- Worker ใช้ resource เป็นแหล่ง implement
- Rerun Phase 1–2 (unless user clears `src/docs/`)

## Pre-flight (confirm before `go`)

| # | Check |
|---|--------|
| P1 | `{PRIOR_PHASE_1}` + `{PRIOR_PHASE_2}` done |
| P2 | `src/docs/project-context/` + `src/docs/specs/{QUEUE}.md` |
| P3 | `specify` CLI; `PYTHONUTF8=1` on Windows |
| P4 | `src/` reset per [FM template manifest](../../../src/FM_TEMPLATE_MANIFEST.md) — **`git restore`** protected scaffold; **ห้ามลบ** `main.go`, `service/`, `tests/`, `version/`, `.gitignore`, `go.sum` |
| P5 | Master can dispatch per `{DISPATCH_METHOD}`; `{SPECIFY_INIT_AI}` matches `{WORKER_RUNTIME}`; `{SPECKIT_PROCEDURES_ROOT}` exists after init |
| P6 | User ยืนยัน **`go`** |

---

## Checklist — Phase A (master — Speckit init)

- [ ] T001 [N] Pre-flight P1–P6 confirmed
- [ ] T002 [N] **master:** verify `src/docs/` — context + queue spec + binding
- [ ] T003 [N] **master:** `PYTHONUTF8=1`; `specify init . --force --ai {SPECIFY_INIT_AI}` in `src/` — script **ps**
- [ ] T004 [N] **master:** verify `.specify/` + `{SPECKIT_PROCEDURES_ROOT}` per [SPECKIT_INTEGRATION](../../../.agents/skills/iom-sdd-init/references/SPECKIT_INTEGRATION.md) + agent folder per `{INIT_AGENT}` (`.kiro/steering/` for Kiro init)

## Checklist — Phase B (master — skills + handoff)

- [ ] T010 [N] **master:** copy `iom-sdd-init` + `iom-sdd-spec` → `src/.agents/skills/`
- [ ] T011 [N] **master:** `src/WORKER_HANDOFF.md` from [WORKER_HANDOFF.template.md](../../../.agents/skills/iom-sdd-init/assets/WORKER_HANDOFF.template.md) — `{INIT_AGENT}`, `{WORKER_RUNTIME}`, `{DISPATCH_METHOD}`, `{SPECIFY_INIT_AI}`, `{SPECKIT_PROCEDURES_ROOT}`, `{SPECKIT_INVOKE_STYLE}`, Speckit chain, INIT_VERIFY, test infra, provenance
- [ ] T011b [N] **master:** baseline gate — `go test ./tests/...` in `{RESOURCE_SANDBOX}/`; record **baseline exit code** in handoff + compare doc
- [ ] T012 [N] **master:** write `DISPATCH.json`; **dispatch** worker per `{DISPATCH_METHOD}`

## Checklist — Phase C (worker — init + Speckit)

- [ ] T020 [N] **worker:** `iom-sdd-init {INIT_AGENT}` — `AGENTS.md`, constitution, INIT_VERIFY (≤3)
- [ ] T021 [N] **worker:** **speckit-specify** — `/speckit.specify` or `/speckit-specify` per `{SPECKIT_INVOKE_STYLE}`; read procedure file under `{SPECKIT_PROCEDURES_ROOT}`; run `create-new-feature.ps1` if required; prompt from `{SDD_ROOT}specs/{QUEUE}.md` + binding
  - ✅ Artifacts: `.specify/feature.json` · `specs/<feature>/spec.md` · `checklists/requirements.md`
- [ ] T022 [N] **worker:** **speckit-plan** — slash or read `{SPECKIT_PROCEDURES_ROOT}` plan procedure; run `setup-plan.ps1 -Json` first
  - ✅ Artifacts: `plan.md` · `research.md` · `data-model.md` · `contracts/` · `quickstart.md`
- [ ] T023 [N] **worker:** **speckit-tasks** — slash or read `{SPECKIT_PROCEDURES_ROOT}` tasks procedure; run `setup-tasks.ps1 -Json` first
  - ✅ Artifact: `tasks.md` with `[ID] [P?] [Story]` format (not ad-hoc `T001` only)
- [ ] T024 [N] **worker:** **speckit-implement** — slash or read `{SPECKIT_PROCEDURES_ROOT}` implement procedure; run `check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` before implement
  - ✅ Report build/test exit codes + **implement provenance** (`generated` | `partial-resource-copy` | `resource-copy`; ห้ามเปิด `{RESOURCE_SANDBOX}/` ระหว่าง implement — **รวม** `backend/`, `tests/testutils/`)

## Checklist — Phase D (master — compare + closeout)

- [ ] T030 [N] **master:** compare structure `src/` vs `{RESOURCE_SANDBOX}/` (`main.go`, `service/`, `backend/`, `tests/`, `version/`)
- [ ] T030b [N] **master:** **provenance gate** — per key Go file: SHA256 byte-compare + substantive-line overlap % (resource → implement); record table in `{COMPARE_ARTIFACT}`

  Key files (minimum): `main.go`, `service/{active-step}.go`, `service/cons.go`, `service/service.go`, `backend/func.go`, `tests/*_test.go`, `tests/testutils/testutils.go`, `version/version.go`

  ```powershell
  # For each file pair: SHA256 match? + % of resource substantive lines (trim, len>15) found in implement
  ```

- [ ] T031 [N] **master:** compare patterns (protocol, step shape, builders, Success/Fail tests)
- [ ] T032 [N] **master:** conformance `src/docs/project-context*` — gaps → improvement items for `iom-sdd` skills
- [ ] T030c [N] **master:** **Speckit artifact gate** — verify worker ran real Speckit flow (not simulation)

  ```powershell
  # From src/ — all must pass for T021–T024 to count as done
  Test-Path .specify/feature.json
  Test-Path specs/*/checklists/requirements.md
  Test-Path specs/*/contracts
  Test-Path specs/*/quickstart.md
  .\.specify\scripts\powershell\check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
  # AVAILABLE_DOCS should include spec.md, plan.md, tasks.md (+ research, data-model, contracts, quickstart when present)
  ```

  If any missing → record **Speckit flow fail** in `{COMPARE_ARTIFACT}` even when Go build passes.

- [ ] T033 [N] **master:** write `{COMPARE_ARTIFACT}` — baseline vs implement test exit codes, **Speckit artifact gate**, **master provenance verdict** (not worker self-report alone), infra blocker classification
- [ ] T034 [N] `task/log.md` + `task/index.md` → **done**

## Definition of done

- [ ] `.specify/` + agent folder per `{INIT_AGENT}` from init
- [ ] INIT_VERIFY passed (or manual summary after 3 retries)
- [ ] Speckit chain complete via **real** `{SPECKIT_PROCEDURES_ROOT}` procedures (T021–T024 + T030c artifacts)
- [ ] `{COMPARE_ARTIFACT}` with structure + pattern + conformance + Speckit gate + T030b provenance
- [ ] ไม่มี `[x]` โดยไม่มี dispatch / override บันทึก

## Compare rubric (T030–T033)

| Area | Pass hint |
|------|-----------|
| Layout | Match baseline dirs/files for active step |
| Protocol | Per binding `{GV_BACKEND_PROTOCOL}` |
| Tests | Success/Fail counts per binding/manifest |
| Context | No `internal/` helpers; `fm/model/payload`; iOM libs first |
| **Baseline test gate** | Run `go test` in `{RESOURCE_SANDBOX}/` first; record exit code |
| **Test infra** | Implement exit **=** baseline exit → **infra blocker** (Redis LOV, wiremock); **worse** → skill/pipeline fail |
| **Implement provenance** | Master **T030b** byte-hash + line-overlap table; worker self-report is input only |
| **Speckit artifact gate** | Master **T030c** — `.specify/feature.json`, checklists, contracts/, quickstart.md, `check-prerequisites.ps1` AVAILABLE_DOCS; simulation = **Speckit flow fail** |
| Gaps | Each gap → one improvement line (context / spec / init / pipeline) |

### Implement provenance (T024 / T030b / T033)

| Label | When | Verdict |
|-------|------|---------|
| **generated** | All key Go files **&lt;15%** substantive-line overlap vs `{RESOURCE_SANDBOX}/`; worker did not read resource during implement | **Pass** if structure/pattern conform |
| **partial-resource-copy** | Any key file **15–49%** overlap, or evident transcription in `backend/` / `tests/testutils/` | **Fail** — skill violation |
| **resource-copy** | Byte-identical **or** **≥50%** substantive-line overlap on any key Go file | **Fail** — skill violation |

**T030b procedure:** Master runs byte-compare **and** line-overlap on key files **after** worker returns. Do **not** accept worker `generated` label without T030b table. Worker must not read `{RESOURCE_SANDBOX}/` during implement (adapter + test harness included).

## Pipeline complete

All three phases done for run **`{RUN_SLUG}`**. Archive tasks via **`iom-todo-task-archive`** when eligible.
