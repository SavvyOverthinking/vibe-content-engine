# vibe-content-engine

An experimental agentic blog writing system built on [Claude Code](https://claude.ai/code).

**This is not a standalone tool.** It runs entirely inside Claude Code using its subagent system. You need Claude Code to use it.

See it in action: [savvyoverthinking.substack.com](https://savvyoverthinking.substack.com/) — all posts produced with this system plus light human editorial passes before publishing.

---

## What It Does

You provide a voice profile and a brief. The system runs a full editorial pipeline — research, structure, drafting, humanization review, voice quality gates, fact-checking, SEO — and delivers a publication-ready article.

```
Brief + Voice Profile
        ↓
[Interrogator]        — extracts your knowledge and argument from the brief
        ↓
[Research Lead]       — finds and validates credible sources
        ↓
[Structure Architect] — designs section-by-section narrative architecture
        ↓
[Voice Writer]        — drafts the article in your voice
        ↓
[Humanizer]           — flags AI-writing patterns (report only, no rewrites)
        ↓
[Tone Police]         — quality gate: must score 9.0+/10 to proceed
        ↓
[Fact Checker]        — quality gate: zero critical citation errors to proceed
        ↓
[SEO Optimizer]       — improves discoverability without touching voice
        ↓
Published article + complete archive
```

Each agent runs in its own Claude Code context window via the Task tool. The orchestrator coordinates handoffs and enforces quality gates.

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

Open the project in Claude Code, then:

```
@orchestrator start
```

The orchestrator prompts for voice profile, brief, and mode, then runs the full pipeline.

**Modes:**
- `automated` — runs end-to-end without pausing (fastest)
- `interactive` — pauses after each stage for review
- `partial` — you specify which stages to run

**Shorthand invocation** (skip the prompts):

```
@orchestrator start Voice: my-voice.md Brief: concepts/briefs/my-topic-brief.md Slug: my-article-slug Mode: automated
```

**Resume an interrupted production:**

```
@orchestrator resume my-article-slug
```

**Check production status:**

```
@orchestrator status
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
| `research-lead` | Finds and validates sources |
| `structure-architect` | Designs narrative architecture |
| `voice-writer` | Drafts the article |
| `humanizer` | Flags AI-writing patterns (report only) |
| `tone-police` | Voice quality gate (9.0+/10 required) |
| `fact-checker` | Citation quality gate (zero critical errors) |
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

## See It Working

All posts at [savvyoverthinking.substack.com](https://savvyoverthinking.substack.com/) were produced with this system and lightly edited before publishing. The pipeline, voice profile structure, and brief format used for those posts are the same ones in this repo.

---

## Notes

- Built and tested on Claude Sonnet 4.5/4.6. Agent quality scales with model capability.
- The voice extractor requires an Anthropic API key and makes LLM calls. Everything else runs through Claude Code with no extra API usage beyond your normal Claude Code subscription.
- Interactive mode is recommended for your first production run so you can see what each stage produces.
- The humanizer produces a flagged report — it does not rewrite your draft. You decide what to change.
