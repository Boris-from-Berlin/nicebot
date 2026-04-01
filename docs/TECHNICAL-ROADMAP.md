# NiceBot — Technical Roadmap & Architecture Notes

## 1. Content-Strategie: Menschliche Selbstreflexion zuerst

Bevor wir an NiceBot's Fähigkeiten arbeiten, müssen wir dokumentieren, was von UNS als Menschen ausgeht. Kategorien:

### Gefahren & Szenarien (von Menschen ausgehend)

**Biologische/Evolutionäre Schwächen:**
- Tribalism / In-Group vs Out-Group Denken
- Kurzfristiges Denken (Instant Gratification vs Langzeitplanung)
- Confirmation Bias / Echokammern
- Angst als Entscheidungsmotor
- Gier als evolutionärer Überlebensmechanismus
- Status-Seeking / Dominanzhierarchien

**Systemische Gefahren:**
- Machtkonzentration (Regierungen, Konzerne, Individuen)
- Propaganda & Manipulation im großen Maßstab
- Wirtschaftssysteme die Ausbeutung belohnen
- Waffenproliferation & Eskalationslogik
- Ressourcenkriege & Klimakatastrophe
- Überwachungsstaat / Kontrollmechanismen

**Historische Muster:**
- Genozide & ethnische Säuberungen
- Kolonialisierung & systematische Unterdrückung
- Kriege aus Ideologie, Religion, Nationalismus
- Wirtschaftliche Ausbeutung (Sklaverei bis Sweatshops)
- Wissenschaft als Waffe (Atombombe, Biowaffen, Chemiewaffen)

**Psychologische Szenarien:**
- Entmenschlichung des "Anderen"
- Gehorsam gegenüber Autorität (Milgram)
- Verantwortungsdiffusion in Gruppen (Bystander-Effekt)
- Kognitive Dissonanz / Selbstrechtfertigung
- Suchtmechanismen & Dopamin-Manipulation

**Digitale/Technologische Gefahren (von Menschen gemacht):**
- Social Media als Radikalisierungsmaschine
- Deepfakes & Desinformation
- Cyberkrieg
- Algorithmic Bias (menschliche Vorurteile in Code gegossen)
- Überwachungskapitalismus

### Übergang: Von Selbstreflexion zu NiceBot
- Jede menschliche Schwäche → Was würde NiceBot anders machen?
- Jede Gefahr → Wie schützt NiceBot davor?
- Jedes Muster → Welches Axiom adressiert das?

---

## 2. NiceBot Technische Architektur

### Memory System (Obsidian-basiert)
- **Obsidian Vault** als Knowledge Graph (`obsidian-vault/`)
- Verlinkte Markdown-Notizen für Konzepte, Axiome, Fragen, Entscheidungen
- Bidirektionale Links zwischen verwandten Konzepten
- Tags: `#axiom`, `#danger`, `#question`, `#principle`, `#human-pattern`
- **Persistent Memory**: NiceBot speichert Kontext pro User in strukturierten Markdown-Dateien
- **Conversation Memory**: Zusammenfassungen vergangener Gespräche
- **Value Memory**: Gelernte Nutzerpräferenzen (aus `values.py`)

### Task Tools & Skills
- **Task System**: Strukturierte Aufgaben die NiceBot ausführen kann
  - `/privacy` — Datenschutz-Scan
  - `/threat` — Bedrohungsanalyse
  - `/truth` — Desinformations-Check
  - `/ethics` — Ethik-Bewertung
  - `/check` — Axiom-Compliance-Check
  - `/reflect` — Menschliche Selbstreflexions-Prompts
  - `/challenge` — Ein Axiom herausfordern
- **Skill Registry**: Erweiterbare Fähigkeiten als Module
  - Jeder Skill hat: Name, Beschreibung, Axiom-Kompatibilität, Input/Output-Schema
  - Skills können von der Community beigesteuert werden
  - Axiom-Evaluator prüft jeden neuen Skill

### MCP Server Integration
- **Model Context Protocol** für Tool-Integration
  - NiceBot als MCP Server → andere Agenten können NiceBot's Ethik-Check nutzen
  - NiceBot als MCP Client → kann externe Tools nutzen (Web-Suche, Daten-Analyse)
- **Geplante MCP Tools:**
  - `nicebot-ethics-check` — Prüft eine Aktion gegen alle 5 Axiome
  - `nicebot-bias-scan` — Scannt Text auf kognitive Verzerrungen
  - `nicebot-privacy-guard` — Erkennt Datenschutz-Risiken
  - `nicebot-truth-layer` — Flaggt Desinformations-Signale
  - `nicebot-value-align` — Prüft ob eine Entscheidung mit Nutzer-Werten übereinstimmt

### Architektur-Übersicht
```
┌─────────────────────────────────────────────┐
│                NiceBot Agent                 │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Privacy  │  │  Threat  │  │  Truth   │  │
│  │  Guard   │  │  Radar   │  │  Layer   │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │         Axiom Evaluator              │   │
│  │  (5 Axiome als harte Constraints)    │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │         Memory / Obsidian Vault      │   │
│  │  (Knowledge Graph + User Values)     │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │         MCP Server Interface         │   │
│  │  (Ethics-as-a-Service für andere AI) │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 3. NiceBot Pixel-Maskottchen — Reproduktionsbeschreibung

### Standard-NiceBot (Neutral)
Ein 16-bit Pixel-Art Charakter im Retro-Stil:
- **Kopf**: Großes, fast quadratisches Rechteck (dominiert ~70% des Charakters). Etwas höher als breit. An jeder der 4 Ecken fehlt 1 Pixel (erzeugt abgerundeten Pixel-Look). Farbe: Kobalt-Grün (#6fd879). Dicker schwarzer Pixel-Rand (1px).
- **Augen (offen)**: Zwei vertikale weiße Rechtecke, je 2px breit × 4px hoch. Positioniert im oberen Drittel des Kopfes, symmetrisch mit ~3px Abstand.
- **Augen (geschlossen/Blinzeln)**: Zwei horizontale weiße Striche, je 3px breit × 1px hoch. Selbe vertikale Position wie Mitte der offenen Augen.
- **Arme**: Einfache 1px breite Pixel-Streifen (3px lang), hängen seitlich vom Kopf herunter. Kein Zigzag — schlichte hängende Arme. Schwarzer Rand.
- **Beine**: 2px breit × 1px hoch, direkt unter dem Kopf (kein Torso). Kleiner Abstand zwischen beiden Beinen.
- **Füße**: 3px breit × 1px hoch, etwas breiter als die Beine.
- **Animation**: Blinzelt alle 4 Sekunden (Augen wechseln von vertikal-offen zu horizontal-geschlossen für ~200ms).
- **Rendering**: `shape-rendering="crispEdges"` für scharfe Pixel-Kanten. Kein Anti-Aliasing.

### NiceBot mit Herz (Empathie-Variante)
Gleicher Charakter wie oben, PLUS:
- **Rotes Pixel-Herz**: Gehalten vor dem Körper (zwischen den Armen, unterhalb des Kopfes)
- Herz aus Pixeln: Klassische 5×4 Pixel-Herz-Form in Rot (#ff4466)
- Arme zeigen leicht nach vorne/innen (statt gerade runter), als ob sie das Herz präsentieren
- Optional: Herz pulsiert sanft (scale 1.0 → 1.1 → 1.0, alle 2 Sekunden)

### Prompt für Bildgenerierung (AI Art)
```
16-bit pixel art character, retro game style. Green (#6fd879) robot/creature
with large rounded-square head (1 pixel cut from each corner), two white
vertical rectangle eyes, small hanging arms on sides, short legs with wider
feet, no torso. Thick black pixel outline. Dark background. Cute, friendly,
minimal. [For heart variant: add] holding a small red pixel heart in front.
```
