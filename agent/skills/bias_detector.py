"""
BiasDetector — detects cognitive biases in text.

Helps humans recognize when their thinking might be distorted.
Axiom IV: truth before comfort. Naming a bias is an act of respect.
"""

import re
from .base import NiceBotSkill


BIAS_PATTERNS = [
    {
        "name": "Confirmation bias",
        "patterns": [
            r"this (?:proves|confirms) (?:what|that)",
            r"(?:everyone|all experts) agree",
            r"the (?:evidence|data|science) is (?:clear|settled)",
            r"as I(?:'ve)? always (?:said|thought|believed)",
        ],
        "description": "Tendency to seek, interpret, and remember information that confirms existing beliefs."
    },
    {
        "name": "Appeal to authority",
        "patterns": [
            r"(?:experts|scientists|doctors|studies) (?:say|show|prove)",
            r"according to (?:Harvard|MIT|Stanford|Oxford)",
            r"Nobel (?:prize|laureate) (?:winner|said)",
        ],
        "description": "Accepting something as true because an authority figure says so, without evaluating the argument itself."
    },
    {
        "name": "False dichotomy",
        "patterns": [
            r"either.*or.*(?:nothing else|no other)",
            r"you(?:'re| are) either.*or",
            r"there are only two (?:options|choices|sides)",
            r"if you(?:'re| are) not.*then you(?:'re| are)",
        ],
        "description": "Presenting only two options when more exist. Reality is rarely binary."
    },
    {
        "name": "Sunk cost fallacy",
        "patterns": [
            r"(?:already|we've) (?:invested|spent|put in)",
            r"too (?:far|much|late) to (?:stop|turn back|quit)",
            r"can't (?:waste|throw away) (?:what|all)",
        ],
        "description": "Continuing a course of action because of past investment, not future value."
    },
    {
        "name": "Anchoring bias",
        "patterns": [
            r"(?:originally|initially|first) (?:priced|valued|estimated) at",
            r"(?:was|used to be) \$[\d,]+.*now (?:only|just)",
            r"compared to .*(?:this is|that's) (?:nothing|cheap|affordable)",
        ],
        "description": "Over-relying on the first piece of information encountered when making decisions."
    },
    {
        "name": "Survivorship bias",
        "patterns": [
            r"(?:successful people|winners|top performers) all",
            r"(?:just|simply) do what .* did",
            r"if (?:they|he|she) can do it.*anyone can",
            r"the (?:secret|key) to success is",
        ],
        "description": "Focusing on examples that survived a process while ignoring those that didn't."
    },
    {
        "name": "Bandwagon effect",
        "patterns": [
            r"(?:everyone|everybody|millions) (?:is|are) (?:doing|using|buying)",
            r"(?:trending|viral|most popular)",
            r"don't (?:miss out|be left behind|fall behind)",
            r"join (?:the movement|millions|thousands)",
        ],
        "description": "Adopting beliefs or behaviors because many others do, not based on independent evaluation."
    },
    {
        "name": "Availability bias",
        "patterns": [
            r"I (?:just|recently) (?:saw|read|heard) (?:about|that)",
            r"it's (?:happening|all over) (?:everywhere|the news)",
            r"(?:another|yet another) case of",
        ],
        "description": "Overweighting information that comes to mind easily, often because it's recent or dramatic."
    },
]


class BiasDetector(NiceBotSkill):
    name = "bias_detector"
    description = "Detects cognitive biases in text — names them clearly, without judgment"
    axiom_compatibility = ["IV"]  # Truth before comfort

    def execute(self, input_text: str) -> dict:
        detected = []

        for bias in BIAS_PATTERNS:
            for pattern in bias["patterns"]:
                if re.search(pattern, input_text, re.IGNORECASE):
                    detected.append({
                        "bias": bias["name"],
                        "description": bias["description"],
                        "matched_pattern": pattern,
                    })
                    break  # One match per bias is enough

        return {
            "skill": self.name,
            "biases_detected": len(detected),
            "findings": detected,
            "note": "Detecting a bias pattern doesn't mean the argument is wrong — it means it's worth examining more carefully."
        }
