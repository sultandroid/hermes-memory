# SSH Pipe Deployment (SCP Alternative)

## When SCP hangs
On Hostinger/shared hosting (port 65002), `scp -P 65002` often hangs at "Authenticating to..." even though SSH works fine with `-o BatchMode=yes`. Use the pipe pattern instead:

```bash
# Upload archive
tar czf /tmp/update.tar.gz index.html assets/ sync.php
ssh -p 65002 user@host "cat > /tmp/update.tar.gz" < /tmp/update.tar.gz

# Extract on server
ssh -p 65002 user@host "cd /target/path && tar xzf /tmp/update.tar.gz && rm /tmp/update.tar.gz"
```

## Incremental deploy (changed files only)
Don't redeploy the full dist every time. Only deploy what changed:
1. Build: `vite build`
2. Check what files changed (compare new hashes)
3. Pack only: `index.html`, new `assets/index-*.js`, new `assets/index-*.css`, `sync.php`
4. Upload + extract on server
5. Old JS/CSS files remain on server but are no longer referenced by `index.html`
