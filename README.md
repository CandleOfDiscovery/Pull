# Job Pull Platform

A production-oriented foundation for a personal real-time job intelligence platform. It separates fast user search from source collection: source connectors produce events, pipeline workers normalize and deduplicate them, PostgreSQL owns truth, OpenSearch serves search, and FastAPI serves React.

## Current implementation

Phase 1 foundation and a vertical job-search slice are implemented: Docker development infrastructure, FastAPI health and versioned jobs endpoint, deterministic freshness labels, a responsive React search experience, connector interface, demo data, and backend tests. The job endpoint deliberately exposes demo data only; database migrations, user authentication, real connectors, Kafka consumers, Airflow DAGs, CV processing, matching, applications, alerts, and notifications remain planned work—not enabled UI claims.

## Run locally

```bash
cp .env.example .env
docker compose up --build -d
```

Open the web app at http://localhost:3000, API docs at http://localhost:8000/docs, and health at http://localhost:8000/health. The compose stack also starts PostgreSQL, Redis, Kafka (KRaft), and OpenSearch for the next implementation phases.

## Development checks

```bash
cd backend && python -m pytest
cd backend && ruff check app tests
cd frontend && npm install && npm run build
```

See [architecture documentation](docs/architecture.md) for ownership boundaries, topology, topics, and source extension guidance.
