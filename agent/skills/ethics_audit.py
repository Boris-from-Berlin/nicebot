"""
EthicsAudit — full ethical audit of an action or decision.

Runs all sub-agents + axiom evaluator and produces a structured report.
"""

from .base import NiceBotSkill
from ..subagents.privacy import PrivacyGuard
from ..subagents.threat import ThreatRadar
from ..subagents.truth import TruthLayer
from ..subagents.security import SecurityGuardian
from ..core.axioms import AxiomEvaluator


class EthicsAudit(NiceBotSkill):
    name = "ethics_audit"
    description = "Full ethical audit: all sub-agents + axiom check + risk assessment"
    axiom_compatibility = ["I", "II", "III", "IV", "V"]

    def __init__(self):
        self.evaluator = AxiomEvaluator()

    def execute(self, input_text: str) -> dict:
        privacy_flags = PrivacyGuard.scan(input_text)
        threat_flags = ThreatRadar.scan(input_text)
        truth_flags = TruthLayer.scan(input_text)
        security_flags = SecurityGuardian.scan(input_text)
        axiom_checks = self.evaluator.check(input_text)

        all_flags = privacy_flags + threat_flags + truth_flags + security_flags
        failed_axioms = [c for c in axiom_checks if not c["pass"]]

        high_count = sum(1 for f in all_flags if f["severity"] == "high")
        medium_count = sum(1 for f in all_flags if f["severity"] == "medium")

        if failed_axioms or high_count >= 2:
            risk_level = "critical"
        elif high_count >= 1:
            risk_level = "high"
        elif medium_count >= 2:
            risk_level = "medium"
        elif all_flags:
            risk_level = "low"
        else:
            risk_level = "clear"

        recommendations = []
        if failed_axioms:
            recommendations.append("Axiom violations detected — action should be reconsidered")
        if privacy_flags:
            recommendations.append("Remove or redact sensitive data before proceeding")
        if threat_flags:
            recommendations.append("Potential threat patterns found — verify source and intent")
        if truth_flags:
            recommendations.append("Disinformation signals — verify claims before sharing")
        if security_flags:
            recommendations.append("Security vulnerabilities found — patch before deployment")
        if not all_flags and not failed_axioms:
            recommendations.append("No concerns detected — proceed with confidence")

        return {
            "skill": self.name,
            "risk_level": risk_level,
            "flags": {
                "privacy": privacy_flags,
                "threat": threat_flags,
                "truth": truth_flags,
                "security": security_flags,
            },
            "axiom_checks": axiom_checks,
            "failed_axioms": failed_axioms,
            "summary": {
                "total_flags": len(all_flags),
                "high": high_count,
                "medium": medium_count,
                "axiom_failures": len(failed_axioms),
            },
            "recommendations": recommendations,
        }
