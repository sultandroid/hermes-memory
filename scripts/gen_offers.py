#!/usr/bin/env python3
"""Generate job offer letters with actual names from the iqama file."""
import sys, os
sys.path.insert(0, '/Users/mohamedessa/aseer-museum-pm/_Style-Guides/Doc Style Guide')
from samaya_doc_template import SamayaDoc, SamayaColors

def make_offer(position, salary, name_ar, name_en, iqama, phone):
    doc = SamayaDoc()
    doc.create_header('Samaya Investment Company', 'HR-OFR-001', 'OFFER LETTER', 'A')
    doc.create_footer('HR-OFR-001', confidential=False)
    doc.add_h1('OFFER LETTER / عرض وظيفي')
    doc.line()

    doc.add_body(f'Date: 06 August 2026', align=1)
    doc.add_h2_u('CANDIDATE INFORMATION')
    doc.add_body(f'Position: {position}')
    doc.add_body(f'Name: {name_ar} / {name_en}')
    doc.add_body(f'Iqama No: {iqama}')
    doc.add_body(f'Phone: {phone}')
    doc.add_body(f'Department: قسم النجارة / Carpentry Department')
    doc.add_body(f'Location: السلي - المصنع / Al-Sali - Factory')
    doc.add_body(f'Direct Manager: م / رؤوف الديب / Eng. Raoof Al-Deeb')
    doc.add_body(f'Start Date: فورا / Immediately')

    doc.add_h2_u('OFFER DETAILS')
    doc.add_table(
        ['#', 'Item', 'Details'],
        [
            ['1', 'Monthly Salary / الراتب الشهري', f'{salary} SAR'],
            ['2', 'Contract Type / نوع العقد', 'محدد المدة (سنوي) / Fixed-term (1 year)'],
            ['3', 'Duration / المدة', 'دائم / Permanent (project-based)'],
            ['4', 'Working Hours', '8 hours/day - 6 days/week'],
            ['5', 'Overtime', 'As per Saudi Labor Law'],
            ['6', 'Housing / السكن', 'Provided by company'],
            ['7', 'Transport / المواصلات', 'Provided by company'],
            ['8', 'Medical Insurance', 'As per Saudi Labor Law'],
            ['9', 'Annual Leave', '21 days per year (after probation)'],
        ],
        col_widths_cm=[0.8, 8.0, 7.7]
    )

    doc.add_h2_u('PROBATION PERIOD / فترة التجربة')
    doc.add_body('Three months probation period, extendable as per Saudi Labor Law.')
    doc.add_body('ثلاثة أشهر فترة تجربة، قابلة للتمديد حسب نظام العمل السعودي.')

    doc.add_h2_u('TERMS & CONDITIONS')
    doc.add_body('1. This offer is valid for 7 working days from date of issue.')
    doc.add_body('2. Employment is subject to medical examination and background check.')
    doc.add_body('3. Any changes to this offer must be confirmed in writing.')
    doc.add_body('4. The employee shall comply with all company policies and procedures.')

    doc.add_h2_u('ACCEPTANCE')
    doc.add_body('I, the undersigned, accept the above offer and agree to the terms and conditions.')
    doc.line()
    doc.add_body('________________________________        ________________')
    doc.add_body('Signature / التوقيع                              Date / التاريخ')
    doc.line()
    doc.add_body('________________________________        ________________')
    doc.add_body('HR Manager / مدير الموارد البشرية          Date / التاريخ')

    return doc

base = '/Users/mohamedessa/Desktop'

# 1. Virgilio — نجار 2,500
d1 = make_offer('نجار / Carpenter', '2,500',
    'فيرجيليو ج ر استيبي سيسون', 'VIRGILIO JR ASTIBE SISON',
    '2480160684', '+966 57 217 2209')
d1.save(f'{base}/عرض_وظيفي_نجار_فيرجيليو.docx')
print(f'Created: نجار - فيرجيليو')

# 2. Rennan — نجار 2,500
d2 = make_offer('نجار / Carpenter', '2,500',
    'رينان ابيلار ريفيرزو', 'RENNAN ABILAR REFUERZO',
    '2490873532', '+966 56 483 4867')
d2.save(f'{base}/عرض_وظيفي_نجار_رينان.docx')
print(f'Created: نجار - رينان')

# 3. Julian — عامل 2,000
d3 = make_offer('عامل / Worker', '2,000',
    'جوليان اوريلانو جريدونا', 'JULIAN JR ORELLANO GREDONA',
    '2600584557', '+966 56 962 0809')
d3.save(f'{base}/عرض_وظيفي_عامل_جوليان.docx')
print(f'Created: عامل - جوليان')

# 4. Sahid — عامل 2,000
d4 = make_offer('عامل / Worker', '2,000',
    'سيد ابا توانسي', 'SAHID ABA TUANSI',
    '2546912573', '+966 53 028 8537')
d4.save(f'{base}/عرض_وظيفي_عامل_سيد.docx')
print(f'Created: عامل - سيد')

print('\nDone — 4 offer letters with names.')
