from fastapi import APIRouter
from sqlalchemy import select

from app.api.deps import CurrentUser, SessionDep
from app.models import UserProfile
from app.schemas.account import ProfileResponse, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])


def response(user_id: object, email: str, profile: UserProfile) -> ProfileResponse:
    return ProfileResponse(user_id=user_id, email=email, name=profile.name, location=profile.location, target_roles=profile.target_roles or [], skills=profile.skills or [], years_experience=profile.years_experience, remote_preference=profile.remote_preference)


@router.get("", response_model=ProfileResponse)
async def get_profile(user: CurrentUser, session: SessionDep) -> ProfileResponse:
    profile = await session.scalar(select(UserProfile).where(UserProfile.user_id == user.id))
    if profile is None:
        profile = UserProfile(user_id=user.id)
        session.add(profile)
        await session.commit()
    return response(user.id, user.email, profile)


@router.put("", response_model=ProfileResponse)
async def update_profile(payload: ProfileUpdate, user: CurrentUser, session: SessionDep) -> ProfileResponse:
    profile = await session.scalar(select(UserProfile).where(UserProfile.user_id == user.id))
    if profile is None:
        profile = UserProfile(user_id=user.id)
        session.add(profile)
    for key, value in payload.model_dump().items():
        setattr(profile, key, value)
    await session.commit()
    await session.refresh(profile)
    return response(user.id, user.email, profile)
