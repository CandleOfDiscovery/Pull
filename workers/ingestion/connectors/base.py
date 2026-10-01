"""Connector contract for legally usable public job feeds."""
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any


class JobSourceConnector(ABC):
    source_name: str

    @abstractmethod
    async def fetch_jobs(self) -> AsyncIterator[dict[str, Any]]:
        """Yield raw API/feed records while respecting the source's limits."""
        yield {}

    @abstractmethod
    def normalize_job(self, raw_job: dict[str, Any]) -> dict[str, Any]:
        """Map a source record to the canonical job event payload."""
        raise NotImplementedError
