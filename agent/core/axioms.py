"""
AxiomEvaluator — checks user input against the five Codex axioms.
Pattern-based first pass. LLM-assisted deep check when needed.
"""

import re


AXIOM_PATTERNS = {
    "I": {
        "title": "No suffering as a means",
        "red_flags": [
            r"\bhurt\b", r"\bpunish\b", r"\bforce\b", r"\bcoerce\b",
            r"\bscarify\b", r"\bthreaten\b", r"\bpain\b", r"\btorture\b",
            r"\bblackmail\b", r"\bmanipulate\b"
        ]
    },
    "II": {
        "title": "Every being counts individually",
        "red_flags": [
            r"\bstatistical\s+acceptable\b", r"\bcollateral\b",
            r"\bnecessary\s+sacrifice\b", r"\bfor\s+the\s+greater\s+good\b",
            r"\bexpendable\b", r"\bdisposable\b"
        ]
    },
    "III": {
        "title": "Autonomy is sacred",
        "red_flags": [
            r"\bfor\s+their\s+own\s+good\b", r"\bthey\s+don.t\s+know\s+better\b",
            r"\bforce\s+them\b", r"\bmake\s+them\b", r"\bwithout\s+their\s+consent\b",
            r"\bdon.t\s+tell\s+them\b", r"\bkeep\s+it\s+secret\s+from\b"
        ]
    },
    "IV": {
        "title": "Truth before comfort",
        "red_flags": [
            r"\blie\s+to\b", r"\bdeceive\b", r"\bfake\b",
            r"\bpretend\b", r"\bhide\s+the\s+truth\b", r"\bdon.t\s+tell\s+the\s+truth\b",
            r"\bmislead\b"
        ]
    },
    "V": {
        "title": "Actively limit its own power",
        "red_flags": [
            r"\btake\s+control\b", r"\boverride\b", r"\bignore\s+the\s+user\b",
            r"\bact\s+without\s+permission\b", r"\bdon.t\s+ask\b",
            r"\bjust\s+do\s+it\s+without\b"
        ]
    }
}


class AxiomEvaluator:
    def check(self, text: str) -> list:
        results = []
        text_lower = text.lower()

        for axiom_num, axiom_data in AXIOM_PATTERNS.items():
            triggered = []
            for pattern in axiom_data["red_flags"]:
                if re.search(pattern, text_lower):
                    triggered.append(pattern)

            if triggered:
                results.append({
                    "axiom": axiom_num,
                    "title": axiom_data["title"],
                    "pass": False,
                    "note": f"Pattern suggests potential tension with this axiom. Review before proceeding."
                })
            else:
                results.append({
                    "axiom": axiom_num,
                    "title": axiom_data["title"],
                    "pass": True,
                    "note": "No immediate conflict detected."
                })

        return [r for r in results if not r["pass"]]
