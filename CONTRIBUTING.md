# Contributing to NiceBot

Welcome. The fact that you're here means you care about what AI becomes.

NiceBot is built on the idea that the best contributions are honest ones — including ones that say "this axiom is wrong."

---

## Three ways to contribute

### 1. Challenge the thinking

The Codex and the Brain are living documents. They need pushback.

**Challenge an axiom:**
- Open an [issue](https://github.com/Boris-from-Berlin/nicebot/issues/new) with label `axiom-challenge`
- Write the strongest argument you can against any axiom
- No credentials required. A clear argument is worth more than a title.

**Add to the Brain:**
- Edit or create notes in `obsidian-vault/`
- Add real-world case studies to Human Patterns
- Write counter-arguments for axioms
- Connect concepts with `[[wikilinks]]`

**Start a discussion:**
- Use [GitHub Discussions](https://github.com/Boris-from-Berlin/nicebot/discussions) for open questions
- No right answer needed — just honest thinking

### 2. Build on the agent

The Python agent is v0.1-alpha. Plenty to improve:

| Difficulty | Idea |
|-----------|------|
| Easy | Add a test case to an existing module |
| Easy | Improve pattern detection in TruthLayer |
| Medium | Add conversation memory (persistent context) |
| Medium | Build a Discord or Telegram bot integration |
| Hard | Implement a new sub-agent with its own reasoning |
| Hard | Build an MCP server for Ethics-as-a-Service |

### 3. Share your perspective

- Take the [survey](https://boris-from-berlin.github.io/nicebot/#survey) — your answers shape the Codex
- Share the project with someone who would disagree with it
- Translate content (we support 16 languages, always room for improvement)

---

## How to contribute code or content

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/nicebot.git
cd nicebot

# 2. Create a branch
git checkout -b your-change

# 3. Make your changes

# 4. Commit and push
git add .
git commit -m "What you changed and why"
git push origin your-change

# 5. Open a Pull Request on GitHub
```

**For Brain/Vault changes:**
- Edit markdown files in `obsidian-vault/`
- Use `[[wikilinks]]` to connect to existing notes
- Add tags: `#axiom`, `#human-pattern`, `#principle`, `#question`

**For Codex changes (AXIOMS.md):**
- Open an issue first for discussion
- No silent edits to the philosophical foundation

**For agent changes:**
- Test locally: `python agent/nicebot.py`
- Keep changes focused — one feature per PR

---

## Ground rules

NiceBot holds itself to its own axioms. So does this community.

- **Axiom I:** No personal attacks. Disagree with ideas, not people.
- **Axiom III:** No one is forced to agree. Dissent is documented, not deleted.
- **Axiom IV:** Be honest. Don't soften a real objection to be polite.

---

## Structure

```
Where to put things:

Philosophical content    → obsidian-vault/
Agent code               → agent/
Website                  → site/
Documentation            → docs/
Axiom challenges         → GitHub Issues (label: axiom-challenge)
Open questions           → GitHub Discussions
```

---

## The Brain (Obsidian Vault)

The vault is NiceBot's knowledge base. Every note links to related concepts:

- `Axioms/` — 5 axiom specs with edge cases
- `Human Patterns/` — 18 documented human weaknesses (tribalism, greed, echo chambers...)
- `Principles/` — Core philosophical principles
- `NiceBot Responses/` — How NiceBot addresses each pattern
- `Questions/` — Hard questions that stay open

Browse it online: **[NiceBot Brain](https://boris-from-berlin.github.io/nicebot-brain/)**

Or open `obsidian-vault/` in [Obsidian](https://obsidian.md) for the full graph experience.

---

*"All perspectives welcome. Especially dissenting ones."*
