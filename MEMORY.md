MacBook Pro M4 Pro, 48GB RAM. Brew + Docker installed.
§
Cloud-only AI. Rejected local LLMs — uninstalled ollama, mlx, mlx-c; deleted ~/.ollama, ~/moa.
§
Cost-conscious + quality-driven. Wants 4-6 proposers (pushed back on 3). DeepSeek required. Speed-sensitive — wants streaming, speculative kickoff, heuristic routing.
§
OpenRouter as cloud gateway (single key, multi-provider). Hermes `ollama` MoA profile active. OpenRouter key NOT in env/keychain/rc as of 2026-07-01 — must be provided manually.
§
~/moa-cloud/ ready: 4 simple + 6 complex props (qwen-72b/7b, gemini-flash, llama-8b, deepseek-chat/coder), agg qwen-72b, router gemini-flash. Has heuristic gate, speculative kickoff, streaming agg, per-tier max_tokens. Untested.
§
Hands-on executor. Runs commands, checks env, expects working CLI not theory. Fix-not-describe.