---
title: วิเคราะห์ใบเสนอราคางานจัดสวน
type: planning
detail: วิเคราะห์ใบเสนอราคาจัดสวนจาก PDF เทียบราคาตลาด และสรุปคำแนะนำก่อนจ่ายมัดจำ
tags: [quotation, landscaping, pricing, pdf, web-research]
created: 2026-06-26
updated: 2026-06-26
---

# วิเคราะห์ใบเสนอราคางานจัดสวน

Related:
- [quotation.pdf](../resources/quotation/quotation.pdf)
- [task/index.md](index.md)
- [task/log.md](log.md)

## Task Requirement

- Goal: วิเคราะห์ความสมเหตุสมผลของใบเสนอราคางานจัดสวนยอดรวม 178,750 บาท โดยตรวจความถูกต้องของข้อมูลจาก PDF, เทียบราคาตลาด, และสรุปความเสี่ยง/คำถามที่ควรถามผู้รับเหมาก่อนตัดสินใจจ่ายมัดจำ
- In scope: อ่านและตรวจข้อมูลจาก `resources/quotation/quotation.pdf`, ดึงรายการและราคา/หน่วย, ทำ web research เพิ่มเติม, แนะนำเครื่องมืออ่าน PDF/OCR ภาษาไทย, และจัดทำรายงานสรุปข้อเสนอแนะ
- Out of scope: ต่อรองราคาหรือสั่งจ้างแทนลูกค้า, ซื้อวัสดุ, เปลี่ยนแปลงงานจัดสวนจริง
- Notes: ให้ตรวจบรรทัดที่อาจดึงข้อมูลผิดจาก PDF เป็นพิเศษ เช่น รายการหญ้า/จำนวนพื้นที่/ราคาต่อหน่วย และเงื่อนไขมัดจำไม่คืน

## Checklist

- [x] T001 [N] Extract quotation data from [quotation.pdf](../resources/quotation/quotation.pdf), including customer/vendor info, item quantities, unit prices, total, deposit, and payment terms.
  - ✅ Extracted all visible line items, total, deposit split, vendor/customer details, and non-refundable deposit term.
- [x] T002 [N] Validate PDF extraction accuracy and recommend suitable PDF/OCR tools for Thai quotation documents.
  - ✅ Validated item subtotals add up to 178,750 บาท; noted that layout/spec fields are incomplete and should be rechecked with layout-aware PDF/OCR tools.
- [x] T003 [N] Perform web research for benchmark prices of grass installation, black gravel, exterior paving, concrete slab work, and sand-wash stepping stones.
  - ✅ Benchmarked grass installation, chipped stone/gravel, concrete slab, exterior floor paving, sand-wash work, and 40x80 stepping stones.
- [x] T004 [N] Compare quotation unit prices against benchmark ranges and flag unusually high, unclear, or reasonable line items.
  - ✅ Compared quoted unit prices and flagged grass, concrete, and exterior paving as requiring clarification.
- [x] T005 [N] Summarize negotiation/checklist questions for the contractor, including material specs, concrete thickness, warranty, timeline, scope, and deposit terms.
  - ✅ Added contractor clarification checklist below.
- [x] T006 [N] Produce a concise Thai analysis report with risks, assumptions, and recommendation before paying the deposit.
  - ✅ Added Thai analysis report below.

## Quotation Data Extracted

- Date: 20/06/2569
- Vendor: บ้านสวนธรรมรัตน์, 55 ถ.อาณาเขต ต.บ้านพรุ อ.หาดใหญ่ จ.สงขลา 90250, โทร 095-6860481 / 087-3977971
- Customer: คุณเก๋, ที่อยู่ สทิงพระ
- Total: 178,750 บาท
- Deposit: 89,375 บาท
- Remaining payment after delivery: 89,375 บาท
- Payment condition: มัดจำแล้ว ไม่สามารถยกเลิกหรือคืนเงินทุกกรณี
- Operation/travel fee: ฟรี

| รายการ | จำนวน | ราคารวม | ราคา/หน่วยจากใบเสนอราคา |
|---|---:|---:|---:|
| หญ้า | 10 ตร.ม. | 15,750 บาท | 1,575 บาท/ตร.ม. |
| หินเกล็ดดำ | 210 ตร.ม. | 63,000 บาท | 300 บาท/ตร.ม. |
| งานปูพื้นภายนอก | 34 ตร.ม. | 51,000 บาท | 1,500 บาท/ตร.ม. |
| งานเทคอนกรีตหน้าบ้าน | 54 ตร.ม. | 40,500 บาท | 750 บาท/ตร.ม. |
| แผ่นทางเดินทรายล้าง 40x80 ซม. | 34 แผ่น | 8,500 บาท | 250 บาท/แผ่น |

Validation: 15,750 + 63,000 + 51,000 + 40,500 + 8,500 = 178,750 บาท ตรงกับยอดรวมใน PDF

## PDF/OCR Tool Recommendation

Use a layout-aware tool before making payment, because the PDF text extraction is readable but does not preserve full table structure/spec detail.

- First choice for Thai quotations: Typhoon OCR 1.5 (`typhoon-ocr`) because it supports Thai/English documents, PDFs/images, layout-aware Markdown, and table extraction.
- For text-layer PDFs: `pdfplumber` or `PyMuPDF` are lightweight options to extract text and tables locally.
- For scanned/image PDFs: Tesseract OCR with Thai language data (`tha`), EasyOCR, PaddleOCR, Google Document AI, or Azure Document Intelligence.
- Practical workflow: export the quotation page to image, run Typhoon OCR or Document AI, then compare quantity/price columns against the original image.

## Market Benchmarks

Sources found during web research:

- Grass installation: หญ้าจริงรวมปูและปรับพื้นเบื้องต้นประมาณ 80-150 บาท/ตร.ม.; บางไร่หญ้าระบุรวมปลูก 20-35 บาท/ตร.ม. สำหรับงานขนาดเหมาะสม
- Black/chipped stone: หินเกล็ดทั่วไปประมาณ 500-650 บาท/ลบ.ม.; หินเกล็ดตกแต่งสวนแบบถุงประมาณ 35-90 บาท/ถุง; หากรวมปรับพื้นและโรยหิน งานเหมาประมาณ 250-350 บาท/ตร.ม. ถือเป็นช่วงที่พบได้
- Concrete slab: เทคอนกรีตหนา 10 ซม. รวมแรงและวัสดุประมาณ 300-500 บาท/ตร.ม. ขึ้นกับ KSC, ไวร์เมช, พื้นที่, รถปั๊ม, และงานเตรียมพื้นที่
- Exterior paving: ค่าแรง+วัสดุพื้นฐานปูกระเบื้องประมาณ 300-550 บาท/ตร.ม.; หินอ่อน/หินเทียมประมาณ 900-1,200 บาท/ตร.ม.; งานทรายล้างประมาณ 450-750 บาท/ตร.ม.
- Sand-wash stepping stone 40x80 ซม.: ราคาขายปลีกประมาณ 120-235 บาท/แผ่น ขึ้นกับสี/เกรด/ผู้ขาย และยังไม่รวมขนส่งหรือติดตั้ง

## Price Assessment

| รายการ | ราคาใบเสนอราคา | Benchmark | Assessment |
|---|---:|---:|---|
| หญ้า | 1,575 บาท/ตร.ม. | ประมาณ 80-150 บาท/ตร.ม. | สูงผิดปกติมาก ต้องตรวจว่า PDF อ่านจำนวนผิดหรือบรรทัดนี้รวมงานอื่นไว้ |
| หินเกล็ดดำ | 300 บาท/ตร.ม. | ประมาณ 250-350 บาท/ตร.ม. ถ้ารวมปรับพื้น/โรยหิน | สมเหตุสมผล |
| งานปูพื้นภายนอก | 1,500 บาท/ตร.ม. | ทั่วไป 300-550; วัสดุพรีเมียม/หิน 900-1,200+ | ค่อนข้างสูง ต้องขอสเปกวัสดุและชั้นพื้น |
| งานเทคอนกรีตหน้าบ้าน | 750 บาท/ตร.ม. | ประมาณ 300-500 บาท/ตร.ม. | สูงกว่าค่ากลาง ต้องถามความหนา KSC ไวร์เมช รถปั๊ม และงานเตรียมพื้น |
| แผ่นทางเดินทรายล้าง | 250 บาท/แผ่น | ประมาณ 120-235 บาท/แผ่น | สูงเล็กน้อยถึงพอรับได้ หากรวมขนส่ง/คัดสี/ติดตั้ง |

## Contractor Questions Before Deposit

ควรถามและขอแก้ใบเสนอราคาให้ชัดเจนก่อนโอนมัดจำ โดยเฉพาะเพราะมีเงื่อนไขไม่คืนเงิน:

1. รายการ "หญ้า 10 ตร.ม. 15,750 บาท" ถูกต้องหรือไม่ ถ้าถูกต้องรวมอะไรบ้าง เช่น ปรับดิน ขนดิน ทราย ปุ๋ย งานระบบน้ำ หรือพื้นที่จริงมากกว่า 10 ตร.ม.
2. หญ้าเป็นชนิดอะไร เช่น นวลน้อย มาเลเซีย ญี่ปุ่น พาสพาลัม หรือหญ้าเทียม และรับประกันรากติด/หญ้าตายกี่วัน
3. หินเกล็ดดำมีความหนากี่ซม. ใช้กี่คิว มีผ้าใยกันวัชพืชหรือไม่ และรวมงานปรับระดับ/อัดบดแล้วหรือยัง
4. งานปูพื้นภายนอกใช้วัสดุอะไร รุ่น/ขนาด/สี/ยี่ห้อใด รวมค่าวัสดุปูพื้นจริงหรือเฉพาะค่าแรง+ปูนทราย
5. งานเทคอนกรีตหน้าบ้านหนากี่ซม., คอนกรีตกี่ KSC, มีไวร์เมช/เหล็กเสริมหรือไม่, มีทรายรองพื้น/บดอัด/ขัดมัน/ slope ระบายน้ำหรือไม่
6. แผ่นทางเดินทรายล้างราคา 250 บาท/แผ่น รวมขนส่งและติดตั้งหรือไม่ และวางบนทราย/หินเกล็ด/ปูนอย่างไร
7. ขอแยกราคาเป็นวัสดุ ค่าแรง ค่าขนส่ง และค่าเครื่องมือ เพื่อเทียบกับราคาตลาดได้ตรงขึ้น
8. ขอระบุระยะเวลางาน วันเริ่ม-วันจบ เงื่อนไขแก้งาน และการรับประกันหลังส่งมอบ
9. ขอปรับเงื่อนไขมัดจำ เช่น มัดจำตามค่าวัสดุจริง หรือแบ่งจ่ายตาม milestone แทนมัดจำ 50% แบบไม่คืน

## Recommendation

คำแนะนำหลักคือยังไม่ควรจ่ายมัดจำทันทีจนกว่าจะได้ใบเสนอราคาฉบับละเอียดกว่าเดิม เพราะมีอย่างน้อย 3 รายการที่ต้องอธิบายเพิ่ม: หญ้า, งานปูพื้นภายนอก, และงานเทคอนกรีต หน้างานอาจมีเหตุผลให้ราคาแพงขึ้นได้ เช่น พื้นที่เข้าถึงยาก งานเตรียมพื้นเยอะ หรือใช้วัสดุพรีเมียม แต่ใบเสนอราคาปัจจุบันยังไม่ให้สเปกพอที่จะพิสูจน์ราคา

หากผู้รับเหมาชี้แจงได้ว่าแต่ละรายการรวมวัสดุ/งานเตรียมพื้นที่/ขนส่ง/รับประกันอะไรบ้าง ราคาโดยรวมอาจยังเจรจาได้ แต่บรรทัด "หญ้า" ควรถูกตรวจเป็นอันดับแรก เพราะราคา 1,575 บาท/ตร.ม. สูงกว่าช่วงตลาดมากและอาจเป็นสัญญาณว่าการดึงตารางจาก PDF หรือการเขียนจำนวนพื้นที่มีข้อผิดพลาด
