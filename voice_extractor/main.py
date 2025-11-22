#!/usr/bin/env python3
"""
Voice Extractor - Extract voice profiles from blog content

Usage:
    python main.py <blog-url> --name <voice-name> [--articles N]

Example:
    python main.py https://medium.com/@user --name my-blog --articles 10
"""

import argparse
import sys
from pathlib import Path

try:
    from scraper import BlogScraper
    from analyzer import VoiceAnalyzer
except ImportError:
    print("Error: Could not import scraper/analyzer modules")
    print("Make sure you're running from the voice_extractor directory")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Extract voice profile from blog content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://medium.com/@username --name my-blog
  python main.py https://yourblog.com --name tech-voice --articles 12
        """
    )

    parser.add_argument("url", help="Blog URL to analyze")
    parser.add_argument("--name", required=True, help="Name for this voice profile")
    parser.add_argument("--articles", type=int, default=10,
                       help="Number of articles to analyze (default: 10)")
    parser.add_argument("--save-examples", action="store_true",
                       help="Save scraped articles as examples")

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"Voice Extractor")
    print(f"{'='*60}\n")

    print(f"📍 Target: {args.url}")
    print(f"🏷️  Voice: {args.name}")
    print(f"📊 Articles: {args.articles}\n")

    # Initialize scraper
    print("🔍 Discovering articles...")
    scraper = BlogScraper(args.url, max_articles=args.articles)

    try:
        articles = scraper.scrape()
    except Exception as e:
        print(f"\n❌ Error scraping articles: {e}")
        sys.exit(1)

    if not articles:
        print("❌ No articles found. Please check the URL and try again.")
        sys.exit(1)

    print(f"✅ Scraped {len(articles)} articles")
    total_words = sum(a.get('word_count', 0) for a in articles)
    print(f"📝 Total words: {total_words:,}\n")

    # Save examples if requested
    if args.save_examples:
        print("💾 Saving article examples...")
        examples_dir = Path(f"../my-voice/examples/{args.name}")
        scraper.save_examples(articles, examples_dir)
        print(f"✅ Examples saved to: {examples_dir}\n")

    # Analyze voice
    print("🤖 Analyzing voice patterns with Claude Sonnet 4.5...")
    print("   (This may take 1-2 minutes...)\n")

    analyzer = VoiceAnalyzer()

    try:
        profile = analyzer.analyze(articles, voice_name=args.name)
    except Exception as e:
        print(f"\n❌ Error analyzing voice: {e}")
        sys.exit(1)

    # Save profile
    profile_path = Path(f"../my-voice/{args.name}.md")
    profile_path.parent.mkdir(parents=True, exist_ok=True)

    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write(profile)

    print(f"✅ Voice profile created!\n")
    print(f"{'='*60}")
    print(f"📄 Profile: {profile_path}")
    if args.save_examples:
        print(f"📂 Examples: my-voice/examples/{args.name}/")
    print(f"{'='*60}\n")

    print("✨ Ready to use this voice in production!")
    print(f"\nNext steps:")
    print(f"1. Review {profile_path}")
    print(f"2. Edit if needed (especially 'What to AVOID' section)")
    print(f"3. Start production: @orchestrator start\n")

if __name__ == "__main__":
    main()
