from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Job
from app.schemas.jobs import JobDetail, JobPage, JobSummary, RemoteType
from app.services.freshness import freshness_label


def job_summary(job: Job) -> JobSummary:
    return JobSummary(
        id=job.id, title=job.title, company=job.company, location=job.location,
        remote_type=job.remote_type, skills=job.skills or [], source=job.source,
        source_url=job.source_url, published_at=job.published_at,
        first_seen_at=job.first_seen_at, freshness=freshness_label(job.first_seen_at),
    )


class JobService:
    async def search(self, session: AsyncSession, q: str | None, location: str | None, remote: RemoteType | None, page: int, page_size: int) -> JobPage:
        statement: Select[tuple[Job]] = select(Job).where(Job.status == "active")
        if q:
            term = f"%{q.strip()}%"
            statement = statement.where(Job.title.ilike(term) | Job.company.ilike(term) | Job.description.ilike(term))
        if location:
            statement = statement.where(Job.location.ilike(f"%{location.strip()}%"))
        if remote:
            statement = statement.where(Job.remote_type == remote.value)
        total = await session.scalar(select(func.count()).select_from(statement.subquery())) or 0
        statement = statement.order_by(Job.published_at.desc().nullslast(), Job.first_seen_at.desc()).offset((page - 1) * page_size).limit(page_size)
        jobs = (await session.scalars(statement)).all()
        return JobPage(items=[job_summary(job) for job in jobs], total=total, next_cursor=str(page + 1) if page * page_size < total else None)

    async def get(self, session: AsyncSession, job_id: UUID) -> JobDetail | None:
        job = await session.get(Job, job_id)
        if job is None:
            return None
        return JobDetail(**job_summary(job).model_dump(), description=job.description, application_url=job.application_url, employment_type=job.employment_type, experience_level=job.experience_level, salary_min=job.salary_min, salary_max=job.salary_max, currency=job.currency, status=job.status)


async def seed_demo_jobs(session: AsyncSession) -> None:
    if await session.scalar(select(func.count()).select_from(Job)):
        return
    now = datetime.now(timezone.utc)
    session.add_all([
        Job(source="Greenhouse", source_job_id="demo-ml-1", source_url="https://boards.greenhouse.io/", application_url="https://boards.greenhouse.io/", title="Machine Learning Engineer", company="Northstar AI", description="Build dependable NLP and machine learning products with Python, PyTorch, Docker, and collaborative engineering practices.", location="Paris, France", country="France", city="Paris", remote_type="hybrid", employment_type="full_time", experience_level="mid", skills=["Python", "PyTorch", "Docker", "NLP"], published_at=now-timedelta(minutes=18), first_seen_at=now-timedelta(minutes=4), last_seen_at=now),
        Job(source="Remotive", source_job_id="demo-ds-1", source_url="https://remotive.com/", application_url="https://remotive.com/", title="Senior Data Scientist", company="Lumen Labs", description="Own experimentation and data products. Strong Python, SQL, and AWS skills are required.", location="Remote — France", country="France", city=None, remote_type="remote", employment_type="full_time", experience_level="senior", skills=["Python", "SQL", "AWS"], published_at=now-timedelta(hours=3), first_seen_at=now-timedelta(hours=1), last_seen_at=now),
    ])
    await session.commit()
