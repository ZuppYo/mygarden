---
title: "Requirements — planning tasks"
type: knowledge
detail: "Guidance for type: planning"
last_refresh: 2026-07-06
---

# Planning task guidance

## Should do

- **Goal:** one research or design outcome that unblocks execution (workflow doc, analysis report, UI spec).
- Document **problems from prior task** with root-cause table when improving an existing workflow.
- Include **research synthesis** (web findings, industry patterns) with explicit *adaptation* to this repo's toolchain.
- Propose target-state workflow diagram or numbered pipeline before checklist items.
- List **affected files** (`design/*.json`, `outline/home.html`, SKILL, AGENTS) in In scope.
- Split large scope into follow-on **execution** task when implementation is substantial (004→005 pattern).

## Should not do

- Leave implementation details only in chat — capture in `design/WORKFLOW.md` or task body for handoff.
- Scope ML training, NeRF, or full 3D mesh reconstruction when lightweight manual tools suffice.
- Plan text-only generative placement — always reference placement registry + hybrid pipeline.

## Typical In scope

- Web research and documented recommendations.
- Schema design (`placements.json`, `occluders.json`, visibility rules).
- UX placement in existing pages (header toolbar, new tabs).
- Analysis reports (quotation risk, PDF tool recommendations, contractor questions).

## Typical Out of scope

- Regenerating all designed PNGs (defer to execution task).
- Vendor negotiation, deposits, physical work.
- Modifying frozen deliverables from prior tasks.

## Gate checks (planning)

| Check | Severity |
|-------|----------|
| Goal present | Warn if missing |
| Out of scope ≥ 2 bullets | Warn |
| Prior task gaps referenced | Warn if improvement without root cause |
| Open questions → Decisions or T001 ask-user | Warn |

## Examples from archive

- **004:** Research → `design/WORKFLOW.md` + placement schema + visibility matrix.
- **006:** UX + occlusion schema before regenerating blends.
- **007:** PDF extract validation + market benchmarks + contractor checklist (no HTML deliverable required).
