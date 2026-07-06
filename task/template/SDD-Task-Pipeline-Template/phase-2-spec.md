---
title: "iom-sdd pipeline Phase 2 — iom-sdd-spec ({RUN_SLUG})"
type: execution
detail: "Phase 2: copy context docs to src/, worker runs iom-sdd-spec, verify queue markdown"
tags: [iom-sdd, pipeline, master-worker, iom-sdd-spec, template, execution]
created: {CREATED}
updated: {UPDATED}
---

# iom-sdd pipeline Phase 2 — `iom-sdd-spec`

> Template: [SDD-Task-Pipeline-Template](./README.md) · Phase 2 of 3 · ต่อจาก `{PRIOR_PHASE_1}`

Related: [iom-sdd-spec SKILL](../../../.agents/skills/iom-sdd-spec/SKILL.md) · Phase 1 task `{PRIOR_PHASE_1}` · binding `{RESOURCE_SANDBOX}/docs/specs/{BASENAME}/GV.binding.md`

## Task Requirement

### เป้าหมาย

ทดสอบ **`iom-sdd-spec`** — Confluence → `src/docs/specs/{QUEUE}.md` โดยใช้ context จาก Phase 1

### ข้อกำหนด

| Rule | ค่า (แก้ตอน instantiate) |
|------|---------------------------|
| Prerequisite | `{PRIOR_PHASE_1}` **done** — `{RESOURCE_SANDBOX}/docs/project-context*` |
| Workspace | `src/` (`{SDD_ROOT}` = `src/docs/`) |
| Queue | `{QUEUE}` |
| Confluence | page `{CONFLUENCE_PAGE_ID}` · `{CONFLUENCE_URL}` |
| Skill | `src/.agents/skills/iom-sdd-spec/` |
| Dispatch | `{DISPATCH_METHOD}` — see [dispatch-profiles.md](./dispatch-profiles.md) |

### ลำดับงาน

1. **master** — copy `{RESOURCE_SANDBOX}/docs/` → `src/docs/`
2. **master** — install skill + `src/WORKER_HANDOFF.md` + dispatch
3. **worker** — `iom-sdd-spec` → `docs/specs/{QUEUE}.md`
4. **master** — verify queue markdown + `validate_spec.py --strict`

### Workspace

| Path | บทบาท |
|------|--------|
| `{RESOURCE_SANDBOX}/docs/` | Source จาก Phase 1 |
| `src/docs/` | SDD tree หลัง copy |
| `src/docs/specs/{QUEUE}.md` | Queue spec output |
| `src/resource/` | Baseline code — **ห้ามแก้** |

### Master → Worker dispatch

Portable contract: [dispatch-profiles.md](./dispatch-profiles.md) — profile **`{DISPATCH_METHOD}`**, `cwd` = `src/`.

```text
1. Write src/WORKER_HANDOFF.md + DISPATCH.json (phase: 2)
2. Dispatch per {DISPATCH_METHOD}
3. Worker writes WORKER_REPORT.md; master verifies before [x]
```

### Legacy Confluence pages (no Change History)

When the source page has **no Change History / N·M·D table**:

| Field | Pipeline expectation |
|-------|---------------------|
| **Sync mode** | Implicit **`legacy`** — omit from spec Metadata (per `iom-sdd-spec` rules) |
| **Export scope** | **Full** §1–§14 canonical sync (same as pre-N/M/D behaviour) |
| **Validator** | `validate_spec.py` treats as legacy/full — all sections required |

Document in worker report: `sync mode: legacy (full export)`. Do not expect **Sync mode** metadata row in output markdown.

### Out of scope

- `iom-sdd-init`, Speckit (Phase 3)

## Pre-flight (confirm before `go`)

| # | Check |
|---|--------|
| P1 | `{PRIOR_PHASE_1}` done — project-context ใน sandbox |
| P2 | `src/` พร้อม (incremental หรือล้าง artifacts เก่า — user ยืนยัน) |
| P3 | Confluence MCP **หรือ** fallback + sign-off |
| P4 | Master can dispatch per `{DISPATCH_METHOD}` (see dispatch-profiles) |
| P5 | User ยืนยัน **`go`** |

---

## Checklist — Phase A (master — copy docs)

- [ ] T001 [N] Pre-flight P1–P5 confirmed
- [ ] T002 [N] **master:** copy `{RESOURCE_SANDBOX}/docs/` → `src/docs/`
- [ ] T003 [N] **master:** verify `src/docs/project-context/` + `src/docs/specs/{BASENAME}/GV.binding.md`

## Checklist — Phase B (master — skill + handoff)

- [ ] T010 [N] **master:** copy `iom-sdd-spec` → `src/.agents/skills/iom-sdd-spec/`
- [ ] T011 [N] **master:** `src/WORKER_HANDOFF.md` — Confluence `{CONFLUENCE_PAGE_ID}`, output `docs/specs/{QUEUE}.md`, validators
- [ ] T012 [N] **master:** write `DISPATCH.json`; **dispatch** worker per `{DISPATCH_METHOD}`

## Checklist — Phase C (worker — run skill)

- [ ] T020 [N] **worker:** fetch Confluence → write `docs/specs/{QUEUE}.md`
- [ ] T021 [N] **worker:** `validate_spec.py --strict` (+ `crosscheck_spec_binding.py` if binding exists)

## Checklist — Phase D (master — verify + closeout)

- [ ] T030 [N] **master:** `src/docs/specs/{QUEUE}.md` exists
- [ ] T031 [N] **master:** validator exit **0** (or `⚠️` + reason)
- [ ] T032 [N] `task/log.md` + `task/index.md` → **done**

## Definition of done

- [ ] `src/docs/` มี context จาก Phase 1
- [ ] worker รัน `iom-sdd-spec` สำเร็จ
- [ ] `{QUEUE}.md` ผ่าน strict validation
- [ ] ไม่มี `[x]` โดยไม่มี dispatch / override บันทึก

## Next phase

→ Instantiate [phase-3-speckit.md](./phase-3-speckit.md) after Phase 2 **done** (`{PRIOR_PHASE_2}` = this task slug).
