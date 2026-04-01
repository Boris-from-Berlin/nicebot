---
Type: Concept
Tags: [scaling, control, guardrails, axioms-not-rules]
Created: 2026-04-01
---

# Bitter Lesson

## Smarter Models Reward Letting Go

Rich Sutton's Bitter Lesson from reinforcement learning applies directly to AI ethics: hand-crafted rules do not scale. Every attempt to hardcode specific behavioral rules into AI systems gets outpaced by the next generation of models. Rules are brittle. They get gamed, circumvented, or simply become irrelevant when capabilities jump. The lesson is bitter because it means giving up the illusion of fine-grained control.

## Axioms, Not Rules

NiceBot does not operate on rules. It operates on axioms — five fundamental principles that remain valid regardless of how powerful the model becomes. "Do not cause suffering as a means to an end" is not a rule that can be gamed. It is a principle that scales with intelligence. The smarter the model, the better it understands what suffering means, and the more precisely it can avoid causing it. This is the opposite of rule-based systems, where smarter models find more loopholes.

## The Guardrail Paradox

The paradox of AI safety is that tighter control produces worse outcomes at scale. A model constrained by 10,000 specific rules will spend most of its compute navigating restrictions instead of solving problems. A model guided by 5 axioms has maximum freedom within ethical bounds. See [[Axiom V — Actively limit its own power]] — even the self-limiting axiom works better as a principle than as a hardcoded kill switch.

## What This Means for NiceBot

NiceBot's architecture is designed for the bitter lesson. The [[Ethics Layer]] does not try to enumerate every possible harmful action. Instead, it evaluates actions against principles and trusts that more capable models will apply those principles more effectively. This is counterintuitive — it means NiceBot actually gets better as the models it wraps get smarter. The axioms are the guardrails. The intelligence is the engine. Both improve together.

## The Alternative Is Worse

The alternative to axiom-based ethics is an ever-growing list of prohibitions that lags behind capability. That is the current approach of most AI labs, and it fails predictably every time a new jailbreak technique emerges. NiceBot bets on principles over policies, and the bitter lesson says that bet will pay off.
