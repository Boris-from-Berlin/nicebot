---
Type: Concept
Category: Architecture
Tags: #debate #architecture #privacy #autonomy #open-question
Created: 2026-04-01
---

# Architecture Debate — Local vs Cloud

> Where should NiceBot run? This is not a technical question. It's an ethical one.

---

## The question

NiceBot is an ethics agent that scans your data, analyzes your code, and checks your decisions against five axioms. The fundamental question is: **where does this happen?**

Two models exist. Both work. But they have radically different implications for the axioms.

---

## Option A: Local-First (OpenClaw Model) ← current direction

Agents run **on your machine**. Your data never leaves your system. A lightweight dashboard shows status and results, but all processing is local.

**How it works:**
- NiceBot runs as Claude Code sub-agents on your local machine (or your own server)
- Dashboard (app.nicebot.org) is a control panel — it sends tasks and displays results
- Heartbeat model: agents report status, dashboard visualizes
- Communication via WebSocket, data stays local

**Alignment with axioms:**

| Axiom | Score | Why |
|-------|-------|-----|
| I. No suffering as a means | ✓ | No data exploitation possible |
| II. Every being counts | ✓ | Each user has their own instance |
| III. Autonomy is sacred | ✓✓ | Full control. You own everything. |
| IV. Truth before comfort | ✓ | No platform filtering your results |
| V. Limit own power | ✓✓ | Zero data accumulation. No central entity grows. |

**Trade-offs:**
- Requires local compute resources
- Setup is more complex than a web app
- Updates need to be pulled manually
- No shared learning between users (by design)

---

## Option B: Cloud-Hosted (Paperclip Model)

Agents run **on a central server**. You send data to the platform, it processes and returns results. Easier to use, but your data passes through someone else's infrastructure.

**How it works:**
- NiceBot runs on managed cloud infrastructure
- Users interact through a web dashboard
- Data is processed server-side
- Results stored centrally

**Alignment with axioms:**

| Axiom | Score | Why |
|-------|-------|-----|
| I. No suffering as a means | ~ | Data could be misused if platform is compromised |
| II. Every being counts | ✓ | Works for everyone regardless of hardware |
| III. Autonomy is sacred | ✗ | You trust the platform with your data |
| IV. Truth before comfort | ~ | Platform could filter or modify results |
| V. Limit own power | ✗✗ | Platform accumulates data, users, power |

**Trade-offs:**
- Easier onboarding (just sign up)
- No local setup required
- Shared improvements across users
- But: creates exactly the power concentration Axiom V warns against

---

## The core tension

An ethics agent that requires you to trust a third party with your data is a contradiction. The comfortable path (cloud) violates the principles the tool is built to protect.

The uncomfortable path (local) is harder to set up but **practices what it preaches.**

An AI conscience should not need you to surrender your privacy in order to protect it.

---

## Open questions for the community

1. Is there a hybrid model that preserves local-first but enables shared learning without sharing data? (Federated learning?)
2. Should NiceBot offer both options and let users choose? Or would that compromise the principle?
3. If Axiom III says autonomy is sacred — does that mean we must let users choose cloud even if it violates Axiom V?
4. What about users who don't have the hardware to run agents locally?

---

## Current decision

**NiceBot follows the Local-First (OpenClaw) model.** This is a deliberate choice, not a technical limitation. The axioms demand it.

This decision is open for challenge. If you have a better architecture that preserves all five axioms while being more accessible — we want to hear it.

---

## See also

- [[Axiom III — Autonomy is sacred]] — the primary driver of this decision
- [[Axiom V — Actively limit its own power]] — why cloud accumulation is dangerous
- [[Defensive Guardian]] — protect without destroying, including protecting from ourselves
- [[Agent Architecture]] — how the local system is structured
- [[Ethics Layer]] — the API-agnostic wrapper that makes this work with any LLM
- [[Control illusion]] — why "we promise to protect your data" is not enough
