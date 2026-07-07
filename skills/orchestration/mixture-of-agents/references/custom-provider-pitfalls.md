# Custom Provider Pitfalls

## The ollama-cloud case

`ollama-cloud` is a **custom/private provider**, not the public ollama.com API. It appears in Hermes config as a provider slug but has no standard base URL or API key — those must be obtained from the user.

### What went wrong in the originating session

1. Agent saw `provider: ollama-cloud` in Hermes config and assumed it was a misconfigured local Ollama.
2. Installed Ollama, pulled 4 models (~12 GB), configured moa-cloud for local inference.
3. User corrected: "I didn't use local LLM, remove it."
4. Agent uninstalled Ollama, deleted models, but then asked for the ollama-cloud URL/key — which the user hasn't provided yet.
5. The config.yaml.bak (which contained the original ollama-cloud settings) was deleted prematurely before the new setup was confirmed working.

### Lessons

- **Never assume a provider name maps to a known service.** `ollama-cloud` is not `ollama.com`. Ask for base URL and API key before any configuration.
- **Backup before destructive changes.** Keep the backup until the new setup is verified working.
- **When the user says "remove," don't suggest replacements.** They want deletion, not migration.
- **If you don't know the provider's details, stop and ask.** Don't proceed with guesses.
