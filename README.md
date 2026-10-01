# Job Pull Platform

A production-oriented foundation for a personal real-time job intelligence platform. It separates fast user search from source collection: source connectors produce events, pipeline workers normalize and deduplicate them, PostgreSQL owns truth, OpenSearch serves search, and FastAPI serves React.

## Current implementation

The current vertical slice includes Docker development infrastructure; a PostgreSQL/SQLite-compatible SQLAlchemy model; Alembic initial migration; secure registration and login; profile editing; persisted job search/detail endpoints; deterministic freshness; explainable deterministic matching; saved jobs; alerts; demo data; a responsive React search experience; and a public-source connector contract. The demo seed is intentionally enabled for local exploration.

Kafka consumers, Airflow DAGs, real source connectors, OpenSearch indexing, CV/object-storage processing, application pipeline UI, notification delivery, and administrative observability remain the next implementation increments. They are not represented as completed product functionality.

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
