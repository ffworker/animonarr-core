import feedparser
from typing import List, Dict
import httpx

# Example RSS scraper for public feeds (e.g., Internet Archive collections).
# The output maps reasonably to the EpisodeCreate schema.
# This is a placeholder—you can map specific feeds to series/episodes as needed.

async def fetch_rss(url: str) -> List[Dict]:
    d = feedparser.parse(url)
    results = []
    for entry in d.entries[:50]:
        title = entry.get("title", "Untitled")
        link = entry.get("link")
        if not link:
            continue
        results.append({
            "title": title,
            "source_url": link
        })
    return results
