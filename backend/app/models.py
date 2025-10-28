from datetime import datetime
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, Date, ForeignKey, DateTime

class Base(DeclarativeBase):
    pass

class Series(Base):
    __tablename__ = "series"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    title_original: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    genres: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    cover_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # e.g., 'rss', 'manual'
    source_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String, nullable=True, default="ongoing")
    monitored: Mapped[bool] = mapped_column(Boolean, default=False)
    added_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    episodes: Mapped[list["Episode"]] = relationship("Episode", back_populates="series", cascade="all, delete-orphan")

class Episode(Base):
    __tablename__ = "episodes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    series_id: Mapped[int] = mapped_column(ForeignKey("series.id"))
    season: Mapped[int] = mapped_column(Integer, default=1)
    episode: Mapped[int] = mapped_column(Integer, default=1)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    air_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    languages: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    status: Mapped[str] = mapped_column(String, default="available")  # available/downloading/downloaded/failed
    download_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sdl_job_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    added_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    series: Mapped[Series] = relationship("Series", back_populates="episodes")

class DownloadRule(Base):
    __tablename__ = "download_rules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    series_id: Mapped[int] = mapped_column(ForeignKey("series.id"))
    quality_profile: Mapped[str] = mapped_column(String, default="best")
    language_preference: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # e.g., 'ger-dub'
    auto_download: Mapped[bool] = mapped_column(Boolean, default=False)
    season_monitoring: Mapped[str] = mapped_column(String, default="all")
