# Deployment to Hostinger (samaya-factory.com) — Retry Pattern

## When the Server is Down

Hostinger shared hosting occasionally becomes unreachable ("No route to host"). When this happens, DO NOT keep trying manually. Use a cron job to retry.

## Cron Job Setup

```bash
# Create the cron job
cronjob action=create \
  name="Deploy RCRC proposal when server is up" \
  schedule="10m" \
  repeat=12 \
  prompt="Deploy the proposal file to samaya-factory.com. File is at /tmp/deploy.html. Run: cat /tmp/deploy.html | ssh -p 65002 -o BatchMode=yes -o ConnectTimeout=15 u517606786@samaya-factory.com 'cat > /home/u517606786/domains/samaya-factory.com/public_html/build/technical-office/Technical-Proposals/RCRC-Exhibition/index.html'. If SSH succeeds, curl check the URL and report HTTP status. If server still down, report and try next cycle. Max 12 attempts (2 hours)."
```

## Why Cron Over Manual Retry

- User doesn't have to ask "did you deploy?" every 5 minutes
- Cron runs in background even when you're working on other tasks
- Rate-limited to one attempt per 10 minutes (avoids hammering the server)
- Auto-removes after success or max attempts reached

## Pre-Deploy Checklist

1. Copy file from OneDrive to `/tmp/deploy.html` FIRST (OneDrive paths cause SSH pipe timeouts)
2. Verify file on server: `ssh -p 65002 ... "ls -lh /path/to/index.html"`
3. HTTP verify: `curl -s -o /dev/null -w "HTTP %{http_code}" --max-time 10 "URL"`
