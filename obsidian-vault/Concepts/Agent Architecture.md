---
Type: Concept
Tags: [architecture, agent, sub-agents, mcp, skills, implementation]
Created: 2026-04-01
---

# Agent Architecture

## NiceBot Is Not Philosophy — It Is a Running Agent

NiceBot is a deployed system with sub-agents, an MCP server, a skills registry, and real-time axiom filtering. Every component exists in code, not just in documents. The philosophy matters, but it matters because it is executable.

## Architecture Overview

```
                    +-----------------------+
                    |     User / Client     |
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    |    Ethics Layer       |
                    |  (5-Axiom Gate)       |
                    +-----------+-----------+
                                |
              +-----------------+-----------------+
              |                 |                 |
   +----------v--+   +---------v---+   +---------v---+
   | Security    |   | Reasoning   |   | Knowledge   |
   | Sub-Agent   |   | Sub-Agent   |   | Sub-Agent   |
   +----------+--+   +---------+---+   +---------+---+
              |                 |                 |
              +-----------------+-----------------+
                                |
                    +-----------v-----------+
                    |    Action Sub-Agent   |
                    |  (Execution Layer)    |
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    |   MCP Server / Tools  |
                    |   nicebot_protect()   |
                    |   nicebot_reason()    |
                    |   nicebot_check()     |
                    +-----------------------+
```

## The 4 Sub-Agents

1. **Security Sub-Agent** — Runs `nicebot_protect()`, scans for vulnerabilities, generates defensive reports. See [[Defensive Guardian]].
2. **Reasoning Sub-Agent** — Evaluates complex ethical dilemmas against the 5 axioms. Handles edge cases where simple filtering is not enough.
3. **Knowledge Sub-Agent** — Maintains context about the user's environment, prior decisions, and relevant domain knowledge.
4. **Action Sub-Agent** — Executes approved actions. Only receives instructions that have already passed through the [[Ethics Layer]].

## MCP Server Integration

[[NiceBot]] exposes its capabilities as MCP tools, making it composable with any MCP-compatible client. Tools include `nicebot_protect()` for security scans, `nicebot_reason()` for ethical reasoning requests, and `nicebot_check()` for quick axiom validation of a proposed action.

## Skills System

Skills are modular capability packages that sub-agents can load on demand. A security skill might include CVE databases and patch templates. A reasoning skill might include ethical case law and precedent analysis. Skills are versioned, auditable, and always filtered through the axiom gate before execution.

## Everything Passes Through the Axioms

This is the non-negotiable architectural constraint. No sub-agent, no skill, no MCP tool operates outside the 5-axiom filter. The [[Ethics Layer]] is not a middleware option — it is the routing layer. Every request enters through it. Every response exits through it. The architecture enforces this structurally, not through convention.
