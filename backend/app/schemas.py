from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date

class SeriesOut(BaseModel):
    id: int
    title: str
    title_original: Optional[str] = None
    description: Optional[str] = None
    genres: Optional[str] = None
    cover_url: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    status: Optional[str] = "ongoing"
    monitored: bool = False
    added_date: datetime
    last_updated: datetime

    class Config:
        from_attributes = True

class EpisodeOut(BaseModel):
    id: int
    series_id: int
    season: int
    episode: int
    title: Optional[str] = None
    air_date: Optional[date] = None
    source_url: str
    languages: Optional[str] = None
    status: str
    download_path: Optional[str] = None
    sdl_job_id: Optional[str] = None
    added_date: datetime

    class Config:
        from_attributes = True

class SeriesCreate(BaseModel):
    title: str
    title_original: Optional[str] = None
    description: Optional[str] = None
    genres: Optional[str] = None
    cover_url: Optional[str] = None
    source: Optional[str] = "manual"
    source_url: Optional[str] = None
    monitored: bool = False

class EpisodeCreate(BaseModel):
    series_id: int
    season: int = 1
    episode: int = 1
    title: Optional[str] = None
    source_url: str
    languages: Optional[str] = None
