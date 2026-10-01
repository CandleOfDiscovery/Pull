from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from app.api.deps import CurrentUser, SessionDep
from app.models import Job, UserProfile
from app.services.matching import analyze_match

router = APIRouter(prefix="/matches", tags=["matching"])


class MatchResponse(BaseModel):
    job_id: UUID
    overall_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    score_breakdown: dict[str, int]
    disclaimer: str


@router.get("/{job_id}", response_model=MatchResponse)
async def get_match(job_id: UUID, user: CurrentUser, session: SessionDep) -> MatchResponse:
    job = await session.get(Job, job_id)
    profile = await session.scalar(select(UserProfile).where(UserProfile.user_id == user.id))
    if job is None:
        raise HTTPException(status_code=404, detail="The requested job could not be found.")
    analysis = analyze_match((profile.skills if profile else []), (profile.target_roles if profile else []), job.skills or [], job.title, job.location, profile.location if profile else None)
    return MatchResponse(job_id=job_id, **analysis.__dict__, disclaimer="This score measures profile-to-job similarity, not likelihood of hiring success.")
