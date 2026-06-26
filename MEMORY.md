Aseer Museum: PD M.Waris Khan. CG docs cite only ER/SOW/DMP. MEP Designer scope: power distribution to specialist systems only — NOT system design. FM200 in firefighting. Toilets=limited.
§
Samaya Odoo PO cashout: state=purchase/done, exclude full-received <1K SAR. Paid: P00893,P00744,P01154,P01331,P01289,P01227,P01222,P01023,P00908,P01587. Outside Odoo: P01094. Supplier 1224=Saba Najad bank Mada Aljezera — vendor accounts Samaya owes, not cash.
§
RCRC Exhibition: Odoo 324. Designer BMA (borismicka.com). BoQ base $8.18M. AV: LED P1.2-P2.6, Epson, QSC, Crestron. Files in _PRICING_DOCS/. codex 0.128.0, kimi 1.47.0. Fugu (`codex-fugu`) Sakana AI model — rate-limited, best for structured audits. Samaya official logo: `_Style-Guides/samaya-rfi-style-guide/assets/samaya.png` (1885x621, not Docs/Branding).
§
Claude Code auth fix: `claude -p` returns 401 when OAuth token expires (~4-5 day lifetime). Check `~/.claude/.credentials.json` expiresAt field. Fix: `cp ~/.claude/.credentials.json{,.bak} && rm ~/.claude/.credentials.json && claude auth login` (not `claude login` — use `auth login` subcommand). This opens browser for OAuth. After sign-in, `claude -p` works again.
§
OneDrive macOS: Never `mv` files in OneDrive — triggers TCC sandbox lock. Use Finder/AppleScript for cross-sandbox file ops. Stage to /tmp before delegating to sandboxed labors.