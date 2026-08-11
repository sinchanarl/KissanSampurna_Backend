from pydantic import BaseModel
from typing import TypeVar, Generic, List
from .reportModels import *
from .generateApiKeyModels import *
from .healthCheckModels import *

ModelType = TypeVar('ModelType', bound=BaseModel)

class ListResponse(BaseModel, Generic[ModelType]):
    items: List[ModelType]
    count: int


class StatusResponse(BaseModel):
    status: str = "ok"
