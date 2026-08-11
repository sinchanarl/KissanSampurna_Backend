from fastapi import APIRouter, HTTPException

from SharedBackend.utils.helpers import model_response
from app.config import get_engine, get_settings
from managers import *
from app.models import StatusResponse

router = APIRouter(prefix="/rules")
settings = get_settings()
engine = get_engine(settings.name)

rules_manager = RuleManager(engine)
crops_manager = CropManager(engine)


@router.get("", response_model=list[RuleSchema.__model__])
async def get_rules():
    async with rules_manager() as session:
        rules = await rules_manager.fetch_all({}, session=session)
        return [rule.model_dump() for rule in rules]


@router.post("", response_model=RuleSchema.__model__)
async def post_rule(
        payload: RuleSchema.__post_model__,
        rabi_crops: list[str] | None = None,
        summer_crops: list[str] | None = None
):
    async with rules_manager() as session:
        rule = await rules_manager.create(payload, session=session, joins=[RuleSchema.recommended_rabi_crops_rel, RuleSchema.recommended_summer_crops_rel])
        for rabi_crop_uid in rabi_crops or []:
            rabi_crop = await crops_manager.fetch(rabi_crop_uid, session=session)
            rule.recommended_rabi_crops_rel.append(rabi_crop)
        for summer_crop_uid in summer_crops or []:
            summer_crop = await crops_manager.fetch(summer_crop_uid, session=session)
            rule.recommended_summer_crops_rel.append(summer_crop)
        return rule.model_dump()


@router.post("/apply", response_model=RuleSchema.__model__, responses={404: {"model": StatusResponse}})
async def apply_rules(payload: RuleSchema.__post_model__):
    async with rules_manager() as session:
        rule = await rules_manager.fetch_all(
            filters=payload.model_dump(exclude_none=True),
            session=session,
            joins=[RuleSchema.recommended_rabi_crops_rel, RuleSchema.recommended_summer_crops_rel]
        )
        if len(rule) == 0:
            return model_response(StatusResponse(status="No rules found"), 404)
        return rule[0].model_dump()
