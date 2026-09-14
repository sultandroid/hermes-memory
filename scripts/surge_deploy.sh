#!/usr/bin/env bash
# surge_deploy.sh — one entry point for publishing a review page to surge.sh,
# with a version ledger so any agent can tell whether a live domain is current.
#
# Flow: classify -> stage inside the owning repo -> publish -> verify LIVE bytes
#       (not just the 200) -> record the revision in SURGE_DEPLOYMENTS.json.
#
# Classification and the naming convention are defined in SURGE.md §3. This script
# enforces the mechanical half: the domain shape, the in-repo staging path, and the
# ledger entry. It will not invent a prefix or borrow another project's domain.
#
# Usage:
#   surge_deploy.sh deploy <canonical.html> <domain> [--repo <path>]
#   surge_deploy.sh check <domain>            # is the live page current vs the ledger?
#   surge_deploy.sh list                      # the ledger, one line per domain
#   surge_deploy.sh verify-all                # re-check every ledger entry over the network
#
# Credentials are never embedded: the token comes from $SURGE_TOKEN or from the hub
# SURGE.md, and is never written to the ledger or printed.

set -uo pipefail

HUB="${HERMES_HUB:-$HOME/hermes-memory}"
LEDGER="$HUB/SURGE_DEPLOYMENTS.json"
SURGE_MD="$HUB/SURGE.md"

say()  { printf '%s\n' "$*"; }
die()  { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

# ---------------------------------------------------------------- toolchain

PY=""
for c in python python3 py; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done
[ -n "$PY" ] || die "no python on PATH (needed for the JSON ledger)"

resolve_surge() {
  if command -v surge >/dev/null 2>&1; then command -v surge; return 0; fi
  local c
  for c in \
      "${LOCALAPPDATA:-}/Temp/node_modules/.bin/surge" \
      "$HOME/opt/nodejs/bin/surge" \
      "$HOME/.hermes/profiles/digitalhermes/home/opt/nodejs/bin/surge"; do
    if [ -n "$c" ] && [ -x "$c" ]; then printf '%s\n' "$c"; return 0; fi
  done
  return 1
}

resolve_token() {
  if [ -n "${SURGE_TOKEN:-}" ]; then printf '%s\n' "$SURGE_TOKEN"; return 0; fi
  [ -f "$SURGE_MD" ] || return 1
  grep -oE '`[a-f0-9]{32}`' "$SURGE_MD" 2>/dev/null | head -1 | tr -d '`'
}

# MSYS path -> native forward-slash path ("C:/Users/…"). Bash builtins (cd, cp, mkdir,
# test) want the MSYS form; native Windows binaries (python, git, node) reject it.
# Convert at every boundary, never assume either side.
native() { cygpath -m "$1" 2>/dev/null || printf '%s\n' "$1"; }

sha256_of() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1
  else shasum -a 256 "$1" | cut -d' ' -f1; fi
}

git_root_of() {   # nearest .git walking up from a file's directory, "" if none
  local d; d="$(cd "$(dirname "$1")" && pwd)"
  while [ "$d" != "/" ] && [ -n "$d" ]; do
    [ -d "$d/.git" ] && { printf '%s\n' "$d"; return 0; }
    d="$(dirname "$d")"
  done
  printf '\n'
}

# ---------------------------------------------------------------- ledger io

ledger_get() {    # ledger_get <domain> <field>
  "$PY" - "$(native "$LEDGER")" "$1" "$2" <<'PYEOF' | tr -d '\r'
import json, sys
path, domain, field = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
except Exception:
    sys.exit(0)
print(data.get("domains", {}).get(domain, {}).get(field, ""))
PYEOF
}

ledger_put() {    # ledger_put <domain> <json-object>
  "$PY" - "$(native "$LEDGER")" "$1" "$2" <<'PYEOF'
import datetime, json, sys
path, domain, payload = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
except Exception:
    data = {"schema": "surge-deployments/1", "domains": {}}
data.setdefault("domains", {})[domain] = json.loads(payload)
data["updated_at"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
    fh.write("\n")
PYEOF
}

# ---------------------------------------------------------------- live check

live_sha() {      # live_sha <domain> -> sha256 of the bytes served, "" on failure
  # curl.exe is a native binary: it cannot write to an MSYS path like /tmp/xxx,
  # it silently writes elsewhere leaving an empty file behind. Convert the path.
  local tmp code
  tmp="$(native "$(mktemp)")"
  code="$(curl -s -m 90 -L "https://$1/" -o "$tmp" -w '%{http_code}' 2>/dev/null)"
  if [ "$code" != "200" ]; then rm -f "$tmp"; printf 'HTTP%s\n' "$code"; return 1; fi
  sha256_of "$tmp"; rm -f "$tmp"
}

# ---------------------------------------------------------------- actions

do_list() {
  "$PY" - "$(native "$LEDGER")" <<'PYEOF'
import json, sys
with open(sys.argv[1], encoding="utf-8") as fh:
    data = json.load(fh)
rows = data.get("domains", {})
if not rows:
    print("ledger empty — no deploys recorded yet")
    sys.exit(0)
print(f"{len(rows)} domain(s) in the ledger\n")
for domain in sorted(rows):
    r = rows[domain]
    print(f"  {domain}")
    print(f"    project   : {r.get('project','?')}")
    print(f"    repo file : {r.get('owner_repo','?')} :: {r.get('repo_file','?')}")
    print(f"    sha256    : {r.get('sha256','?')[:16]}…  {r.get('bytes','?')} bytes")
    print(f"    deployed  : {r.get('deployed_at','?')}  (repo commit {r.get('repo_commit','?')})")
    print(f"    snapshot  : {r.get('snapshot','—')}")
PYEOF
}

do_check() {
  local domain="$1" want got
  want="$(ledger_get "$domain" sha256)"
  [ -n "$want" ] || die "'$domain' is not in the ledger — nothing to compare against"
  got="$(live_sha "$domain")" || die "live fetch for $domain failed ($got)"
  if [ "$want" = "$got" ]; then
    say "CURRENT   $domain"
    say "          live sha256 matches the ledger (${got:0:16}…)"
  else
    say "STALE     $domain"
    say "          ledger ${want:0:16}…  !=  live ${got:0:16}…"
    say "          the domain is serving bytes that are not the recorded revision"
    return 1
  fi
}

do_verify_all() {
  local domain rc=0
  while IFS= read -r domain; do
    [ -n "$domain" ] || continue
    do_check "$domain" || rc=1
  done < <("$PY" - "$(native "$LEDGER")" <<'PYEOF' | tr -d '\r'
import json, sys
with open(sys.argv[1], encoding="utf-8") as fh:
    print("\n".join(sorted(json.load(fh).get("domains", {}))))
PYEOF
)
  return $rc
}

do_deploy() {
  local src="$1" domain="$2" repo_override="${3:-}"
  [ -f "$src" ] || die "canonical file not found: $src"
  case "$domain" in
    *[A-Z]*|*_*|*" "*) die "domain '$domain' breaks the convention: lowercase and hyphens only" ;;
    *.surge.sh) : ;;
    *) die "domain must end in .surge.sh (got '$domain')" ;;
  esac

  local slug="${domain%.surge.sh}"
  local repo="$repo_override"
  [ -n "$repo" ] || repo="$(git_root_of "$src")"
  [ -n "$repo" ] || die "no git repo around '$src' — surge staging must live inside the owning repo (SURGE.md §3 step 3)"

  local stage="$repo/_PUBLISH/$slug"
  mkdir -p "$stage"
  cp "$src" "$stage/index.html"
  printf '%s\n' "$domain" > "$stage/CNAME"

  local src_sha stage_sha
  src_sha="$(sha256_of "$src")"
  stage_sha="$(sha256_of "$stage/index.html")"
  [ "$src_sha" = "$stage_sha" ] || die "staging copy differs from the canonical file"

  local token surge_cli
  token="$(resolve_token)"; [ -n "$token" ] || die "no surge token (\$SURGE_TOKEN unset and none found in SURGE.md)"
  surge_cli="$(resolve_surge)" || die "surge CLI not found (see SURGE.md §2)"

  say "deploying $src"
  say "  domain : $domain"
  say "  repo   : $repo"
  say "  stage  : ${stage#$repo/}/index.html"
  say "  sha256 : ${src_sha:0:16}…  ($(wc -c < "$src" | tr -d ' ') bytes)"
  say ""

  local out snapshot
  out="$(cd "$stage" && SURGE_TOKEN="$token" "$surge_cli" publish ./ "$domain" 2>&1)" || {
    printf '%s\n' "$out"; die "surge publish failed"; }
  printf '%s\n' "$out" | grep -E 'Success|Production|Live preview|error|Error' || true
  snapshot="$(printf '%s\n' "$out" | grep -oE '[0-9]{13}-[a-z0-9.-]+\.surge\.sh' | head -1)"

  say ""
  # Right after a publish the edge can still serve the previous body for a few
  # seconds, so a single read is not evidence. Retry before declaring a mismatch.
  local got attempt
  for attempt in 1 2 3 4 5 6; do
    got="$(live_sha "$domain")" || die "post-deploy verify failed ($got)"
    [ "$got" = "$src_sha" ] && break
    say "  … edge not settled (attempt $attempt: ${got:0:12}…), retrying"
    sleep 5
  done
  if [ "$got" != "$src_sha" ]; then
    die "LIVE BYTES MISMATCH after deploy — ledger not written (live ${got:0:16}… vs source ${src_sha:0:16}…)"
  fi
  say "verified  live sha256 == source sha256 (${got:0:16}…)"

  local repo_commit hub_commit
  repo_commit="$(git -C "$(native "$repo")" rev-parse --short HEAD 2>/dev/null || echo '')"
  hub_commit="$(git -C "$(native "$HUB")" rev-parse --short HEAD 2>/dev/null || echo '')"

  ledger_put "$domain" "$("$PY" - "$(native "$src")" "$domain" "$slug" "$(native "$repo")" "$src_sha" "$snapshot" "$repo_commit" "$hub_commit" "$(wc -c < "$src" | tr -d ' ')" <<'PYEOF'
import json, os, subprocess, sys, datetime
src, domain, slug, repo, sha, snapshot, rcommit, hcommit, nbytes = sys.argv[1:10]

def sh(cmd, cwd=None):
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True).stdout.strip()
    except Exception:
        return ""

owner = sh(["git", "-C", repo, "remote", "get-url", "origin"])
owner = owner.replace("https://github.com/", "").replace(".git", "").split(":")[-1]

print(json.dumps({
    "project": os.path.basename(repo),
    "owner_repo": owner,
    "repo_file": os.path.basename(src),
    "stage_dir": f"_PUBLISH/{slug}",
    "sha256": sha,
    "bytes": int(nbytes),
    "snapshot": snapshot or None,
    "repo_commit": rcommit,
    "hub_commit": hcommit,
    "verified_http": 200,
    "deployed_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
}, ensure_ascii=False))
PYEOF
)"

  say ""
  say "recorded in $(basename "$LEDGER")"
  [ -n "$snapshot" ] && say "frozen snapshot: https://$snapshot/"
  say "live: https://$domain/"
}

do_seed() {       # baseline an ALREADY-live domain that predates the ledger
  local domain="$1" repo_override="${2:-}" got slug repo repo_commit
  got="$(live_sha "$domain")" || die "cannot read https://$domain/ ($got)"
  slug="${domain%.surge.sh}"
  repo="$repo_override"
  if [ -n "$repo" ]; then
    [ -d "$repo" ] || die "repo not found: $repo"
  else
    repo=""
  fi
  say "baseline  $domain"
  say "  live sha256 : ${got:0:16}…"
  say "  NOTE: baselined from the live edge, not from a publish performed here."
  say "        Re-run 'deploy' with the canonical file to bind it to source control."
  ledger_put "$domain" "$("$PY" - "$domain" "$slug" "$got" "${repo:-}" <<'PYEOF'
import datetime, json, os, subprocess, sys
domain, slug, sha, repo = sys.argv[1:5]

def sh(cmd, cwd=None):
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True).stdout.strip()
    except Exception:
        return ""

owner = sh(["git", "-C", repo, "remote", "get-url", "origin"]) if repo else ""
owner = owner.replace("https://github.com/", "").replace(".git", "").split(":")[-1]
print(json.dumps({
    "project": os.path.basename(repo) if repo else "(unmapped)",
    "owner_repo": owner,
    "repo_file": None,
    "stage_dir": f"_PUBLISH/{slug}",
    "origin": "baseline-observed",
    "sha256": sha,
    "repo_commit": sh(["git", "-C", repo, "rev-parse", "--short", "HEAD"]) if repo else "",
    "verified_http": 200,
    "baselined_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
}, ensure_ascii=False))
PYEOF
)"
}

# ---------------------------------------------------------------- entry

cmd="${1:-}"; shift || true
case "$cmd" in
  deploy)
    [ $# -ge 2 ] || die "usage: surge_deploy.sh deploy <canonical.html> <domain> [--repo <path>]"
    src="$1"; domain="$2"; shift 2
    repo=""
    if [ "${1:-}" = "--repo" ]; then repo="${2:-}"; fi
    do_deploy "$src" "$domain" "$repo" ;;
  check)      [ $# -ge 1 ] || die "usage: surge_deploy.sh check <domain>"; do_check "$1" ;;
  seed)       [ $# -ge 1 ] || die "usage: surge_deploy.sh seed <domain> [--repo <path>]"
              domain="$1"; shift; repo=""
              [ "${1:-}" = "--repo" ] && repo="${2:-}"
              do_seed "$domain" "$repo" ;;
  list)       do_list ;;
  verify-all) do_verify_all ;;
  *)          sed -n '2,20p' "$0"; exit 2 ;;
esac
