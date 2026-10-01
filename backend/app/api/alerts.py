from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import CurrentUser, SessionDep
from app.models import Alert
from app.schemas.account import AlertCreate, AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


def serialize(alert: Alert) -> AlertResponse:
    return AlertResponse(id=alert.id, query=alert.query, location=alert.location, remote_type=alert.remote_type, min_match=alert.min_match, enabled=alert.enabled, created_at=alert.created_at)


@router.get("", response_model=list[AlertResponse])
async def list_alerts(user: CurrentUser, session: SessionDep) -> list[AlertResponse]:
    alerts = (await session.scalars(select(Alert).where(Alert.user_id == user.id).order_by(Alert.created_at.desc()))).all()
    return [serialize(alert) for alert in alerts]


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(payload: AlertCreate, user: CurrentUser, session: SessionDep) -> AlertResponse:
    alert = Alert(user_id=user.id, **payload.model_dump())
    session.add(alert)
    await session.commit()
    await session.refresh(alert)
    return serialize(alert)


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(alert_id: UUID, user: CurrentUser, session: SessionDep) -> None:
    alert = await session.get(Alert, alert_id)
    if alert is None or alert.user_id != user.id:
        raise HTTPException(status_code=404, detail="Alert not found")
    await session.delete(alert)
    await session.commit()
