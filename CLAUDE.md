# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **blog production system** built on Claude Code subagents. It transforms concepts into publication-ready blog posts through an orchestrated multi-agent workflow while maintaining authentic voice.

## Architecture: Subagents via Task Tool

**IMPORTANT**: The blog production agents are defined as proper Claude Code subagents in `.claude/agents/` with YAML frontmatter. The orchestrator invokes them using the **Task tool**.

### Subagent Locations

Blog production subagents are included at the **project level** (`.claude/agents/`), so they work automatically when you clone this repo:

- `.claude/agents/interrogator.md`
- `.claude/agents/research-lead.md`
- `.claude/agents/structure-architect.md`
- `.claude/agents/voice-writer.md`
- `.claude/agents/humanizer.md`
- `.claude/agents/tone-police.md`
- `.claude/agents/fact-checker.md`
- `.claude/agents/seo-optimizer.md`
- `.claude/agents/editorial-director.md`
- `.claude/agents/production-manager.md`

To make agents available across all projects, copy them to `~/.claude/agents/`.

### How Subagent Invocation Works

```
User: "@orchestrator start"

Orchestrator workflow:
1. Asks user for voice, brief, mode
2. Uses Task tool: subagent_type="interrogator"
3. Interrogator runs in its own context window
4. Returns output: working/interrogation-{slug}.md
5. Uses Task tool: subagent_type="research-lead"
6. Research-lead runs in its own context window
7. Returns output: working/research-validation-{slug}.md
8. ... continues through all stages
```

### Subagent File Format

Each subagent has YAML frontmatter specifying:
- `name`: Subagent identifier (e.g., "interrogator")
- `description`: When to use this subagent (Claude uses this for auto-delegation)
- `model`: Which model to use. Defaults to `inherit` (the agent runs on whatever model you're running Claude Code with). You can pin a tier (`sonnet` / `opus` / `haiku`) or a specific model ID per agent if you want to. **Do not hard-code dated model IDs** — they go stale and break the agent when that snapshot is retired.
- `allowed-tools`: Tool restrictions for this subagent

Example:
```yaml
---
name: interrogator
description: MUST BE USED for extracting knowledge from article briefs...
model: inherit
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Interrogator Agent
[agent instructions...]
```

## System Requirements

### Voice Profile (REQUIRED)

The system requires a voice profile before use:

**Extract a voice profile**:
```bash
cd voice_extractor
pip install -r requirements.txt
python main.py https://blog-url --name my-voice --articles 10
```

This creates:
- `my-voice/my-voice.md` - Voice profile
- `my-voice/examples/my-voice/*.md` - Example articles

**Voice profiles must include**:
1. Core Identity - Who is writing
2. Philosophy - Core belief driving writing
3. Tone Characteristics - 3-4 specific traits
4. Writing Style - Structure, language, **what to AVOID**
5. Content Patterns - Typical structures
6. Key Themes - Main topics/angles
7. Audience Relationship - Who you're addressing
8. Voice Consistency Markers - Signature phrases

**Critical Section**: "What to AVOID" - The more specific, the better output quality

## Agent Workflow

### Production Orchestrator (`@orchestrator start`)

Main coordinator that invokes subagents via Task tool:

1. **interrogator** - Extracts author's knowledge from brief
2. **research-lead** - Validates with credible sources
3. **structure-architect** - Designs narrative architecture
4. **voice-writer** - Creates draft in authentic voice
5. **humanizer** - Reviews for AI-writing patterns, produces flagged report (no rewrites)
6. **tone-police** - Quality gate: voice consistency (must score 9+/10)
7. **fact-checker** - Quality gate: independent fact verification (must pass)
8. **seo-optimizer** - Optimizes discoverability without breaking voice
9. **Final assembly** - Creates published version

### Subagent Roles

**interrogator** - Knowledge extraction
- Probes brief for insights
- Maps metaphors if present
- Documents operational details
- Output: `working/interrogation-{slug}.md`

**research-lead** - Source validation
- Finds 3-6 credible sources
- Validates claims
- Prepares citations
- **Knowledge source**: live web research (default) or a local knowledge base, no internet — set by the orchestrator at startup
- Output: `working/research-validation-{slug}.md`

**structure-architect** - Narrative design
- Identifies structure type (Pattern/Metaphor/Challenge/Mechanism)
- Designs section-by-section blueprint
- Maps research integration
- Output: `working/structure-blueprint-{slug}.md`

**voice-writer** - Draft creation
- Reads voice profile + examples
- Follows structure blueprint
- Integrates research naturally
- Maintains voice throughout
- Output: `working/draft-{slug}-v1.md`

**humanizer** - AI pattern review (report only)
- Scans for 24 AI-writing patterns from Wikipedia's AI writing guide
- Flags with severity: 🔴 Definitely fix / 🟡 Worth considering / 🟢 Cosmetic
- Suggests alternatives but NEVER rewrites the draft
- User reviews report and decides what to change
- Report: `working/humanizer-report-{slug}.md`
- No draft output — original `draft-{slug}-v1.md` proceeds unchanged

**tone-police** - Voice consistency check
- Scans for AI-tells
- Scores voice consistency (X/10)
- **Quality Gate**: Must score 9.0+ with zero critical AI-tells
- Output: `working/tone-police-report-{slug}.md`

**fact-checker** - Independent fact verification (online or local-KB)
- Independently verifies every claim against original sources
- **Knowledge source**: the open web via WebSearch/WebFetch (default), or a local knowledge base only (no internet) — set by the orchestrator at startup
- Catches confabulation: invented stats, drifted quotes, misattributed claims
- Cross-references research-validation first, then verifies anything unverified against the chosen source
- Checks uncited factual assertions, not just linked citations
- In local-KB mode, any claim the KB can't support is a critical issue
- **Quality Gate**: Must have zero critical issues
- Output: `working/fact-check-report-{slug}.md`

**seo-optimizer** - Discoverability
- Creates title variants
- Writes meta description
- Suggests voice-safe keyword optimizations
- **Rule**: Voice > SEO always
- Output: `working/seo-optimization-{slug}.md`

**editorial-director** - (Optional) Overall quality review
- Can be used for pre-quality-gate review
- Not part of standard automated workflow
- Output: `working/editorial-review-{slug}.md`

## File Organization

```
BlogProductionSystem/
├── .claude/                         # Claude Code configuration
│   ├── commands/
│   │   └── orchestrator.md          # @orchestrator slash command
│   └── agents/                      # Subagent definitions
│       └── *.md                     # (10 production agents)
│
├── voice_extractor/                 # Python voice extraction tool
│   ├── main.py                      # CLI entry point
│   ├── scraper.py                   # Web scraping
│   ├── analyzer.py                  # LLM voice analysis
│   └── requirements.txt             # Python dependencies
│
├── my-voice/                        # Voice profiles (gitignored)
│   ├── {voice-name}.md              # Voice profile
│   └── examples/
│       └── {voice-name}/*.md        # Example articles
│
├── concepts/                        # Article briefs and templates
│   ├── templates/                   # Brief templates
│   └── briefs/                      # Saved article briefs
│
├── working/                         # Active production workspace
│   ├── .state-{slug}.json           # Production state (for resume)
│   └── [stage outputs]
│
├── archive/                         # Completed production artifacts
│   └── {slug}/
│
├── published/                       # Final articles
│   ├── {slug}.md
│   └── PRODUCTION-SUMMARY-{SLUG}.md
│
├── CLAUDE.md                        # This file
└── README.md                        # User documentation
```

## Typical Workflows

### Full Production from Concept

```
User: "@orchestrator start"

Orchestrator:
1. Voice Selection - Interactive picker
2. Brief Input - Load/template/paste
3. Mode Selection - Automated/Interactive/Partial

Then invokes subagents via Task tool:
- Task(interrogator) → extraction
- Task(research-lead) → validation
- Task(structure-architect) → blueprint
- Task(voice-writer) → draft
- Task(humanizer) → AI pattern review report (user decides fixes)
- Task(tone-police) → quality gate
- Task(fact-checker) → quality gate
- Task(seo-optimizer) → optimization
- Final assembly → publish

Output:
- published/{slug}.md
- archive/{slug}/[all artifacts]
- published/PRODUCTION-SUMMARY-{SLUG}.md
```

### Resume In-Progress Production

```
User: "@orchestrator resume article-slug"

Orchestrator:
- Loads state from working/.state-article-slug.json
- Shows current progress
- Continues from last checkpoint
```

## Quality Gates (Strict Enforcement)

### Tone Check Gate
**Requirement**: Score 9.0+/10 with zero critical AI-tells

**If FAILED**:
- User must choose: regenerate / manual edit / abort
- Cannot proceed to publication with failing tone check

### Fact Check Gate
**Requirement**: Zero critical issues (no broken links, inaccurate claims, misattributions)

**If FAILED**:
- User must fix issues before proceeding
- Cannot publish with broken citations or false claims

## Voice-Specific Writing Rules

### Research Integration Pattern

**Voice-First Integration** (always):
```
CORRECT:
"I've watched teams with 70+ NPS fail at enterprise.
[CB Insights research](url) validates: 42% of startups fail because they
built for users who love it but can't buy it."

INCORRECT:
"According to CB Insights (2024), 42% of startups fail due to no market
need, demonstrating that user satisfaction doesn't equal viability."
```

### Citation Format
- **Always use inline links**: `[source description](url)`
- **Never use footnotes** or numbered citations

### AI-Tells to AVOID
- "In today's [X] landscape..."
- "It's important to note that..."
- "Leverage" as verb, "synergy", "best practices"
- "Furthermore", "Moreover" (excessive use)

## Commands

- `@orchestrator start` - New production
- `@orchestrator resume {slug}` - Resume in-progress
- `@orchestrator status` - Show all productions

## Subagent Installation

The blog production subagents are included in `.claude/agents/` and work automatically at the project level. To make them available across all projects, copy them to `~/.claude/agents/`.

Required subagents:
- interrogator.md
- research-lead.md
- structure-architect.md
- voice-writer.md
- humanizer.md
- tone-police.md
- fact-checker.md
- seo-optimizer.md
- editorial-director.md
- production-manager.md

## Technical Notes

### Subagent Context Isolation
Each subagent runs in its own context window, which:
- Prevents context pollution between stages
- Allows specialized tool restrictions per agent
- Returns only relevant results to orchestrator

### Python Voice Extractor
**Dependencies**: See `voice_extractor/requirements.txt`
**Environment**: Requires `ANTHROPIC_API_KEY` environment variable

## Version

System: Blog Production v2.1 (Task Tool Architecture)
Claude Model: Agents use `model: inherit` — they run on whatever model you're running Claude Code with. Pin a tier (`sonnet`/`opus`/`haiku`) per agent in its frontmatter if you want to.
