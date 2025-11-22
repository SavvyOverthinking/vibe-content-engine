# GitHub Repository Setup Guide

This guide will help you publish the Blog Production System to GitHub.

## Step 1: Verify What Will Be Published

Run this command to see what will be committed (excludes your personal files):

```bash
git status --ignored
```

**What WILL be published** (public):
- ✅ All agent definitions (`agents/*.md`)
- ✅ Voice extractor tool (`voice_extractor/`)
- ✅ Voice templates (`voice-templates/`)
- ✅ Documentation (`README.md`, `CLAUDE.md`)
- ✅ Configuration files (`.gitignore`, `LICENSE`)

**What will NOT be published** (excluded by .gitignore):
- ❌ Your voice profiles (`my-voice/*.md`)
- ❌ Your example articles (`my-voice/examples/`)
- ❌ Archive directory (`archive/`)
- ❌ Published articles (`published/`)
- ❌ Working files (`working/`)
- ❌ Concept briefs (`concepts/`)

## Step 2: Initialize Git Repository

If not already initialized:

```bash
cd "C:\Users\hamak\github\BlogProductionSystem"
git init
```

## Step 3: Create .gitkeep Files

Ensure empty directories are tracked:

```bash
# Create .gitkeep in directories that should exist but be empty
touch working/.gitkeep
touch my-voice/.gitkeep
touch my-voice/examples/.gitkeep
```

## Step 4: Stage Your Files

```bash
# Add all public files (respects .gitignore)
git add .

# Verify what's staged
git status
```

You should see:
- Agent definitions
- Voice extractor
- README, CLAUDE.md, LICENSE
- .gitignore
- Voice templates

You should NOT see:
- Your personal voice profiles
- Archive or published content
- Working directory files

## Step 5: Create Initial Commit

```bash
git commit -m "Initial commit: Blog Production System with web-resilient agents

- Multi-agent blog production workflow
- Voice-first content creation
- Automated research with fallback sources
- Web request resilience (30s timeouts)
- Flexible fact-checking quality gates
- Voice extraction tool
- Complete documentation"
```

## Step 6: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name**: `blog-production-system` (or your preferred name)
   - **Description**: "AI-powered blog production system with voice preservation, automated research, and quality gates"
   - **Visibility**: ✅ Public
   - **Initialize**: ❌ Do NOT add README, .gitignore, or license (we have these)
3. Click "Create repository"

## Step 7: Connect Local to GitHub

GitHub will show you commands. Use the "push an existing repository" section:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/blog-production-system.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 8: Verify on GitHub

1. Go to your repository URL: `https://github.com/YOUR_USERNAME/blog-production-system`
2. Verify the README displays correctly
3. Check that personal files are NOT visible:
   - No `Savvyoverthinking-voice.md`
   - No `archive/` or `published/` content
   - No working files

## Step 9: Add Repository Metadata (Optional)

On GitHub repository page:

1. Click "⚙️ Settings"
2. Scroll to "About" section (top right)
3. Add topics (helps discoverability):
   - `claude-code`
   - `ai-agents`
   - `content-creation`
   - `blog-automation`
   - `voice-preservation`
   - `research-automation`
4. Click "Save changes"

## Step 10: Create Repository Description (Optional)

Add a compelling description in the "About" section:

```
Transform concepts into publication-ready blog posts while preserving your authentic voice.
Multi-agent system powered by Claude Code with automated research, quality gates, and SEO optimization.
```

## Future Updates

When you make changes to the agent system:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with descriptive message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Protecting Your Personal Content

The `.gitignore` is configured to protect:
- Your voice profiles
- Your published articles
- Your archive
- Your working files
- Your concept briefs

**Important**: Never run `git add -f` (force add) on these directories - it bypasses .gitignore protection.

## Sharing Your Repository

Once published, you can share:
- Repository URL: `https://github.com/YOUR_USERNAME/blog-production-system`
- Direct link to README: `https://github.com/YOUR_USERNAME/blog-production-system#readme`
- Clone command: `git clone https://github.com/YOUR_USERNAME/blog-production-system.git`

## Troubleshooting

### "Personal files showing in git status"

If you see your voice profiles or published content:

```bash
# Check .gitignore is working
git check-ignore -v my-voice/Savvyoverthinking-voice.md

# Should output: .gitignore:2:my-voice/*.md
```

If not ignored:
```bash
# Remove from staging
git reset HEAD my-voice/*.md
git reset HEAD published/*
git reset HEAD archive/*
```

### "Repository already exists"

If you get an error that remote already exists:

```bash
# Check current remote
git remote -v

# Remove old remote if needed
git remote remove origin

# Add correct remote
git remote add origin https://github.com/YOUR_USERNAME/blog-production-system.git
```

### "Authentication failed"

Use a GitHub Personal Access Token instead of password:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (all)
4. Copy token
5. Use token as password when pushing

Or set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

## Success!

Your Blog Production System is now public and ready for others to use!

Consider adding:
- ⭐ Star your own repository (shows confidence)
- 📝 Create issues for planned improvements
- 🎯 Add a discussion board for community questions
- 📊 Enable GitHub Actions for automated testing (future enhancement)

---

**Need help?** Check GitHub's documentation: https://docs.github.com/en/repositories
