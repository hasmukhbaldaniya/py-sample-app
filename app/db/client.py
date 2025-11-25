import os
from typing import Any, Generator

from fastapi import FastAPI
from sqlalchemy import URL, Engine, MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from starlette.requests import Request

from app.core import settings


class Base(DeclarativeBase):
    pass


class DBClient:
    _engine: Engine
    _session_factory: Any = None

    @classmethod
    def initialise(cls, app: FastAPI) -> None:
        """
        Initializes SQLAlchemy engine, session maker, and declarative base.
        """

        db_url = settings.db_url  # type: ignore

        cls._engine = create_engine(
            db_url,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
        )

        cls._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=cls._engine,
            expire_on_commit=False,
        )

        app.state.db_engine = cls._engine
        app.state.db_session_factory = cls._session_factory

        cls.create_models()
        cls.bind_and_reflect()

    @classmethod
    def create_models(cls) -> None:
        """
        Creates the database tables based on the models.
        """
        # Import all models here to ensure they are registered with Base
        from app.db import models  # noqa: F401

        Base.metadata.create_all(bind=cls._engine)

    @classmethod
    def bind_and_reflect(cls) -> MetaData:
        """
        Reflects the database schema using the engine.
        """
        metadata = MetaData()
        metadata.reflect(bind=cls._engine)
        return metadata

    @staticmethod
    def get_db_session(request: Request) -> Generator[Session, None, None]:
        """
        Create and get a database session from FastAPI request object.

        :param request: current request.
        :yield: database session.
        """
        session = request.app.state.db_session_factory()
        try:
            yield session
        finally:
            session.commit()
            session.close()
