"""
NiceBot Skill — base class for all extensible skills.

Skills are higher-level capabilities built on top of sub-agents.
Community can contribute new skills via Pull Requests.
"""


class NiceBotSkill:
    name = "base"
    description = "Base skill — do not use directly"
    axiom_compatibility = ["I", "II", "III", "IV", "V"]

    def execute(self, input_text: str) -> dict:
        """Run the skill on input text. Returns structured result."""
        raise NotImplementedError(f"Skill '{self.name}' must implement execute()")

    def __repr__(self):
        return f"<NiceBotSkill: {self.name}>"
