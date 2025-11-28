from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate


def create_movie(db: Session, data: MovieCreate) -> Movie:
    # Prevent duplicate TMDB ID if provided
    if data.tmdb_id is not None:
        exists = db.query(Movie).filter(Movie.tmdb_id == data.tmdb_id).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Movie with this TMDB ID already exists.",
            )

    movie = Movie(**data.dict())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def list_movies(
    db: Session,
    title: str | None,
    min_rating: float | None,
    skip: int,
    limit: int,
) -> list[Movie]:
    query = db.query(Movie)

    if title:
        query = query.filter(func.lower(Movie.title).contains(title.lower()))

    if min_rating is not None:
        query = query.filter(Movie.vote_average >= min_rating)

    return query.offset(skip).limit(limit).all()


def get_movie_by_id(db: Session, movie_id: int) -> Movie:
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found.",
        )

    return movie


def update_movie(db: Session, movie_id: int, data: MovieUpdate) -> Movie:
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found.",
        )

    update_data = data.dict(exclude_unset=True)

    # Prevent duplicate TMDB ID
    if "tmdb_id" in update_data and update_data["tmdb_id"] is not None:
        exists = (
            db.query(Movie)
            .filter(Movie.tmdb_id == update_data["tmdb_id"], Movie.id != movie_id)
            .first()
        )
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Movie with this TMDB ID already exists.",
            )

    for key, value in update_data.items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)

    return movie


def delete_movie(db: Session, movie_id: int) -> None:
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found.",
        )

    db.delete(movie)
    db.commit()
