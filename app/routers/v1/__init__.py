from fastapi import APIRouter

from app.config import get_settings
from app.models import *

from .analyze import router as analyze_router

settings = get_settings()

router = APIRouter()
# Include only the analysis endpoints for now; other routers require the
# SharedBackend DB-backed managers and will be enabled once the shared
# submodule / DB is available.
router.include_router(analyze_router)

@router.get("/health-check", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(
        status=f"{settings.name}[node:{0}/{0}] is running with {0}/{0} passing",
        version=settings.version,
        commit=settings.commit,
        branch=settings.branch,
        build_time=settings.build_time,
        build_number=settings.build_number,
        build_tags=settings.build_tags,
    )
