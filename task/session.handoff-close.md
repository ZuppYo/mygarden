---
title: "Handoff — วิเคราะห์ใบเสนอ v2 เสร็จ รอต่อรองผู้รับเหมา"
type: handoff
detail: task 012 done; qt-v2 deliverables; รอคำตอบคอนกรีต 12cm / overlay / มัดจำ
tags: [handoff, quotation, v2]
created: 2026-07-13
updated: 2026-07-13
---

# Handoff — ใบเสนอ v2 บ้านสวนธรรมรัตน์

**Status:** 4 active task(s) · ทุกรายการ `done` · งานถัดไป = ต่อรอง/รอคำตอบผู้รับเหมา (ไม่มี task เปิด)

---

## Reload chain

Start at [`AGENTS.md`](../AGENTS.md) § Reload pack (canonical `@` list). This file is step 2 when Continuity § Reload points here. Playbook: [iom-todo-handoff reference](../.agents/skills/iom-todo-handoff/reference.md#reload-playbook).

---

## One-line summary

วิเคราะห์ quotation v2 (228,475) เทียบ v1 และราคากลางเสร็จแล้ว — รอคำตอบบริษัทเรื่องคอนกรีต 12 cm, overlay พื้นที่, และมัดจำ 100,000 ก่อนตัดสินใจ.

---

## Session outcomes (2026-07-13)

### Deliverables

| ไฟล์ | เนื้อหา |
|------|---------|
| [qt-v2/comparison-v1-v2.html](../resources/quotation/qt-v2/comparison-v1-v2.html) | diff v1 → v2 |
| [qt-v2/comparison.html](../resources/quotation/qt-v2/comparison.html) | v2 vs ราคากลาง |
| [qt-v2/contractor-message.md](../resources/quotation/qt-v2/contractor-message.md) | ข้อความถามผู้รับเหมา |
| [summary.html](../resources/quotation/summary.html) §4b–4d | สรุป v2, SCG ปูพื้น, ขอบกั้นดิน |
| [qt-v2/scg-paving-reference.jpg](../resources/quotation/qt-v2/scg-paving-reference.jpg) | รูปปูพื้น SCG จริง |
| [qt-v2/edge-block-reference.jpg](../resources/quotation/qt-v2/edge-block-reference.jpg) | รูปขอบกั้นดินบล็อกซีเมน |

### ตัวเลขสำคัญ

| ฉบับ | ยอด | หมายเหตุ |
|------|-----|----------|
| v1 แก้หญ้า 100 ตร.ม. | 178,750 | PDF หญ้า 10 ผิด |
| v2 จริง | **228,475** | มัดจำ 100,000 |
| v1 หน่วย + พื้นที่ 197/111/129 + ขอบกั้นดิน | ~223,953 | ไม่รวมแม็คโคร 6,000 |
| กลาง × plan-2 (4 รายการ) | 121,266 | ฐานต่อรอง |

### ชี้แจงบริษัท (ยืนยันแล้ว)

- **คอนกรีต 129 ตร.ม.** — v1 แค่ทางลาด 54 · v2 รวมถนนเชื่อม = โซนเทาแผน (~102 ตร.ม. แต่ v2 ระบุ 129)
- **ขอบกั้นดิน 3,375** — บล็อกซีเมน 13.5 × 250 (น่าจะเป็น **เมตร** ไม่ใช่ ตร.ม.) · v1 ลืมใส่
- **ค่าบริการ 6,000** = แม็คโครปรับพื้นที่ · v1 ลืมใส่
- **ปูพื้น 1,500/ตร.ม.** — สมเหตุสมผลถ้า SCG UVT ติดตั้งครบ (ต่ำกว่า SCG Home 1,890)

### คุยเพิ่มในแชท (ยังไม่มีคำตอบบริษัท)

- คอนกรีต **15 → 12 cm** (mesh เดิม) — Mazda 3 หลัก / กระบะอนาคต → ประมาณลด **~10,000–19,000** (ยอดรวม ~209k–215k)
- หิน 111 vs แผน 83.7 — ยังไม่ชี้แจง
- มัดจำ 100,000 ไม่คืน — ยังเสี่ยงหลัก

---

## Active tasks

### 011-southern-benchmark-pricing — สำรวจราคากลางภาคใต้

- **Status:** done · **Updated:** 2026-07-06
- **Goal:** ราคากลางภาคใต้เทียบ summary.html
- **Pending:** none
- **Next:** archive optional (`iom-todo-task-archive`)

### 012-master-task-quotation-v2-analysis — วิเคราะห์ใบเสนอ v2

- **Status:** done · **Updated:** 2026-07-13
- **Goal:** v1/v2 + v2 vs ราคากลาง
- **Pending:** none (sub-task 01+02 done)
- **Next:** archive optional หลังได้คำตอบบริษัทหรือต่อรองเสร็จ

### 012-01-sub-task-compare-v1-v2

- **Status:** done · **Pending:** none

### 012-02-sub-task-v2-benchmark

- **Status:** done · **Pending:** none · อัปเดต SCG/ขอบกั้นดิน 13/07

---

## Next session

1. `@AGENTS.md` → § Reload pack + Continuity
2. อ่าน [contractor-message.md](../resources/quotation/qt-v2/contractor-message.md) — ส่ง/ติดตามคำตอบบริษัท
3. เมื่อได้ราคาคอนกรีต 12 cm → อัปเดต comparison + summary
4. Optional: archive task 011, 012 (`iom-todo-task-archive`)
5. Optional: sync หญ้า 157.5/100 ตร.ม. → `benchmark-quotation.html`, `qt-v1/*` (ค้างจาก snapshot เก่า)
