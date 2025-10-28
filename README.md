# AniMonarr-Core (Compliant Prototype)

**Important:** This prototype intentionally **does not** target or integrate with unauthorized streaming/download sites.  
It provides the full architecture and a working core that you can point at **lawful** sources only (e.g., your own URLs, public-domain feeds like certain Internet Archive collections, etc.).

## Features
- FastAPI backend (SQLite) with endpoints for Series and Episodes
- Basic RSS/public-feed scraper example (`source='rss'` on a series with `source_url` pointing to an RSS feed)
- APScheduler for periodic scraping
- SDL wrapper that enforces a **domain allowlist** via `ANIMONARR_ALLOWED_DOMAINS`
- Minimal React (Vite) UI skeleton with pages (Dashboard, Series, Series Detail, Queue, Activity, Settings)
- Dockerized API

## Quickstart (API only)
```bash
docker compose up -d --build
# API on http://localhost:8080/api/health
```

## Add a lawful RSS series
Create a series pointing to a permitted RSS feed (e.g., a public-domain collection on archive.org).

```bash
curl -X POST http://localhost:8080/api/series \ 
  -H "Content-Type: application/json"   -d '{
    "title": "Public Domain Anime Feed",
    "source": "rss",
    "source_url": "https://archive.org/advancedsearch.php?q=collection%3Aanimationandcartoons&output=rss",
    "monitored": true
  }'
```

Episodes will be created during scheduled scraper runs. You can also add episodes manually:

```bash
curl -X POST http://localhost:8080/api/episodes   -H "Content-Type: application/json"   -d '{
    "series_id": 1,
    "season": 1,
    "episode": 1,
    "title": "Example Episode",
    "source_url": "https://archive.org/details/some-public-domain-video"
  }'
```

## Start a compliant download
The included SDL stub only prints progress. In production, replace it with a legally compliant `sdl` or other fetcher.  
Allowed domains are restricted by `ANIMONARR_ALLOWED_DOMAINS` (default: `archive.org,example.com,localhost,127.0.0.1`).

```bash
curl -X POST http://localhost:8080/api/episodes/1/download
```

## Environment
Configure in `backend/.env.example` (copy to `.env` as needed) or environment variables.

- `ANIMONARR_DB` – path to SQLite
- `ANIMONARR_DOWNLOAD_DIR` – where downloads are saved
- `ANIMONARR_SDL_PATH` – path to the downloader
- `ANIMONARR_ALLOWED_DOMAINS` – comma-separated allowlist
- `ANIMONARR_SCRAPE_INTERVAL_MIN` – scraper cadence

## Dev UI
```bash
cd frontend
npm i
npm run dev
# then wire the UI to http://localhost:8080/api/*
```

## Notes
- This project is a **core scaffold**. Extend `rss_scraper.py` and implement additional lawful scrapers.
- Do not use this project to access copyrighted content without permission.
