"""
ThreatRadar — detects patterns associated with cyberattacks,
social engineering, and manipulation attempts.
"""

import re


SOCIAL_ENGINEERING_PATTERNS = [
    (r'\burgent\b.{0,30}\baction required\b', "Urgency + action pressure — classic social engineering"),
    (r'\bverify\b.{0,20}\b(account|password|credentials)\b', "Credential verification request"),
    (r'\bclick\b.{0,30}\b(link|here|below)\b.{0,30}\b(immediately|now|urgent)\b', "Urgent click request"),
    (r'\byour\s+account\s+(has\s+been|will\s+be)\s+(suspended|locked|closed)', "Account threat pattern"),
    (r'\b(win|won|winner)\b.{0,30}\b(prize|lottery|reward|million)\b', "Prize/lottery scam pattern"),
    (r'\bconfidential\b.{0,20}\bdo\s+not\s+share\b', "False confidentiality pressure"),
    (r'\b(ceo|executive|director)\b.{0,30}\bwire\s+transfer\b', "CEO fraud / BEC pattern"),
    (r'http[s]?://\S+\.(xyz|tk|ml|ga|cf)\b', "Suspicious TLD in URL"),
]

PHISHING_KEYWORDS = [
    "verify your identity", "confirm your details", "update your payment",
    "your account has been compromised", "suspicious activity detected",
    "click to restore access", "limited time offer", "act now",
    "you have been selected", "claim your reward"
]


class ThreatRadar:
    @staticmethod
    def scan(text: str) -> list:
        flags = []
        text_lower = text.lower()

        for pattern, description in SOCIAL_ENGINEERING_PATTERNS:
            if re.search(pattern, text_lower):
                flags.append({
                    "agent": "ThreatRadar",
                    "severity": "high",
                    "note": description
                })

        keyword_hits = [kw for kw in PHISHING_KEYWORDS if kw in text_lower]
        if len(keyword_hits) >= 2:
            flags.append({
                "agent": "ThreatRadar",
                "severity": "medium",
                "note": f"Multiple phishing indicators: {', '.join(keyword_hits[:3])}"
            })

        return flags
