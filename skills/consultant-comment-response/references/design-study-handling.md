# Design Study Handling — NRS Cost Notification Pattern

When NRS submits a Design Study in response to CG/Ministry requests (e.g., object schedule changes, gallery redesigns), it typically includes:

1. **Design proposals** per gallery (showcase changes, new elements)
2. **Additional time/cost** — Director + Senior Designer days at agreed rates
3. **Actions required from Samaya** (structural, logistics, etc.)

## Workflow

### 1. Read the study

Extract the full email body via AppleScript. Identify:
- Which galleries are affected
- What changes are proposed
- What Samaya-side actions are required
- The additional cost claimed

### 2. Create team assignment templates

For structural/logistics actions (e.g., G12 Archaeology 3-4 ton stone), create fill-in-the-blank templates:

**Structural template** covers:
- Loading assessment of object on slab/screed/tiling
- Plinth design including spreader plates
- Slab capacity and reinforcement requirements

**Logistics template** covers:
- Method statement for moving object into basement
- Access route, lifting equipment, handling procedure
- Safety considerations and required approvals

### 3. Draft cost notification email

Send to Project Manager (Waris) and Adel Darwish:

```
Subject: NRS Design Study [NUMBER] — Additional Time/Cost Incurred

Dear Eng. Waris and Eng. Adel,

NRS has submitted Design Study [NUMBER] in response to [CG/Ministry request].
The study covers changes to [galleries].

Jim Richards has noted the following additional time spent:

- Director: [N] days @ [rate] SAR/day = [total] SAR
- Senior Designer: [N] days @ [rate] SAR/day = [total] SAR
- Total: [total] SAR

Please advise how you want to proceed regarding this cost — is this within
NRS's existing scope or do we need to raise a variation/PO?

Regards,
Mohamed Sultan
```

### 4. Track the cost

- Note the additional cost in project cost tracking
- Confirm with PM whether it's in-scope or a variation
- If variation, raise PO before NRS issues the study formally

## Pitfalls

- NRS rates: Director ~9,000 SAR/day, Senior Designer ~4,500 SAR/day (verify per contract)
- The study is sent as DRAFT — formal issue comes after Samaya confirms acceptance of cost
- Structural/logistics actions on Samaya side may need separate budget
- The study may affect the CRS response (showcase changes may resolve some CG comments)
