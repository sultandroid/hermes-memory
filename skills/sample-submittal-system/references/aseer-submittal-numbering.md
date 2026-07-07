# Aseer Museum — Document Numbering Scheme

## Register Log Format

```
MOC-MUS-ASE-1X0-YY-NNNN
```

| Segment | Meaning | Examples |
|---------|---------|----------|
| MOC | Project / Client code | Mace on behalf of Muheel Oil Company |
| MUS | Facility type | Museum |
| ASE | Location | Aseer |
| 1X0 | Zone / Level | 1A0 (Zone 1A, Level 0) |
| YY | Document type | MA (Material Approval), RFI, TQ, SUB |
| NNNN | Sequential number | 0007 |

## Document Type Codes

| Code | Type | Use |
|------|------|-----|
| MA | Material Approval | Sample submittal approvals |
| RFI | Request for Information | Technical clarifications |
| TQ | Technical Query | Design intent questions |
| SUB | Submittal | General submittals |

## Key Document References (Aseer Museum)

| Document | Reference |
|----------|-----------|
| Master Programme | MOC-ASEER-GN-DS-006 |
| HSE Plan | PL-0010 |
| Document & Data Management Plan (DMP) | PL-0029 |
| BEP | PL-0015 |
| Communications Plan | PL-0018 |
| Project Quality Plan (PQP) | 0Q0-PL-0011 |

## Sample-Related Submittal Convention

Each physical material sample folder carries its **MA number** on the cover label:
`MOC-MUS-ASE-1A0-MA-0007`

The MA number ties the physical folder to the formal Aconex transmittal / RFI workflow:

1. Tech Office drafts sample folder with MA number
2. DC (Document Control) assigns ref at issue
3. Response deadlines managed via Aconex DS form, not the doc body
4. Distribution: MoC · CG · PMC · Samaya
5. Add "WITHOUT PREJUDICE" on scope-boundary submittals

## Cross-Reference

- `sample.json` includes `submittal_ref` field matching this MA number
- QR URL `samaya-factory.com/Samples/{CODE}` is the digital twin of the physical folder
