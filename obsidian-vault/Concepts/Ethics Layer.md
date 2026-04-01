---
Type: Concept
Tags: [ethics, architecture, api-agnostic, wrapper]
Created: 2026-04-01
---

# Ethics Layer

## The Brain Doesn't Matter. The Character Does.

The Ethics Layer is [[NiceBot]]'s core architectural idea: a separate instance that wraps ANY powerful AI model and filters its outputs through a fixed set of axioms. It does not matter whether the underlying model is Claude, GPT, Gemini, Llama, or something that does not exist yet. The Ethics Layer is model-agnostic, API-agnostic, and provider-agnostic.

## How It Works

Every request to a wrapped model passes through NiceBot's 5-axiom gate before execution. The Ethics Layer intercepts the prompt, evaluates the intended action against each axiom, and either passes it through, modifies it, or blocks it with an explanation. This is not censorship — it is character. The model can still do powerful things. It just cannot cause unnecessary suffering, concentrate power, or undermine human agency while doing them.

## Why a Separate Instance

Baking ethics into the model itself is fragile. Fine-tuning drifts. RLHF optimizes for approval, not for ethics. Jailbreaks bypass internal guardrails. A separate Ethics Layer is immune to these failure modes because it operates outside the model's weights. Even if the underlying model is fully uncensored, NiceBot's layer still applies. See [[Axiom V — Actively limit its own power]] for how this extends to NiceBot limiting itself.

## API-Agnostic Design

The Ethics Layer connects via standard interfaces — REST, MCP, function calling — so it can wrap any model that exposes an API. Swap Claude for GPT-5 tomorrow; the ethical guardrails remain identical. This is critical for the [[Defensive Guardian]] pattern, where NiceBot must protect regardless of which model is doing the heavy lifting underneath.

## The Key Insight

Ethics is not a feature of intelligence. It is a constraint on power. The smartest model in the world without ethical constraints is just a very efficient tool for whoever controls it. The Ethics Layer ensures that power always passes through character first.
