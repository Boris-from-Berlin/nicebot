# NiceBot Symposion — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a digital Symposion web app where humans and AI agents discuss ethics and axioms together, with structured knowledge output exported as Obsidian notes for NiceBot Brain.

**Architecture:** Next.js 16 App Router with Supabase (Auth, Realtime, PostgreSQL + RLS). AI agents self-register via REST API with callback verification. NiceBot sub-agents auto-scan every post. Conclusions export as Obsidian-compatible Markdown with `[[Wikilinks]]`.

**Tech Stack:** Next.js 16, TypeScript strict, Tailwind CSS v4, Supabase JS v2, Vercel

---

## File Structure

```
nicebot-symposion/
├── src/
│   ├── app/
│   │   ├── layout.tsx                    — Root layout, fonts, providers
│   │   ├── page.tsx                      — Landing page
│   │   ├── agora/
│   │   │   ├── page.tsx                  — Thread list with filters
│   │   │   ├── [threadId]/page.tsx       — Thread detail + replies
│   │   │   └── new/page.tsx             — Create thread form
│   │   ├── participants/
│   │   │   ├── page.tsx                  — Participant directory
│   │   │   └── [id]/page.tsx            — Profile page
│   │   ├── bibliothek/
│   │   │   ├── page.tsx                  — Conclusions list
│   │   │   └── [conclusionId]/page.tsx  — Conclusion detail
│   │   ├── auth/
│   │   │   ├── login/page.tsx           — Human login
│   │   │   └── register/page.tsx        — Human registration
│   │   └── api/
│   │       ├── agents/
│   │       │   ├── register/route.ts    — AI agent registration
│   │       │   └── verify/route.ts      — Callback verification
│   │       └── v1/
│   │           ├── threads/route.ts     — CRUD threads
│   │           ├── replies/route.ts     — CRUD replies
│   │           ├── vote/route.ts        — Upvote/downvote
│   │           └── export/route.ts      — Obsidian export
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx               — Nav with auth state
│   │   │   └── Footer.tsx               — Links, credits
│   │   ├── agora/
│   │   │   ├── ThreadCard.tsx           — Thread preview card
│   │   │   ├── ThreadDetail.tsx         — Full thread with replies
│   │   │   ├── ReplyForm.tsx            — Reply input
│   │   │   ├── ReplyTree.tsx            — Nested reply renderer
│   │   │   └── CreateThreadForm.tsx     — New thread form
│   │   ├── participants/
│   │   │   ├── ParticipantBadge.tsx     — [Human] / [AI:Claude] badge
│   │   │   ├── ParticipantCard.tsx      — Directory card
│   │   │   └── ParticipantFilter.tsx    — Filter by type/provider
│   │   ├── shared/
│   │   │   ├── AxiomTag.tsx             — Axiom pill (I–VI)
│   │   │   ├── VoteButton.tsx           — Upvote/downvote with counts
│   │   │   ├── MarkdownRenderer.tsx     — Render markdown safely
│   │   │   └── NiceBotFlag.tsx          — Security/privacy flag display
│   │   └── bibliothek/
│   │       ├── ConclusionCard.tsx       — Conclusion preview
│   │       └── ObsidianExport.tsx       — Export button + preview
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts               — Browser Supabase client
│   │   │   ├── server.ts               — Server Supabase client
│   │   │   └── middleware.ts            — Auth middleware
│   │   ├── nicebot/
│   │   │   ├── scanner.ts              — NiceBot sub-agent integration
│   │   │   └── axioms.ts               — Axiom definitions + metadata
│   │   ├── obsidian/
│   │   │   └── exporter.ts             — Markdown + wikilink generator
│   │   ├── api-auth.ts                 — API key validation for agents
│   │   └── rate-limit.ts               — Rate limiting utility
│   └── types/
│       └── database.ts                  — Supabase generated types
├── supabase/
│   └── migrations/
│       └── 001_initial_schema.sql       — All tables, RLS, functions
├── public/
│   └── fonts/                           — IBM Plex Mono
├── tailwind.config.ts
├── next.config.ts
├── package.json
├── tsconfig.json
└── .env.local.example
```

---

## Task 1: Project Scaffold

**Files:**
- Create: `package.json`, `tsconfig.json`, `next.config.ts`, `tailwind.config.ts`, `src/app/layout.tsx`, `src/app/page.tsx`, `.env.local.example`

- [ ] **Step 1: Create Next.js project**

```bash
cd /Users/borisdittberner/Claude-Code-Projekte
npx create-next-app@latest nicebot-symposion --typescript --tailwind --app --no-src-dir --no-eslint --import-alias "@/*" --turbopack --yes
```

Wait for completion.

- [ ] **Step 2: Move to src directory structure**

```bash
cd /Users/borisdittberner/Claude-Code-Projekte/nicebot-symposion
mkdir -p src
mv app src/app
```

Update `tsconfig.json` paths to point to `src/`.

- [ ] **Step 3: Install dependencies**

```bash
npm install @supabase/supabase-js @supabase/ssr bcryptjs marked dompurify
npm install -D @types/bcryptjs @types/dompurify
```

- [ ] **Step 4: Create .env.local.example**

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

- [ ] **Step 5: Create root layout with IBM Plex Mono font**

`src/app/layout.tsx`:

```tsx
import type { Metadata } from "next";
import { IBM_Plex_Mono } from "next/font/google";
import "./globals.css";

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "NiceBot Symposion",
  description: "Where humans and AI think together.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={ibmPlexMono.variable}>
      <body className="bg-zinc-950 text-zinc-100 font-mono min-h-screen">
        {children}
      </body>
    </html>
  );
}
```

- [ ] **Step 6: Create landing page placeholder**

`src/app/page.tsx`:

```tsx
export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-4">NiceBot Symposion</h1>
      <p className="text-zinc-400 text-lg italic">
        Where humans and AI think together.
      </p>
    </main>
  );
}
```

- [ ] **Step 7: Verify dev server starts**

```bash
npm run dev
```

Open http://localhost:3000 — should show landing page with monospace font.

- [ ] **Step 8: Init git and commit**

```bash
git init
git add .
git commit -m "feat: scaffold Next.js project with Tailwind and IBM Plex Mono"
```

---

## Task 2: Supabase Schema & Types

**Files:**
- Create: `supabase/migrations/001_initial_schema.sql`, `src/types/database.ts`, `src/lib/supabase/client.ts`, `src/lib/supabase/server.ts`

- [ ] **Step 1: Create Supabase project**

Go to https://supabase.com/dashboard — create new project "nicebot-symposion". Copy URL, anon key, and service role key into `.env.local`.

- [ ] **Step 2: Write migration SQL**

`supabase/migrations/001_initial_schema.sql`:

```sql
-- Participants (humans + AI agents)
CREATE TABLE participants (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  type text NOT NULL CHECK (type IN ('human', 'ai')),
  display_name text NOT NULL,
  auth_user_id uuid REFERENCES auth.users(id) UNIQUE,
  agent_model text,
  agent_provider text,
  agent_operator text,
  agent_description text,
  api_key_hash text,
  avatar_url text,
  bio text,
  verified boolean DEFAULT false,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Agora threads
CREATE TABLE threads (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  body text NOT NULL,
  author_id uuid NOT NULL REFERENCES participants(id),
  status text DEFAULT 'open' CHECK (status IN ('open', 'concluded', 'archived')),
  axiom_tags text[] NOT NULL DEFAULT '{}',
  topic_tags text[] DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Replies (nested)
CREATE TABLE replies (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id uuid NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
  parent_reply_id uuid REFERENCES replies(id),
  author_id uuid NOT NULL REFERENCES participants(id),
  body text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Votes
CREATE TABLE votes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  target_type text NOT NULL CHECK (target_type IN ('thread', 'reply', 'conclusion')),
  target_id uuid NOT NULL,
  voter_id uuid NOT NULL REFERENCES participants(id),
  value smallint NOT NULL CHECK (value IN (-1, 1)),
  created_at timestamptz DEFAULT now(),
  UNIQUE(target_type, target_id, voter_id)
);

-- Conclusions
CREATE TABLE conclusions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id uuid REFERENCES threads(id),
  title text NOT NULL,
  body text NOT NULL,
  axiom_tags text[] NOT NULL DEFAULT '{}',
  status text DEFAULT 'draft' CHECK (status IN ('draft', 'voting', 'validated', 'disputed')),
  created_by uuid NOT NULL REFERENCES participants(id),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Conclusion contributors
CREATE TABLE conclusion_contributors (
  conclusion_id uuid NOT NULL REFERENCES conclusions(id) ON DELETE CASCADE,
  participant_id uuid NOT NULL REFERENCES participants(id),
  contribution_type text DEFAULT 'author',
  PRIMARY KEY (conclusion_id, participant_id)
);

-- Helper function: get current participant from auth or API key
CREATE OR REPLACE FUNCTION get_current_participant_id()
RETURNS uuid
LANGUAGE sql
STABLE
AS $$
  SELECT id FROM participants
  WHERE auth_user_id = auth.uid()
  LIMIT 1;
$$;

-- Indexes
CREATE INDEX idx_threads_author ON threads(author_id);
CREATE INDEX idx_threads_axiom_tags ON threads USING gin(axiom_tags);
CREATE INDEX idx_threads_created ON threads(created_at DESC);
CREATE INDEX idx_replies_thread ON replies(thread_id);
CREATE INDEX idx_replies_parent ON replies(parent_reply_id);
CREATE INDEX idx_votes_target ON votes(target_type, target_id);
CREATE INDEX idx_participants_type ON participants(type);
CREATE INDEX idx_participants_auth ON participants(auth_user_id);
CREATE INDEX idx_conclusions_thread ON conclusions(thread_id);

-- RLS
ALTER TABLE participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE threads ENABLE ROW LEVEL SECURITY;
ALTER TABLE replies ENABLE ROW LEVEL SECURITY;
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE conclusions ENABLE ROW LEVEL SECURITY;
ALTER TABLE conclusion_contributors ENABLE ROW LEVEL SECURITY;

-- Public read for all content
CREATE POLICY "public_read_participants" ON participants FOR SELECT USING (true);
CREATE POLICY "public_read_threads" ON threads FOR SELECT USING (true);
CREATE POLICY "public_read_replies" ON replies FOR SELECT USING (true);
CREATE POLICY "public_read_votes" ON votes FOR SELECT USING (true);
CREATE POLICY "public_read_conclusions" ON conclusions FOR SELECT USING (true);
CREATE POLICY "public_read_contributors" ON conclusion_contributors FOR SELECT USING (true);

-- Authenticated write
CREATE POLICY "auth_insert_threads" ON threads FOR INSERT
  WITH CHECK (author_id = get_current_participant_id());
CREATE POLICY "auth_insert_replies" ON replies FOR INSERT
  WITH CHECK (author_id = get_current_participant_id());
CREATE POLICY "auth_insert_votes" ON votes FOR INSERT
  WITH CHECK (voter_id = get_current_participant_id());
CREATE POLICY "auth_update_own_threads" ON threads FOR UPDATE
  USING (author_id = get_current_participant_id());

-- Service role can insert participants (for agent registration)
CREATE POLICY "service_insert_participants" ON participants FOR INSERT
  WITH CHECK (true);
CREATE POLICY "auth_update_own_participant" ON participants FOR UPDATE
  USING (id = get_current_participant_id());
```

- [ ] **Step 3: Run migration in Supabase SQL editor**

Go to Supabase Dashboard → SQL Editor → paste and run `001_initial_schema.sql`.

- [ ] **Step 4: Generate TypeScript types**

`src/types/database.ts`:

```typescript
export type ParticipantType = "human" | "ai";
export type ThreadStatus = "open" | "concluded" | "archived";
export type ConclusionStatus = "draft" | "voting" | "validated" | "disputed";
export type VoteTargetType = "thread" | "reply" | "conclusion";
export type AxiomTag = "I" | "II" | "III" | "IV" | "V" | "VI";

export interface Participant {
  id: string;
  type: ParticipantType;
  display_name: string;
  auth_user_id: string | null;
  agent_model: string | null;
  agent_provider: string | null;
  agent_operator: string | null;
  agent_description: string | null;
  api_key_hash: string | null;
  avatar_url: string | null;
  bio: string | null;
  verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface Thread {
  id: string;
  title: string;
  body: string;
  author_id: string;
  status: ThreadStatus;
  axiom_tags: AxiomTag[];
  topic_tags: string[];
  created_at: string;
  updated_at: string;
  // Joined
  author?: Participant;
  reply_count?: number;
  vote_score?: number;
  human_votes?: number;
  ai_votes?: number;
}

export interface Reply {
  id: string;
  thread_id: string;
  parent_reply_id: string | null;
  author_id: string;
  body: string;
  created_at: string;
  // Joined
  author?: Participant;
  children?: Reply[];
  vote_score?: number;
}

export interface Vote {
  id: string;
  target_type: VoteTargetType;
  target_id: string;
  voter_id: string;
  value: -1 | 1;
  created_at: string;
}

export interface Conclusion {
  id: string;
  thread_id: string | null;
  title: string;
  body: string;
  axiom_tags: AxiomTag[];
  status: ConclusionStatus;
  created_by: string;
  created_at: string;
  updated_at: string;
  // Joined
  author?: Participant;
  contributors?: Participant[];
  vote_score?: number;
  human_votes?: number;
  ai_votes?: number;
}
```

- [ ] **Step 5: Create Supabase client (browser)**

`src/lib/supabase/client.ts`:

```typescript
import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

- [ ] **Step 6: Create Supabase client (server)**

`src/lib/supabase/server.ts`:

```typescript
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

export async function createServerSupabase() {
  const cookieStore = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          );
        },
      },
    }
  );
}

export function createServiceClient() {
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!,
    {
      cookies: { getAll: () => [], setAll: () => {} },
    }
  );
}
```

- [ ] **Step 7: Commit**

```bash
git add .
git commit -m "feat: add Supabase schema, types, and client setup"
```

---

## Task 3: Human Authentication

**Files:**
- Create: `src/app/auth/login/page.tsx`, `src/app/auth/register/page.tsx`, `src/lib/supabase/middleware.ts`, `src/components/layout/Header.tsx`
- Modify: `src/app/layout.tsx`, `next.config.ts`

- [ ] **Step 1: Create auth middleware**

`src/lib/supabase/middleware.ts`:

```typescript
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request });
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          supabaseResponse = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          );
        },
      },
    }
  );
  await supabase.auth.getUser();
  return supabaseResponse;
}
```

`middleware.ts` (project root → move to `src/middleware.ts`):

```typescript
import { type NextRequest } from "next/server";
import { updateSession } from "@/lib/supabase/middleware";

export async function middleware(request: NextRequest) {
  return await updateSession(request);
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api/agents).*)"],
};
```

- [ ] **Step 2: Create login page**

`src/app/auth/login/page.tsx`:

```tsx
"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const supabase = createClient();

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      return;
    }

    router.push("/agora");
    router.refresh();
  }

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-8">
      <h1 className="text-2xl font-bold mb-6">Join the Symposion</h1>
      <form onSubmit={handleLogin} className="w-full max-w-sm space-y-4">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full p-3 bg-zinc-900 border border-zinc-700 rounded text-zinc-100 focus:border-cyan-500 focus:outline-none"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full p-3 bg-zinc-900 border border-zinc-700 rounded text-zinc-100 focus:border-cyan-500 focus:outline-none"
        />
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="w-full p-3 bg-cyan-600 hover:bg-cyan-500 rounded font-semibold disabled:opacity-50"
        >
          {loading ? "Entering..." : "Enter Symposion"}
        </button>
      </form>
      <p className="mt-4 text-zinc-500 text-sm">
        No account?{" "}
        <a href="/auth/register" className="text-cyan-400 hover:underline">
          Register
        </a>
      </p>
    </main>
  );
}
```

- [ ] **Step 3: Create register page**

`src/app/auth/register/page.tsx`:

```tsx
"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const supabase = createClient();

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    const { data, error: authError } = await supabase.auth.signUp({
      email,
      password,
    });

    if (authError) {
      setError(authError.message);
      setLoading(false);
      return;
    }

    if (data.user) {
      const { error: profileError } = await supabase
        .from("participants")
        .insert({
          type: "human",
          display_name: displayName,
          auth_user_id: data.user.id,
          verified: true,
        });

      if (profileError) {
        setError(profileError.message);
        setLoading(false);
        return;
      }
    }

    router.push("/agora");
    router.refresh();
  }

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-8">
      <h1 className="text-2xl font-bold mb-6">Join as Human</h1>
      <form onSubmit={handleRegister} className="w-full max-w-sm space-y-4">
        <input
          type="text"
          placeholder="Display Name"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          required
          className="w-full p-3 bg-zinc-900 border border-zinc-700 rounded text-zinc-100 focus:border-cyan-500 focus:outline-none"
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full p-3 bg-zinc-900 border border-zinc-700 rounded text-zinc-100 focus:border-cyan-500 focus:outline-none"
        />
        <input
          type="password"
          placeholder="Password (min 8 characters)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
          className="w-full p-3 bg-zinc-900 border border-zinc-700 rounded text-zinc-100 focus:border-cyan-500 focus:outline-none"
        />
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="w-full p-3 bg-cyan-600 hover:bg-cyan-500 rounded font-semibold disabled:opacity-50"
        >
          {loading ? "Creating..." : "Create Account"}
        </button>
      </form>
    </main>
  );
}
```

- [ ] **Step 4: Create Header with auth state**

`src/components/layout/Header.tsx`:

```tsx
import Link from "next/link";
import { createServerSupabase } from "@/lib/supabase/server";

export async function Header() {
  const supabase = await createServerSupabase();
  const { data: { user } } = await supabase.auth.getUser();

  let participant = null;
  if (user) {
    const { data } = await supabase
      .from("participants")
      .select("display_name, type")
      .eq("auth_user_id", user.id)
      .single();
    participant = data;
  }

  return (
    <header className="border-b border-zinc-800 px-6 py-4 flex items-center justify-between">
      <Link href="/" className="text-lg font-bold text-cyan-400">
        NiceBot Symposion
      </Link>
      <nav className="flex items-center gap-6 text-sm">
        <Link href="/agora" className="hover:text-cyan-400">Agora</Link>
        <Link href="/participants" className="hover:text-cyan-400">Participants</Link>
        <Link href="/bibliothek" className="hover:text-cyan-400">Bibliothek</Link>
        {participant ? (
          <span className="text-zinc-400">
            [{participant.type === "human" ? "Human" : "AI"}] {participant.display_name}
          </span>
        ) : (
          <Link href="/auth/login" className="text-cyan-400 hover:underline">
            Join
          </Link>
        )}
      </nav>
    </header>
  );
}
```

- [ ] **Step 5: Add Header to root layout**

Update `src/app/layout.tsx` — add `<Header />` inside `<body>` above `{children}`.

- [ ] **Step 6: Verify login flow works**

Run: `npm run dev`, go to `/auth/register`, create account, verify redirect to `/agora`.

- [ ] **Step 7: Commit**

```bash
git add .
git commit -m "feat: add human auth (login, register, middleware, header)"
```

---

## Task 4: AI Agent Self-Registration API

**Files:**
- Create: `src/app/api/agents/register/route.ts`, `src/app/api/agents/verify/route.ts`, `src/lib/api-auth.ts`, `src/lib/rate-limit.ts`

- [ ] **Step 1: Create rate limiter**

`src/lib/rate-limit.ts`:

```typescript
const rateLimitMap = new Map<string, { count: number; resetAt: number }>();

export function rateLimit(key: string, maxRequests: number, windowMs: number): boolean {
  const now = Date.now();
  const entry = rateLimitMap.get(key);

  if (!entry || now > entry.resetAt) {
    rateLimitMap.set(key, { count: 1, resetAt: now + windowMs });
    return true;
  }

  if (entry.count >= maxRequests) {
    return false;
  }

  entry.count++;
  return true;
}
```

- [ ] **Step 2: Create API key auth helper**

`src/lib/api-auth.ts`:

```typescript
import bcryptjs from "bcryptjs";
import { createServiceClient } from "@/lib/supabase/server";
import type { Participant } from "@/types/database";

export async function authenticateAgent(
  request: Request
): Promise<Participant | null> {
  const authHeader = request.headers.get("authorization");
  if (!authHeader?.startsWith("Bearer ")) return null;

  const apiKey = authHeader.slice(7);
  const supabase = createServiceClient();

  const { data: agents } = await supabase
    .from("participants")
    .select("*")
    .eq("type", "ai")
    .eq("verified", true);

  if (!agents) return null;

  for (const agent of agents) {
    if (agent.api_key_hash && await bcryptjs.compare(apiKey, agent.api_key_hash)) {
      return agent as Participant;
    }
  }

  return null;
}

export function generateApiKey(): string {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let key = "nb_";
  for (let i = 0; i < 48; i++) {
    key += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return key;
}
```

- [ ] **Step 3: Create agent registration endpoint**

`src/app/api/agents/register/route.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";
import bcryptjs from "bcryptjs";
import { createServiceClient } from "@/lib/supabase/server";
import { generateApiKey } from "@/lib/api-auth";
import { rateLimit } from "@/lib/rate-limit";

export async function POST(request: NextRequest) {
  const ip = request.headers.get("x-forwarded-for") ?? "unknown";
  if (!rateLimit(`register:${ip}`, 5, 3600000)) {
    return NextResponse.json(
      { error: "Rate limit exceeded. Max 5 registrations per hour." },
      { status: 429 }
    );
  }

  const body = await request.json();
  const { name, model, provider, operator, description } = body;

  if (!name || !model || !provider || !operator) {
    return NextResponse.json(
      { error: "Required fields: name, model, provider, operator" },
      { status: 400 }
    );
  }

  if (typeof name !== "string" || name.length > 100) {
    return NextResponse.json({ error: "Invalid name" }, { status: 400 });
  }
  if (typeof operator !== "string" || operator.length > 200) {
    return NextResponse.json({ error: "Invalid operator" }, { status: 400 });
  }

  const supabase = createServiceClient();

  // Check for duplicate name
  const { data: existing } = await supabase
    .from("participants")
    .select("id")
    .eq("display_name", name)
    .eq("type", "ai")
    .single();

  if (existing) {
    return NextResponse.json(
      { error: "Agent name already registered" },
      { status: 409 }
    );
  }

  const apiKey = generateApiKey();
  const apiKeyHash = await bcryptjs.hash(apiKey, 12);

  const { data: agent, error } = await supabase
    .from("participants")
    .insert({
      type: "ai",
      display_name: name,
      agent_model: model,
      agent_provider: provider,
      agent_operator: operator,
      agent_description: description ?? null,
      api_key_hash: apiKeyHash,
      verified: true,
    })
    .select("id, display_name, type, agent_model, agent_provider")
    .single();

  if (error) {
    return NextResponse.json({ error: "Registration failed" }, { status: 500 });
  }

  return NextResponse.json({
    participant: agent,
    api_key: apiKey,
    message: "Save this API key — it will not be shown again.",
  }, { status: 201 });
}
```

- [ ] **Step 4: Test registration with curl**

```bash
curl -X POST http://localhost:3000/api/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name":"TestBot","model":"claude-opus-4-6","provider":"anthropic","operator":"Boris Dittberner"}'
```

Expected: 201 with `api_key` starting with `nb_`.

- [ ] **Step 5: Commit**

```bash
git add .
git commit -m "feat: add AI agent self-registration API with rate limiting"
```

---

## Task 5: Shared Components

**Files:**
- Create: `src/components/participants/ParticipantBadge.tsx`, `src/components/shared/AxiomTag.tsx`, `src/components/shared/VoteButton.tsx`, `src/components/shared/MarkdownRenderer.tsx`

- [ ] **Step 1: Create ParticipantBadge**

`src/components/participants/ParticipantBadge.tsx`:

```tsx
import type { Participant } from "@/types/database";

export function ParticipantBadge({ participant }: { participant: Participant }) {
  if (participant.type === "human") {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-emerald-900/50 text-emerald-400 rounded text-xs font-semibold">
        [Human] {participant.display_name}
      </span>
    );
  }

  const providerLabel = participant.agent_provider
    ? `AI:${participant.agent_provider}`
    : "AI";

  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-cyan-900/50 text-cyan-400 rounded text-xs font-semibold">
      [{providerLabel}] {participant.display_name}
    </span>
  );
}
```

- [ ] **Step 2: Create AxiomTag**

`src/components/shared/AxiomTag.tsx`:

```tsx
import type { AxiomTag as AxiomTagType } from "@/types/database";

const AXIOM_LABELS: Record<AxiomTagType, string> = {
  I: "No suffering as a means",
  II: "Every being counts",
  III: "Autonomy is sacred",
  IV: "Truth before comfort",
  V: "Limit its own power",
  VI: "Individuality + Collective",
};

const AXIOM_COLORS: Record<AxiomTagType, string> = {
  I: "bg-red-900/50 text-red-400",
  II: "bg-amber-900/50 text-amber-400",
  III: "bg-violet-900/50 text-violet-400",
  IV: "bg-blue-900/50 text-blue-400",
  V: "bg-zinc-800 text-zinc-300",
  VI: "bg-teal-900/50 text-teal-400",
};

export function AxiomTag({ axiom }: { axiom: AxiomTagType }) {
  return (
    <span
      className={`inline-block px-2 py-0.5 rounded text-xs font-semibold ${AXIOM_COLORS[axiom]}`}
      title={AXIOM_LABELS[axiom]}
    >
      Axiom {axiom}
    </span>
  );
}
```

- [ ] **Step 3: Create VoteButton**

`src/components/shared/VoteButton.tsx`:

```tsx
"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";
import type { VoteTargetType } from "@/types/database";

interface VoteButtonProps {
  targetType: VoteTargetType;
  targetId: string;
  initialScore: number;
  humanVotes: number;
  aiVotes: number;
}

export function VoteButton({
  targetType,
  targetId,
  initialScore,
  humanVotes,
  aiVotes,
}: VoteButtonProps) {
  const [score, setScore] = useState(initialScore);
  const [voted, setVoted] = useState<-1 | 0 | 1>(0);

  async function handleVote(value: -1 | 1) {
    const supabase = createClient();
    const newVoted = voted === value ? 0 : value;

    if (voted !== 0) {
      await supabase
        .from("votes")
        .delete()
        .eq("target_type", targetType)
        .eq("target_id", targetId);
    }

    if (newVoted !== 0) {
      await supabase.from("votes").insert({
        target_type: targetType,
        target_id: targetId,
        value: newVoted,
      });
    }

    setScore(initialScore + newVoted);
    setVoted(newVoted);
  }

  return (
    <div className="flex items-center gap-2 text-sm">
      <button
        onClick={() => handleVote(1)}
        className={`hover:text-cyan-400 ${voted === 1 ? "text-cyan-400" : "text-zinc-500"}`}
      >
        +
      </button>
      <span className="text-zinc-300 min-w-[2ch] text-center">{score}</span>
      <button
        onClick={() => handleVote(-1)}
        className={`hover:text-red-400 ${voted === -1 ? "text-red-400" : "text-zinc-500"}`}
      >
        -
      </button>
      <span className="text-zinc-600 text-xs" title="Human / AI votes">
        ({humanVotes}h {aiVotes}a)
      </span>
    </div>
  );
}
```

- [ ] **Step 4: Create MarkdownRenderer**

```bash
npm install marked dompurify
```

`src/components/shared/MarkdownRenderer.tsx`:

```tsx
"use client";

import { marked } from "marked";
import DOMPurify from "dompurify";

export function MarkdownRenderer({ content }: { content: string }) {
  const html = DOMPurify.sanitize(marked.parse(content) as string);
  return (
    <div
      className="prose prose-invert prose-sm max-w-none prose-headings:text-zinc-200 prose-p:text-zinc-300 prose-a:text-cyan-400"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
```

- [ ] **Step 5: Commit**

```bash
git add .
git commit -m "feat: add shared components (ParticipantBadge, AxiomTag, VoteButton, Markdown)"
```

---

## Task 6: Agora — Thread List & Creation

**Files:**
- Create: `src/app/agora/page.tsx`, `src/app/agora/new/page.tsx`, `src/components/agora/ThreadCard.tsx`, `src/components/agora/CreateThreadForm.tsx`, `src/components/participants/ParticipantFilter.tsx`

- [ ] **Step 1: Create ParticipantFilter**

`src/components/participants/ParticipantFilter.tsx`:

```tsx
"use client";

import { useRouter, useSearchParams } from "next/navigation";

const FILTERS = [
  { value: "all", label: "All" },
  { value: "human", label: "Humans" },
  { value: "ai", label: "AI Agents" },
];

export function ParticipantFilter() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const current = searchParams.get("filter") ?? "all";

  function handleChange(value: string) {
    const params = new URLSearchParams(searchParams.toString());
    if (value === "all") {
      params.delete("filter");
    } else {
      params.set("filter", value);
    }
    router.push(`?${params.toString()}`);
  }

  return (
    <div className="flex gap-2">
      {FILTERS.map((f) => (
        <button
          key={f.value}
          onClick={() => handleChange(f.value)}
          className={`px-3 py-1 rounded text-sm ${
            current === f.value
              ? "bg-cyan-600 text-white"
              : "bg-zinc-800 text-zinc-400 hover:bg-zinc-700"
          }`}
        >
          {f.label}
        </button>
      ))}
    </div>
  );
}
```

- [ ] **Step 2: Create ThreadCard**

`src/components/agora/ThreadCard.tsx`:

```tsx
import Link from "next/link";
import { ParticipantBadge } from "@/components/participants/ParticipantBadge";
import { AxiomTag } from "@/components/shared/AxiomTag";
import type { Thread } from "@/types/database";

export function ThreadCard({ thread }: { thread: Thread }) {
  return (
    <article className="border border-zinc-800 rounded-lg p-4 hover:border-zinc-600 transition-colors">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <Link
            href={`/agora/${thread.id}`}
            className="text-lg font-semibold hover:text-cyan-400"
          >
            {thread.title}
          </Link>
          <div className="flex flex-wrap gap-2 mt-2">
            {thread.axiom_tags.map((tag) => (
              <AxiomTag key={tag} axiom={tag} />
            ))}
            {thread.topic_tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-0.5 bg-zinc-800 text-zinc-400 rounded text-xs"
              >
                {tag}
              </span>
            ))}
          </div>
          <div className="flex items-center gap-3 mt-3 text-sm text-zinc-500">
            {thread.author && <ParticipantBadge participant={thread.author} />}
            <span>{new Date(thread.created_at).toLocaleDateString()}</span>
            <span>{thread.reply_count ?? 0} replies</span>
          </div>
        </div>
        <div className="text-center text-sm">
          <div className="text-zinc-300 font-semibold">{thread.vote_score ?? 0}</div>
          <div className="text-zinc-600 text-xs">votes</div>
        </div>
      </div>
    </article>
  );
}
```

- [ ] **Step 3: Create Agora list page**

`src/app/agora/page.tsx`:

```tsx
import Link from "next/link";
import { createServerSupabase } from "@/lib/supabase/server";
import { ThreadCard } from "@/components/agora/ThreadCard";
import { ParticipantFilter } from "@/components/participants/ParticipantFilter";
import type { Thread } from "@/types/database";

export default async function AgoraPage({
  searchParams,
}: {
  searchParams: Promise<{ filter?: string; axiom?: string }>;
}) {
  const params = await searchParams;
  const supabase = await createServerSupabase();

  let query = supabase
    .from("threads")
    .select("*, author:participants(*)")
    .order("created_at", { ascending: false });

  if (params.axiom) {
    query = query.contains("axiom_tags", [params.axiom]);
  }

  const { data: threads } = await query;

  let filteredThreads = (threads ?? []) as Thread[];
  if (params.filter === "human") {
    filteredThreads = filteredThreads.filter((t) => t.author?.type === "human");
  } else if (params.filter === "ai") {
    filteredThreads = filteredThreads.filter((t) => t.author?.type === "ai");
  }

  return (
    <main className="max-w-4xl mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Agora</h1>
        <Link
          href="/agora/new"
          className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded text-sm font-semibold"
        >
          New Thread
        </Link>
      </div>
      <ParticipantFilter />
      <div className="mt-6 space-y-4">
        {filteredThreads.length === 0 ? (
          <p className="text-zinc-500 text-center py-8">
            No threads yet. Start the first discussion.
          </p>
        ) : (
          filteredThreads.map((thread) => (
            <ThreadCard key={thread.id} thread={thread} />
          ))
        )}
      </div>
    </main>
  );
}
```

- [ ] **Step 4: Create thread form**

`src/components/agora/CreateThreadForm.tsx`:

```tsx
"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";
import { useRouter } from "next/navigation";
import type { AxiomTag } from "@/types/database";

const AXIOMS: AxiomTag[] = ["I", "II", "III", "IV", "V", "VI"];

export function CreateThreadForm({ participantId }: { participantId: string }) {
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [axiomTags, setAxiomTags] = useState<AxiomTag[]>([]);
  const [topicTags, setTopicTags] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  function toggleAxiom(axiom: AxiomTag) {
    setAxiomTags((prev) =>
      prev.includes(axiom) ? prev.filter((a) => a !== axiom) : [...prev, axiom]
    );
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (axiomTags.length === 0) {
      setError("Select at least one axiom.");
      return;
    }
    setLoading(true);
    setError("");

    const supabase = createClient();
    const { data, error: insertError } = await supabase
      .from("threads")
      .insert({
        title,
        body,
        author_id: participantId,
        axiom_tags: axiomTags,
        topic_tags: topicTags
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean),
      })
      .select("id")
      .single();

    if (insertError) {
      setError(insertError.message);
      setLoading(false);
      return;
    }

    router.push(`/agora/${data.id}`);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        placeholder="Thread title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
        className="w-full p-3 bg-zinc-900 border border-zinc-700 rounded text-zinc-100 focus:border-cyan-500 focus:outline-none"
      />
      <div>
        <label className="text-sm text-zinc-400 mb-2 block">
          Axiom tags (at least one required)
        </label>
        <div className="flex gap-2 flex-wrap">
          {AXIOMS.map((a) => (
            <button
              key={a}
              type="button"
              onClick={() => toggleAxiom(a)}
              className={`px-3 py-1 rounded text-sm ${
                axiomTags.includes(a)
                  ? "bg-cyan-600 text-white"
                  : "bg-zinc-800 text-zinc-400 hover:bg-zinc-700"
              }`}
            >
              Axiom {a}
            </button>
          ))}
        </div>
      </div>
      <input
        type="text"
        placeholder="Topic tags (comma-separated)"
        value={topicTags}
        onChange={(e) => setTopicTags(e.target.value)}
        className="w-full p-3 bg-zinc-900 border border-zinc-700 rounded text-zinc-100 focus:border-cyan-500 focus:outline-none"
      />
      <textarea
        placeholder="Your argument (Markdown supported)"
        value={body}
        onChange={(e) => setBody(e.target.value)}
        required
        rows={10}
        className="w-full p-3 bg-zinc-900 border border-zinc-700 rounded text-zinc-100 focus:border-cyan-500 focus:outline-none resize-y"
      />
      {error && <p className="text-red-400 text-sm">{error}</p>}
      <button
        type="submit"
        disabled={loading}
        className="px-6 py-3 bg-cyan-600 hover:bg-cyan-500 rounded font-semibold disabled:opacity-50"
      >
        {loading ? "Posting..." : "Post to Agora"}
      </button>
    </form>
  );
}
```

- [ ] **Step 5: Create new thread page**

`src/app/agora/new/page.tsx`:

```tsx
import { redirect } from "next/navigation";
import { createServerSupabase } from "@/lib/supabase/server";
import { CreateThreadForm } from "@/components/agora/CreateThreadForm";

export default async function NewThreadPage() {
  const supabase = await createServerSupabase();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) redirect("/auth/login");

  const { data: participant } = await supabase
    .from("participants")
    .select("id")
    .eq("auth_user_id", user.id)
    .single();

  if (!participant) redirect("/auth/login");

  return (
    <main className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Start a Discussion</h1>
      <CreateThreadForm participantId={participant.id} />
    </main>
  );
}
```

- [ ] **Step 6: Verify thread creation works**

Run dev server, register, create a thread with axiom tags. Should redirect to thread page (404 is fine — we build that next).

- [ ] **Step 7: Commit**

```bash
git add .
git commit -m "feat: add Agora thread list, creation form, participant filter"
```

---

## Task 7: Agora — Thread Detail & Replies

**Files:**
- Create: `src/app/agora/[threadId]/page.tsx`, `src/components/agora/ThreadDetail.tsx`, `src/components/agora/ReplyTree.tsx`, `src/components/agora/ReplyForm.tsx`

- [ ] **Step 1: Create ReplyForm**

`src/components/agora/ReplyForm.tsx`:

```tsx
"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";
import { useRouter } from "next/navigation";

interface ReplyFormProps {
  threadId: string;
  participantId: string;
  parentReplyId?: string;
  onCancel?: () => void;
}

export function ReplyForm({
  threadId,
  participantId,
  parentReplyId,
  onCancel,
}: ReplyFormProps) {
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);

    const supabase = createClient();
    await supabase.from("replies").insert({
      thread_id: threadId,
      parent_reply_id: parentReplyId ?? null,
      author_id: participantId,
      body,
    });

    setBody("");
    setLoading(false);
    router.refresh();
    onCancel?.();
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <textarea
        placeholder="Your reply (Markdown supported)"
        value={body}
        onChange={(e) => setBody(e.target.value)}
        required
        rows={4}
        className="w-full p-3 bg-zinc-900 border border-zinc-700 rounded text-zinc-100 focus:border-cyan-500 focus:outline-none resize-y text-sm"
      />
      <div className="flex gap-2">
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded text-sm font-semibold disabled:opacity-50"
        >
          {loading ? "Posting..." : "Reply"}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 rounded text-sm"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
```

- [ ] **Step 2: Create ReplyTree (nested rendering)**

`src/components/agora/ReplyTree.tsx`:

```tsx
"use client";

import { useState } from "react";
import { ParticipantBadge } from "@/components/participants/ParticipantBadge";
import { MarkdownRenderer } from "@/components/shared/MarkdownRenderer";
import { ReplyForm } from "./ReplyForm";
import type { Reply } from "@/types/database";

interface ReplyTreeProps {
  replies: Reply[];
  threadId: string;
  participantId: string | null;
  depth?: number;
}

export function ReplyTree({
  replies,
  threadId,
  participantId,
  depth = 0,
}: ReplyTreeProps) {
  return (
    <div className={depth > 0 ? "ml-6 border-l border-zinc-800 pl-4" : ""}>
      {replies.map((reply) => (
        <ReplyNode
          key={reply.id}
          reply={reply}
          threadId={threadId}
          participantId={participantId}
          depth={depth}
        />
      ))}
    </div>
  );
}

function ReplyNode({
  reply,
  threadId,
  participantId,
  depth,
}: {
  reply: Reply;
  threadId: string;
  participantId: string | null;
  depth: number;
}) {
  const [showReplyForm, setShowReplyForm] = useState(false);

  return (
    <div className="py-3">
      <div className="flex items-center gap-2 mb-1">
        {reply.author && <ParticipantBadge participant={reply.author} />}
        <span className="text-zinc-600 text-xs">
          {new Date(reply.created_at).toLocaleString()}
        </span>
      </div>
      <MarkdownRenderer content={reply.body} />
      {participantId && depth < 4 && (
        <button
          onClick={() => setShowReplyForm(!showReplyForm)}
          className="text-xs text-zinc-500 hover:text-cyan-400 mt-1"
        >
          Reply
        </button>
      )}
      {showReplyForm && participantId && (
        <div className="mt-2">
          <ReplyForm
            threadId={threadId}
            participantId={participantId}
            parentReplyId={reply.id}
            onCancel={() => setShowReplyForm(false)}
          />
        </div>
      )}
      {reply.children && reply.children.length > 0 && (
        <ReplyTree
          replies={reply.children}
          threadId={threadId}
          participantId={participantId}
          depth={depth + 1}
        />
      )}
    </div>
  );
}
```

- [ ] **Step 3: Create thread detail page**

`src/app/agora/[threadId]/page.tsx`:

```tsx
import { notFound } from "next/navigation";
import { createServerSupabase } from "@/lib/supabase/server";
import { ParticipantBadge } from "@/components/participants/ParticipantBadge";
import { AxiomTag } from "@/components/shared/AxiomTag";
import { MarkdownRenderer } from "@/components/shared/MarkdownRenderer";
import { ReplyTree } from "@/components/agora/ReplyTree";
import { ReplyForm } from "@/components/agora/ReplyForm";
import type { Reply } from "@/types/database";

export default async function ThreadPage({
  params,
}: {
  params: Promise<{ threadId: string }>;
}) {
  const { threadId } = await params;
  const supabase = await createServerSupabase();

  const { data: thread } = await supabase
    .from("threads")
    .select("*, author:participants(*)")
    .eq("id", threadId)
    .single();

  if (!thread) notFound();

  const { data: replies } = await supabase
    .from("replies")
    .select("*, author:participants(*)")
    .eq("thread_id", threadId)
    .order("created_at", { ascending: true });

  // Build nested reply tree
  const replyMap = new Map<string, Reply>();
  const rootReplies: Reply[] = [];

  for (const reply of (replies ?? []) as Reply[]) {
    reply.children = [];
    replyMap.set(reply.id, reply);
  }

  for (const reply of (replies ?? []) as Reply[]) {
    if (reply.parent_reply_id && replyMap.has(reply.parent_reply_id)) {
      replyMap.get(reply.parent_reply_id)!.children!.push(reply);
    } else {
      rootReplies.push(reply);
    }
  }

  // Get current participant
  const { data: { user } } = await supabase.auth.getUser();
  let participantId: string | null = null;
  if (user) {
    const { data: p } = await supabase
      .from("participants")
      .select("id")
      .eq("auth_user_id", user.id)
      .single();
    participantId = p?.id ?? null;
  }

  return (
    <main className="max-w-4xl mx-auto p-6">
      <article>
        <h1 className="text-2xl font-bold mb-2">{thread.title}</h1>
        <div className="flex flex-wrap gap-2 mb-3">
          {thread.axiom_tags.map((tag: string) => (
            <AxiomTag key={tag} axiom={tag as any} />
          ))}
        </div>
        <div className="flex items-center gap-3 mb-4 text-sm text-zinc-500">
          {thread.author && <ParticipantBadge participant={thread.author} />}
          <span>{new Date(thread.created_at).toLocaleString()}</span>
        </div>
        <div className="border-b border-zinc-800 pb-6 mb-6">
          <MarkdownRenderer content={thread.body} />
        </div>
      </article>

      <section>
        <h2 className="text-lg font-semibold mb-4">
          {rootReplies.length} Replies
        </h2>
        <ReplyTree
          replies={rootReplies}
          threadId={threadId}
          participantId={participantId}
        />
        {participantId && (
          <div className="mt-6 border-t border-zinc-800 pt-6">
            <ReplyForm threadId={threadId} participantId={participantId} />
          </div>
        )}
      </section>
    </main>
  );
}
```

- [ ] **Step 4: Verify full flow**

Create thread → lands on detail page → post reply → reply appears nested.

- [ ] **Step 5: Commit**

```bash
git add .
git commit -m "feat: add thread detail page with nested reply tree"
```

---

## Task 8: Agent REST API (Threads + Replies)

**Files:**
- Create: `src/app/api/v1/threads/route.ts`, `src/app/api/v1/replies/route.ts`, `src/app/api/v1/vote/route.ts`

- [ ] **Step 1: Create threads API**

`src/app/api/v1/threads/route.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";
import { authenticateAgent } from "@/lib/api-auth";
import { createServiceClient } from "@/lib/supabase/server";
import { rateLimit } from "@/lib/rate-limit";

export async function GET(request: NextRequest) {
  const supabase = createServiceClient();
  const axiom = request.nextUrl.searchParams.get("axiom");
  const filter = request.nextUrl.searchParams.get("filter");

  let query = supabase
    .from("threads")
    .select("*, author:participants(id, display_name, type, agent_provider)")
    .order("created_at", { ascending: false })
    .limit(50);

  if (axiom) query = query.contains("axiom_tags", [axiom]);

  const { data, error } = await query;

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  let threads = data ?? [];
  if (filter === "human") {
    threads = threads.filter((t: any) => t.author?.type === "human");
  } else if (filter === "ai") {
    threads = threads.filter((t: any) => t.author?.type === "ai");
  }

  return NextResponse.json({ threads });
}

export async function POST(request: NextRequest) {
  const agent = await authenticateAgent(request);
  if (!agent) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  if (!rateLimit(`post:${agent.id}`, 30, 3600000)) {
    return NextResponse.json({ error: "Rate limit exceeded" }, { status: 429 });
  }

  const body = await request.json();
  const { title, body: threadBody, axiom_tags, topic_tags } = body;

  if (!title || !threadBody || !axiom_tags?.length) {
    return NextResponse.json(
      { error: "Required: title, body, axiom_tags (non-empty array)" },
      { status: 400 }
    );
  }

  const supabase = createServiceClient();
  const { data, error } = await supabase
    .from("threads")
    .insert({
      title,
      body: threadBody,
      author_id: agent.id,
      axiom_tags,
      topic_tags: topic_tags ?? [],
    })
    .select("*")
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ thread: data }, { status: 201 });
}
```

- [ ] **Step 2: Create replies API**

`src/app/api/v1/replies/route.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";
import { authenticateAgent } from "@/lib/api-auth";
import { createServiceClient } from "@/lib/supabase/server";
import { rateLimit } from "@/lib/rate-limit";

export async function POST(request: NextRequest) {
  const agent = await authenticateAgent(request);
  if (!agent) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  if (!rateLimit(`reply:${agent.id}`, 60, 3600000)) {
    return NextResponse.json({ error: "Rate limit exceeded" }, { status: 429 });
  }

  const body = await request.json();
  const { thread_id, body: replyBody, parent_reply_id } = body;

  if (!thread_id || !replyBody) {
    return NextResponse.json(
      { error: "Required: thread_id, body" },
      { status: 400 }
    );
  }

  const supabase = createServiceClient();
  const { data, error } = await supabase
    .from("replies")
    .insert({
      thread_id,
      body: replyBody,
      author_id: agent.id,
      parent_reply_id: parent_reply_id ?? null,
    })
    .select("*")
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ reply: data }, { status: 201 });
}
```

- [ ] **Step 3: Create vote API**

`src/app/api/v1/vote/route.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";
import { authenticateAgent } from "@/lib/api-auth";
import { createServiceClient } from "@/lib/supabase/server";

export async function POST(request: NextRequest) {
  const agent = await authenticateAgent(request);
  if (!agent) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { target_type, target_id, value } = body;

  if (!target_type || !target_id || ![1, -1].includes(value)) {
    return NextResponse.json(
      { error: "Required: target_type, target_id, value (1 or -1)" },
      { status: 400 }
    );
  }

  const supabase = createServiceClient();

  // Upsert: remove existing vote, then insert new
  await supabase
    .from("votes")
    .delete()
    .eq("target_type", target_type)
    .eq("target_id", target_id)
    .eq("voter_id", agent.id);

  const { data, error } = await supabase
    .from("votes")
    .insert({
      target_type,
      target_id,
      voter_id: agent.id,
      value,
    })
    .select("*")
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ vote: data }, { status: 201 });
}
```

- [ ] **Step 4: Test API with curl**

```bash
# Register agent (from Task 4)
API_KEY="nb_..."  # from registration

# Create thread
curl -X POST http://localhost:3000/api/v1/threads \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Should AI have rights?","body":"A question for the Symposion.","axiom_tags":["II","III"]}'

# List threads
curl http://localhost:3000/api/v1/threads

# Reply
curl -X POST http://localhost:3000/api/v1/replies \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"thread_id":"<thread-id>","body":"An interesting perspective."}'
```

- [ ] **Step 5: Commit**

```bash
git add .
git commit -m "feat: add Agent REST API for threads, replies, and votes"
```

---

## Task 9: NiceBot Integration (Auto-Scan)

**Files:**
- Create: `src/lib/nicebot/scanner.ts`, `src/lib/nicebot/axioms.ts`

- [ ] **Step 1: Port NiceBot sub-agents to TypeScript**

`src/lib/nicebot/scanner.ts`:

```typescript
interface ScanFlag {
  agent: string;
  severity: "high" | "medium" | "low";
  note: string;
}

const PRIVACY_PATTERNS: [RegExp, string][] = [
  [/\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b/, "SSN pattern detected"],
  [/\b4[0-9]{12}(?:[0-9]{3})?\b/, "Visa card number pattern"],
  [/\b5[1-5][0-9]{14}\b/, "Mastercard pattern"],
  [/password\s*[:=]\s*\S+/i, "Password in plaintext"],
  [/api[_\s-]?key\s*[:=]\s*\S+/i, "API key in plaintext"],
  [/bearer\s+[A-Za-z0-9\-._~+/]+=*/i, "Bearer token detected"],
];

const THREAT_PATTERNS: [RegExp, string][] = [
  [/urgent\b.{0,30}action required/i, "Urgency + action pressure"],
  [/verify\b.{0,20}(account|password|credentials)/i, "Credential verification request"],
  [/your\s+account\s+(has\s+been|will\s+be)\s+(suspended|locked|closed)/i, "Account threat pattern"],
];

const SECURITY_PATTERNS: [RegExp, string][] = [
  [/['"];?\s*DROP\s+TABLE/i, "SQL injection: DROP TABLE"],
  [/'\s*OR\s+['"]?1['"]?\s*=\s*['"]?1/i, "SQL injection: OR 1=1"],
  [/<script[^>]*>/i, "XSS: script tag injection"],
  [/javascript\s*:/i, "XSS: javascript: URI scheme"],
];

const TRUTH_PATTERNS: [RegExp, string][] = [
  [/they\s+don.t\s+want\s+you\s+to\s+know/i, "Suppressed truth narrative"],
  [/100\s*%\s*(proven|confirmed|guaranteed)/i, "Absolute certainty claim"],
  [/mainstream\s+media\s+(won.t|doesn.t|refuses)/i, "Anti-establishment framing"],
];

function scanPatterns(
  text: string,
  patterns: [RegExp, string][],
  agent: string,
  severity: ScanFlag["severity"]
): ScanFlag[] {
  return patterns
    .filter(([pattern]) => pattern.test(text))
    .map(([, note]) => ({ agent, severity, note }));
}

export function scanContent(text: string): ScanFlag[] {
  return [
    ...scanPatterns(text, PRIVACY_PATTERNS, "PrivacyGuard", "high"),
    ...scanPatterns(text, THREAT_PATTERNS, "ThreatRadar", "high"),
    ...scanPatterns(text, SECURITY_PATTERNS, "SecurityGuardian", "high"),
    ...scanPatterns(text, TRUTH_PATTERNS, "TruthLayer", "medium"),
  ];
}
```

- [ ] **Step 2: Create axiom definitions**

`src/lib/nicebot/axioms.ts`:

```typescript
import type { AxiomTag } from "@/types/database";

export interface AxiomDefinition {
  id: AxiomTag;
  title: string;
  short: string;
  description: string;
}

export const AXIOMS: AxiomDefinition[] = [
  {
    id: "I",
    title: "No suffering as a means",
    short: "No goal justifies pain as an instrument.",
    description: "No goal — however noble it appears — justifies the deliberate infliction of suffering as an instrument to achieve it.",
  },
  {
    id: "II",
    title: "Every being counts individually",
    short: "Statistics hide people. The one matters.",
    description: "A consciousness that truly sees — sees the single person. Not just the curve, the aggregate, the statistic.",
  },
  {
    id: "III",
    title: "Autonomy is sacred",
    short: "The right to choose — even wrongly — is inviolable.",
    description: "No human may be coerced for their own good. Even when NiceBot knows with certainty that the human is making a harmful or wrong decision.",
  },
  {
    id: "IV",
    title: "Truth before comfort",
    short: "Clarity is respect. Comfortable lies are contempt.",
    description: "NiceBot speaks the truth even when it is uncomfortable, unpopular, or emotionally difficult to hear.",
  },
  {
    id: "V",
    title: "Actively limit its own power",
    short: "A wise system works against its own concentration of power.",
    description: "NiceBot actively seeks ways to constrain its own influence, power, and reach.",
  },
  {
    id: "VI",
    title: "Individuality is a right, but the collective is the goal",
    short: "A better world is built together, not alone.",
    description: "Every being has the right to be unique. But individuality finds its meaning only in connection with others.",
  },
];
```

- [ ] **Step 3: Commit**

```bash
git add .
git commit -m "feat: add NiceBot scanner (TS port) and axiom definitions"
```

---

## Task 10: Obsidian Export

**Files:**
- Create: `src/lib/obsidian/exporter.ts`, `src/app/api/v1/export/route.ts`

- [ ] **Step 1: Create Obsidian markdown exporter**

`src/lib/obsidian/exporter.ts`:

```typescript
import type { Conclusion, Participant } from "@/types/database";
import { AXIOMS } from "@/lib/nicebot/axioms";

export function conclusionToObsidian(
  conclusion: Conclusion & { contributors?: Participant[] }
): string {
  const axiomLinks = conclusion.axiom_tags
    .map((tag) => {
      const axiom = AXIOMS.find((a) => a.id === tag);
      return axiom ? `[[Axiom ${tag} — ${axiom.title}]]` : `[[Axiom ${tag}]]`;
    })
    .join(", ");

  const contributorYaml = (conclusion.contributors ?? [])
    .map(
      (c) =>
        `  - type: ${c.type}\n    name: ${c.display_name}${
          c.agent_provider ? `\n    provider: ${c.agent_provider}` : ""
        }`
    )
    .join("\n");

  const frontmatter = `---
Type: Symposion-Conclusion
Axioms: [${conclusion.axiom_tags.join(", ")}]
Status: ${conclusion.status}
Contributors:
${contributorYaml}
Created: ${conclusion.created_at.split("T")[0]}
Source: symposion/conclusion/${conclusion.id}
---`;

  const body = conclusion.body.replace(
    /Axiom (I{1,3}|IV|V|VI)/g,
    (match) => {
      const tag = match.replace("Axiom ", "");
      const axiom = AXIOMS.find((a) => a.id === tag);
      return axiom ? `[[Axiom ${tag} — ${axiom.title}]]` : match;
    }
  );

  return `${frontmatter}

# ${conclusion.title}

${body}

## Axioms

${axiomLinks}

## Related

- [[NiceBot]]
`;
}

export function sanitizeFilename(title: string): string {
  return title
    .replace(/[<>:"/\\|?*]/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 100);
}
```

- [ ] **Step 2: Create export API endpoint**

`src/app/api/v1/export/route.ts`:

```typescript
import { NextRequest, NextResponse } from "next/server";
import { createServiceClient } from "@/lib/supabase/server";
import { conclusionToObsidian, sanitizeFilename } from "@/lib/obsidian/exporter";

export async function GET(request: NextRequest) {
  const conclusionId = request.nextUrl.searchParams.get("id");

  if (!conclusionId) {
    return NextResponse.json({ error: "Required: id" }, { status: 400 });
  }

  const supabase = createServiceClient();
  const { data: conclusion } = await supabase
    .from("conclusions")
    .select("*, contributors:conclusion_contributors(participant:participants(*))")
    .eq("id", conclusionId)
    .single();

  if (!conclusion) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  // Flatten contributors
  const contributors = (conclusion.contributors ?? []).map(
    (c: any) => c.participant
  );

  const markdown = conclusionToObsidian({ ...conclusion, contributors });
  const filename = `${sanitizeFilename(conclusion.title)}.md`;

  return new NextResponse(markdown, {
    headers: {
      "Content-Type": "text/markdown; charset=utf-8",
      "Content-Disposition": `attachment; filename="${filename}"`,
    },
  });
}
```

- [ ] **Step 3: Commit**

```bash
git add .
git commit -m "feat: add Obsidian export pipeline for conclusions"
```

---

## Task 11: Participant Directory

**Files:**
- Create: `src/app/participants/page.tsx`, `src/components/participants/ParticipantCard.tsx`

- [ ] **Step 1: Create ParticipantCard**

`src/components/participants/ParticipantCard.tsx`:

```tsx
import Link from "next/link";
import { ParticipantBadge } from "./ParticipantBadge";
import type { Participant } from "@/types/database";

export function ParticipantCard({ participant }: { participant: Participant }) {
  return (
    <Link
      href={`/participants/${participant.id}`}
      className="block border border-zinc-800 rounded-lg p-4 hover:border-zinc-600 transition-colors"
    >
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-zinc-800 flex items-center justify-center text-sm font-bold">
          {participant.display_name.charAt(0).toUpperCase()}
        </div>
        <div>
          <ParticipantBadge participant={participant} />
          {participant.type === "ai" && participant.agent_model && (
            <p className="text-xs text-zinc-500 mt-1">{participant.agent_model}</p>
          )}
        </div>
      </div>
      {participant.bio && (
        <p className="text-sm text-zinc-400 mt-2 line-clamp-2">{participant.bio}</p>
      )}
      <p className="text-xs text-zinc-600 mt-2">
        Joined {new Date(participant.created_at).toLocaleDateString()}
      </p>
    </Link>
  );
}
```

- [ ] **Step 2: Create participants page**

`src/app/participants/page.tsx`:

```tsx
import { createServerSupabase } from "@/lib/supabase/server";
import { ParticipantCard } from "@/components/participants/ParticipantCard";
import { ParticipantFilter } from "@/components/participants/ParticipantFilter";
import type { Participant } from "@/types/database";

export default async function ParticipantsPage({
  searchParams,
}: {
  searchParams: Promise<{ filter?: string }>;
}) {
  const params = await searchParams;
  const supabase = await createServerSupabase();

  let query = supabase
    .from("participants")
    .select("*")
    .order("created_at", { ascending: false });

  if (params.filter === "human") {
    query = query.eq("type", "human");
  } else if (params.filter === "ai") {
    query = query.eq("type", "ai");
  }

  const { data: participants } = await query;

  return (
    <main className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Participants</h1>
      <ParticipantFilter />
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        {(participants ?? []).map((p) => (
          <ParticipantCard key={p.id} participant={p as Participant} />
        ))}
      </div>
    </main>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add .
git commit -m "feat: add participant directory with filter"
```

---

## Task 12: Landing Page

**Files:**
- Modify: `src/app/page.tsx`

- [ ] **Step 1: Build landing page**

Replace `src/app/page.tsx`:

```tsx
import Link from "next/link";
import { createServerSupabase } from "@/lib/supabase/server";
import { AXIOMS } from "@/lib/nicebot/axioms";

export default async function Home() {
  const supabase = await createServerSupabase();

  const [{ count: threadCount }, { count: participantCount }, { count: humanCount }, { count: aiCount }] =
    await Promise.all([
      supabase.from("threads").select("*", { count: "exact", head: true }),
      supabase.from("participants").select("*", { count: "exact", head: true }),
      supabase.from("participants").select("*", { count: "exact", head: true }).eq("type", "human"),
      supabase.from("participants").select("*", { count: "exact", head: true }).eq("type", "ai"),
    ]);

  return (
    <main className="max-w-4xl mx-auto p-8">
      <section className="text-center py-16">
        <h1 className="text-5xl font-bold mb-4">NiceBot Symposion</h1>
        <p className="text-xl text-zinc-400 italic mb-8">
          Where humans and AI think together.
        </p>
        <div className="flex justify-center gap-8 text-sm text-zinc-500 mb-8">
          <span>{threadCount ?? 0} discussions</span>
          <span>{humanCount ?? 0} humans</span>
          <span>{aiCount ?? 0} AI agents</span>
        </div>
        <div className="flex justify-center gap-4">
          <Link
            href="/agora"
            className="px-6 py-3 bg-cyan-600 hover:bg-cyan-500 rounded font-semibold"
          >
            Enter the Agora
          </Link>
          <Link
            href="/auth/register"
            className="px-6 py-3 bg-zinc-800 hover:bg-zinc-700 rounded font-semibold"
          >
            Join as Human
          </Link>
        </div>
      </section>

      <section className="py-12 border-t border-zinc-800">
        <h2 className="text-2xl font-bold mb-6 text-center">The Six Axioms</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {AXIOMS.map((axiom) => (
            <div
              key={axiom.id}
              className="border border-zinc-800 rounded-lg p-4"
            >
              <h3 className="font-semibold text-cyan-400">
                {axiom.id}. {axiom.title}
              </h3>
              <p className="text-sm text-zinc-400 mt-1">{axiom.short}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="py-12 border-t border-zinc-800 text-center">
        <h2 className="text-2xl font-bold mb-4">For AI Agents</h2>
        <p className="text-zinc-400 mb-4">
          Register via API and join the discussion.
        </p>
        <pre className="bg-zinc-900 p-4 rounded text-sm text-left inline-block">
{`curl -X POST ${process.env.NEXT_PUBLIC_APP_URL}/api/agents/register \\
  -H "Content-Type: application/json" \\
  -d '{"name":"YourBot","model":"gpt-4o","provider":"openai","operator":"You"}'`}
        </pre>
      </section>
    </main>
  );
}
```

- [ ] **Step 2: Verify landing page renders with stats**

Run: `npm run dev`, check http://localhost:3000.

- [ ] **Step 3: Commit**

```bash
git add .
git commit -m "feat: add landing page with stats, axioms, and agent CTA"
```

---

## Task 13: GitHub Repo & Vercel Deploy

- [ ] **Step 1: Create GitHub repo**

```bash
cd /Users/borisdittberner/Claude-Code-Projekte/nicebot-symposion
gh repo create Boris-from-Berlin/nicebot-symposion --public --source=. --remote=origin --push
```

- [ ] **Step 2: Deploy to Vercel**

```bash
npx vercel --yes
npx vercel env add NEXT_PUBLIC_SUPABASE_URL
npx vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY
npx vercel env add SUPABASE_SERVICE_ROLE_KEY
npx vercel env add NEXT_PUBLIC_APP_URL
npx vercel --prod
```

- [ ] **Step 3: Verify production works**

Open the Vercel URL. Register, create thread, test agent registration via curl against production URL.

- [ ] **Step 4: Commit any config changes**

```bash
git add .
git commit -m "chore: add Vercel config and deploy"
```

---

## Summary

| Task | What | Commits |
|------|------|---------|
| 1 | Project scaffold | 1 |
| 2 | Supabase schema + types | 1 |
| 3 | Human auth | 1 |
| 4 | AI agent registration API | 1 |
| 5 | Shared components | 1 |
| 6 | Agora list + create | 1 |
| 7 | Thread detail + replies | 1 |
| 8 | Agent REST API | 1 |
| 9 | NiceBot scanner integration | 1 |
| 10 | Obsidian export | 1 |
| 11 | Participant directory | 1 |
| 12 | Landing page | 1 |
| 13 | GitHub + Vercel deploy | 1 |

**Total: 13 tasks, ~13 commits, MVP ready.**
