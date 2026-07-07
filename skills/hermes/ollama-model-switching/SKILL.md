---
name: ollama-model-switching
description: "Handle switching between Ollama Cloud models with context awareness and session restart guidance."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [hermes, model-switching, ollama, cloud-provider]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [hermes-agent]
---

## Overview

This skill automates and documents the workflow for switching between Ollama Cloud models in Hermes Agent. It ensures the model context is properly loaded and provides guidance for session restarts when necessary.

## Key Steps

1. **Verify Active Model:** Check the current active model via `hermes model`.
2. **Switch Model:** Configure the new model in `config.yaml` with the Ollama Cloud provider.
3. **Restart Session:** Restart the session (`/reset` in chat or `hermes` CLI) to ensure the model context loads correctly.

## Configuration

### Provider Setup

Ensure the Ollama Cloud provider is pinned in `config.yaml`:
```yaml
model:
  provider: ollama-cloud
  base_url: https://ollama.com/v1
  api_key: $OLLAMA_API_KEY
```

### Current Model Context

- **Active Model:** `ministral-3:3b` (default Ollama Cloud model).
- **Pitfalls:**
  - Forgetting to restart the session after switching models.
  - Incorrectly configured `base_url` or `api_key` in `config.yaml`.

## Workflow

### Switching Models

1. **Check Current Model:**
   ```bash
   hermes model
   ```

2. **Update `config.yaml`:**
   ```bash
   hermes config set model.provider ollama-cloud
   hermes config set model.base_url https://ollama.com/v1
   hermes config set model.api_key $OLLAMA_API_KEY
   ```

3. **Restart Session:**
   ```bash
   hermes --reset
   ```

## Pitfalls

- **Session Context Loss:** Always restart the session after switching models to ensure the model context is loaded correctly.
- **API Key Exhaustion:** Ensure the `ollama-cloud` API key is valid and not exhausted.
- **Model Unavailability:** Verify the model exists in Ollama Cloud before switching.

## Verification

After switching models, verify the new model is active:
```bash
hermes model
```

If the model is not active, check the logs for errors and ensure the session was restarted properly.

## References

- [Ollama Cloud Provider Setup](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [Hermes Model Configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
---

## References Directory

### references/

- `ollama-model-switching-checklist.md`
  A step-by-step checklist for switching models with Ollama Cloud.