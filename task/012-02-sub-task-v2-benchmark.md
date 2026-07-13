---
title: เปรียบเทียบ v2 กับราคากลาง
type: execution
detail: Sub-task 02 · master: วิเคราะห์ใบเสนอราคา v2 บ้านสวนธรรมรัตน์
tags: [sub-task, quotation, v2, benchmark, plan-2, comparison, html]
role: child
parent: 012-master-task-quotation-v2-analysis
master_nnn: "012"
sub_nn: "02"
created: 2026-07-13
updated: 2026-07-13
---

# เปรียบเทียบ v2 กับราคากลาง

> **Parent master:** [วิเคราะห์ใบเสนอราคา v2 บ้านสวนธรรมรัตน์](./012-master-task-quotation-v2-analysis.md) · family `012` · sub-task `02`

Related:
- [comparison.html](../resources/quotation/qt-v2/comparison.html)
- [summary.html](../resources/quotation/summary.html) — §4b
- [012-01-sub-task-compare-v1-v2](./012-01-sub-task-compare-v1-v2.md)

## Checklist

- [x] T001 [U] อ่านผลจาก sub-task 01
  - ✅ ใช้ตัวเลข v2 validate แล้ว
- [x] T002 [N] v2 ราคา/หน่วย vs ราคากลาง
  - ✅ หินตรงกลาง · หญ้า +25% · ปู +100% · คอนกรีตสูง (สเปก 15cm) · แผ่น +39%
- [x] T003 [N] กลาง × จำนวน v2 vs v2
  - ✅ กลาง 146,610 vs v2 219,100 (5 รายการ) = +72,490 (+49%)
- [x] T004 [N] กลาง × plan-2 vs v2×แผน
  - ✅ กลาง 121,266 vs v2×แผน 186,105 (4 รายการ) = +64,839 (+53%)
- [x] T005 [N] รายการใหม่
  - ✅ ซัมโน้นดำ 250/ตร.ม. เทียบแผ่นทางเดินได้ · ค่าบริการ 6,000 ควรอยู่ในเหมาเดิมหรือแจกแจง
- [x] T006 [N] HTML + summary.html
  - ✅ qt-v2/comparison.html · summary.html §4b
- [x] T007 [N] สรุปภาษาไทย
  - ✅ § Results ด้านล่าง

## Results

**วันที่วิเคราะห์:** 13/07/2569

### สรุป: v2 สมเหตุสมผลแค่ไหน?

**ปานกลาง–สูง** — ดีขึ้นจาก v1 เรื่องความชัดของพื้นที่หญ้าและสเปกคอนกรีต แต่ **ยอดรวมยังสูงกว่าราคากลางมาก** โดยเฉพาะปูพื้น 1,500/ตร.ม.

| ฐานเปรียบเทียบ | ยอด | ส่วนต่างจาก v2 |
|----------------|-----|----------------|
| ราคากลาง × plan-2 (4 รายการ) | 121,266 | v2 สูงกว่า ~88% ถ้าใช้จำนวน v2 ทั้งหมด |
| ราคากลาง × จำนวน v2 (5 รายการ) | 146,610 | **+81,865 (+56%)** |
| v2 หน่วย × plan-2 (4 รายการ) | 186,105 | +42,370 จากกลาง×แผน |
| **v2 รวม** | **228,475** | — |

### รายการที่สมเหตุสมผล / ควรคุย

| รายการ | ประเมิน |
|--------|---------|
| หิน 300/ตร.ม. | สอดคล้องกลาง |
| หญ้า 150/ตร.ม. | สูงกว่ากลาง 25% แต่อยู่ในช่วงตลาด 80–150 |
| คอนกรีต 750 (15 cm) | ถ้าเทียบกลาง 10 cm แพงมาก — ปรับ ~675 ยังสูง ~11% |
| ปูพื้น 1,500 | สมเหตุสมผลถ้าเป็น **SCG UVT ติดตั้งครบ** แบบรูปงานจริง (ต่ำกว่า SCG Home 1,890) — ดู [contractor-message.md](../resources/quotation/qt-v2/contractor-message.md) |
| ซัมโน้นดำ + ค่าบริการ | ควรรวมใน scope หรือแยกชัด |

### คำแนะนำมัดจำ

- **อย่าจ่าย 100,000 บาท** จน overlay แผน + ได้สเปกปูพื้น + แจกแจงค่าบริการ
- **เป้าหมายต่อรอง:** กลาง × plan-2 ≈ **121,266** (+ แผ่นทางเดิน/ซัมโน้นตามจริง) ≈ **127,000–135,000** เป็นฐานคุย
- ขอมัดจำแบบ milestone หรือ ≤50% ของยอดที่ตกลงหลังปรับพื้นที่

### อัปเดตปูพื้น SCG (13/07/2569)

รูปงานติดตั้งจริงยืนยันสเปกใกล้ **SCG UVT ลายคอบเบิล** — ราคา **1,500/ตร.ม.** สมเหตุสมผลถ้ารวมติดตั้งครบ (ต่ำกว่า [SCG Home 1,890](https://www.scghome.com/promotions/pave)) · ร่างข้อความถามผู้รับเหมาแล้วที่ `qt-v2/contractor-message.md`

### Deliverables

| Output | Path |
|--------|------|
| v1 vs v2 | [qt-v2/comparison-v1-v2.html](../resources/quotation/qt-v2/comparison-v1-v2.html) |
| v2 vs กลาง | [qt-v2/comparison.html](../resources/quotation/qt-v2/comparison.html) |
| ข้อความถามผู้รับเหมา | [qt-v2/contractor-message.md](../resources/quotation/qt-v2/contractor-message.md) |
| รูปงานปูพื้น SCG จริง | [qt-v2/scg-paving-reference.jpg](../resources/quotation/qt-v2/scg-paving-reference.jpg) |
| สรุปใน summary | [summary.html §4b–4c](../resources/quotation/summary.html) |
