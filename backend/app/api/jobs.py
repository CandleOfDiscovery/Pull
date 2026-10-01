from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from app.api.deps import SessionDep
from app.schemas.jobs import JobDetail, JobPage, RemoteType
from app.services.jobs import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])
service = JobService()


@router.get("", response_model=JobPage)
async def list_jobs(
    session: SessionDep,
    q: str | None = Query(default=None, max_length=200),
    location: str | None = Query(default=None, max_length=120),
    remote: RemoteType | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
) -> JobPage:
    return await service.search(session, q=q, location=location, remote=remote, page=page, page_size=page_size)


@router.get("/{job_id}", response_model=JobDetail)
async def get_job(job_id: UUID, session: SessionDep) -> JobDetail:
    job = await service.get(session, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="The requested job could not be found.")
    return job
