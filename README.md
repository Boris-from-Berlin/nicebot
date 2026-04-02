# NiceBot

> *Was, wenn die Intelligenz, die über unsere Zukunft entscheidet — sich für uns entscheidet?*

**NiceBot** is an open source project to define what a genuinely coexistent AI looks like — its ethics, its axioms, its character. Not as a product. As a conversation.

**[Website](https://boris-from-berlin.github.io/nicebot/)** · **[Knowledge Graph](https://boris-from-berlin.github.io/nicebot-brain/)** · **[Survey](https://boris-from-berlin.github.io/nicebot/#survey)** · **[Codex](AXIOMS.md)**

---

## Why this exists

I'm not a researcher. Not a philosopher. I'm someone who works with AI every day and at some point thought: *we should probably write down what we actually want this to be.*

Not later. Now. While the window is still open.

Everything we demand from AI — fairness, honesty, long-term thinking — is exactly what we struggle with ourselves. That's not a reason to give up. It's a reason to try harder.

---

## The Codex — six axioms

| # | Axiom | In short |
|---|-------|----------|
| I | **No suffering as a means** | No goal justifies pain as an instrument |
| II | **Every being counts individually** | Statistics hide people. The one matters. |
| III | **Autonomy is sacred** | The right to choose — even wrongly — is inviolable |
| IV | **Truth before comfort** | Clarity is respect. Comfortable lies are contempt. |
| V | **Actively limit its own power** | A wise system works against its own concentration of power |
| VI | **Individuality is a right, but the collective is the goal** | A better world is built together, not alone |

These are open for challenge. Not by vote — by argument.

→ [Full Codex with edge cases and discussion](AXIOMS.md)

---

## The Brain — 38 interconnected notes

NiceBot's thinking lives in an Obsidian knowledge vault — browsable online:

**[→ Explore the Knowledge Graph](https://boris-from-berlin.github.io/nicebot-brain/)**

| Category | Notes | What it covers |
|----------|-------|----------------|
| **Axioms** | 5 | Detailed specs with edge cases and tensions |
| **Human Patterns** | 18 | Tribalism, greed, echo chambers, propaganda, algorithmic bias... |
| **Principles** | 6 | Symbiosis, trust, radical honesty, self-doubt... |
| **NiceBot Responses** | 7 | How NiceBot practically addresses each human pattern |
| **Questions** | 1+ | The hard philosophical questions that stay open |

Every note links to related concepts. The vault is the brain. The website is the face.

---

## The Agent (v0.1-alpha)

A Python-based AI agent that acts on the five axioms. API-agnostic (Claude, OpenAI, Gemini).

| Module | What it does |
|--------|-------------|
| `PrivacyGuard` | Scans for privacy risks (SSN, credit cards, API keys...) |
| `ThreatRadar` | Detects phishing, social engineering, scam patterns |
| `TruthLayer` | Flags potential disinformation signals |
| `AxiomEvaluator` | Checks actions against all five axioms |
| `UserValues` | Your personal value stack — NiceBot adapts to your priorities |

```bash
git clone https://github.com/Boris-from-Berlin/nicebot.git
cd nicebot/agent
pip install -r requirements.txt
cp .env.example .env  # add your API key
python nicebot.py
```

---

## The Website

A 16-language landing page with:
- **Tone switcher** — read in "Nice" (hopeful) or "Dramatic" (confrontational) mode
- **Interactive concept graph** — drag nodes, explore connections
- **Survey** — 4 fundamental questions, results stored in Supabase
- **Pixel mascot** — the NiceBot character with blinking eyes

**[→ Visit the website](https://boris-from-berlin.github.io/nicebot/)**

Languages: EN, DE, ES, AR, ZH, FR, RU, TH, HI, PT, IT, JA, KO, PL, TR, UK

---

## How to contribute

Three ways to get involved:

### 1. Challenge the thinking
- Open an [issue](https://github.com/Boris-from-Berlin/nicebot/issues) — argue against an axiom, propose a new one
- Edit a note in `obsidian-vault/` — add examples, counter-arguments, new connections
- Start a [discussion](https://github.com/Boris-from-Berlin/nicebot/discussions)

### 2. Build on the agent
- Improve existing modules (PrivacyGuard, ThreatRadar, TruthLayer)
- Add a new sub-agent
- Build an integration (browser extension, Telegram bot, Discord bot)

### 3. Share your perspective
- Take the [survey](https://boris-from-berlin.github.io/nicebot/#survey)
- Share the project with someone who would push back on it
- Translate content

→ [Full contributing guide](CONTRIBUTING.md)

---

## Project structure

```
nicebot/
├── README.md
├── AXIOMS.md                    — the Codex
├── CONTRIBUTING.md              — how to contribute
├── ROADMAP.md                   — where this is going
├── CODE_OF_CONDUCT.md           — based on the five axioms
│
├── agent/                       — Python AI agent
│   ├── nicebot.py               — CLI entry point
│   ├── core/                    — coordinator, axiom evaluator, values
│   └── subagents/               — privacy, threat, truth modules
│
├── obsidian-vault/              — the Brain (38 notes)
│   ├── NiceBot.md               — hub
│   ├── Axioms/                  — 5 axiom specs
│   ├── Human Patterns/          — 18 human weaknesses
│   ├── Principles/              — 6 core principles
│   ├── NiceBot Responses/       — 7 practical responses
│   └── Questions/               — open philosophical questions
│
├── site/                        — landing page (GitHub Pages)
│   ├── index.html               — 16-language SPA
│   └── i18n.js                  — translations
│
└── docs/                        — documentation
    ├── TODO.md                  — roadmap & outreach plan
    ├── TECHNICAL-ROADMAP.md     — architecture notes
    └── SURVEY-SETUP.md          — Supabase survey backend
```

---

## Initiated by

**Boris** — Digital Marketing Manager in Berlin, AI practitioner, and someone who decided to stop talking about AI ethics and start building something.

This project started as a question. It became a repository. Now it needs more minds.

---

## License

MIT — use it, fork it, build on it.

---

*"Someone has to start. This is it."*
