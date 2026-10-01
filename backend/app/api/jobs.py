from fastapi import APIRouter, Query

from app.schemas.jobs import JobPage, RemoteType
from app.services.jobs import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])
service = JobService()


@router.get("", response_model=JobPage)
async def list_jobs(
    q: str | None = Query(default=None, max_length=200),
    location: str | None = Query(default=None, max_length=120),
    remote: RemoteType | None = None,
    page_size: int = Query(default=25, ge=1, le=100),
) -> JobPage:
    return service.search(q=q, location=location, remote=remote, page_size=page_size)
