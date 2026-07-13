---
title: วิเคราะห์ใบเสนอราคา v2 บ้านสวนธรรมรัตน์
type: planning
detail: Master — เปรียบเทียบ quotation v1/v2 แล้วเทียบ v2 กับราคากลาง (plan-2 + summary.html)
tags: [master, quotation, v2, benchmark, comparison, ban-suan-thammarat]
role: master
parent: null
master_nnn: "012"
created: 2026-07-13
updated: 2026-07-13
---

# วิเคราะห์ใบเสนอราคา v2 บ้านสวนธรรมรัตน์

> Template: [master-task/skeleton](../task/template/master-task/skeleton.md)

Related:
- [007-analyze-landscaping-quotation](archive/2026-06-26/007-analyze-landscaping-quotation.md) — วิเคราะห์ v1 เดิม
- [011-southern-benchmark-pricing](011-southern-benchmark-pricing.md) — ราคากลางภาคใต้
- [quotation.pdf](../resources/quotation/quotation.pdf) — v1 (20/06/2569)
- [quotation-v2.pdf](../resources/quotation/quotation-v2.pdf) — v2 (12/07/2569)
- [summary.html](../resources/quotation/summary.html) — ราคากลาง + พื้นที่ plan-2
- [task/index.md](index.md) · [task/log.md](log.md)

## Task Requirement

### Goal

รับใบเสนอราคา **ฉบับใหม่ (v2)** จากบ้านสวนธรรมรัตน์ แล้ว (1) เปรียบเทียบกับ v1 โดยคำนึงถึงการ clarify หญ้า 10→100 ตร.ม. ใน v1 (2) เทียบ v2 กับราคากลางและพื้นที่ plan-2 เพื่อสรุปความสมเหตุสมผลก่อนตัดสินใจมัดจำ

### In scope

- ดึงรายการ/จำนวน/ราคา/เงื่อนไขจาก `quotation-v2.pdf` และเทียบกับ `quotation.pdf`
- บันทึกการเปลี่ยนแปลง: พื้นที่, รายการใหม่, สเปกคอนกรีต, ค่าเดินทาง/บริการ, โครงสร้างมัดจำ
- เทียบ v2 กับราคากลางใน [summary.html](../resources/quotation/summary.html) (ทั่วประเทศ + ภาคใต้) และพื้นที่ plan-2
- สร้างรายงาน HTML หรืออัปเดต `qt-v2/` ถ้า checklist กำหนด

### Out of scope

- ต่อรองหรือสั่งจ้างแทนลูกค้า
- แก้ไข PDF ต้นฉบับของผู้รับเหมา
- งานออกแบบภาพจัดสวน

### Acceptance criteria (master-level)

- [x] Sub-task 01 (v1 vs v2) เสร็จ — มีตาราง diff และสรุปความเสี่ยง
- [x] Sub-task 02 (v2 vs benchmark) เสร็จ — มีตารางเทียบราคากลาง + plan-2
- [x] อัปเดต `summary.html` §4b และ `qt-v2/comparison.html`

### Context จาก PDF (draft — รอ validate ใน sub-task 01)

| รายการ | v1 (PDF) | v1 แก้หญ้า | v2 (12/07/2569) |
|--------|----------|------------|-----------------|
| หญ้า | 10 ตร.ม. / 15,750 | **100** @ 157.5 | หญ้านวลน้อย **197** / 29,550 |
| หินเกล็ดดำ | 210 / 63,000 | เหมือน PDF | **111** / 33,300 |
| ปูพื้นภายนอก | 34 / 51,000 | เหมือน PDF | 34 / 51,000 |
| คอนกรีต | 54 / 40,500 | เหมือน PDF | **129** / 96,750 (+สเปก wire mesh 4mm, หนา 15cm, 240) |
| แผ่นทางเดินทรายล้าง | 34 / 8,500 | เหมือน PDF | 34 / 8,500 |
| รายการใหม่ | — | — | ซัมโน้นดำ 13.5 / 3,375 · ค่าบริการ 6,000 |
| รวม | **178,750** | — | **228,475** |
| มัดจำ | 89,375 / 89,375 | — | **100,000** / 128,475 |

## Children

| NN | Slug | Type | Status | Template / note |
|----|------|------|--------|-----------------|
| 01 | [012-01-sub-task-compare-v1-v2](012-01-sub-task-compare-v1-v2.md) | planning | done | เปรียบเทียบ v1 vs v2 |
| 02 | [012-02-sub-task-v2-benchmark](012-02-sub-task-v2-benchmark.md) | execution | done | v2 vs ราคากลาง + plan-2 |

## Activity

### [2026-07-13 11:25] executed | 012-master-task-quotation-v2-analysis
- completed: sub-task 01 + 02
- note: v2 228,475 vs กลาง 146,610 (+56%); สรุป qt-v2 + summary §4b

### [2026-07-13 09:55] created | system
- note: Master 012 — รับ quotation-v2.pdf จากบ้านสวนธรรมรัตน์; spawn sub-task 01 แล้ว 02
