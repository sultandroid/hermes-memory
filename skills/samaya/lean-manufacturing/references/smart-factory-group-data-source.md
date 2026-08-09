# Smart Factory Telegram Group — Data Source for the Lean System

Collected 2026-08-08. The user wants to seed the Lean system with real factory data before deciding whether to move it to Odoo.

## Group identity
- **Chat ID:** `-5440607372` (channel_directory.json name: "Factory", type: group)
- The bot reads this group live but does **not** archive other members' messages in the session DB (`state.db`).
- Group members of interest: **Raoof** (رؤوف, Production Manager) and **Mostafa** (مصطفى) — they will fill the daily checklists once launched.

## Where group messages DO and DO NOT live
- `~/.hermes/state.db` `messages` table stores only the bot's own conversations (DM + the group's replies from Mohamed Essa). **Other members' raw group messages are NOT persisted there.**
- `logs/gateway.log*` — "inbound message" lines are logged, but only for Mohamed Essa's own sends; other members' messages appear only as "Flushing text batch ... (N chars)" with no content.
- Conclusion: **group history is not retrievable from local state** — to harvest real data you must either (a) fetch history via the Telegram Bot API `getUpdates`/`getChatHistory` while live, or (b) capture it going forward once the bot starts logging them.

## Implication for the lean-data harvest
Do not assume past group messages are already in the repo or DB. Plan the harvest as a **going-forward capture** (wire the bot to log/save group messages into the lean intake), or fetch explicitly via the Bot API when the collection phase starts.

## Checklist co-design (user preference)
Before launch, design the daily checklists **together with the user** — Mostafa and Raoof will fill them. Never ship checklists cold; the user wants to avoid confusing the team ("ما نشتتش الناس").
