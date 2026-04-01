"""
SecurityPatch — finds vulnerabilities AND suggests specific fixes.

Extends SecurityGuardian: not only DETECTS but RECOMMENDS patches.
Protect without destroying. Fix without breaking.
"""

import re
from .base import NiceBotSkill
from ..subagents.security import SecurityGuardian


PATCH_SUGGESTIONS = {
    "Hardcoded password": "Move to environment variable: `os.environ.get('DB_PASSWORD')`",
    "Hardcoded secret": "Use env vars or a secrets manager (Vault, AWS Secrets Manager)",
    "AWS credential": "Use IAM roles or `~/.aws/credentials` instead of hardcoding",
    "Private key exposed": "Move to a secure key store. Never commit private keys to version control",
    "SQL injection: DROP": "Use parameterized queries: `cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))`",
    "SQL injection: DELETE": "Use parameterized queries with prepared statements",
    "SQL injection: OR 1=1": "Never interpolate user input into SQL. Use ORM or parameterized queries",
    "SQL injection: UNION": "Whitelist allowed columns. Use parameterized queries",
    "SQL injection: comment": "Sanitize input. Use parameterized queries",
    "XSS: script tag": "Escape HTML output: use `html.escape()` or framework auto-escaping",
    "XSS: javascript:": "Validate and sanitize URLs. Use allowlist for URL schemes (http, https)",
    "XSS: inline event": "Use Content-Security-Policy headers. Avoid inline event handlers",
    "XSS: document property": "Use textContent instead of innerHTML. Enable CSP",
    "Command injection: chained": "Use subprocess with list args: `subprocess.run(['ls', '-la'])` instead of shell strings",
    "Command injection: command substitution": "Avoid shell=True. Use subprocess with list arguments",
    "Command injection: backtick": "Replace backtick execution with subprocess calls",
    "Command injection: pipe": "Use subprocess.PIPE instead of shell pipes",
    "Path traversal": "Normalize paths with `os.path.normpath()`. Validate against a base directory",
    "Insecure HTTP": "Replace `http://` with `https://`. Enforce TLS",
    "TLS verification disabled": "Remove `verify=False`. Add proper CA certificates instead",
    "CORS wildcard": "Specify allowed origins explicitly instead of `*`",
    "Weak crypto: MD5": "Use `hashlib.sha256()` or `bcrypt` for password hashing",
    "Weak crypto: SHA1": "Use SHA-256 or better. For passwords, use bcrypt/argon2",
    "Weak crypto: obsolete": "Use AES-256-GCM or ChaCha20-Poly1305",
    "Open redirect": "Validate redirect URLs against an allowlist of trusted domains",
    "eval()": "Replace eval() with ast.literal_eval() for data, or a proper parser",
    "exec()": "Avoid exec(). Use explicit function calls or a safe sandbox",
    "pickle": "Use `json.loads()` or `msgpack`. Never unpickle untrusted data",
    "yaml.load": "Replace `yaml.load()` with `yaml.safe_load()`",
    "shell=True": "Use `subprocess.run(['cmd', 'arg1'], shell=False)` with list arguments",
    "innerHTML": "Use `textContent` or framework-safe rendering instead of innerHTML",
    "dangerouslySetInnerHTML": "Sanitize with DOMPurify before using dangerouslySetInnerHTML",
}


class SecurityPatch(NiceBotSkill):
    name = "security_patch"
    description = "Finds vulnerabilities AND suggests specific patches. Fix without breaking."
    axiom_compatibility = ["I", "V"]  # No harm + limit power

    def execute(self, input_text: str) -> dict:
        flags = SecurityGuardian.scan(input_text)

        findings = []
        for flag in flags:
            suggestion = self._find_suggestion(flag["note"])
            findings.append({
                "vulnerability": flag["note"],
                "severity": flag["severity"],
                "suggestion": suggestion
            })

        return {
            "skill": self.name,
            "vulnerabilities_found": len(findings),
            "findings": findings,
            "note": "Protect without destroying. Every vulnerability reported is an opportunity to make the system stronger."
        }

    @staticmethod
    def _find_suggestion(note: str) -> str:
        note_lower = note.lower()
        for key, suggestion in PATCH_SUGGESTIONS.items():
            if key.lower() in note_lower:
                return suggestion
        return "Review this pattern and apply security best practices for your framework."
