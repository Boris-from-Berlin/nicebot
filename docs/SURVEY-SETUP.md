# NiceBot Survey — Supabase Setup

## 1. Supabase Projekt erstellen

Gehe zu https://supabase.com und erstelle ein neues Projekt (oder nutze ein bestehendes).

## 2. Tabelle anlegen

Führe dieses SQL in Supabase SQL Editor aus:

```sql
-- Votes Tabelle
CREATE TABLE nicebot_votes (
  id SERIAL PRIMARY KEY,
  question_id TEXT NOT NULL,
  option_index INT NOT NULL,
  count INT DEFAULT 0,
  UNIQUE(question_id, option_index)
);

-- Seed mit allen Fragen/Optionen (4 Fragen × 4 Optionen)
INSERT INTO nicebot_votes (question_id, option_index, count)
SELECT q, o, 0
FROM unnest(ARRAY['q1','q2','q3','q4']) AS q,
     generate_series(0,3) AS o
ON CONFLICT DO NOTHING;

-- RPC Funktion zum Inkrementieren
CREATE OR REPLACE FUNCTION increment_vote(qid TEXT, opt_idx INT)
RETURNS VOID AS $$
BEGIN
  UPDATE nicebot_votes
  SET count = count + 1
  WHERE question_id = qid AND option_index = opt_idx;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Row Level Security
ALTER TABLE nicebot_votes ENABLE ROW LEVEL SECURITY;

-- Jeder darf lesen
CREATE POLICY "Public read" ON nicebot_votes
  FOR SELECT USING (true);

-- Nur über RPC schreiben (SECURITY DEFINER)
```

## 3. API Keys in index.html eintragen

Öffne `site/index.html` und ersetze:

```js
const SUPABASE_URL = ''; // ← deine Supabase URL
const SUPABASE_KEY = ''; // ← dein anon/public key
```

Findest du unter: Supabase Dashboard → Settings → API → URL und anon key.

## 4. Auswertung abrufen

### Im Supabase Dashboard
- Gehe zu Table Editor → `nicebot_votes`
- Sortiere nach `count DESC`

### Per API
```bash
curl 'https://YOUR_PROJECT.supabase.co/rest/v1/nicebot_votes?select=*&order=question_id,option_index' \
  -H 'apikey: YOUR_ANON_KEY'
```

### Per SQL
```sql
SELECT
  question_id,
  option_index,
  count,
  ROUND(count * 100.0 / SUM(count) OVER (PARTITION BY question_id), 1) AS pct
FROM nicebot_votes
ORDER BY question_id, option_index;
```

## 5. Ohne Supabase

Solange `SUPABASE_URL` und `SUPABASE_KEY` leer sind, funktioniert die Survey trotzdem — nur ohne Persistenz. Votes werden lokal gezählt und nach Page-Refresh zurückgesetzt.
