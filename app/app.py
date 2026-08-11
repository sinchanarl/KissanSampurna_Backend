from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import admin_router, v1_router

settings = get_settings()

# TODO: Integrate SharedBackend for future API key and entity management
# from SharedBackend.managers import ApiKeyManager, BaseSchema, EntityManager
# from SharedBackend.middlewares import SDKMiddleware, EntityMiddleware

app = FastAPI(
    title="Kisaan Sampurna - Crop Disease Detection API",
    description="AI-powered crop disease detection system",
    version="1.0.0"
)

app.include_router(admin_router, prefix="/admin")
app.include_router(v1_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Add SDKMiddleware for API key validation when SharedBackend is initialized
# TODO: Add EntityMiddleware for entity management when SharedBackend is initialized

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
