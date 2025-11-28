from datetime import datetime, date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Float, Integer, Date, DateTime, func

from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tmdb_id: Mapped[int | None] = mapped_column(unique=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    overview: Mapped[str | None] = mapped_column(Text)
    release_date: Mapped[date | None] = mapped_column(Date)
    genre_ids: Mapped[str | None] = mapped_column(String)
    vote_average: Mapped[float | None] = mapped_column(Float)
    vote_count: Mapped[int | None] = mapped_column(Integer)
    poster_path: Mapped[str | None] = mapped_column(String)
    backdrop_path: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.datetime("now"),
        nullable=False,
    )
