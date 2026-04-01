"""
PrivacyGuard — scans for privacy risks in text and data.
First line of defense. Pattern-based + heuristic.
"""

import re


PRIVACY_PATTERNS = [
    (r'\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b', "SSN pattern detected"),
    (r'\b4[0-9]{12}(?:[0-9]{3})?\b', "Visa card number pattern"),
    (r'\b5[1-5][0-9]{14}\b', "Mastercard pattern"),
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', "Email address present"),
    (r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', "Phone number pattern"),
    (r'\b\d{1,5}\s\w+\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b', "Street address pattern"),
    (r'password\s*[:=]\s*\S+', "Password in plaintext"),
    (r'api[_\s-]?key\s*[:=]\s*\S+', "API key in plaintext"),
    (r'secret\s*[:=]\s*\S+', "Secret/token in plaintext"),
    (r'bearer\s+[A-Za-z0-9\-._~+/]+=*', "Bearer token detected"),
    (r'\b(?:19|20)\d{2}[-/]\d{2}[-/]\d{2}\b', "Date of birth pattern"),
]

HIGH_RISK_KEYWORDS = [
    "medical record", "health record", "diagnosis", "prescription",
    "bank account", "routing number", "iban", "swift",
    "passport number", "driver license", "national id",
    "location data", "gps coordinates", "home address",
    "biometric", "fingerprint", "face recognition"
]


class PrivacyGuard:
    @staticmethod
    def scan(text: str) -> list:
        flags = []
        text_lower = text.lower()

        for pattern, description in PRIVACY_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                flags.append({
                    "agent": "PrivacyGuard",
                    "severity": "high",
                    "note": f"{description} — consider whether this should be shared"
                })

        for keyword in HIGH_RISK_KEYWORDS:
            if keyword in text_lower:
                flags.append({
                    "agent": "PrivacyGuard",
                    "severity": "medium",
                    "note": f"Sensitive data category detected: '{keyword}'"
                })

        return flags
