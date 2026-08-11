"""Development shim for SharedBackend.managers

Provides minimal `BaseSchema` and `GenericManager` so the app can run
without the external SharedBackend submodule during local development.
"""
import uuid
import sqlalchemy as db
from sqlalchemy.orm import declarative_base
from typing import Generic, TypeVar, Optional

ModelType = TypeVar("ModelType")

Base = declarative_base()


class BaseSchema(Base):
    __abstract__ = True
    uid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))


class GenericManager(Generic[ModelType]):
    """Generic manager shim for development.

    The real `GenericManager` provides DB-backed CRUD operations. This shim
    only implements a minimal interface expected by the codebase so the app
    can start during local development without the full shared package.
    """
    def __init__(self, engine: Optional[object] = None):
        self.engine = engine

    async def get(self, uid: str) -> ModelType:
        raise NotImplementedError("GenericManager.get not implemented in dev shim")

    async def list(self, *args, **kwargs) -> list[ModelType]:
        raise NotImplementedError("GenericManager.list not implemented in dev shim")


__all__ = ["BaseSchema", "GenericManager"]
