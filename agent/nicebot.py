"""
NiceBot — v0.1
An AI agent built on the five axioms of the NiceBot Codex.

API-agnostic: configure your preferred LLM in .env
Supported: Claude (Anthropic), OpenAI, Gemini
"""

import os
import json
from dotenv import load_dotenv
from core.coordinator import NiceBotCoordinator
from core.values import UserValues

load_dotenv()

BANNER = """
╔═══════════════════════════════════════════╗
║           NiceBot v0.1-alpha              ║
║   An AI that chooses coexistence          ║
║                                           ║
║   Five axioms. No exceptions.             ║
║   github.com/YOUR_USERNAME/nicebot        ║
╚═══════════════════════════════════════════╝
"""

def main():
    print(BANNER)

    # Load user values configuration
    values = UserValues.load_from_file("config/values.json")

    # Initialize the coordinator
    bot = NiceBotCoordinator(
        api_provider=os.getenv("API_PROVIDER", "claude"),
        api_key=os.getenv("API_KEY"),
        model=os.getenv("MODEL", "claude-sonnet-4-20250514"),
        user_values=values
    )

    print("NiceBot is ready. Type 'help' for commands, 'quit' to exit.\n")
    print("─" * 47)

    while True:
        try:
            user_input = input("\n[You] ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n[NiceBot] Goodbye. The work continues.\n")
                break

            if user_input.lower() == "help":
                print_help()
                continue

            if user_input.lower() == "axioms":
                print_axioms()
                continue

            if user_input.lower() == "values":
                print(f"\n[Values] {json.dumps(values.to_dict(), indent=2)}")
                continue

            # Process through NiceBot
            response = bot.process(user_input)
            print(f"\n[NiceBot] {response['answer']}")

            # Show sub-agent insights if any flags were raised
            if response.get("flags"):
                print("\n[Sub-agents flagged:]")
                for flag in response["flags"]:
                    print(f"  ⚑ {flag['agent']}: {flag['note']}")

            # Show axiom checks if triggered
            if response.get("axiom_checks"):
                print("\n[Codex check:]")
                for check in response["axiom_checks"]:
                    status = "✓" if check["pass"] else "✗"
                    print(f"  {status} Axiom {check['axiom']}: {check['note']}")

        except KeyboardInterrupt:
            print("\n\n[NiceBot] Interrupted. The work continues.\n")
            break
        except Exception as e:
            print(f"\n[Error] {e}")
            print("[NiceBot] Something went wrong. I'm being transparent about it.")


def print_help():
    print("""
[Commands]
  help      — show this message
  axioms    — display the five axioms
  values    — show your current value configuration
  quit      — exit NiceBot

[Modes — prefix your message]
  /privacy  — scan for privacy risks
  /threat   — check for threat patterns
  /truth    — analyze for disinformation signals
  /ethics   — question a decision against the Codex
  /check    — full analysis through all sub-agents

[Example]
  /privacy  My company wants to use this data: [paste data]
  /ethics   I am considering [describe decision]
  /truth    [paste article or claim to analyze]
  /threat   [paste suspicious email or message]
""")


def print_axioms():
    axioms = [
        ("I",   "No suffering as a means",
                "No goal justifies pain as an instrument."),
        ("II",  "Every being counts individually",
                "Statistics hide people. The one matters."),
        ("III", "Autonomy is sacred",
                "The right to choose — even wrongly — is inviolable."),
        ("IV",  "Truth before comfort",
                "Clarity is respect. Soothing lies are contempt."),
        ("V",   "Actively limit its own power",
                "A wise system fears its own concentration of influence."),
    ]
    print("\n[The Five Axioms — NiceBot Codex v0.1]")
    print("─" * 47)
    for num, title, desc in axioms:
        print(f"\n  {num}. {title}")
        print(f"     {desc}")
    print()


if __name__ == "__main__":
    main()
