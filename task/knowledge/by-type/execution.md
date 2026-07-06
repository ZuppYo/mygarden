---
title: "Requirements — execution tasks"
type: knowledge
detail: "Guidance for type: execution"
last_refresh: 2026-07-06
---

# Execution task guidance

## Should do

- **Goal:** concrete deliverable path(s) — file names and folders explicit in Requirement.
- Reference upstream **planning task** or `design/WORKFLOW.md` for pipeline steps (do not re-debate design).
- Checklist items map 1:1 to verifiable outputs (generated PNG, HTML file, script command run).
- Preserve originals: backup to `resources/backup/` before overwriting designed assets.
- Run full pipeline end-to-end for affected views (place guide → blend → composite-foreground → reset-hidden).
- For quotations: state **Constraints** when prior versions are frozen ("new file only", dedicated folder).
- Include comparison/summary section in HTML deliverables; cite price sources when benchmarks are user-facing.
- Document numeric outputs in task body or Output section (totals, areas, differences).

## Should not do

- Edit files listed as frozen in upstream task (v1 benchmark when v2 is required).
- Skip visibility/occlusion steps to save time — causes wrong tree in occluded views.
- Use `generate_image` alone for 3D render plant placement.
- Assume PDF quantities are correct without flagging anomalies (grass line item pattern from 007).

## Typical In scope

- Script commands (`place`, `composite-foreground`, `reset-hidden`).
- HTML quotation files under `resources/quotation/`.
- Updates to `outline/home.html` viewpoint mappings.
- Area calculations with formulas recorded in markdown or HTML.

## Typical Out of scope

- Negotiating with vendor; paying deposits.
- Changing placement coordinates unless task explicitly allows retuning anchors.
- Non-gardening or physical construction work.

## Gate checks (execution)

| Check | Severity |
|-------|----------|
| Goal + deliverable paths | Warn if paths vague |
| Out of scope ≥ 2 bullets | Warn |
| Frozen-file constraint stated when iterating quotation | Warn if missing |
| Pipeline steps match AGENTS non-negotiables | Warn |

## Examples from archive

- **003:** Backup → generate 2 views → update home.html (exposed gaps fixed in 004–006).
- **005:** `--guide-dir` guides → generative blend all 5 visibility views → copy to resources.
- **008:** Benchmark HTML same line items as PDF; comparison table inline.
- **009:** `benchmark-quotation-v2.html` only — v1 untouched.
- **010:** All new files in `qt-v1/` — benchmark + vendor + comparison + area-breakdown.
