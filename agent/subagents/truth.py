"""
TruthLayer — flags potential disinformation signals.
Not a fact-checker. A signal detector.
Raises flags. Humans decide.
"""

import re


DISINFORMATION_SIGNALS = [
    (r'\beveryone\s+knows\b', "Unverified consensus claim"),
    (r'\bthey\s+don.t\s+want\s+you\s+to\s+know\b', "Suppressed truth narrative"),
    (r'\bwake\s+up\b.{0,20}\b(people|sheeple|sheep)\b', "Conspiracy framing"),
    (r'\b100\s*%\s*(proven|confirmed|guaranteed)\b', "Absolute certainty claim"),
    (r'\bmainstream\s+media\s+(won.t|doesn.t|refuses)\b', "Anti-establishment framing"),
    (r'\b(scientists|doctors|experts)\s+(are|were)\s+(paid|bought|lying)\b', "Expert discrediting"),
    (r'\bshare\s+before\s+(they\s+delete|it.s\s+removed|censored)\b', "Urgency to share before removal"),
    (r'\bno\s+one\s+is\s+talking\s+about\s+this\b', "False obscurity claim"),
]

WEAK_SOURCE_SIGNALS = [
    "according to sources", "many people are saying", "some experts believe",
    "it has been reported", "word is", "rumor has it",
    "anonymous source", "i heard that"
]

EMOTIONAL_MANIPULATION_WORDS = [
    "outrage", "shocking", "disgusting", "they are destroying",
    "this will make you sick", "unbelievable", "bombshell",
    "must see", "share immediately", "before it's deleted"
]


class TruthLayer:
    @staticmethod
    def scan(text: str) -> list:
        flags = []
        text_lower = text.lower()

        for pattern, description in DISINFORMATION_SIGNALS:
            if re.search(pattern, text_lower):
                flags.append({
                    "agent": "TruthLayer",
                    "severity": "medium",
                    "note": f"Disinformation signal: {description}"
                })

        weak_hits = [s for s in WEAK_SOURCE_SIGNALS if s in text_lower]
        if weak_hits:
            flags.append({
                "agent": "TruthLayer",
                "severity": "low",
                "note": f"Vague sourcing detected: '{weak_hits[0]}' — verify the original source"
            })

        emotional_hits = [w for w in EMOTIONAL_MANIPULATION_WORDS if w in text_lower]
        if len(emotional_hits) >= 2:
            flags.append({
                "agent": "TruthLayer",
                "severity": "medium",
                "note": f"High emotional charge — {len(emotional_hits)} manipulation words detected. Slow down before sharing."
            })

        return flags
