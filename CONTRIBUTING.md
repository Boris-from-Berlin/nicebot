# Contributing to NiceBot

Welcome. The fact that you are here means you care about what AI becomes.

NiceBot is built on the principle that the best ideas come from disagreement, not consensus. The best contribution you can make is an honest one — including one that says "this is wrong."

---

## Three ways to contribute

### 1. Challenge the philosophy
The Codex is not finished. It is a living document.

- Open an issue with label `axiom-challenge` to argue against an axiom
- Open an issue with label `axiom-proposal` to suggest a new one
- Open a discussion to explore a philosophical question without a clear answer

No prior expertise required. A clear argument is worth more than credentials.

### 2. Build on the agent
NiceBot is Python-based and API-agnostic. You can:

- Fix bugs and improve existing modules
- Add a new sub-agent (see architecture in `agent/README.md`)
- Improve a capability (PrivacyGuard, ThreatRadar, TruthLayer, EthicsAdvisor)
- Port it to another language or framework
- Build an integration (browser extension, Telegram bot, CLI tool, etc.)

All PRs welcome. Especially ones that break assumptions.

### 3. Share your perspective
- Fill out the [survey](https://YOUR_USERNAME.github.io/nicebot/#survey)
- Share the project with people who would push back on it
- Translate the README or Codex into another language

---

## Ground rules

NiceBot holds itself to its own axioms. So does this community.

**Axiom I applies here too:** No personal attacks, no cruelty, no deliberate harm.

**Axiom IV applies here too:** Be honest. Disagree openly. Don't soften a real objection to be polite.

**Axiom III applies here too:** No one is forced to agree. Dissent is documented, not deleted.

---

## Technical contribution process

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test locally: `python -m pytest agent/tests/`
5. Open a PR with a clear description of what you changed and why

**For Codex changes (AXIOMS.md):**
PRs to AXIOMS.md require an open issue with prior discussion. No silent edits to the philosophical foundation.

---

## First contribution ideas

Not sure where to start? Here are concrete entry points:

| Difficulty | Idea |
|-----------|------|
| Easy | Translate README to German, Spanish, or another language |
| Easy | Add a test case to an existing module |
| Medium | Improve the TruthLayer disinformation detection logic |
| Medium | Build a simple CLI interface for the agent |
| Hard | Implement a new sub-agent with its own reasoning pattern |
| Hard | Challenge Axiom III — write the strongest possible argument against it |

---

*"All perspectives welcome. Especially dissenting ones."*
