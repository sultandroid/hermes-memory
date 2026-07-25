# systemd unit template for Hermes Agent gateway

## Why not the default `hermes-gateway.service`?

The default unit name collides with Hermes's self-restart policy. Renaming to `hermes-gw.service` (or similar) lets you run `systemctl restart hermes-gw.service` without triggering the policy. The unit's internal name has no functional impact.

## Recommended unit

Save as `/etc/systemd/system/hermes-gw.service`:

```ini
[Unit]
Description=Hermes Agent Gateway (Telegram)
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=hermes
Group=hermes
WorkingDirectory=/home/hermes/.hermes/profiles/<profile-name>
Environment="PATH=/opt/hermes-agent/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="HOME=/home/hermes"
ExecStart=/opt/hermes-agent/venv/bin/hermes --profile <profile-name> gateway run
Restart=always
RestartSec=10
TimeoutStopSec=210s
StandardOutput=append:/var/log/hermes/gateway.log
StandardError=append:/var/log/hermes/gateway.err.log
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=read-only
ReadWritePaths=/home/hermes /opt/hermes /var/log/hermes

[Install]
WantedBy=multi-user.target
```

Replace:
- `<profile-name>` with your profile (e.g. `default`, `digitalhermes`)
- `WorkingDirectory=` with the profile's directory if using a profile

## Apply

```bash
sudo systemctl daemon-reload
sudo systemctl enable hermes-gw.service
sudo systemctl start hermes-gw.service
sudo systemctl status hermes-gw.service
```

## Critical settings explained

| Setting | Why |
|---------|-----|
| `Restart=always` | Recover from crashes, OOM kills, network blips |
| `RestartSec=10` | 10s between restarts — gives Telegram session lock time to release |
| `TimeoutStopSec=210s` | Hermes `agent.restart_drain_timeout=180s`; 210s gives 30s headroom so systemd doesn't SIGKILL mid-drain |
| `ProtectSystem=full` | Read-only `/`, `/usr`, `/boot`; only `ReadWritePaths` are writable |
| `ProtectHome=read-only` | Read-only `/home`, `/root`, `/run/user` |
| `NoNewPrivileges=true` | No setuid / setgid bit escalation |
| `ReadWritePaths=` | Whitelist: hermes user home, hermes install, log dir |

## Log rotation

The unit uses `StandardOutput=append:` which **never rotates**. Add a logrotate config to avoid filling `/var/log`:

```bash
sudo tee /etc/logrotate.d/hermes-gateway <<'EOF'
/var/log/hermes/gateway.log /var/log/hermes/gateway.err.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 hermes hermes
    sharedscripts
    postrotate
        # Tell the gateway to reopen its log files.
        # If hermes doesn't have SIGHUP support, restart is required.
        systemctl kill -s HUP hermes-gw.service 2>/dev/null || true
    endscript
}
EOF
```

If the gateway doesn't reopen logs on SIGHUP, change `postrotate` to:
```bash
systemctl restart hermes-gw.service
```

## Verifying after deploy

```bash
# 1. Service is active
sudo systemctl is-active hermes-gw.service
# Expect: active

# 2. Process is running with the right profile
ps -ef | grep "venv/bin/hermes" | grep -v grep
# Expect: 1 process with --profile <profile-name>

# 3. Live Telegram connections
ss -tnp state established | grep -E "api.telegram|2001:67c:4e8"
# Expect: 1-3 connections

# 4. No errors in the log
tail -50 /var/log/hermes/gateway.err.log | grep -E "ERROR|FATAL"
# Expect: empty
```

## Remote restart without the self-restart policy

```bash
# From a context that isn't the running gateway
ssh root@server 'systemctl restart hermes-gw.service && sleep 5 && systemctl is-active hermes-gw.service'
```
