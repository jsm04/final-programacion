from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

from app import STRCNX

Base = declarative_base()


if STRCNX is None:
    raise ValueError("Database connection is not configured.")

engine = create_engine(STRCNX)


def create_db_and_tables():
    Base.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
