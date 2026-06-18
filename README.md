# vibe-content-engine

An agentic blog writing system built on [Claude Code](https://claude.ai/code).

**This is not a standalone tool.** It runs entirely inside Claude Code using its subagent system. You need Claude Code to use it.

---

## What It Does

You provide a voice profile and a brief. The system runs a full editorial pipeline — research, structure, drafting, humanization review, voice quality gates, fact-checking, SEO — and delivers a publication-ready article.

```
Brief + Voice Profile
        ↓
[Interrogator]        — extracts your knowledge and argument from the brief
        ↓
[Research Lead]       — finds and validates sources (live web research or a local knowledge base)
        ↓
[Structure Architect] — designs section-by-section narrative architecture
        ↓
[Voice Writer]        — drafts the article in your voice
        ↓
[Humanizer]           — flags AI-writing patterns (report only, no rewrites)
        ↓
[Tone Police]         — quality gate: must score 9.0+/10 to proceed
        ↓
[Fact Checker]        — quality gate: independent fact verification, zero critical errors to proceed
        ↓
[SEO Optimizer]       — improves discoverability without touching voice
        ↓
Published article + complete archive
```

Each agent runs in its own Claude Code context window via the Task tool. The orchestrator coordinates handoffs and enforces quality gates.

---

## See It Working

All posts at [savvyoverthinking.substack.com](https://savvyoverthinking.substack.com/) were produced with this system and lightly edited before publishing. The pipeline, voice profile structure, and brief format used for those posts are the same ones in this repo.

---

## Requirements

- [Claude Code](https://claude.ai/code) — required, this runs inside it
- Python 3.8+ — for voice extraction only
- Anthropic API key — for voice extraction only

---

## Setup

### Step 1: Clone and install

```bash
git clone https://github.com/SavvyOverthinking/vibe-content-engine.git
cd vibe-content-engine
```

No additional Claude Code setup needed — the agents are defined in `.claude/agents/` and load automatically when you open the project in Claude Code.

### Step 2: Extract your voice profile

```bash
export ANTHROPIC_API_KEY="your-key-here"

cd voice_extractor
pip install -r requirements.txt
python main.py https://your-blog.com --name my-voice --articles 10 --save-examples
```

This creates `my-voice/my-voice.md` (voice profile) and `my-voice/examples/my-voice/*.md` (sample articles for calibration).

Analyze 8-12 representative articles minimum. The "What to AVOID" section of the generated profile is the most important part — the more specific, the better.

### Step 3: Review and refine the voice profile

Open `my-voice/my-voice.md` and edit:
- Tone characteristics
- Writing style patterns
- Signature phrases
- **What to AVOID** — be brutal here

The system enforces this list through multiple quality gates.

---

## Writing a Brief

A brief is a markdown file that tells the system what to write and why. It does not need to be polished prose — structured notes work fine. The interrogator agent extracts what matters.

Copy a template and fill it in:

```bash
cp concepts/templates/standard-brief.md concepts/briefs/my-topic-brief.md
```

**Available templates:**
- `standard-brief.md` — general article structure
- `metaphor-brief.md` — narrative built around a central metaphor
- `challenge-brief.md` — problem/solution based

A good brief includes:
- The thesis or core argument
- Key observations and data points
- Specific examples and evidence
- Tone notes
- Source inventory (URLs you want cited)
- What the piece is NOT (scope control)

Richer briefs produce better output. The system does not invent your argument — it develops and validates the one you provide.

---

## Running Production

Open the project in Claude Code and prompt the orchestrator. There are three ways to drive it — from least to most control. All three run the same pipeline.

### 1. Interactive — let it ask you

```
@orchestrator start
```

It walks you through four questions, then runs the pipeline:

1. **Voice** — which profile from `my-voice/` to write in
2. **Brief** — load one from `concepts/briefs/`, start from a template, or paste it
3. **Mode** — `automated`, `interactive`, or `partial`
4. **Knowledge source** — `online` or `local` (see below)

### 2. Shorthand — pass the settings inline

Skip the questions by naming the settings in your prompt. Anything you provide is used as-is; anything you leave out, it asks about.

```
@orchestrator start Voice: my-voice.md Brief: concepts/briefs/my-topic-brief.md Slug: my-article-slug Mode: automated Source: online
```

| Setting | What it controls | Example |
|---|---|---|
| `Voice` | Voice profile in `my-voice/` | `my-voice.md` |
| `Brief` | Path to the brief | `concepts/briefs/my-topic-brief.md` |
| `Slug` | Output filename / id | `agent-control-theory` |
| `Mode` | `automated` / `interactive` / `partial` | `automated` |
| `Source` | `online`, or `local:<path>` for an offline knowledge base | `local:/abs/path/to/kb` |

**Modes:** `automated` runs end-to-end without pausing (fastest) · `interactive` pauses after each stage for review · `partial` runs only the stages you name.

### 3. Natural language — just describe the job

The orchestrator also reads plain-English instructions and maps them to the same settings. This is the most flexible way to prompt it — handy when you want to derive a voice on the fly, point it at a source folder, or set hard constraints. For example:

> Run a full production in automated mode. Develop the voice from the draft at `./drafts/my-post.md`, then rebuild that post. Don't use the web — research and fact-check **only** against the files in `./knowledge/`. Include links to every citation, and avoid any personal or business-sensitive details.

The orchestrator reads that as: `Mode: automated`, voice derived from the draft, brief = the draft, and `Source: local:./knowledge/` — then runs without further questions.

### Knowledge source: online vs local

- **`online`** (default) — research-lead and fact-checker use live web research to find and independently verify sources.
- **`local`** — they draw **only** from a local knowledge base you provide; **no internet**. Give the absolute path to the folder. Every claim is traced back to those files, and anything the knowledge base can't support is flagged. Use it for private corpora, internal docs, or any piece where you want full provenance and zero outside sources.

### Resume or check status

```
@orchestrator resume my-article-slug   # continue an interrupted run
@orchestrator status                   # list in-progress + published work
```

---

## Output

Completed articles land in `published/your-slug.md` alongside a production summary. All working artifacts (interrogation, research validation, structure blueprint, draft, quality gate reports, SEO report) are archived to `archive/your-slug/`.

---

## Quality Gates

**Tone Police** requires a 9.0+/10 score with zero critical AI-tells before proceeding. If it fails, the system stops and you choose: regenerate, edit manually, or abort.

**Fact Checker** requires zero critical issues — no broken citations, inaccurate claims, or misattributions. Warnings are noted but don't block. Critical issues do.

These gates exist to protect voice consistency and factual accuracy. They block for real.

---

## File Organization

```
.claude/
├── agents/         # All 10 subagent definitions (loaded automatically)
└── commands/
    └── orchestrator.md

voice_extractor/    # Python voice extraction tool
concepts/
└── templates/      # Brief templates (standard, metaphor, challenge)

my-voice/           # Your voice profiles — gitignored, not shared
working/            # Active production workspace — gitignored
archive/            # Completed production artifacts — gitignored
published/          # Your published articles — gitignored
```

Personal files (voice profiles, briefs, working files, published articles) are gitignored. Only the system infrastructure is in the repo.

---

## What's in `.claude/agents/`

Ten production subagents, each with YAML frontmatter specifying allowed tools and model:

| Agent | Role |
|---|---|
| `orchestrator` | Coordinates the pipeline, enforces quality gates |
| `interrogator` | Extracts argument and knowledge from brief |
| `research-lead` | Finds and validates sources (web research or local knowledge base) |
| `structure-architect` | Designs narrative architecture |
| `voice-writer` | Drafts the article |
| `humanizer` | Flags AI-writing patterns (report only) |
| `tone-police` | Voice quality gate (9.0+/10 required) |
| `fact-checker` | Independent fact-check gate — web or local KB (zero critical errors) |
| `seo-optimizer` | Optimizes discoverability without touching voice |
| `editorial-director` | Optional overall quality review |

To make the agents available across all your projects (not just this one), copy them to `~/.claude/agents/`.

---

## Research Integration

The system uses a voice-first citation pattern:

```
CORRECT:
"I've watched teams with 70+ NPS fail at enterprise.
[CB Insights data](url) confirms: 42% of startups fail because
users love the product but can't buy it."

INCORRECT:
"According to CB Insights (2024), 42% of startups fail due to no
market need, demonstrating that user satisfaction doesn't equal viability."
```

Your observation leads. Research validates. The writer agents enforce this.

---

## Notes

- Agents use `model: inherit`, so they run on whatever model you have Claude Code set to — run Opus for the strongest writing, or pin a tier (`sonnet`/`opus`/`haiku`) per agent in its frontmatter. Built and tested on Sonnet 4.5/4.6 and Opus; quality scales with model capability.
- The voice extractor requires an Anthropic API key and makes LLM calls. Everything else runs through Claude Code with no extra API usage beyond your normal Claude Code subscription.
- Interactive mode is recommended for your first production run so you can see what each stage produces.
- The humanizer produces a flagged report — it does not rewrite your draft. You decide what to change.
