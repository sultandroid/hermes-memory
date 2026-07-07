# QR Landing Page Deployment

Each sample folder has a QR code on the label linking to `samaya-factory.com/Samples/{CODE}/`.

## Files needed for deployment

```
sample-folder/
  index.html          ← Landing page (photo, specs, download links)
  photo-{CODE}.jpg    ← Sample photo
  qr-{CODE}.png       ← QR code image
  datasheet-*.pdf     ← TDS/technical datasheets
  test-report-*.pdf   ← Test reports
```

## Server structure (samaya-factory.com)

This hosting uses a `.htaccess` rewrite rule:
```
RewriteRule ^(.*)$ /build/$1 [L]
```
So `samaya-factory.com/Samples/CODE/` maps to `domains/samaya-factory.com/public_html/build/Samples/CODE/`.

## Deploy steps

```bash
# 1. Stage files in a temp directory
mkdir -p /tmp/deploy && cd /tmp/deploy
cp /path/to/sample-folder/index.html .
cp /path/to/sample-folder/photo-*.jpg .
cp /path/to/sample-folder/qr-*.png .
cp /path/to/sample-folder/datasheet-*.pdf .

# 2. Create remote directory
ssh -p 65002 u517606786@samaya-factory.com \
  'mkdir -p domains/samaya-factory.com/public_html/build/Samples/{CODE}'

# 3. Upload via tar pipe
tar czf - . | ssh -p 65002 u517606786@samaya-factory.com \
  'cd domains/samaya-factory.com/public_html/build/Samples/{CODE} && tar xzf - && chmod 644 *.*'

# 4. Verify
curl -s -o /dev/null -w "%{http_code}" "https://samaya-factory.com/Samples/{CODE}/"
```

## Permission fix

Files uploaded via tar pipe preserve local permissions. The web server needs `644` (readable by all). Always run `chmod 644 *.*` after extraction.

## Landing page content

Include in `index.html`:
- Project info from DMP in the header (project reference, client, consultant, designer)
- Sample photo with specs
- Download buttons for each datasheet PDF
- QR code (redundant — already on the printed label, but useful for digital visitors)
