# Import Logistics Multiplier Matrix — KSA Landed Cost

## Purpose

When verifying BoQ prices against origin-country market prices, apply the correct logistics multiplier to convert FOB/EXW prices to KSA landed (delivered, duty-paid) cost. Do NOT accept BoQ USD prices at face value — they often exclude ALL import costs.

## Multipliers by Origin

| Origin | Multiplier | Column Label | Breakdown Detail |
|--------|-----------|-------------|------------------|
| **EU** | ×1.33 | Import_EU | Shipping 4% + Insurance 0.4% + Customs 5.2% + Clearance 2.5% + Bank 1% + Distributor 17.5% + Contingency 2.4% = 33% |
| **USA** | ×1.25 | Import_US | Shipping 3% + Insurance 0.4% + Customs 5.2% + Clearance 2.5% + Bank 1% + Distributor 15% = 25% |
| **China** | ×1.20 | Import_China | Shipping 5% + Insurance 0.4% + Customs 5.2% + Clearance 2.5% + Bank 1% + Distributor 12% = 20% |
| **Local KSA** | ×1.00 | Local_KSA | No import costs — use local supplier price |
| **Mixed Origin** | ×1.15 | Mixed | Average of partial import + local content |

## Brand → Origin Classification

### Import_EU (×1.33)
| Category | Brands / Keywords |
|----------|------------------|
| Lighting | DGA (Ariel, Tono, Armonia), FLOS, Prolights, LUXAM, Cooledge, XLINE, Twils, DESIGNCONCEPTS |
| Lighting control | Enttec, Eldoled, LTECH, DMX, Visual Production (CueCore, B Station, Kiosc Touch) |
| Furniture | Calligaris, B&B Italia, Poltrona Frau, Molteni&C, LAGO, ACERBIS, BK CONTRACT, ARTEMEST, Laskasas, Draenert, NORR11, brunner, gianfranco |
| Ceiling | Barrisol, Leben |
| AV processing | Brainsalt, Seki Han |

### Import_US (×1.25)
| Brand | Products |
|-------|----------|
| Epson | Projectors, lenses (PU1007B, PQ2008B, ELPLM08) |
| QSC | Ceiling speakers, subwoofers (AD-C4T-LPZB, AD-S112SW) |
| Crestron | Control systems, touch panels (PMC2, TSW-770) |
| Brightsign | Media players (XT1144) |
| Cisco | Networking (SF350-48) |
| Eaton | Power (UPS 9PX) |
| Nexmosphere | Sensors (XM-7-25) |
| Chief | Mounts (RPMA, XS1U) |
| Iiyama | Displays (TF5515-B1AG) |
| Binepad | Controllers (Rotary Encoder V2) |
| Exact Solutions | PrimeT-CU-32 |

### Import_China (×1.20)
| Brand | Products |
|-------|----------|
| LOPU | LED tiles (LP-TC2.6 floor, LP-P1.2 GOB, LP-P1.25 flexible) |
| Muxwave | Transparent LED (M2 P2.5, MX-P2.9) |
| Brainsalt | Media servers, USB encoders |

### Mixed Origin (×1.15)
| Category | Rationale |
|----------|-----------|
| Marble | Italian/Egyptian import + KSA fabrication |
| Carpet | European fibre + KSA installation |
| Aluminum ceiling | Import coils + local fabrication |
| Glass | Float glass import + local processing |
| Acoustic fabric | Import fabric + local installation |
| Corian/Dibond | Import sheet + local fabrication |
| Steel | Import raw + KSA fabrication |

### Local KSA (×1.00)
| Category | Examples |
|----------|----------|
| Civil | Demolition, blockwork, concrete |
| Paint | Jotun, Sigma, Caparol — made in KSA |
| Gypsum | Saudi Gypsum, Almana boards |
| Drywall | Local installation labour |
| MDF/carpentry | Local joinery, Sadu |
| Installation | Labour for AV, lighting, exhibition fit-out |
| Graphics | Local print production |
| Riyadh stone | Local stone cladding |

## Dimensional Conversion Logic

When classifying items in openpyxl automation:

```python
# Classify an item by brand keyword → origin → multiplier
CLASSIFICATION_RULES = [
    # Format: (brand_keywords, import_category, multiplier)
    (['dga', 'flos', 'armonia', 'tоno', 'ariel', 'prolights', 'luxam',
      'cooledge', 'enttec', 'eldoled', 'ltech', 'dmx', 'cuecore', 'b station',
      'calligaris', 'b&b italia', 'poltrona', 'molteni', 'lago', 'laskasas',
      'draenert', 'norr11', 'acerbis', 'bk contract', 'artemest', 'brainsalt',
      'barrisol', 'leben', 'brunner', 'xline', 'twils', 'designconcepts'], 'Import_EU', 1.33),
    (['epson', 'qsc', 'crestron', 'brightsign', 'cisco', 'nexmosphere',
      'chief', 'iiyama', 'binepad', 'exact solutions', 'eaton ups'], 'Import_US', 1.25),
    (['lopu', 'muxwave'], 'Import_China', 1.20),
]

def classify_item(description):
    """Returns (import_category, multiplier)."""
    d = str(description).lower() if description else ''
    for keywords, category, multiplier in CLASSIFICATION_RULES:
        for kw in keywords:
            if kw.lower() in d:
                return (category, multiplier)
    return ('Local_KSA', 1.0)
```

## Multipliers Applied as Percentage Add-Ons

| Cost Component | EU | US | China | Local |
|---------------|:--:|:--:|:-----:|:-----:|
| Ocean/air freight | 4% | 3% | 5% | — |
| Marine insurance | 0.4% | 0.4% | 0.4% | — |
| Saudi Customs (5% duty) | 5.2% | 5.2% | 5.2% | — |
| Clearance & handling | 2.5% | 2.5% | 2.5% | — |
| Bank charges / LC | 1% | 1% | 1% | — |
| Distributor margin | 17.5% | 15% | 12% | — |
| Contingency (incidental) | 2.4% | 1.9% | 1.6% | — |
| TOTAL | **33%** | **25%** | **20%** | **0%** |

## Example: Landed Cost Calculation

| Step | AV Item (Epson from US) | Lighting (DGA from EU) | LED (LOPU from China) |
|------|------------------------|----------------------|----------------------|
| Origin price (FOB) | $10,000 | €1,000 ($1,158) | $600 (FOB Shenzhen) |
| × multiplier | ×1.25 | ×1.33 | ×1.20 |
| Landed base ($) | $12,500 | $1,540 | $720 |
| Hidden costs (3%) | $375 | $46 | $22 |
| Overhead (7%) | $875 | $108 | $50 |
| Profit (15%) | $2,063 | $254 | $119 |
| **All-in ($)** | **$15,813** | **$1,948** | **$911** |
| vs BoQ price | $10,000 +58% | $1,158 (no markup!) +68% | $600 +52% |

## Evidence Source Preferences by Import Type

| Import Type | Best Source | Backup Source |
|-------------|-------------|---------------|
| EU | Manufacturer website (EUR list) | European design retailer website |
| US | B&H Photo Video (USD) | Manufacturer MSRP or CDW |
| China | Alibaba (FOB) | Competitor Chinese brand (Absen, Unilumin) |
| KSA | Local supplier quotation | Previous Samaya project benchmark |
