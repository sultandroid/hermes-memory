# Aseer Museum Gallery Data Structure

## Gallery entry format

```typescript
interface GalleryData {
  id: string;       // short key like 'g4', 'g7', 'lb3', 'ec'
  title: string;    // display name like 'G4 – Saudi Art'
  floor: string;    // 'basement' | 'lower-ground' | 'ground'
  views: View[];    // array of view objects
}

interface View {
  viewName: string;     // unique name like 'G4_View_1'
  filename: string;     // path like '/aseer/images/g4_G4_View_1.jpg'
  desc: string;         // description
  hotspots: Hotspot[];  // material hotspots (can be empty [])
}
```

## Floor classification (from NRS folder names)

| floor value | NRS folder | VIS range |
|-------------|-----------|-----------|
| `basement` | 0_BASEMENT | VIS001–VIS016 |
| `lower-ground` | 1_LOWER GROUND FLOOR | VIS017–VIS020 |
| `ground` | 2_Ground Floor | VIS021–VIS025 |

## Gallery-to-VIS mapping (from location plan PDFs)

### Basement (BF)
| Gallery | VIS images |
|---------|-----------|
| G4 Saudi Art | g4_G4_View_1.jpg, g4_G4_View_2.jpg |
| G5 Making Space | g5_G5_View_11B.jpg |
| G6 Saudi Art | g6_G6_View_3.jpg, g6_G6_View_3B.jpg, g6_G6_View_4.jpg |
| G7 Reem Alnasser | bf_VIS13.jpg |
| G8 Al Qatt | g8_G8_View_5.jpg, g8_G8_View_6.jpg |
| G9 Flowersmen | g9_G9_View_7.jpg |
| G10 Faisal Samra | bf_VIS14.jpg |
| G11 Script | g11_G11_View_8.jpg, g11_G11_View_8B.jpg |
| G12 Archaeology | g12_G12_View_9.jpg, g12_G12_View_10.jpg, g12_G12_View_10B.jpg |
| G13 Tarek Atoui | bf_VIS15.jpg |
| LB3 Lobby | lb3_LB3_View_11.jpg, lb3_LB3_View_12.jpg |

### Lower Ground (LGF)
| Gallery | VIS images |
|---------|-----------|
| G1 Welcome Gallery | lgf_VIS17.jpg, lgf_VIS18.jpg |
| G2 Ayman Zedani | lgf_VIS19.jpg |
| G3 Al Muftaha | lgf_VIS20.jpg |
| G14 Hamra Abbas | lgf_VIS20.jpg |
| LB2 King Khaled | lgf_VIS17.jpg |

### Ground Floor (GF)
| Gallery | VIS images |
|---------|-----------|
| LB1 Al Bahar | gf_VIS21.jpg |
| EC Education Centre | gf_VIS22.jpg |
| RT Retail | gf_VIS23.jpg |
| VI VIP Reception | gf_VIS24.jpg |

## Image naming convention

- Original NRS images: `MOC-ASE-AR-ARC-{FLOOR}-DDD-VIS{NNN}.jpg`
- Copied to repo as: `{floor_prefix}_VIS{NNN}.jpg` where floor_prefix = `bf_`, `lgf_`, `gf_`
- Existing gallery images (from earlier NRS renders): `g{NN}_G{NN}_View_{N}.jpg` or `lb3_LB3_View_{N}.jpg`

## Server image paths

All images served from: `/aseer/images/{filename}.jpg`
URL: `https://samaya-factory.com/aseer/images/{filename}.jpg`

New images uploaded via SCP get 700 permissions — must `chmod 644` or they return 403.
