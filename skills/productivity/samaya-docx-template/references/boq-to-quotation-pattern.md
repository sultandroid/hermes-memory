# BOQ-to-Quotation Pattern — Design Consultancy

## Context

User provided a BOQ xlsx (`KHM-MED-08-BOQ-ID-T-00-Talha-PC.xlsx`) for Khair El-Khalq Museum with items across Divisions 6, 8, 9, 10, 11, 12, 13, 26, 27. User said "use samaya doc style to make quotation for this project, make items per divisions."

**First attempt:** Generated a construction/supply-and-install quotation with blank rate/amount columns.

**User correction:** "الاقتباس للاعمال الاستشاريه والتصميميه لكن ارجوا التفصيل لها ويكون المجموع ٤٤٠ الف ريال" — it's for design consultancy services, total 440,000 SAR.

## Lesson

Always clarify service type before generating a quotation from a BOQ. The same BOQ items can represent either:
- **Construction scope** (supply + install materials)
- **Design consultancy scope** (design development, shop drawings, material selection, coordination)

## Distribution pattern for fixed-total design consultancy quotation

### Division allocation (440,000 SAR total)

| Division | Description | Fee (SAR) | Basis |
|----------|-------------|:---------:|-------|
| 6 | Wood, Plastics and Composites | 45,000 | 6 wood paneling items + 1 custom fabrication item |
| 8 | Openings | 35,000 | Doors, glazing, auto gate, mirrors |
| 9 | Finishes | 85,000 | Gypsum, ceilings, flooring, carpet, painting (largest division) |
| 10 | Specialties | 30,000 | Signage, banners, partitions |
| 11 | Audio-Visual | 40,000 | LED screens, projectors |
| 12 | Furnishings | 55,000 | Cushions, counter, tables, seating, benches |
| 13 | Special Construction | 25,000 | Prophet's Tent Model (single complex item) |
| 26 | Electrical | 75,000 | Lighting control, interior lighting |
| 27 | Communications | 30,000 | PA system |
| - | Additional Services | 20,000 | Coordination + site support |

### Per-item rate calculation

For each item within a division:
1. Decide the item's share of the division fee based on complexity
2. Compute `rate = item_amount / qty`
3. Round rates to clean numbers (500, 1,000, 2,000, etc.)
4. Adjust the largest item in the division to absorb any rounding gap

### DOCX structure

- H1: "DESIGN CONSULTANCY QUOTATION"
- H2 per division (2.0 through 10.0)
- H3 per sub-section (e.g. "06 42 00 - Wood Paneling Design")
- 6-column table: Item, Description, Unit, Qty, Rate (SAR), Amount (SAR)
- Division subtotal line (bold, right-aligned)
- Summary table at end with all divisions + total
- Terms & Conditions section
- Approval/QC block

### Doc ref pattern

`KHM-SAM-QTN-DSGN-001` — project code + SAM + QTN + DSGN for design consultancy.

### Gen script pattern

```python
import sys, os
_template_dir = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide"
sys.path.insert(0, _template_dir)
from samaya_doc_template import SamayaDoc, SamayaColors

doc = SamayaDoc()
doc.create_header(project_name="Khair El-Khalq Museum", doc_ref="KHM-SAM-QTN-DSGN-001", doc_type="QTN", revision="00", date="Jul 2026")
doc.create_footer("KHM-SAM-QTN-DSGN-001")
doc.add_h1("DESIGN CONSULTANCY QUOTATION")
# ... per-division tables ...
doc.save("/path/to/output.docx")
```

### Verification

After generation, verify:
- Each division subtotal matches the planned allocation
- Sum of all division subtotals = 440,000
- All rates are positive and reasonable
- No blank rate/amount cells (they were blank in the construction version — fill them in the consultancy version)
