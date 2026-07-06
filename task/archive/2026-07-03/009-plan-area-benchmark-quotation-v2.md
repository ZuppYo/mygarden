---
title: วิเคราะห์พื้นที่จากแผนบ้านและสร้าง benchmark-quotation v2
type: execution
detail: คำนวณพื้นที่หินเกล็ดดำรอบบ้านในกรอบแดงและพื้นที่ปลูกหญ้าที่เหลือ จาก plan.jpg แล้วสร้างใบเสนอราคากลาง v2 เป็น HTML แยกไฟล์
tags: [quotation, benchmark, plan, area-calculation, landscaping, html, v2]
created: 2026-07-03
updated: 2026-07-03
---

# วิเคราะห์พื้นที่จากแผนบ้านและสร้าง benchmark-quotation v2

Related:
- [plan.jpg](../resources/quotation/plan.jpg)
- [benchmark-quotation.html](../resources/quotation/benchmark-quotation.html) *(อ้างอิงราคา/หน่วย v1 — ห้ามแก้ไข)*
- [007-analyze-landscaping-quotation](007-analyze-landscaping-quotation.md)
- [008-create-benchmark-landscaping-quotation](008-create-benchmark-landscaping-quotation.md)
- [task/index.md](index.md)
- [task/log.md](log.md)

## Task Requirement

- Goal: วิเคราะห์พื้นที่จาก [plan.jpg](../resources/quotation/plan.jpg) (ผังแปลนกำแพง สเกล 1:175) เพื่อประเมินราคางานจัดสวนตามราคากลาง โดยแยกเป็น (1) ปูหินเกล็ดดำเฉพาะพื้นที่รอบบ้านภายในกรอบสีแดง ตัดพื้นที่ตัวบ้านออก และ (2) ปลูกหญ้าพื้นที่ที่เหลือทั้งหมด แล้วสร้าง **benchmark-quotation version 2** เป็น HTML ใหม่
- In scope: อ่านมิติจากแผน/กริด, คำนวณพื้นที่กรอบแดง พื้นที่ตัวบ้าน พื้นที่หินเกล็ดดำ พื้นที่หญ้า, ใช้ราคากลางจาก v1 หรือช่วงตลาดใน task 007/008, สร้าง `resources/quotation/benchmark-quotation-v2.html` พร้อมสรุปการคำนวณและสมมติฐาน
- Out of scope: แก้ไข `benchmark-quotation.html`, `quotation.pdf`, หรือไฟล์ v1 อื่นๆ; ต่อรองราคากับผู้รับเหมา; สั่งจ้างงานจริง
- Constraints: **ห้ามแก้ของเดิม** — สร้างไฟล์ v2 ใหม่เท่านั้น
- Scope clarification (งานปลูกหญ้า):
  - **หินเกล็ดดำ:** พื้นที่ในกรอบแดง − พื้นที่ตัวบ้าน (hatched footprint ภายในกรอบ)
  - **หญ้า:** พื้นที่ที่เหลือทั้งแปลง (นอกกรอบแดง + ภายในกรอบที่ไม่ใช่ตัวบ้านและไม่ปูหิน — ถ้ามี) ลบโครงสร้องอื่นที่ไม่ปลูกหญ้า เช่น carport/ทางรถ ตามที่ระบุในแผนและบันทึกในรายงาน
- Preliminary dimensions from plan (ให้ยืนยันตอน execute):
  - แปลงรวมประมาณ 12.88 × 42.35 ม. (หรือ 12.00 ม. ด้านบน)
  - กรอบแดง: สูง ~15.00 ม. (5 ช่องกริด × 3.00 ม.), กว้างเต็มแปลง ~12.00–12.88 ม., เริ่มห่างจากขอบบน ~12.35 ม.
  - ตัวบ้านในกรอบแดง: แบ่งเป็นบล็อกตามกริด (ประมาณ 60–110 ตร.ม. ขึ้นกับวิธี trace footprint)

## Checklist

- [x] T001 [N] วิเคราะห์ [plan.jpg](../resources/quotation/plan.jpg) — ระบุขอบเขตกรอบแดง, footprint ตัวบ้าน, carport/โครงสร้องอื่น และมิติอ้างอิงจากกริด/สเกล 1:175
  - ✅ กรอบแดง 12.00×15.00 ม.; บ้านในกรอบ 86.7 ตร.ม.; carport 5.80×6.00 ม.; แปลงรวม ~521.4 ตร.ม.
- [x] T002 [N] คำนวณพื้นที่ (ตร.ม.): กรอบแดงรวม, ตัวบ้านในกรอบ, พื้นที่หินเกล็ดดำ (กรอบแดง − บ้าน), พื้นที่ปลูกหญ้า (ที่เหลือทั้งแปลง − โครงสร้องที่ไม่ปลูก) พร้อมแสดงสูตรและสมมติฐาน
  - ✅ หินเกล็ดดำ 93.3 ตร.ม.; หญ้า 306.6 ตร.ม. (สนามบน 148.2 + สนามล่าง 158.4)
- [x] T003 [N] กำหนดราคากลาง/หน่วยสำหรับหินเกล็ดดำและหญ้า (อ้างอิง v1/007) และคำนวณราคารวม benchmark v2 + มัดจำ 50% ถ้าใช้รูปแบบเดียวกับใบเสนอราคาจริง
  - ✅ หิน 300 บาท/ตร.ม., หญ้า 120 บาท/ตร.ม.; รวม 64,782 บาท; มัดจำ 32,391 บาท
- [x] T004 [N] สร้าง `resources/quotation/benchmark-quotation-v2.html` — ใบเสนอราคากลาง v2 อ่านง่าย พิมพ์ได้ มีตารางพื้นที่และรายการราคา (**ไฟล์ใหม่เท่านั้น**)
  - ✅ สร้าง [benchmark-quotation-v2.html](../resources/quotation/benchmark-quotation-v2.html) โดยไม่แก้ไฟล์ v1
- [x] T005 [N] เพิ่มตารางเปรียบเทียบ v2 vs ใบเสนอราคาจริง (`quotation.pdf`) และ/หรือ v1 ถ้ามีรายการที่เทียบได้
  - ✅ เทียบหญ้า+หิน: ใบจริง 78,750 บาท vs v2 64,782 บาท (−13,968 บาท); รวมตารางเทียบ v1 ใน HTML
- [x] T006 [N] สรุปข้อจำกัดการวัดจากแผน, ความคลาดเคลื่อนที่เป็นไปได้, และคำแนะนำก่อนใช้ตัวเลขต่อรอง
  - ✅ บันทึกข้อจำกัด ±5–10%, ความเสี่ยงจำนวนหญ้าในใบจริง, และคำแนะนำวัดหน้างานใน HTML

## Output

- HTML: [benchmark-quotation-v2.html](../resources/quotation/benchmark-quotation-v2.html)
- Gravel area: 93.3 ตร.ม. → 27,990 บาท
- Grass area: 306.6 ตร.ม. → 36,792 บาท
- Total v2: 64,782 บาท | Deposit 50%: 32,391 บาท
- vs actual (grass+gravel only): 78,750 บาท → actual higher by 13,968 บาท
