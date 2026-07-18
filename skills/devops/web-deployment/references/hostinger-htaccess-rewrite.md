# Hostinger `.htaccess` Rewrite Rule — samaya-factory.com

## The Rule

The root `.htaccess` at `~/domains/samaya-factory.com/public_html/.htaccess` contains:

```apache
RewriteEngine on
RewriteCond %{HTTP_HOST} ^samaya-factory.com$ [NC,OR]
RewriteCond %{HTTP_HOST} ^://samaya-factory.com$ [NC]
RewriteCond %{REQUEST_URI} !^/build/
RewriteRule ^(.*)$ /build/$1 [L]
```

**Effect:** Every request to `https://samaya-factory.com/PATH` is internally rewritten to `/build/PATH`. Files must be placed under `public_html/build/`, not `public_html/`.

## Impact

| If you upload to | URL resolves? | Notes |
|-----------------|:-------------:|-------|
| `public_html/assets/logos/logo.png` | ❌ 404 | Rewrite sends to `/build/assets/logos/logo.png` |
| `public_html/build/assets/logos/logo.png` | ✅ 200 | Correct location |

## Fix

Always create directories and upload under `public_html/build/`:

```bash
ssh -p 65002 user@host "mkdir -p ~/domains/samaya-factory.com/public_html/build/assets/logos"
cat local-file.png | ssh -p 65002 user@host "cat > ~/domains/samaya-factory.com/public_html/build/assets/logos/file.png"
```

## Verification

```bash
curl -s -o /dev/null -w "%{http_code}" https://samaya-factory.com/assets/logos/file.png
# Expected: 200
```

## Detection

If a file uploads successfully (visible via `ls` on server) but returns 404 via HTTP, check `.htaccess` for a rewrite rule. The symptom is: file exists on disk, curl returns 404.
