import os, asyncio, logging, json, signal
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import get_db, init_db, SessionLocal
from .models import Series, Episode, DownloadRule
from .schemas import SeriesOut, EpisodeOut, SeriesCreate, EpisodeCreate
from .sdl_wrapper import SDLManager
from .scheduler import AniMonarrScheduler
from datetime import datetime

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AniMonarr-Core API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sdl_manager = SDLManager()
scheduler = AniMonarrScheduler(SessionLocal, sdl_manager)

@app.on_event("startup")
async def on_startup():
    init_db()
    scheduler.start()

@app.get("/api/series", response_model=List[SeriesOut])
def list_series(search: Optional[str] = None, monitored: Optional[bool] = None, db: Session = Depends(get_db)):
    q = db.query(Series)
    if search:
        like = f"%{search}%"
        q = q.filter(Series.title.ilike(like) | Series.title_original.ilike(like))
    if monitored is not None:
        q = q.filter(Series.monitored == monitored)
    return q.order_by(Series.id.desc()).all()

@app.post("/api/series", response_model=SeriesOut)
def create_series(payload: SeriesCreate, db: Session = Depends(get_db)):
    s = Series(
        title=payload.title,
        title_original=payload.title_original,
        description=payload.description,
        genres=payload.genres,
        cover_url=payload.cover_url,
        source=payload.source,
        source_url=payload.source_url,
        monitored=payload.monitored,
        added_date=datetime.utcnow(),
        last_updated=datetime.utcnow(),
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@app.get("/api/series/{series_id}", response_model=SeriesOut)
def get_series(series_id: int, db: Session = Depends(get_db)):
    s = db.query(Series).get(series_id)
    if not s:
        raise HTTPException(404, "Series not found")
    return s

@app.post("/api/series/{series_id}/monitor", response_model=SeriesOut)
def monitor_series(series_id: int, monitored: bool, db: Session = Depends(get_db)):
    s = db.query(Series).get(series_id)
    if not s:
        raise HTTPException(404, "Series not found")
    s.monitored = monitored
    s.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(s)
    return s

@app.get("/api/series/{series_id}/episodes", response_model=List[EpisodeOut])
def list_episodes(series_id: int, db: Session = Depends(get_db)):
    eps = db.query(Episode).filter(Episode.series_id == series_id).order_by(Episode.season, Episode.episode).all()
    return eps

@app.post("/api/episodes", response_model=EpisodeOut)
def create_episode(payload: EpisodeCreate, db: Session = Depends(get_db)):
    s = db.query(Series).get(payload.series_id)
    if not s:
        raise HTTPException(404, "Series not found")
    ep = Episode(
        series_id=payload.series_id,
        season=payload.season,
        episode=payload.episode,
        title=payload.title,
        source_url=payload.source_url,
        status="available",
        added_date=datetime.utcnow(),
        languages=payload.languages
    )
    db.add(ep)
    db.commit()
    db.refresh(ep)
    return ep

@app.post("/api/episodes/{episode_id}/download")
def download_episode(episode_id: int, db: Session = Depends(get_db)):
    ep = db.query(Episode).get(episode_id)
    if not ep:
        raise HTTPException(404, "Episode not found")
    try:
        job_id, proc = sdl_manager.download_episode(episode_id, ep.source_url, quality="best")
        ep.status = "downloading"
        ep.sdl_job_id = job_id
        db.commit()
        return {"job_id": job_id, "status": "downloading"}
    except Exception as e:
        raise HTTPException(400, f"Download failed to start: {e}")

@app.get("/api/health")
def health():
    return {"ok": True, "time": datetime.utcnow().isoformat()}
