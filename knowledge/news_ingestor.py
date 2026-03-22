# knowledge/news_ingestor.py
#
# LIVE NEWS INGESTION — H4 PHASE 3 UPGRADE
#
# TWO MODES:
#
# MODE A — LIVE (forward prediction):
#   Fetches today's real news from RSS feeds about your topic.
#   Use this when you want to predict what will happen next.
#   The outcome is unknown. You check accuracy days/weeks later.
#
# MODE B — HISTORICAL (backtest validation):
#   Loads a pre-written historical document about a past event.
#   The document deliberately omits the final outcome.
#   Use this to measure system accuracy against known history.
#
# CRITICAL RULE:
#   Never use live news for backtesting.
#   Live articles often describe the outcome in hindsight.
#   That is data leakage — the answer is already in the input.
#   Historical documents are carefully written to stop before the outcome.
#
# How it plugs into the existing system:
#   Both modes return a filepath to a .txt document in data/inputs/.
#   That filepath is passed to build_knowledge_graph() exactly like
#   any manually uploaded document. Nothing downstream changes.

import os
import sys
import re
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Attempt feedparser import — graceful fallback if not installed
try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False

INPUTS_DIR           = "data/inputs"
HISTORICAL_DOCS_DIR  = "data/historical_events/docs"
HISTORICAL_INDEX     = "data/historical_events/index.json"


# ─────────────────────────────────────────────────────────────────────────────
# RSS FEED REGISTRY
# All free, no API keys required, no rate limits for personal use
# ─────────────────────────────────────────────────────────────────────────────

RSS_FEEDS = {
    "economic_times": {
        "url"    : "https://economictimes.indiatimes.com/rssfeedstopstories.cms",
        "name"   : "Economic Times India",
        "region" : "india",
        "domains": ["economy", "finance", "rbi", "market", "policy"]
    },
    "reuters_business": {
        "url"    : "https://feeds.reuters.com/reuters/businessNews",
        "name"   : "Reuters Business",
        "region" : "global",
        "domains": ["business", "market", "economy", "finance"]
    },
    "bbc_business": {
        "url"    : "http://feeds.bbci.co.uk/news/business/rss.xml",
        "name"   : "BBC Business",
        "region" : "global",
        "domains": ["business", "economy", "market"]
    },
    "hindu_economy": {
        "url"    : "https://www.thehindu.com/business/Economy/?service=rss",
        "name"   : "The Hindu Economy",
        "region" : "india",
        "domains": ["india", "economy", "policy", "rbi"]
    },
    "moneycontrol": {
        "url"    : "https://www.moneycontrol.com/rss/latestnews.xml",
        "name"   : "Moneycontrol India",
        "region" : "india",
        "domains": ["market", "stocks", "economy", "rbi", "finance"]
    }
}


# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _clean_text(text: str) -> str:
    """Strip HTML tags and normalize whitespace."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)   # HTML entities like &amp;
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _article_matches(title: str, summary: str, topics: list) -> bool:
    """
    Check if an article is relevant to the given topics.
    Requires at least one topic keyword to appear in title or summary.
    Case-insensitive partial match.
    """
    combined = (title + " " + summary).lower()
    return any(topic.lower() in combined for topic in topics)


def _fetch_one_feed(feed_id: str, feed_info: dict,
                    topics: list, max_articles: int) -> list:
    """
    Fetch one RSS feed and return matching articles.
    Non-fatal: returns empty list on any error.
    """
    if not FEEDPARSER_AVAILABLE:
        return []

    try:
        feed = feedparser.parse(feed_info["url"])
        articles = []

        for entry in feed.entries[:max_articles * 3]:  # check 3× to allow filtering
            if len(articles) >= max_articles:
                break

            title   = _clean_text(getattr(entry, "title",   ""))
            summary = _clean_text(getattr(entry, "summary", ""))

            if not title:
                continue

            if topics and not _article_matches(title, summary, topics):
                continue

            articles.append({
                "title"    : title,
                "summary"  : summary,
                "source"   : feed_info["name"],
                "url"      : getattr(entry, "link",      ""),
                "published": getattr(entry, "published", ""),
                "feed_id"  : feed_id
            })

        return articles

    except Exception as e:
        print(f"    Warning: {feed_info['name']} unavailable — {e}")
        return []


def _format_articles_as_document(
    articles: list,
    topics: list,
    mode: str = "live"
) -> str:
    """
    Convert a list of article dicts into one clean text document.
    The document is plain text, readable by document_parser.py.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if not articles:
        # Return a minimal fallback document so the pipeline doesn't crash
        return (
            f"News Digest: {', '.join(topics)}\n"
            f"Generated: {timestamp}\n\n"
            f"No relevant articles were found for the given topics.\n"
            f"The system will run with limited world model context.\n"
            f"Consider uploading a manual document for better predictions.\n"
        )

    source_names = list(dict.fromkeys(a["source"] for a in articles))  # deduplicated

    header = (
        f"News Digest: {', '.join(topics)}\n"
        f"Mode: {'Live — forward prediction' if mode == 'live' else 'Historical — validation'}\n"
        f"Generated: {timestamp}\n"
        f"Articles: {len(articles)} from {len(source_names)} sources "
        f"({', '.join(source_names)})\n"
        f"{'─' * 50}\n\n"
    )

    body_parts = []
    for i, article in enumerate(articles, 1):
        parts = [f"[Article {i} — {article['source']}]"]
        parts.append(f"Headline: {article['title']}")
        if article.get("published"):
            parts.append(f"Published: {article['published']}")
        if article.get("summary") and article["summary"] != article["title"]:
            parts.append(f"\n{article['summary']}")
        parts.append("")   # blank line separator
        body_parts.append("\n".join(parts))

    return header + "\n".join(body_parts)


# ─────────────────────────────────────────────────────────────────────────────
# MODE A — LIVE NEWS (forward prediction)
# ─────────────────────────────────────────────────────────────────────────────

def fetch_live_news(
    topics: list,
    max_per_feed: int = 4,
    feeds: list = None,
    save: bool = True
) -> dict:
    """
    MODE A: Fetch today's real news and save as input document.

    USE FOR: predicting what will happen next about a current event.
    DO NOT USE FOR: backtesting (articles describe outcomes in hindsight).

    topics      : keywords to filter articles
                  e.g. ["RBI", "interest rate", "India inflation"]
    max_per_feed: max articles to take from each RSS feed
    feeds       : list of feed IDs to use (default: all feeds)
                  options: "economic_times", "reuters_business",
                           "bbc_business", "hindu_economy", "moneycontrol"
    save        : save document to data/inputs/ and return filepath
                  if False, returns document text directly

    Returns dict:
      filepath      : path to saved document (if save=True)
      document      : full document text
      article_count : number of articles fetched
      sources       : list of source names used
      topics        : topics that were searched
      word_count    : approximate word count
    """

    if not FEEDPARSER_AVAILABLE:
        raise ImportError(
            "feedparser not installed.\n"
            "Fix: pip install feedparser==6.0.11"
        )

    print(f"\n  Fetching live news...")
    print(f"  Topics  : {topics}")
    print(f"  Feeds   : {feeds or 'all'}")

    active_feeds = {
        k: v for k, v in RSS_FEEDS.items()
        if feeds is None or k in feeds
    }

    all_articles = []
    for feed_id, feed_info in active_feeds.items():
        print(f"  Checking {feed_info['name']}...", end=" ", flush=True)
        articles = _fetch_one_feed(feed_id, feed_info, topics, max_per_feed)
        print(f"{len(articles)} articles")
        all_articles.extend(articles)

    # Deduplicate by title similarity
    seen_titles = set()
    unique_articles = []
    for article in all_articles:
        title_key = article["title"].lower()[:60]
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_articles.append(article)

    print(f"\n  Total unique articles: {len(unique_articles)}")

    document = _format_articles_as_document(unique_articles, topics, mode="live")
    word_count = len(document.split())

    result = {
        "document"     : document,
        "article_count": len(unique_articles),
        "sources"      : list(dict.fromkeys(a["source"] for a in unique_articles)),
        "topics"       : topics,
        "word_count"   : word_count,
        "mode"         : "live",
        "timestamp"    : datetime.now().isoformat()
    }

    if save:
        os.makedirs(INPUTS_DIR, exist_ok=True)
        timestamp    = datetime.now().strftime("%Y%m%d_%H%M")
        safe_topic   = re.sub(r"[^a-zA-Z0-9]", "_", topics[0])[:20]
        filename     = f"live_{safe_topic}_{timestamp}.txt"
        filepath     = os.path.join(INPUTS_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(document)

        result["filepath"] = filepath
        print(f"  Saved   : {filepath}")
        print(f"  Size    : {word_count} words")

    return result


# ─────────────────────────────────────────────────────────────────────────────
# MODE B — HISTORICAL DOCUMENTS (backtesting)
# ─────────────────────────────────────────────────────────────────────────────

def load_historical_document(event_id: str) -> dict:
    """
    MODE B: Load a pre-written historical document for backtesting.

    USE FOR: measuring prediction accuracy against past events.
    The document describes context WITHOUT revealing the final outcome.

    event_id : one of the IDs from data/historical_events/index.json
               e.g. "rbi_rate_hike_2022", "india_demonetization_2016"

    Returns dict:
      filepath      : path to the historical document
      document      : full document text
      event_id      : the event ID
      actual_outcome: the documented real outcome (for scoring later)
      date          : when the event occurred
      description   : brief event description
    """

    if not os.path.exists(HISTORICAL_INDEX):
        raise FileNotFoundError(
            f"Historical events index not found: {HISTORICAL_INDEX}\n"
            f"Make sure data/historical_events/index.json exists."
        )

    with open(HISTORICAL_INDEX) as f:
        events = json.load(f)

    event = next((e for e in events if e["event_id"] == event_id), None)

    if event is None:
        available = [e["event_id"] for e in events]
        raise ValueError(
            f"Event '{event_id}' not found.\n"
            f"Available events: {available}"
        )

    doc_path = os.path.join(HISTORICAL_DOCS_DIR, event["document_file"])

    if not os.path.exists(doc_path):
        raise FileNotFoundError(
            f"Historical document not found: {doc_path}\n"
            f"Check that data/historical_events/docs/{event['document_file']} exists."
        )

    with open(doc_path, "r", encoding="utf-8") as f:
        document = f.read()

    print(f"\n  Historical document loaded:")
    print(f"  Event   : {event_id}")
    print(f"  Date    : {event['date']}")
    print(f"  Topic   : {event['description'][:70]}...")
    print(f"  Actual  : {event['actual_outcome']}")
    print(f"  Note    : Actual outcome is for scoring only — "
          f"NOT shown to simulation")

    return {
        "filepath"      : doc_path,
        "document"      : document,
        "event_id"      : event_id,
        "actual_outcome": event["actual_outcome"],
        "date"          : event["date"],
        "description"   : event["description"],
        "domain"        : event.get("domain", "unknown"),
        "word_count"    : len(document.split()),
        "mode"          : "historical"
    }


def list_historical_events() -> list:
    """
    Return a list of all available historical events for backtesting.
    Useful for the UI dropdown.
    """
    if not os.path.exists(HISTORICAL_INDEX):
        return []

    with open(HISTORICAL_INDEX) as f:
        events = json.load(f)

    return [
        {
            "event_id"      : e["event_id"],
            "date"          : e["date"],
            "description"   : e["description"],
            "actual_outcome": e["actual_outcome"],
            "domain"        : e.get("domain", "unknown")
        }
        for e in events
    ]


# ─────────────────────────────────────────────────────────────────────────────
# UNIFIED INTERFACE
# Used by the Flask API — returns a filepath regardless of mode
# ─────────────────────────────────────────────────────────────────────────────

def get_document_for_simulation(
    mode: str,
    topics: list = None,
    event_id: str = None
) -> dict:
    """
    Single entry point for both modes. Used by api/routes.py.

    mode     : "live" or "historical"
    topics   : required for mode="live"
               e.g. ["RBI", "interest rate", "inflation"]
    event_id : required for mode="historical"
               e.g. "rbi_rate_hike_2022"

    Returns dict with at minimum:
      filepath       : path to document file
      mode           : "live" or "historical"
      word_count     : approximate word count
      actual_outcome : only present for mode="historical" (for scoring)
    """

    if mode == "live":
        if not topics:
            raise ValueError("topics required for live mode")
        return fetch_live_news(topics=topics, save=True)

    elif mode == "historical":
        if not event_id:
            raise ValueError("event_id required for historical mode")
        return load_historical_document(event_id=event_id)

    else:
        raise ValueError(f"Unknown mode: '{mode}'. Use 'live' or 'historical'.")


# ─────────────────────────────────────────────────────────────────────────────
# BACKWARD COMPATIBILITY ALIASES
# These names are used by tests and older API code.
# They wrap the main functions with the same signatures.
# ─────────────────────────────────────────────────────────────────────────────

def fetch_articles(topics: list, max_per_feed: int = 5) -> list:
    """
    Fetch raw article dicts from RSS feeds matching topics.
    Returns list of article dicts with title, summary, source, url, published.
    Used by tests and the fetch_news_document wrapper below.
    """
    if not FEEDPARSER_AVAILABLE:
        print("  Warning: feedparser not installed. Run: pip install feedparser==6.0.11")
        return []

    all_articles = []
    for feed_id, feed_info in RSS_FEEDS.items():
        articles = _fetch_one_feed(feed_id, feed_info, topics, max_per_feed)
        all_articles.extend(articles)

    # Deduplicate by title
    seen = set()
    unique = []
    for a in all_articles:
        key = a["title"].lower()[:60]
        if key not in seen:
            seen.add(key)
            unique.append(a)

    return unique


def fetch_news_document(topics: list, save: bool = True):
    """
    Alias for fetch_live_news() — kept for backward compatibility.
    Fetches live news and saves as input document.
    Returns filepath string (if save=True) or document text (if save=False).
    """
    if save:
        result = fetch_live_news(topics=topics, save=True)
        return result.get("filepath", "")
    else:
        result = fetch_live_news(topics=topics, save=False)
        return result.get("document", "")