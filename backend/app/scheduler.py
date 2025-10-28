import os, asyncio, logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from .rss_scraper import fetch_rss
from .models import Series, Episode
from datetime import datetime

log = logging.getLogger(__name__)

SCRAPE_INTERVAL_MIN = int(os.getenv("ANIMONARR_SCRAPE_INTERVAL_MIN", "15"))

class AniMonarrScheduler:
    def __init__(self, db_sessionmaker, sdl_manager):
        self.scheduler = AsyncIOScheduler()
        self.db_sessionmaker = db_sessionmaker
        self.sdl_manager = sdl_manager

    def start(self):
        self.scheduler.add_job(self.run_scrapers, "interval", minutes=SCRAPE_INTERVAL_MIN)
        self.scheduler.start()

    async def run_scrapers(self):
        # Example: loop series with source='rss' and source_url as RSS feed URL
        try:
            with self.db_sessionmaker() as db:
                rss_series = db.query(Series).filter(Series.source == "rss").all()
                for s in rss_series:
                    items = await fetch_rss(s.source_url)
                    for idx, item in enumerate(items, start=1):
                        # naive dedupe by title+source_url
                        exists = db.query(Episode).filter(
                            Episode.series_id == s.id,
                            Episode.title == item["title"],
                            Episode.source_url == item["source_url"]
                        ).first()
                        if exists:
                            continue
                        ep = Episode(
                            series_id=s.id,
                            season=1,
                            episode=idx,
                            title=item["title"],
                            source_url=item["source_url"],
                            status="available",
                            added_date=datetime.utcnow(),
                        )
                        db.add(ep)
                    s.last_updated = datetime.utcnow()
                    db.commit()
        except Exception as e:
            log.exception("Scraper run failed: %s", e)
# am Ende der Datei ergänzen
    async def scrape_once_now(self):
        await self.run_scrapers()
