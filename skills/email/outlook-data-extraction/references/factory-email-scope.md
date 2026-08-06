# Factory Email Extraction — Scope Reference

> When extracting emails related to Samaya Factory from Outlook, include ALL of the following categories — not just profile/brochure emails.

## Full Scope (user-corrected 2026-08-02)

| Category | Include? | Examples |
|----------|----------|----------|
| **Operational POs** (أوامر شراء تشغيلية) | ✅ YES | `P02139 (المصنع - سائل تنظيف ماكينه الشريط)`, `P02226 (المصنع - كشف مصروفات)` |
| **Manufacturing Orders** (أوامر تصنيع) | ✅ YES | `P02264 (متاجر الغمامة - المصنع - اخشاب متنوعه)`, `P02171 (المصنع - غراء للمكبس)` |
| **Factory Manager approvals** | ✅ YES | `Purchase Order Approval: Factory Manager` مسندة إليك |
| **Factory Profile / Prequalification** | ✅ YES | `اوراق مصنع سمايا`, `Updated Samaya prequalification` |
| **Product Catalog** | ✅ YES | `Samaya_Factory_Bilingual_Product_Catalog` |
| **Feasibility Study** | ✅ YES | `دراسة الجدوى لمصنع المدينة` |
| **Website / Hosting** | ✅ YES | `Your domain has been suspended`, `Verify your email address` |
| **Cash out / Expenses** | ✅ YES | `Samaya Factory Cash out Summary`, `P02226 (المصنع - كشف مصروفات)` |
| **Vendor Prequalification** | ✅ YES | `Prequalification Documents Molitor`, `vendor Prequalification Documents` |
| **Staffing / Recruitment** | ✅ YES | `طلب توظيف نجار ومساعدين نجار للمصنع` |
| **Maintenance** | ✅ YES | `طلب صيانة مكيفات المصنع وغرفة المستودع` |

## Search Query Pattern

```sql
SELECT Message_NormalizedSubject, Message_TimeReceived, Message_SenderList, 
       Message_DisplayTo, Message_Size, Record_RecordID
FROM Mail 
WHERE Message_NormalizedSubject LIKE '%مصنع%' 
   OR Message_NormalizedSubject LIKE '%Factory%' 
   OR Message_NormalizedSubject LIKE '%factory%'
ORDER BY Message_TimeReceived DESC
LIMIT 200;
```

This catches ALL factory-related emails including operational POs, manufacturing orders, and approvals — not just profile/brochure content.

## Raoof Eldeeb (رؤوف الديب) — Email Extraction

Raoof Eldeeb (raoof@samayainvest.com) is the **Production Manager** (مسؤول الإنتاج بالمصنع) at Samaya Factory. When extracting his emails, use these patterns:

### Search by email address (precise — preferred)
```sql
WHERE Message_SenderAddressList LIKE '%raoof@samayainvest.com%'
   OR Message_ToRecipientAddressList LIKE '%raoof@samayainvest.com%'
```

### Search by display name (broader — catches CC'd mentions)
```sql
WHERE Message_SenderList LIKE '%Raoof%'
   OR Message_DisplayTo LIKE '%Raoof%'
   OR Message_RecipientList LIKE '%raoof%'
```

### Common email types FROM Raoof
| Type | Examples |
|------|----------|
| **Incident reports** | إثبات واقعة, Staff Violation Memos |
| **Purchase requests** | طلبات شراء للمصنع متاخره, طلب زيادة عهد الورشة |
| **HR actions** | طلب انهاء خدمات العامل, اشعار بعودة, مباشره عمل, اوفر تايم |
| **Production updates** | استلام أبواب, طباعة استيكر, لوجو جبل عمر |
| **External submissions** | اوراق مصنع سمايا (to vendors/authorities) |

### Common email types TO Raoof
| Type | Examples |
|------|----------|
| **Bank statements** | كشوف حسابات بنك الراجحي (forwarded by Ibrahim Shaaban) |
| **Manager instructions** | طلب تحقيق, طلب انهاء خدمات, صيانة سقف المستودع |
| **Catalog/design sharing** | Samaya_Factory_Bilingual_Product_Catalog |
| **ERP notifications** | Purchase Order approvals mentioning @Raoof Aldeeb |

### Key contacts in Raoof's network
| Person | Role | Email |
|--------|------|-------|
| Sultan Issa | Technical Office Manager | sultan@samayainvest.com |
| Ibrahim Shaaban | Finance/Admin | i.shaaban@samayainvest.com |
| Bandar Alquayyid | HR | B.Alquayyid@samayainvest.com |
| Osama Shaikh | HR/Support | osama@samayainvest.com |
| Mohammed Mahfoudh | Procurement | M.mahfoudh@samayainvest.com |
| Kamel Etman | Project Manager | K.Etman@samayainvest.com |
| Anas Aljunaidel | Finance | AlJunaidel@samayainvest.com |
| Yosry Hafiz | Finance | yosry@samayainvest.com |

## Exclusion Rules

- **Zamzam Museum factory submissions** (e.g., `ZAM-NWC-CTR-MAR-EL-052-نموذج تقديم مواد (MAR) اعتماد نظام التأريض والحماية من الصواعق (مصنع رفاهية الطاقة للصناعة)`) — these are about a DIFFERENT factory (supplier's factory), not Samaya Factory. Exclude unless the user asks for them.
- **ERP system notifications** that just say "Done" with no context — exclude.
