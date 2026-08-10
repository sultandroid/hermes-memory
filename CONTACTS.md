# CONTACTS — Key People

*Verified from Odoo res.users + hr.employee. Roles from Odoo job titles where available.*

## Samaya Team

| Name | Role (Odoo) | Email | Odoo ID |
|------|------------|-------|---------|
| Sultan Issa | Technical Office Manager | sultan@samayainvest.com | 151 |
| Ahmed Salah S. Kadous | Project Manager | ahmed.salah@samayainvest.com | 162 |
| Ahmed Awwad | Designer | awwad@samayainvest.com | 152 |
| Ahmed Saad | Project Manager | a.saad@samayainvest.com | 164 |
| Ibrahim Shaaban | Accountant | i.shaaban@samayainvest.com | 169 |

## Samaya Team (no hr.employee record — roles from email/project context)

| Name | Role (inferred) | Email | Odoo ID |
|------|----------------|-------|---------|
| Ali Abdel Rahman | Technical Office (DD design packages) | ali.abdelrahman@samayainvest.com | 160 |
| Hesham Abd Elhameed | Document Control | hesham.a@samayainvest.com | 163 |
| Adel Darwesh | Project Manager | adel@samayainvest.com | 7 |
| Mohamed Samir | Site Execution / Procurement | m.samir@samayainvest.com | 564 |
| Mohammed Elshaikh | Project Planner | elshaikh@samayainvest.com | 157 |
| Hani Alghamdi | Purchasing Lead | H.Alghamdi@samayainvest.com | 478 |
| Kareem Hussain | Project Manager (Jabal Omar) | kareem.hussain@samayainvest.com | 165 |
| Mohamed Said | — | mohamed.said@samayainvest.com | 166 |
| Ahmed Khaleel | Accountant | ahmed@samayainvest.com | 170 |
| Talha Yousf | — | talha.yousaf@samayainvest.com | 154 |
| Mohammed Hakmi | Lighting Engineer | m.hakami@samayainvest.com | — |

## Samaya Sales / Commercial (added 2026-08-10 — from Odoo hr.employee)

| Name | Job Title | Manager (parent) | Email | Phone | Odoo ID | Dept |
|------|-----------|------------------|-------|-------|---------|------|
| **خالد احمد محمد العبيدي** (Khaled Al-Obaidi) | **Sales Department Manager** (Odoo) | فواز عبدالله محمد المحرج (CEO, id=953) | k.abeedy@samayainvest.com | 966500686620 | **900** | Samaya / قسم المبيعات (101) |
| **علاء حسين نمر الشوا** (Alaa Al Shawa) | **Sales Coordinator** (توقيع البريد) — Odoo: salesman | خالد احمد محمد العبيدي (id=900) | a.alshawa@samayainvest.com | 966509133868 | **945** | Samaya / قسم المبيعات (101) |
| فواز عبدالله محمد المحرج | Chief Executive Officer | — | fawaz@samayainvest.com | 966555212600 | 953 | Samaya / مكتب الرئيس التنفيدي (93) |
| ياسر بن احمد حمدان الذيباني | Sales Manager | مشعل معتمد خوجلي مصطفى (id=1008) | yaser01@samaya.me | 966531051078 | 3057 | Rawasin (38) |
| مشعل معتمد خوجلي مصطفى | Sales and Operations Manager | حسين عبد الحكم خليل كريم (id=3417) | meshalkhojali@taibahgifts.com | 966533390062 | 1008 | Taibah Gifts (28) |

> **ملاحظات Odoo (تحقق 2026-08-10):**
> - **التسلسل الإداري للمبيعات:** علاء (Sales Coordinator) ← خالد (Sales Dept Manager) ← فواز (CEO).
> - **المسمى الوظيفي:** توقيع البريد أدق من Odoo — علاء = **Sales Coordinator** (Odoo يسجّله "salesman" فقط). عند تعارض، يُفضَّل توقيع البريد.
> - **`hire_date` غير مسجلة** في Odoo لهذه الجهات (فارغة) — لا يوجد تاريخ مباشرة.
> - **سجلات res.partner المكررة:** علاء (1553/5534)، خالد (1508/5533/5546/8026) — يُفضَّل السجل العربي/الأحدث.
> - **قاعدة ربط Odoo:** كل جهة سمايا تُربط برقمها في Odoo (`hr.employee` → id، و`res.partner` → id) لتسهيل الربط الآلي.

## External

| Name | Role | Email |
|------|------|-------|
| Hossam Mabrouk | CG Consultant (ACE) | hmabrouk@cg.com.sa |
| **Mansour Al-Mutairi** | **Acting CG Project Manager** (replaced Elbaz, Jul 2026) | **malrezeni@cg.com.sa** |
| Mohamed Al-Baz | CG Project Director | melbaz@cg.com.sa |
| Mohamed Elbaz | CG Senior Electrical Engineer (monitoring capacity only) | melbaz@cg.com.sa |
| Ahmed Ghoneim | CG Lighting Consultant Specialist | aghoneim@cg.com.sa |
| Maged Zamzam | CG | mzamzam@cg.com.sa |
| Jim Richards | Director — Nissen Richards Studio | jim.r@nissenrichardsstudio.com |
| NRS | Design Lead (A2742) | Nissen Richards Studio |

## Assignment Rules

- **Sultan** → DD stage technical packages ONLY. Not PM.
- **Prequal / procurement** → Hani + Mohamed Samir (NOT Ali)
- **Site work** (construction, fabrication, handover) → Mohamed Samir
- **DD stage technical work** → Sultan + Ali
- **Procurement submittals** → Hani + Samir
- **Material submittals from baseline** → Hani + Samir
- **Contractor scope reference items** → prefix `[REF]`, stage 39/40/479, assign to Samir/Hani
- **Document control / daily reports** → Hesham
- **Coordination / mfg orders** → Ahmed Salah
- **Schedule review** → Sultan + Mohamed Elshaikh

## Added 2026-07-31 — SulKIMICLAW

| Name | Role | Email | Notes |
|------|------|-------|-------|
| Dr. Waleed Salah | BIM Manager (Aseer) | — | NRS BIM lead, reports to Jim Richards |
| Eng. Waris Sultan | Project Director (Exhibitions) | — | From 13-Jun-2026, exhibitions scope |
| Dogan Kozan | Lighting Engineer / Lead | — | Spec: ZNA (signed), workshop presenter |
| Sulaiman Obiya | Acoustic Consultant / Lead | — | Spec: TransOrient (Code B), workshop presenter |
| Magdy Saleha | Graphics Designer / Lead | — | Spec: Graphite (Code B), workshop presenter |
| Bashir Zain | Sub-contractor (Civil) | — | Guardrailing installation, 30-Jul-2026 |

## Communication Channels

| Channel | Identifier | Agent |
|---------|-----------|-------|
| Telegram (personal) | @mohSulabbas | SulKIMICLAW |
| Telegram (bot) | @SulKimiClaw_bot | SulKIMICLAW |
| Email (primary) | sultan@samayainvest.com | All |
| Email (personal) | mohamedsultanabbas@gmail.com | All |
