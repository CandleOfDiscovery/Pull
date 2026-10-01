from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class RemoteType(StrEnum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class JobSummary(BaseModel):
    id: UUID
    title: str
    company: str
    location: str | None = None
    remote_type: RemoteType | None = None
    skills: list[str] = Field(default_factory=list)
    source: str
    source_url: HttpUrl
    published_at: datetime | None = None
    first_seen_at: datetime
    freshness: str


class JobPage(BaseModel):
    items: list[JobSummary]
    next_cursor: str | None = None
    total: int


class JobDetail(JobSummary):
    description: str
    application_url: HttpUrl | None = None
    employment_type: str | None = None
    experience_level: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    currency: str | None = None
    status: str
