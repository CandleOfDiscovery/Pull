from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.alerts import router as alerts_router
from app.api.jobs import router as jobs_router
from app.api.matches import router as matches_router
from app.api.profile import router as profile_router
from app.api.saved import router as saved_router
from app.core.database import SessionLocal, engine
from app.models.base import Base
from app.services.jobs import seed_demo_jobs


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with SessionLocal() as session:
        await seed_demo_jobs(session)
    yield

app = FastAPI(title="Job Pull API", version="0.2.0", openapi_url="/api/v1/openapi.json", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(profile_router, prefix="/api/v1")
app.include_router(matches_router, prefix="/api/v1")
app.include_router(saved_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/ready", tags=["system"])
async def ready() -> dict[str, str]:
    return {"status": "ready"}
