from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.schemas.movie import MovieCreate, MovieRead, MovieUpdate
from app.services import movie_service, tmdb
from app.database import get_session


SessionDep = Annotated[Session, Depends(get_session)]

movie_router = APIRouter(prefix="/movies", tags=["Movies"])


@movie_router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new movie",
    description="Create a new movie entry with the provided information.",
)
def create_movie(movie: MovieCreate, db: SessionDep):
    return movie_service.create_movie(db, movie)


@movie_router.get(
    "/",
    response_model=list[MovieRead],
    status_code=status.HTTP_200_OK,
    summary="List movies",
    description="Retrieve a list of movies with optional filters such as title, minimum rating, and pagination.",
)
def list_movies(
    db: SessionDep,
    title: str | None = None,
    min_rating: float | None = None,
    skip: int = 0,
    limit: int = 10,
):
    return movie_service.list_movies(db, title, min_rating, skip, limit)


@movie_router.get(
    "/{movie_id}",
    response_model=MovieRead,
    status_code=status.HTTP_200_OK,
    summary="Get movie by ID",
    description="Retrieve a movie by its unique ID.",
)
def get_movie_by_id(movie_id: int, db: SessionDep):
    return movie_service.get_movie_by_id(db, movie_id)


@movie_router.put(
    "/{movie_id}",
    response_model=MovieRead,
    status_code=status.HTTP_200_OK,
    summary="Update movie",
    description="Update an existing movie with new field values.",
)
def update_movie(movie_id: int, movie: MovieUpdate, db: SessionDep):
    return movie_service.update_movie(db, movie_id, movie)


@movie_router.delete(
    "/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete movie",
    description="Delete a movie from the system.",
)
def delete_movie(movie_id: int, db: SessionDep):
    movie_service.delete_movie(db, movie_id)
    return None


# TMDB ROUTES

@movie_router.post(
    "/import/popular",
    response_model=list[MovieRead],
    status_code=status.HTTP_201_CREATED,
    summary="Import popular movies from TMDB",
    description="Import a list of popular movies from TMDB. Supports optional pagination using the 'page' query parameter.",
)
def import_popular_movies(db: SessionDep, page: int = 1):
    return tmdb.import_popular_movies(db, page)


@movie_router.post(
    "/import/{tmdb_id}",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
    summary="Import movie by TMDB ID",
    description="Fetch a movie from The Movie Database (TMDB) using its ID and store it in the system.",
)
def import_movie_by_tmdb_id(tmdb_id: int, db: SessionDep):
    return tmdb.import_movie_by_tmdb_id(db, tmdb_id)


@movie_router.get(
    "/search/{query}",
    status_code=status.HTTP_200_OK,
    summary="Search movies in TMDB",
    description="Search for movies in TMDB without storing them locally.",
)
def search_movies_tmdb(query: str):
    return tmdb.search_movies_tmdb(query)
