from fastapi import APIRouter, Depends, HTTPException
import uuid

from app.models import *
from app.config import get_settings
from app.utils import dependencies as D

settings = get_settings()

# Lightweight local API key generation for development/testing.
# Replace with `SharedBackend.managers.ApiKeyManager` when submodule is available.
router = APIRouter(dependencies=[Depends(D.master_key_dependency)])


@router.get("/health-check")
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


@router.post("/generate-api-key", response_model=GenerateApiKeyResponse)
async def generate_api_key(payload: GenerateApiKeyRequest):
    # Dev stub: create a UUID uid and key and return it. No persistence.
    uid = str(uuid.uuid4())
    key = str(uuid.uuid4())
    return GenerateApiKeyResponse(uid=uid, key=key, scopes=payload.scopes)


@router.delete("/revoke-api-key/{uid}", response_model=StatusResponse)
async def revoke_api_key(uid: str):
    # Dev stub: no-op revoke (no persistence). In production, delegate to ApiKeyManager.
    return StatusResponse()
