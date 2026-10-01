from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.schemas.jobs import JobPage, JobSummary, RemoteType
from app.services.freshness import freshness_label


NOW = datetime.now(timezone.utc)
DEMO_JOBS = [
    JobSummary(id=UUID("11111111-1111-1111-1111-111111111111"), title="Machine Learning Engineer", company="Northstar AI", location="Paris, France", remote_type=RemoteType.HYBRID, skills=["Python", "PyTorch", "Docker", "NLP"], source="Greenhouse", source_url="https://boards.greenhouse.io/", published_at=NOW - timedelta(minutes=18), first_seen_at=NOW - timedelta(minutes=4), freshness="Very Fresh"),
    JobSummary(id=UUID("22222222-2222-2222-2222-222222222222"), title="Senior Data Scientist", company="Lumen Labs", location="Remote — France", remote_type=RemoteType.REMOTE, skills=["Python", "SQL", "AWS"], source="Remotive", source_url="https://remotive.com/", published_at=NOW - timedelta(hours=3), first_seen_at=NOW - timedelta(hours=1), freshness="Fresh"),
]


class JobService:
    """Search boundary; replace its demo repository with OpenSearch in phase two."""

    def search(self, q: str | None, location: str | None, remote: RemoteType | None, page_size: int) -> JobPage:
        jobs = DEMO_JOBS
        if q:
            query = q.lower()
            jobs = [job for job in jobs if query in f"{job.title} {job.company} {' '.join(job.skills)}".lower()]
        if location:
            jobs = [job for job in jobs if job.location and location.lower() in job.location.lower()]
        if remote:
            jobs = [job for job in jobs if job.remote_type == remote]
        items = [job.model_copy(update={"freshness": freshness_label(job.first_seen_at)}) for job in jobs[:page_size]]
        return JobPage(items=items, total=len(jobs))
