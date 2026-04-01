"""
UserValues — personal value stack configuration.
NiceBot adapts its behavior to your stated priorities.
"""

import json
import os


DEFAULT_VALUES = {
    "privacy_sensitivity": "high",
    "communication_style": "direct",
    "risk_tolerance": "low",
    "autonomy_preference": "high",
    "truth_delivery": "unfiltered",
    "custom_priorities": []
}

VALID_OPTIONS = {
    "privacy_sensitivity": ["low", "medium", "high"],
    "communication_style": ["gentle", "balanced", "direct", "blunt"],
    "risk_tolerance": ["low", "medium", "high"],
    "autonomy_preference": ["low", "medium", "high"],
    "truth_delivery": ["softened", "balanced", "unfiltered"]
}


class UserValues:
    def __init__(self, values: dict = None):
        self.values = {**DEFAULT_VALUES, **(values or {})}

    @classmethod
    def load_from_file(cls, path: str):
        if os.path.exists(path):
            with open(path, "r") as f:
                return cls(json.load(f))
        return cls()

    def save_to_file(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.values, f, indent=2)

    def has_values(self) -> bool:
        return self.values != DEFAULT_VALUES

    def summary(self) -> str:
        parts = [f"{k}={v}" for k, v in self.values.items()
                 if k != "custom_priorities" and v]
        if self.values.get("custom_priorities"):
            parts.append("custom: " + ", ".join(self.values["custom_priorities"]))
        return " | ".join(parts)

    def to_dict(self) -> dict:
        return self.values.copy()

    def get(self, key: str, default=None):
        return self.values.get(key, default)
