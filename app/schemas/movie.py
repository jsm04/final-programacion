from typing import Optional

from datetime import date, datetime
from pydantic import BaseModel


class MovieBase(BaseModel):
    tmdb_id: Optional[int] = None
    title: str
    overview: Optional[str] = None
    release_date: Optional[date] = None
    genre_ids: Optional[str] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None


class MovieCreate(MovieBase):
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "tmdb_id": 299534,
                "title": "Avengers: Endgame",
                "overview": "The Avengers assemble once more to reverse Thanos' actions.",
                "release_date": "2019-04-24",
                "genre_ids": "[12, 878, 28]",
                "vote_average": 8.3,
                "vote_count": 23000,
                "poster_path": "/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg",
                "backdrop_path": "/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
            }
        }


class MovieUpdate(BaseModel):
    tmdb_id: Optional[int] = None
    title: Optional[str] = None
    overview: Optional[str] = None
    release_date: Optional[date] = None
    genre_ids: Optional[str] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Fight Club (Director's Cut)",
                "overview": "Updated extended description.",
                "vote_average": 8.5,
                "poster_path": "/newPoster.jpg",
            }
        }


class MovieRead(MovieBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "tmdb_id": 550,
                "title": "Fight Club",
                "overview": "A ticking-time-bomb insomniac meets a soap salesman.",
                "release_date": "1999-10-15",
                "genre_ids": "[18, 53]",
                "vote_average": 8.4,
                "vote_count": 26000,
                "poster_path": "/bptfVGEQuv6vDTIMVCHjJ9Dz8PX.jpg",
                "backdrop_path": "/fCayJrkfRaCRCTh8GqN30f8oyQF.jpg",
                "created_at": "2025-01-01T12:00:00Z",
            }
        }
