from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.api.deps import CurrentUser, SessionDep
from app.models import Job, SavedJob

router = APIRouter(prefix="/saved-jobs", tags=["saved jobs"])


class SaveJobRequest(BaseModel):
    job_id: UUID
    note: str | None = Field(default=None, max_length=2000)


class SavedJobResponse(BaseModel):
    id: UUID
    job_id: UUID
    note: str | None


@router.get("", response_model=list[SavedJobResponse])
async def list_saved_jobs(user: CurrentUser, session: SessionDep) -> list[SavedJobResponse]:
    records = (await session.scalars(select(SavedJob).where(SavedJob.user_id == user.id))).all()
    return [SavedJobResponse(id=item.id, job_id=item.job_id, note=item.note) for item in records]


@router.post("", response_model=SavedJobResponse, status_code=status.HTTP_201_CREATED)
async def save_job(payload: SaveJobRequest, user: CurrentUser, session: SessionDep) -> SavedJobResponse:
    if await session.get(Job, payload.job_id) is None:
        raise HTTPException(status_code=404, detail="Job not found")
    existing = await session.scalar(select(SavedJob).where(SavedJob.user_id == user.id, SavedJob.job_id == payload.job_id))
    if existing:
        return SavedJobResponse(id=existing.id, job_id=existing.job_id, note=existing.note)
    saved = SavedJob(user_id=user.id, **payload.model_dump())
    session.add(saved)
    await session.commit()
    await session.refresh(saved)
    return SavedJobResponse(id=saved.id, job_id=saved.job_id, note=saved.note)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unsave_job(job_id: UUID, user: CurrentUser, session: SessionDep) -> None:
    saved = await session.scalar(select(SavedJob).where(SavedJob.user_id == user.id, SavedJob.job_id == job_id))
    if saved is None:
        raise HTTPException(status_code=404, detail="Saved job not found")
    await session.delete(saved)
    await session.commit()
