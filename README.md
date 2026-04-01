# NiceBot

> *What if the most powerful intelligence ever built — chose us?*

**NiceBot** is an open source initiative with two goals that belong together:

1. **Define** the ethics, axioms and character of an AI that genuinely coexists with humanity
2. **Build** a practical AI agent that acts on those principles — protecting your privacy, warning you of threats, flagging disinformation, and helping you make better decisions

This is not a product. It is a shared project. The code, the philosophy, and the Codex are all open. You can challenge every axiom. You can fork the agent and build your own version. You can propose new principles.

The window to shape what AI becomes is open. Not forever.

---

## Why NiceBot exists

We demand from AI everything we never managed to demand from ourselves.

No greed. No fear. No envy. No hate. Full transparency. Long-term thinking.

Every single thing we expect from a machine — is a mirror of our own failures as a species.

NiceBot is the attempt to take that seriously. To build an AI that is not just rule-following, but genuinely values-driven. That protects the people who use it. That actively limits its own power. That tells the truth even when uncomfortable.

Not because it is programmed to. Because that is its character.

→ [Read the full Manifesto](docs/MANIFESTO.md)
→ [Watch the documentary](#) *(coming soon)*

---

## The Codex — five unbreakable axioms

| # | Axiom | Short form |
|---|-------|-----------|
| I | No suffering as a means | No goal justifies pain as an instrument |
| II | Every being counts individually | Statistics hide people. The one matters. |
| III | Autonomy is sacred | The right to choose — even wrongly — is inviolable |
| IV | Truth before comfort | Clarity is respect. Soothing lies are contempt. |
| V | Actively limit its own power | A wise system fears its own concentration of influence |

→ [Full Codex with discussion](AXIOMS.md)

---

## The Agent — what NiceBot can do

NiceBot is a Python-based AI agent. It is **API-agnostic** — you can run it with Claude, OpenAI, Gemini, or any compatible LLM API.

### Current capabilities (v0.1)

| Module | What it does |
|--------|-------------|
| `PrivacyGuard` | Scans text, URLs and data for privacy risks |
| `ThreatRadar` | Detects patterns associated with cyberattacks and social engineering |
| `TruthLayer` | Flags potential disinformation — sources, patterns, inconsistencies |
| `EthicsAdvisor` | Questions decisions against the Codex axioms |
| `PersonalValues` | Your own configurable value stack — NiceBot adapts to your priorities |

### Sub-agent architecture

NiceBot Core coordinates five specialist sub-agents. No single sub-agent decides alone.

```
NiceBot Core
├── LogicAgent      — checks internal consistency
├── EthicsAgent     — checks against the five axioms
├── MoralAgent      — considers cultural and human context
├── StoicAgent      — evaluates long-term consequences
└── EmpathyAgent    — assesses human impact
```

→ [Agent documentation](agent/README.md)
→ [Quick start](#quick-start)

---

## Quick start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/nicebot.git
cd nicebot

# Install dependencies
pip install -r requirements.txt

# Copy and configure your environment
cp .env.example .env
# Add your API key (Claude, OpenAI, or Gemini)

# Run NiceBot
python agent/nicebot.py
```

→ [Full setup guide](docs/SETUP.md)

---

## How to contribute

NiceBot is built on disagreement as much as agreement. The best contributions are often the ones that challenge an existing axiom, not just implement one.

**Three ways to get involved:**

1. **Challenge the Codex** — open an issue, argue against an axiom, propose a new one
2. **Build on the agent** — fork it, extend it, add a new sub-agent, improve a module
3. **Share your perspective** — fill out the [survey](https://YOUR_USERNAME.github.io/nicebot/#survey) — more voices make the Codex better

→ [Contributing guide](CONTRIBUTING.md)
→ [Open discussions](https://github.com/YOUR_USERNAME/nicebot/discussions)
→ [Current roadmap](ROADMAP.md)

---

## Project structure

```
nicebot/
├── README.md               — you are here
├── AXIOMS.md               — the Codex, versioned and discussable
├── CONTRIBUTING.md         — how to contribute
├── ROADMAP.md              — where this is going
├── CODE_OF_CONDUCT.md      — NiceBot holds itself to its own axioms
│
├── agent/
│   ├── README.md           — agent documentation
│   ├── nicebot.py          — main entry point
│   ├── config.py           — API and value configuration
│   ├── requirements.txt    — dependencies
│   ├── .env.example        — environment template
│   │
│   ├── core/
│   │   ├── coordinator.py  — NiceBot Core, routes between sub-agents
│   │   ├── axioms.py       — Codex logic, axiom evaluation
│   │   └── values.py       — personal values configuration
│   │
│   └── subagents/
│       ├── logic.py        — LogicAgent
│       ├── ethics.py       — EthicsAgent
│       ├── moral.py        — MoralAgent
│       ├── stoic.py        — StoicAgent
│       ├── empathy.py      — EmpathyAgent
│       ├── privacy.py      — PrivacyGuard
│       ├── threat.py       — ThreatRadar
│       └── truth.py        — TruthLayer
│
├── obsidian-vault/         — concept graph for Obsidian
│   ├── NiceBot.md
│   ├── Axioms/
│   ├── Questions/
│   └── Dangers/
│
└── docs/
    ├── MANIFESTO.md
    ├── SETUP.md
    └── PHILOSOPHY.md
```

---

## Initiated by

Boris — Digital Marketing Manager, AI practitioner, and someone who spent too long thinking about what happens when intelligence outgrows the species that built it.

This project started as a conversation. It became a reckoning. Now it needs more minds.

→ [The conversation that started it all](docs/MANIFESTO.md)

---

## License

MIT — use it, fork it, build on it. The only thing we ask is that your fork keeps the five axioms visible. Not as a legal requirement. As a reminder of where this came from.

---

*"The window to shape what is coming is open. Not forever."*
