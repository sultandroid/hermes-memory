# PHP Sync Server — Full Reference

Copy of the complete PHP sync server, as used in the Aseer Museum interactive app (Jun 2026).

## Directory layout

```
webroot/
├── index.html          # SPA entry
├── assets/             # JS/CSS/images
├── sync.php            # ← this file
└── hotspot-data/       # ← created automatically on first POST
    ├── g4_G4_View_1.json
    ├── g6_G6_View_3.json
    └── ...
```

## Server requirements

- PHP 7.4+ (tested on Hostinger/LiteSpeed with PHP 8.3)
- Write permissions on the webroot directory
- No database needed

## Full PHP code

```php
<?php
/**
 * Hotspot sync endpoint — one file, no database.
 *
 * GET  /sync.php?gallery=X&view=Y   → returns hotspot JSON array
 * POST /sync.php                     → body: JSON { gallery, view, hotspots }
 * GET  /sync.php?export=1            → returns all hotspot data
 */

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

$dataDir = __DIR__ . '/hotspot-data';
if (!is_dir($dataDir)) mkdir($dataDir, 0755, true);

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Export all
    if (isset($_GET['export'])) {
        $all = [];
        foreach (glob("$dataDir/*.json") as $f) {
            $key = basename($f, '.json');
            $all[$key] = json_decode(file_get_contents($f), true) ?? [];
        }
        header('Content-Type: application/json');
        echo json_encode($all);
        exit;
    }

    // Single gallery/view
    $gallery = $_GET['gallery'] ?? '';
    $view = $_GET['view'] ?? '';
    if (!$gallery || !$view) { http_response_code(400); echo '[]'; exit; }
    $key = "{$gallery}_{$view}";
    $file = "$dataDir/{$key}.json";
    header('Content-Type: application/json');
    if (file_exists($file)) {
        echo file_get_contents($file);
    } else {
        echo '[]';
    }
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $body = json_decode(file_get_contents('php://input'), true);
    if (!$body || !isset($body['gallery']) || !isset($body['view']) || !isset($body['hotspots'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing gallery, view, or hotspots']);
        exit;
    }
    $key = "{$body['gallery']}_{$body['view']}";
    $file = "$dataDir/{$key}.json";
    file_put_contents($file, json_encode($body['hotspots'], JSON_PRETTY_PRINT));
    header('Content-Type: application/json');
    echo json_encode(['ok' => true, 'count' => count($body['hotspots'])]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed']);
```

## API endpoints

| Method | URL | Body | Response |
|--------|-----|------|----------|
| GET | `sync.php?gallery=g4&view=G4_View_1` | — | `[{code: "...", x: 50, y: 50}, ...]` or `[]` |
| GET | `sync.php?export=1` | — | `{"g4_G4_View_1": [...], ...}` |
| POST | `sync.php` | `{"gallery":"g4","view":"G4_View_1","hotspots":[...]}` | `{"ok":true,"count":7}` |

## Reset all data

```bash
ssh user@host "rm -rf ~/domains/domain.com/public_html/app/hotspot-data/"
```

## Testing locally

```bash
php -S localhost:8080 sync.php
curl http://localhost:8080/sync.php?gallery=g4&view=test
```
