import os
import requests

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.schemas.movie import MovieCreate

TMDB_BASE_URL = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")


def _api_headers():
    if not TMDB_ACCESS_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="TMDB access token not configured.",
        )

    return {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
    }

def _fetch_tmdb_movie(tmdb_id: int) -> dict:
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
    response = requests.get(url, headers=_api_headers(), timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TMDB movie not found.",
        )

    return response.json()


def import_movie_by_tmdb_id(db: Session, tmdb_id: int) -> Movie:
    # Prevent duplicates
    exists = db.query(Movie).filter(Movie.tmdb_id == tmdb_id).first()
    if exists:
        return exists

    tmdb_data = _fetch_tmdb_movie(tmdb_id)

    movie_data = MovieCreate(
        tmdb_id=tmdb_data.get("id"),
        title=tmdb_data.get("title") or "Untitled",
        overview=tmdb_data.get("overview") or "",
        release_date=tmdb_data.get("release_date"),
        genre_ids=str([g["id"] for g in tmdb_data.get("genres", [])]),
        vote_average=tmdb_data.get("vote_average") or 0.0,
        vote_count=tmdb_data.get("vote_count") or 0,
        poster_path=tmdb_data.get("poster_path") or "",
        backdrop_path=tmdb_data.get("backdrop_path") or "",
    )

    movie = Movie(**movie_data.dict())
    db.add(movie)
    db.commit()
    db.refresh(movie)

    return movie


def import_popular_movies(db: Session, page: int = 1) -> list[Movie]:
    url = f"{TMDB_BASE_URL}/movie/popular?page={page}"

    response = requests.get(url, headers=_api_headers(), timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch popular movies from TMDB.",
        )

    movies_json = response.json().get("results", [])
    imported_movies = []

    for m in movies_json:
        existing = db.query(Movie).filter(Movie.tmdb_id == m["id"]).first()
        if existing:
            imported_movies.append(existing)
            continue

        movie_data = MovieCreate(
            tmdb_id=m.get("id"),
            title=m.get("title") or "Untitled",
            overview=m.get("overview") or "",
            release_date=m.get("release_date"),
            genre_ids=str(m.get("genre_ids", [])),
            vote_average=m.get("vote_average") or 0.0,
            vote_count=m.get("vote_count") or 0,
            poster_path=m.get("poster_path") or "",
            backdrop_path=m.get("backdrop_path") or "",
        )

        movie = Movie(**movie_data.dict())
        db.add(movie)
        db.commit()
        db.refresh(movie)

        imported_movies.append(movie)

    return imported_movies


def search_movies_tmdb(query: str) -> dict:
    url = f"{TMDB_BASE_URL}/search/movie?query={query}"

    response = requests.get(url, headers=_api_headers(), timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to search TMDB.",
        )

    return response.json()
