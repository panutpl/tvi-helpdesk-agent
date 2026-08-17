# คู่มือพนักงานใหม่ TechCorp — New Employee Onboarding Guide

> Welcome to TechCorp! 🎉
> เอกสารนี้รวบรวมสิ่งที่พนักงานใหม่ต้องทำในช่วง 2 สัปดาห์แรก
> อัปเดตล่าสุด: มกราคม 2568

---

## ก่อนวันเริ่มงาน (Pre-boarding)

HR จะส่งเอกสารต่อไปนี้ทาง email ก่อนวันเริ่มงาน 3 วัน:

- [ ] สัญญาจ้าง (ลงนาม digital ผ่าน DocuSign)
- [ ] แบบฟอร์มข้อมูลส่วนตัว (ชื่อบัญชีธนาคาร, ผู้ติดต่อฉุกเฉิน)
- [ ] เลือก laptop: MacBook Pro 14" (M3) หรือ ThinkPad X1 Carbon (สำหรับ Windows/Linux users)
- [ ] ถ่ายรูปสำหรับบัตรพนักงาน (ส่ง file ให้ HR)

---

## วันแรก (Day 1)

### เช้า (9:00 - 12:00)

| เวลา | กิจกรรม | สถานที่ |
|------|---------|---------|
| 9:00 | รายงานตัวที่ Reception ชั้น 1 | Lobby |
| 9:15 | รับบัตรพนักงาน + Welcome Kit | HR Office (ชั้น 3) |
| 9:30 | Office Tour โดย HR | ทั่วออฟฟิศ |
| 10:00 | IT Setup Session — รับ laptop, ตั้งค่า accounts | IT Corner (ชั้น 4) |
| 11:00 | พบ Line Manager — แนะนำทีม | ห้องทีม |
| 11:30 | Lunch with Buddy (บริษัทเลี้ยง) | ร้านอาหารใกล้ออฟฟิศ |

### บ่าย (13:00 - 17:00)

| เวลา | กิจกรรม | สถานที่ |
|------|---------|---------|
| 13:00 | Company Introduction Presentation | Meeting Room A (ชั้น 5) |
| 14:00 | HR Orientation — สิทธิ์ลา, เบิกเงิน, สวัสดิการ | Meeting Room A |
| 15:00 | Security Awareness Training (online) | ที่โต๊ะตัวเอง |
| 16:00 | Setup development environment (สำหรับ engineering) | ที่โต๊ะตัวเอง |
| 16:30 | 1-on-1 กับ Line Manager — เป้าหมาย 30/60/90 วัน | ห้อง Manager |

---

## IT Setup Checklist

สิ่งที่ต้องทำให้เสร็จในวันแรก:

### Accounts ที่จะได้รับ:

- [ ] **Email:** firstname.l@techcorp.co.th (Google Workspace)
- [ ] **Slack:** ใช้ email บริษัท join workspace "TechCorp"
- [ ] **HRMS:** https://hrms.techcorp.co.th (login ด้วย SSO)
- [ ] **IT Portal:** https://it-portal.techcorp.co.th
- [ ] **GitHub:** จะถูกเพิ่มเข้า org "techcorp-eng" (สำหรับ engineering)
- [ ] **Google Drive:** จะถูกเพิ่มเข้า Shared Drive ของทีม

### ตั้งค่าที่ต้องทำ:

- [ ] ตั้ง password ตาม IT Security Policy (อย่างน้อย 12 ตัวอักษร, ตัวใหญ่+เล็ก+ตัวเลข+อักขระพิเศษ)
- [ ] ตั้งค่า MFA (Multi-Factor Authentication) ด้วย Google Authenticator
- [ ] ติดตั้ง VPN (WireGuard) — download config จาก IT Portal
- [ ] ติดตั้ง CrowdStrike Falcon (endpoint protection)
- [ ] ลงทะเบียน laptop ใน MDM system

### สำหรับ Engineering Team เพิ่มเติม:

- [ ] Request GitHub access ผ่าน IT Portal → "Access Request"
- [ ] Clone main repositories (ดู README ใน GitHub org)
- [ ] ติดตั้ง development tools: Docker, Node.js/Python, IDE
- [ ] ขอ access staging environment (ผ่าน Line Manager approve)
- [ ] Setup local development environment ตาม repo README

---

## สัปดาห์แรก (Week 1)

### Mandatory Training (ต้องเสร็จภายใน 7 วัน):

| Training | Platform | Duration | Deadline |
|----------|----------|----------|----------|
| Security Awareness | LMS | 45 นาที | Day 1 |
| Data Privacy & PDPA | LMS | 30 นาที | Day 3 |
| Code of Conduct | LMS | 20 นาที | Day 5 |
| Anti-harassment Policy | LMS | 25 นาที | Day 5 |
| Tool Training (role-specific) | Scheduled by Manager | 1-2 ชั่วโมง | Day 5 |

**LMS Access:** https://learn.techcorp.co.th (login ด้วย SSO)

### การเข้าร่วม Meetings:

- **Daily Standup:** ทุกวัน 9:30 (เข้าร่วมตั้งแต่ Day 2)
- **Weekly Team Meeting:** ทุกวันจันทร์ 14:00
- **All Hands:** ทุกวันศุกร์แรกของเดือน 16:00
- **1-on-1 with Manager:** สัปดาห์ละครั้ง (นัดเวลากับ Manager)

---

## สัปดาห์ที่สอง (Week 2)

### เป้าหมาย:
- เริ่มทำงานจริง (small task / bug fix / shadow senior)
- เข้าใจ codebase หลัก (สำหรับ engineering)
- เข้าใจ workflow และ tools ของทีม
- ตั้ง 30-day goals กับ Manager

### Buddy System:
- ทุกคนจะได้รับ "Buddy" (เพื่อนพนักงานที่อยู่มานานกว่า)
- Buddy จะช่วยตอบคำถามทั่วไป, พาไปกินข้าว, แนะนำคนในบริษัท
- นัด Buddy coffee chat อย่างน้อยสัปดาห์ละ 1 ครั้ง ในช่วงเดือนแรก

---

## 30 / 60 / 90 Day Milestones

### 30 วันแรก — "Learn & Absorb"
- เข้าใจ product/service ของบริษัท
- เข้าใจ tech stack และ architecture (engineering)
- Complete all mandatory training
- Deliver first small contribution (PR merged / task completed)

### 60 วัน — "Contribute"
- ทำงานได้ independently (ไม่ต้อง hand-hold ตลอด)
- เข้าใจ business context ของทีม
- มีส่วนร่วมใน sprint/project planning
- ผ่านการประเมินทดลองงาน checkpoint (informal)

### 90 วัน — "Own"
- รับผิดชอบ feature/area ได้เอง
- **ผ่านทดลองงาน** (Manager + HR ร่วมประเมิน)
- เริ่ม mentor คนอื่นได้ในบางเรื่อง

---

## สวัสดิการที่ได้รับทันที

| สวัสดิการ | รายละเอียด | เริ่มใช้ได้ |
|----------|------------|------------|
| ประกันสุขภาพ (OPD/IPD) | วงเงิน OPD 30,000 บาท/ปี, IPD 500,000 บาท/ปี | วันแรกที่เริ่มงาน |
| ประกันทันตกรรม | 10,000 บาท/ปี | วันแรกที่เริ่มงาน |
| ค่า WFH allowance | 1,000 บาท/เดือน (สำหรับค่า internet/ไฟ) | เดือนแรก |
| Gym ในออฟฟิศ | ฟรี | วันแรก (ใช้บัตรพนักงาน tap เข้า) |
| กองทุนสำรองเลี้ยงชีพ | บริษัทสมทบ 5% ของเงินเดือน | หลังผ่านทดลองงาน |
| Annual health checkup | ปีละ 1 ครั้ง (โรงพยาบาลพันธมิตร) | หลังทำงานครบ 6 เดือน |
| Flexible benefit | 20,000 บาท/ปี (เลือกใช้ตาม category) | หลังผ่านทดลองงาน |

---

## Slack Channels ที่ควร Join

| Channel | วัตถุประสงค์ |
|---------|-------------|
| #general | ประกาศทั่วไปของบริษัท |
| #random | คุยเล่น, แชร์ของสนุก |
| #it-support | ถามปัญหา IT ทั่วไป |
| #ask-hr | ถามเรื่อง HR, ลา, เบิกเงิน |
| #ask-finance | ถามเรื่องเบิกค่าใช้จ่าย |
| #security-incident | รายงาน security issues |
| #team-[your-team] | Channel ของทีมคุณ |
| #engineering (ถ้าเป็น eng) | อัปเดต technical ของ engineering |
| #lunch-buddies | หาคนไปกินข้าวด้วย |
| #wfh-today | แจ้งวัน WFH |

---

## ติดต่อเมื่อมีปัญหา

| ปัญหา | ติดต่อ |
|-------|--------|
| IT issues (password, VPN, laptop) | #it-support หรือ it-helpdesk@techcorp.co.th |
| HR questions (ลา, เบิกเงิน, สัญญา) | #ask-hr หรือ hr@techcorp.co.th |
| Office/Facilities (ห้องประชุม, parking) | #office-admin หรือ admin@techcorp.co.th |
| Security concerns | #security-incident หรือ security@techcorp.co.th |
| งาน/ทีม | Line Manager ของคุณ |
| ทั่วไป/ไม่แน่ใจถามใคร | Buddy ของคุณ |

---

> 💡 **Pro tip:** ช่วง 2 สัปดาห์แรก ให้เน้น "ถาม" มากกว่า "ทำ" — ไม่มีใครคาดหวังให้คุณ productive ตั้งแต่วันแรก สิ่งสำคัญคือเข้าใจ context ก่อน แล้วค่อยๆ contribute
