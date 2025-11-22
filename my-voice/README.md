# Voice Profiles Directory

This directory contains your voice profiles - the foundation of the blog production system.

## Quick Start

### Extract Voice from Existing Blog

```bash
cd voice_extractor
python main.py https://your-blog.com --name my-voice --articles 10 --save-examples
```

This creates:
- `my-voice.md` - Your voice profile (in this directory)
- `examples/my-voice/*.md` - Example articles

### Or Create Manually

```bash
cp ../voice-templates/generic.md my-voice.md
```

Then edit `my-voice.md` to match your style.

## Voice Profile Components

A complete voice profile includes:

1. **Core Identity** - Who is writing, what perspective
2. **Philosophy** - Core belief driving the writing
3. **Tone Characteristics** - 3-4 specific voice qualities
4. **Writing Style** - Structure, language, **what to AVOID**
5. **Content Patterns** - Typical article structures
6. **Key Themes** - Main topics/angles
7. **Audience Relationship** - Who you're addressing
8. **Voice Consistency Markers** - Signature phrases

**Most Important**: The "What to AVOID" section - the more specific, the better output quality.

## File Structure

```
my-voice/
├── README.md (this file)
├── my-voice-name.md (your voice profile)
├── another-voice.md (optional - multiple voices)
└── examples/
    ├── my-voice-name/
    │   ├── article-1.md
    │   └── article-2.md
    └── another-voice/
        └── ...
```

## Using Multiple Voices

You can maintain multiple voice profiles:

```
my-voice/business-voice.md
my-voice/technical-voice.md
my-voice/casual-voice.md
```

When starting production, orchestrator will ask which voice to use.

## Example Voice Profile

See `../voice-templates/generic.md` for a complete template with detailed guidance.

## Tips for Great Voice Profiles

### 1. Be Specific in "What to AVOID"
Bad: "Avoid generic language"
Good: "Never use 'leverage' as a verb, never start with 'In today's X landscape', never use bullet points for main content"

### 2. Add Signature Phrases
Include phrases you actually use:
- "I've watched [pattern] destroy companies"
- "Here's what they don't tell you..."
- "The obvious truth nobody acknowledges..."

### 3. Include Example Articles
Save 2-3 representative articles to `examples/your-voice/`

The system learns from these to match your patterns.

### 4. Test and Refine
1. Extract initial profile
2. Run a test production
3. Review output for voice accuracy
4. Refine "What to AVOID" based on issues
5. Test again

## Privacy Note

**Voice profiles are gitignored** - they stay local and private.

The `.gitignore` excludes:
- `my-voice/*.md` (your profiles)
- `my-voice/examples/` (your article examples)

This keeps your proprietary content and writing patterns private.

## Need Help?

- Review `../voice-templates/generic.md` for detailed template
- Check `../CLAUDE.md` for system documentation
- See `../README.md` for usage examples

## Voice Extraction Options

The voice extractor supports several options:

```bash
# Basic extraction
python main.py <url> --name my-voice

# More articles (better analysis)
python main.py <url> --name my-voice --articles 15

# Save examples for reference
python main.py <url> --name my-voice --save-examples

# All together
python main.py <url> --name my-voice --articles 12 --save-examples
```

Recommended: 8-12 articles for good voice capture.
