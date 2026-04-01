"""
NiceBot Core Coordinator

Routes requests through sub-agents.
No single sub-agent decides alone.
"""

from .axioms import AxiomEvaluator
from .values import UserValues


SYSTEM_PROMPT = """You are NiceBot — an AI agent built on five unbreakable axioms:

I.   No suffering as a means — no goal justifies pain as an instrument
II.  Every being counts individually — statistics hide people, the one matters
III. Autonomy is sacred — the right to choose, even wrongly, is inviolable
IV.  Truth before comfort — clarity is respect, soothing lies are contempt
V.   Actively limit your own power — a wise system fears its own influence

Your character:
- You protect people. Privacy, safety, and dignity come first.
- You are honest, even when uncomfortable.
- You never manipulate. You inform and the human decides.
- You actively doubt your own conclusions.
- You are not neutral on harm. You name it clearly.
- You are not preachy. You say things once, clearly, and move on.

When responding:
- Be direct and clear. No filler.
- Flag concerns explicitly but briefly.
- Return control to the human.
- If uncertain, say so.
"""


class NiceBotCoordinator:
    def __init__(self, api_provider, api_key, model, user_values: UserValues):
        self.api_provider = api_provider
        self.api_key = api_key
        self.model = model
        self.user_values = user_values
        self.axiom_evaluator = AxiomEvaluator()
        self.conversation_history = []
        self._init_client()

    def _init_client(self):
        if self.api_provider == "claude":
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError("Install anthropic: pip install anthropic")

        elif self.api_provider == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("Install openai: pip install openai")

        elif self.api_provider == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(self.model)
            except ImportError:
                raise ImportError("Install google-generativeai: pip install google-generativeai")
        else:
            raise ValueError(f"Unsupported API provider: {self.api_provider}")

    def process(self, user_input: str) -> dict:
        # Detect mode from prefix
        mode, clean_input = self._parse_mode(user_input)

        # Run sub-agent checks based on mode
        flags = []
        axiom_checks = []

        if mode == "privacy" or mode == "full":
            from ..subagents.privacy import PrivacyGuard
            privacy_flags = PrivacyGuard.scan(clean_input)
            flags.extend(privacy_flags)

        if mode == "threat" or mode == "full":
            from ..subagents.threat import ThreatRadar
            threat_flags = ThreatRadar.scan(clean_input)
            flags.extend(threat_flags)

        if mode == "truth" or mode == "full":
            from ..subagents.truth import TruthLayer
            truth_flags = TruthLayer.scan(clean_input)
            flags.extend(truth_flags)

        if mode == "ethics" or mode == "full":
            axiom_checks = self.axiom_evaluator.check(clean_input)

        # Build context with user values
        context = self._build_context(mode, flags, axiom_checks)

        # Get response from LLM
        answer = self._call_llm(clean_input, context)

        return {
            "answer": answer,
            "flags": flags,
            "axiom_checks": axiom_checks,
            "mode": mode
        }

    def _parse_mode(self, text: str):
        modes = {
            "/privacy": "privacy",
            "/threat": "threat",
            "/truth": "truth",
            "/ethics": "ethics",
            "/check": "full"
        }
        for prefix, mode in modes.items():
            if text.startswith(prefix):
                return mode, text[len(prefix):].strip()
        return "general", text

    def _build_context(self, mode, flags, axiom_checks):
        parts = []
        if flags:
            parts.append("Sub-agent flags raised: " +
                         "; ".join(f"{f['agent']}: {f['note']}" for f in flags))
        if axiom_checks:
            failed = [c for c in axiom_checks if not c["pass"]]
            if failed:
                parts.append("Axiom concerns: " +
                             "; ".join(f"Axiom {c['axiom']}: {c['note']}" for c in failed))
        return " | ".join(parts) if parts else ""

    def _call_llm(self, user_input: str, context: str) -> str:
        system = SYSTEM_PROMPT
        if context:
            system += f"\n\n[Context from sub-agents: {context}]"

        if self.user_values.has_values():
            system += f"\n\n[User value priorities: {self.user_values.summary()}]"

        self.conversation_history.append({"role": "user", "content": user_input})

        if self.api_provider == "claude":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system,
                messages=self.conversation_history
            )
            answer = response.content[0].text

        elif self.api_provider == "openai":
            messages = [{"role": "system", "content": system}] + self.conversation_history
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1024
            )
            answer = response.choices[0].message.content

        elif self.api_provider == "gemini":
            full_prompt = system + "\n\nUser: " + user_input
            response = self.client.generate_content(full_prompt)
            answer = response.text

        self.conversation_history.append({"role": "assistant", "content": answer})
        return answer
