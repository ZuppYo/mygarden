---
title: คำนวณพื้นที่ plan-2 และสร้าง quotation qt-v1
type: execution
detail: วัดพื้นที่ตามสีจาก plan-2.jpg แล้วสร้างใบเสนอราคา 2 ฉบับ (ราคากลาง vs บริษัท) เก็บใน qt-v1
tags: [quotation, plan-2, area-calculation, benchmark, comparison, html, qt-v1]
created: 2026-07-03
updated: 2026-07-03
---

# คำนวณพื้นที่ plan-2 และสร้าง quotation qt-v1

Related:
- [plan-2.jpg](../resources/quotation/plan-2.jpg)
- [quotation.pdf](../resources/quotation/quotation.pdf)
- [007-analyze-landscaping-quotation](007-analyze-landscaping-quotation.md)
- [008-create-benchmark-landscaping-quotation](008-create-benchmark-landscaping-quotation.md)
- [009-plan-area-benchmark-quotation-v2](009-plan-area-benchmark-quotation-v2.md)
- [benchmark-quotation.html](../resources/quotation/benchmark-quotation.html) *(อ้างอิงราคากลาง v1 — ห้ามแก้ไข)*
- [benchmark-quotation-v2.html](../resources/quotation/benchmark-quotation-v2.html) *(อ้างอิง — ห้ามแก้ไข)*
- Output folder: [qt-v1](../resources/quotation/qt-v1/)
- [task/index.md](index.md)
- [task/log.md](log.md)

## Task Requirement

- Goal: วิเคราะห์พื้นที่จาก [plan-2.jpg](../resources/quotation/plan-2.jpg) ตามโซนสีที่ highlight แล้วคำนวณราคาต่อตารางเมตรเทียบกับราคากลาง โดยจัดทำ **2 ใบเสนอราคา** แยกกัน — (1) ราคากลางตลาด และ (2) ราคาต่อหน่วยจาก [quotation.pdf](../resources/quotation/quotation.pdf) — ใช้พื้นที่ที่คำนวณจากแผนเป็นฐานเดียวกัน แล้วเก็บผลลัพธ์ทั้งหมดใน `resources/quotation/qt-v1/`
- ความหมายสีในแผน:
  - **เขียว** — ปลูกหญ้านวลน้อย
  - **แดง** — หินเกล็ดดำ + รองพื้นด้วยแผ่นกันวัชพืช (พื้นที่สุทธิ = กรอบแดง − footprint ตัวบ้านภายในกรอบ)
  - **เหลือง** — งานปูพื้นภายนอก
  - **เทา** — งานเทคอนกรีตหน้าบ้าน
  - **น้ำเงิน** — โรงจอดรถ (carport)
- In scope: อ่านมิติจากกริด/ตัวเลขบนแผน, คำนวณพื้นที่แต่ละสีพร้อมสูตรและสมมติฐาน, กำหนดราคา/หน่วยจากราคากลาง (อ้างอิง 007/008) และราคาจากใบเสนอจริง (007), สร้าง HTML quotation 2 ไฟล์ + ตารางเปรียบเทียบ + สรุปราคา/ตร.ม. ใน `qt-v1/`
- Out of scope: แก้ไข `quotation.pdf`, `benchmark-quotation.html`, `benchmark-quotation-v2.html`, หรือไฟล์ v1/v2 อื่นๆ; ต่อรองราคากับผู้รับเหมา; สั่งจ้างงานจริง
- Constraints: สร้างไฟล์ใหม่ใน `qt-v1/` เท่านั้น; ห้ามแก้ไข quotation เวอร์ชันก่อนหน้า

## Checklist

- [x] T001 [N] วิเคราะห์ [plan-2.jpg](../resources/quotation/plan-2.jpg) — ยืนยันขอบเขตแต่ละสี (เขียว/แดง/เหลือง/เทา/น้ำเงิน), footprint ตัวบ้านในกรอบแดง, และมิติอ้างอิงจากกริด
  - ✅ แปลง 12.88×42.35 ม.; กรอบแดง 15 ม.; บ้านในกรอบ 109.5 ตร.ม.; carport น้ำเงิน 6.08×6 ม.
- [x] T002 [N] คำนวณพื้นที่ (ตร.ม.) แยกตามสี พร้อมสูตร สมมติฐาน และตารางสรุป (รวมราคา/ตร.ม. ต่อรายการ)
  - ✅ เขียว 177.3, แดง 83.7, เหลือง 38.6, เทา 102.0, น้ำเงิน 36.5 ตร.ม.
- [x] T003 [N] สร้างโฟลเดอร์ `resources/quotation/qt-v1/` และไฟล์สรุปการคำนวณพื้นที่ (เช่น `area-breakdown.md` หรือรวมใน HTML)
  - ✅ สร้าง [area-breakdown.md](../resources/quotation/qt-v1/area-breakdown.md)
- [x] T004 [N] สร้าง `resources/quotation/qt-v1/benchmark-quotation.html` — ใบเสนอราคากลาง ใช้พื้นที่จากแผน × ราคากลาง (007/008) รูปแบบอ่านง่าย พิมพ์ได้
  - ✅ รวม 4 รายการ 121,266 บาท; รวม carport 137,682 บาท
- [x] T005 [N] สร้าง `resources/quotation/qt-v1/vendor-quotation.html` — ใบเสนอราคาตามหน่วยจาก [quotation.pdf](../resources/quotation/quotation.pdf) × พื้นที่จากแผน (รูปแบบเดียวกับ benchmark)
  - ✅ รวม 4 รายการ 438,818 บาท (เทียบ PDF เดิม 178,750 บาท)
- [x] T006 [N] สร้าง `resources/quotation/qt-v1/comparison.html` (หรือรวมในไฟล์ใดไฟล์หนึ่ง) — ตารางเปรียบเทียบ 2 quotation: ราคา/หน่วย, ราคารวม, ส่วนต่าง %, และราคา/ตร.ม. ต่อสี/รายการ
  - ✅ ส่วนต่าง +317,552 บาท (+262%); หญ้าบริษัทสูงกว่ากลาง 13 เท่า/ตร.ม.
- [x] T007 [N] สรุปข้อจำกัดการวัดจากแผน, รายการที่ไม่มีใน PDF (เช่น carport น้ำเงิน), ความคลาดเคลื่อน ±5–10%, และคำแนะนำก่อนใช้ตัวเลขต่อรอง
  - ✅ บันทึกใน comparison.html และ area-breakdown.md

## Output

| ไฟล์ | คำอธิบาย |
|------|----------|
| [qt-v1/benchmark-quotation.html](../resources/quotation/qt-v1/benchmark-quotation.html) | ราคากลาง 121,266 บาท (4 รายการ) |
| [qt-v1/vendor-quotation.html](../resources/quotation/qt-v1/vendor-quotation.html) | หน่วยบริษัท × แผน 438,818 บาท |
| [qt-v1/comparison.html](../resources/quotation/qt-v1/comparison.html) | เปรียบเทียบ +262% |
| [qt-v1/area-breakdown.md](../resources/quotation/qt-v1/area-breakdown.md) | สูตรและตัวเลขพื้นที่ |

- พื้นที่: หญ้า 177.3 | หิน 83.7 | ปูพื้น 38.6 | คอนกรีต 102.0 | carport 36.5 ตร.ม.
- ราคากลางรวม: 137,682 บาท (รวม carport) | มัดจำ 50%: 68,841 บาท
- ราคาบริษัท (แผน): 438,818 บาท | vs PDF เดิม 178,750 บาท
