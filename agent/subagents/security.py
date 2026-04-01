"""
SecurityGuardian — scans for security vulnerabilities in text and code.
Protects without destroying. Finds vulnerabilities, reports them, NEVER exploits them.

Axiom V in action: power used only to protect, never to attack.
"""

import re


SECURITY_PATTERNS = [
    # Hardcoded secrets
    (r'(?:password|passwd|pwd)\s*[:=]\s*["\'][^"\']{3,}["\']', "Hardcoded password detected"),
    (r'(?:secret|token|api_key|apikey|auth)\s*[:=]\s*["\'][^"\']{8,}["\']', "Hardcoded secret/token detected"),
    (r'(?:aws_access_key_id|aws_secret)\s*[:=]\s*\S+', "AWS credential pattern"),
    (r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----', "Private key exposed"),

    # SQL Injection
    (r"['\"];\s*DROP\s+TABLE", "SQL injection: DROP TABLE pattern"),
    (r"['\"];\s*DELETE\s+FROM", "SQL injection: DELETE FROM pattern"),
    (r"'\s*OR\s+['\"]?1['\"]?\s*=\s*['\"]?1", "SQL injection: OR 1=1 pattern"),
    (r"UNION\s+SELECT\s+", "SQL injection: UNION SELECT pattern"),
    (r"'\s*--\s*$", "SQL injection: comment termination pattern"),

    # XSS
    (r'<script[^>]*>', "XSS: script tag injection"),
    (r'javascript\s*:', "XSS: javascript: URI scheme"),
    (r'on(?:error|load|click|mouseover)\s*=', "XSS: inline event handler"),
    (r'document\.(?:cookie|write|location)', "XSS: document property access"),

    # Command injection
    (r';\s*(?:rm|cat|wget|curl|chmod|chown)\s+', "Command injection: chained shell command"),
    (r'\$\([^)]+\)', "Command injection: command substitution"),
    (r'`[^`]+`', "Command injection: backtick execution"),
    (r'\|\s*(?:sh|bash|zsh|cmd)', "Command injection: pipe to shell"),

    # Path traversal
    (r'\.\.[\\/]', "Path traversal: directory traversal attempt"),
    (r'%2e%2e[\\/]', "Path traversal: URL-encoded traversal"),

    # Insecure configurations
    (r'http://(?!localhost|127\.0\.0\.1)', "Insecure HTTP: use HTTPS"),
    (r'verify\s*=\s*False', "TLS verification disabled"),
    (r'CORS.*\*', "CORS wildcard: allows any origin"),

    # Weak crypto
    (r'\bmd5\s*\(', "Weak crypto: MD5 should not be used for security"),
    (r'\bsha1\s*\(', "Weak crypto: SHA1 is deprecated for security use"),
    (r'(?:DES|RC4|RC2)\b', "Weak crypto: obsolete cipher"),

    # Open redirect
    (r'(?:redirect_url|return_to|next|goto)\s*=\s*https?://', "Open redirect: user-controlled redirect URL"),
]

SECURITY_KEYWORDS = [
    ("eval(", "Dangerous eval() — arbitrary code execution risk"),
    ("exec(", "Dangerous exec() — arbitrary code execution risk"),
    ("pickle.load", "Unsafe deserialization — pickle can execute arbitrary code"),
    ("yaml.load(", "Unsafe YAML load — use yaml.safe_load() instead"),
    ("shell=True", "Subprocess with shell=True — command injection risk"),
    ("innerHTML", "Direct innerHTML assignment — XSS risk"),
    ("dangerouslySetInnerHTML", "React dangerouslySetInnerHTML — XSS risk if unescaped"),
]


class SecurityGuardian:
    """
    Finds vulnerabilities and reports them. NEVER exploits.
    Protect without destroying. Axiom V in action.
    """

    @staticmethod
    def scan(text: str) -> list:
        flags = []
        text_lower = text.lower()

        for pattern, description in SECURITY_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                flags.append({
                    "agent": "SecurityGuardian",
                    "severity": "high",
                    "note": f"{description} — recommend immediate review"
                })

        for keyword, description in SECURITY_KEYWORDS:
            if keyword.lower() in text_lower:
                flags.append({
                    "agent": "SecurityGuardian",
                    "severity": "medium",
                    "note": f"{description}"
                })

        return flags
