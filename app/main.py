import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from contextlib import asynccontextmanager
import requests

from app import PORT
from app.database import create_db_and_tables
from app.routers.user import user_router
from app.routers.movie import movie_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


def create_app() -> FastAPI:
    server = FastAPI(title="Final programacion Movie Backend API", lifespan=lifespan)

    server.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    server.include_router(user_router, prefix="/api")
    server.include_router(movie_router, prefix="/api")

    @server.get("/favicon.ico")
    async def favicon():
        return Response(status_code=204)

    @server.exception_handler(Exception)
    async def global_exception_handler(_: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "error": str(exc),
            },
        )

    @server.exception_handler(requests.exceptions.RequestException)
    async def requests_error_handler(
        _: Request, exc: requests.exceptions.RequestException
    ):
        return JSONResponse(
            status_code=502,
            content={
                "detail": "Error communicating with external service",
                "error": str(exc),
            },
        )

    return server


app = create_app()


if __name__ == "__main__":
    try:
        uvicorn.run(
            "main:app",
            port=PORT,
            reload=False,
        )
    except OSError as e:
        logger.critical("OS error while starting server: %s", e, exc_info=True)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
