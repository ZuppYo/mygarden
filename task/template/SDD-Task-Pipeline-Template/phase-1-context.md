---
title: "iom-sdd pipeline Phase 1 — iom-sdd-context ({RUN_SLUG})"
type: execution
detail: "Phase 1: master/worker test iom-sdd-context on {RESOURCE_SANDBOX}"
tags: [iom-sdd, pipeline, master-worker, iom-sdd-context, template, execution]
created: {CREATED}
updated: {UPDATED}
---

# iom-sdd pipeline Phase 1 — `iom-sdd-context`

> Template: [SDD-Task-Pipeline-Template](./README.md) · Phase 1 of 3

Related: [iom-sdd-context SKILL](../../../.agents/skills/iom-sdd-context/SKILL.md) · [PORTABILITY](../../../.agents/skills/iom-sdd-context/references/PORTABILITY.md) · sandbox `{RESOURCE_SANDBOX}/`

## Task Requirement

### เป้าหมาย

ทดสอบ skill **`iom-sdd-context`** แบบ **master** + **worker** — สร้าง `docs/project-context*` + binding ใน sandbox

### ข้อกำหนด

| Rule | ค่า (แก้ตอน instantiate) |
|------|---------------------------|
| Roles | **master** (`{MASTER_RUNTIME}`) · **worker** (`{WORKER_RUNTIME}`) |
| Dispatch | `{DISPATCH_METHOD}` — see [dispatch-profiles.md](./dispatch-profiles.md) |
| Handoff | `WORKER_HANDOFF.md` + `DISPATCH.json` ก่อน start worker **ทุกครั้ง** |
| Sandbox (scan source) | `{RESOURCE_SANDBOX}` — **context only**; Speckit implement ห้าม copy จาก path นี้ |
| Junction (ถ้ามี) | `{JUNCTION_TARGET}` |
| Basename | `{BASENAME}` |
| Skill install | `{RESOURCE_SANDBOX}/.agents/skills/iom-sdd-context/` |

### ลำดับงาน

1. **master** — prepare `.agents/skills/iom-sdd-context` ใน sandbox
2. **master** — `WORKER_HANDOFF.md` + `DISPATCH.json` + dispatch worker per `{DISPATCH_METHOD}`
3. **worker** — รัน `iom-sdd-context` (read-only scan; write เฉพาะ `docs/`)
4. **master** — verify `docs/project-context/` และ/หรือ `docs/project-context-{BASENAME}/` + `docs/specs/{BASENAME}/GV.binding.md`

### Workspace

| Path | บทบาท |
|------|--------|
| `{RESOURCE_SANDBOX}/` | Scan target + workspace root |
| `{RESOURCE_SANDBOX}/.agents/skills/iom-sdd-context/` | Skill copy |
| `{RESOURCE_SANDBOX}/docs/project-context*/` | Output ที่ master verify |

### Master → Worker dispatch

Portable contract: [dispatch-profiles.md](./dispatch-profiles.md) — profile **`{DISPATCH_METHOD}`**, `cwd` = `{RESOURCE_SANDBOX}/`.

```text
1. Write {RESOURCE_SANDBOX}/WORKER_HANDOFF.md + DISPATCH.json (phase: 1)
2. Dispatch per {DISPATCH_METHOD}:
   - cursor-task-tool — Cursor Task tool when {MASTER_RUNTIME} = {WORKER_RUNTIME} = cursor
   - async-handoff — separate worker session when runtimes differ
3. Worker writes WORKER_REPORT.md; master verifies before [x]
```

### Out of scope

- `iom-sdd-spec`, `iom-sdd-init`, Speckit (Phase 2–3)
- แก้ source นอก `docs/` โดยไม่ยืนยัน

## Pre-flight (confirm before `go`)

| # | Check |
|---|--------|
| P1 | Sandbox path มีอยู่ / junction ถูกต้อง |
| P2 | มี source พร้อม scan (`service/`, `backend/`, …) |
| P3 | Master can dispatch per `{DISPATCH_METHOD}` (see dispatch-profiles) |
| P4 | User ยืนยัน **`go`** |

---

## Checklist — Phase A (master — environment)

- [ ] T001 [N] Pre-flight P1–P4 confirmed
- [ ] T002 [N] **master:** ตรวจ sandbox — baseline บันทึก (ไม่แก้ source นอก `docs/`)
- [ ] T003 [N] **master:** copy `iom-sdd-context` → `{RESOURCE_SANDBOX}/.agents/skills/iom-sdd-context/` (SKILL.md, references/, assets/, scripts/)
- [ ] T004 [N] **master:** handoff ระบุ skill path ชัดเจน

## Checklist — Phase B (master — handoff + dispatch)

- [ ] T010 [N] **master:** เขียน `{RESOURCE_SANDBOX}/WORKER_HANDOFF.md` — binding-only + `go` defaults, expected outputs
- [ ] T011 [N] **master:** write `DISPATCH.json`; **dispatch** worker per `{DISPATCH_METHOD}`

## Checklist — Phase C (worker — run skill)

- [ ] T020 [N] **worker:** รัน `iom-sdd-context` ตาม handoff (`--mode=binding-only` unless overridden)
- [ ] T021 [N] **worker:** report — manifest, binding, bundle paths, validators, blockers

## Checklist — Phase D (master — verify + closeout)

- [ ] T030 [N] **master:** verify `docs/project-context*` + `docs/specs/{BASENAME}/GV.binding.md` + `scan-manifest.json`
- [ ] T031 [N] **master:** validators exit 0 (`validate_scan_manifest.py`, `validate_binding.py`, `validate-binding.ps1`)
- [ ] T032 [N] Append `task/log.md`; update `task/index.md` → **done** when DoD ครบ

## Definition of done

- [ ] `.agents/skills/iom-sdd-context` ใน sandbox ก่อน dispatch
- [ ] handoff + `DISPATCH.json` + dispatch per profile
- [ ] worker รัน skill สำเร็จ
- [ ] `docs/project-context*` ใน sandbox
- [ ] ไม่มี `[x]` โดยไม่มี dispatch / override บันทึก

## Next phase

→ Instantiate [phase-2-spec.md](./phase-2-spec.md) after Phase 1 **done** (`{PRIOR_PHASE_1}` = this task slug).
