from fastapi import APIRouter

from app.config import get_engine, get_settings
from managers import *

router = APIRouter(prefix="/crops")
settings = get_settings()
engine = get_engine(settings.name)

crop_manager = CropManager(engine)


@router.post("", response_model=CropSchema.__model__)
async def post_crop(payload: CropSchema.__post_model__):
    async with crop_manager() as session:
        crop = await crop_manager.create(payload, session=session)
        return crop.model_dump()


@router.get("")
async def get_crops():
    async with crop_manager() as session:
        crops = await crop_manager.fetch_all({}, session=session)
        return crops.model_dump()


@router.get("/{uid}", response_model=CropSchema.__model__)
async def get_crop(uid: str):
    async with crop_manager() as session:
        crop = await crop_manager.fetch(uid, session=session)
        return crop.model_dump()
