#!/usr/bin/env python3
"""
NiceBot MCP Server — Ethics-as-a-Service

Exposes NiceBot's capabilities as MCP tools over JSON-RPC stdio.
Any AI system (Claude, GPT, Gemini, local models) can use NiceBot as its conscience.

Usage:
    python agent/mcp/server.py

Protocol: JSON-RPC 2.0 over stdin/stdout (MCP stdio transport)
"""

import sys
import json

# Add parent directories to path
sys.path.insert(0, sys.path[0] + '/..')
sys.path.insert(0, sys.path[0] + '/../..')

from subagents.privacy import PrivacyGuard
from subagents.threat import ThreatRadar
from subagents.truth import TruthLayer
from subagents.security import SecurityGuardian
from core.axioms import AxiomEvaluator


TOOLS = [
    {
        "name": "nicebot_protect",
        "description": "Full NiceBot analysis: runs ALL sub-agents (privacy, threat, truth, security) + axiom evaluator. Returns complete protection report. Use this as the single entry point.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text, code, or action to analyze"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "nicebot_ethics_check",
        "description": "Check a planned action against NiceBot's 5 axioms. Returns which axioms pass or fail.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Action or decision to evaluate"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "nicebot_privacy_scan",
        "description": "Scan text for privacy risks: SSN, credit cards, API keys, personal data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to scan for privacy risks"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "nicebot_threat_scan",
        "description": "Detect phishing, social engineering, and scam patterns.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to scan for threats"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "nicebot_truth_check",
        "description": "Flag potential disinformation signals, weak sourcing, and manipulation tactics.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to check for disinformation"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "nicebot_security_scan",
        "description": "Scan code or text for security vulnerabilities: SQL injection, XSS, hardcoded secrets, weak crypto. Finds and reports — NEVER exploits.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Code or text to scan for vulnerabilities"}
            },
            "required": ["text"]
        }
    }
]

axiom_evaluator = AxiomEvaluator()


def handle_tool_call(name, arguments):
    text = arguments.get("text", "")

    if name == "nicebot_protect":
        privacy = PrivacyGuard.scan(text)
        threat = ThreatRadar.scan(text)
        truth = TruthLayer.scan(text)
        security = SecurityGuardian.scan(text)
        axioms = axiom_evaluator.check(text)
        failed_axioms = [a for a in axioms if not a["pass"]]

        all_flags = privacy + threat + truth + security
        risk = "critical" if any(f["severity"] == "high" for f in all_flags) or failed_axioms else \
               "medium" if all_flags else "low"

        return {
            "risk_level": risk,
            "flags": all_flags,
            "axiom_concerns": failed_axioms,
            "summary": f"{len(all_flags)} flags raised, {len(failed_axioms)} axiom concerns"
        }

    elif name == "nicebot_ethics_check":
        checks = axiom_evaluator.check(text)
        failed = [c for c in checks if not c["pass"]]
        return {"axiom_checks": checks, "failed": failed, "all_pass": len(failed) == 0}

    elif name == "nicebot_privacy_scan":
        return {"flags": PrivacyGuard.scan(text)}

    elif name == "nicebot_threat_scan":
        return {"flags": ThreatRadar.scan(text)}

    elif name == "nicebot_truth_check":
        return {"flags": TruthLayer.scan(text)}

    elif name == "nicebot_security_scan":
        return {"flags": SecurityGuardian.scan(text)}

    return {"error": f"Unknown tool: {name}"}


def send(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
        except json.JSONDecodeError:
            continue

        method = request.get("method", "")
        req_id = request.get("id")

        if method == "initialize":
            send({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "nicebot",
                        "version": "0.2.0"
                    }
                }
            })

        elif method == "tools/list":
            send({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": TOOLS}
            })

        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            result = handle_tool_call(tool_name, arguments)
            send({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        elif method == "notifications/initialized":
            pass  # Client acknowledged initialization

        else:
            send({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            })


if __name__ == "__main__":
    main()
