# Observability Service

Centralized observability service for LLM evaluation telemetry, distributed tracing, and analytics.

## Features

- **Distributed Tracing**: Track end-to-end flows with trace IDs and span hierarchies
- **Token & Cost Tracking**: Monitor LLM token usage and estimated costs per evaluation
- **Performance Metrics**: Latency, throughput, and resource utilization
- **Red Team Analytics**: Attack success rate (ASR) trends and vulnerability tracking
- **Aggregated Analytics**: Historical data analysis and trend visualization

## Architecture

### Database Schema

**Traces**: Track end-to-end execution flows
- `trace_id` (PK), `start_time`, `end_time`, `status`, `root_span_id`

**Spans**: Individual operations within a trace
- `span_id` (PK), `trace_id` (FK), `parent_span_id`, `name`, `span_type`, `duration_ms`, `attributes`

**Evaluation Runs**: Per-run evaluation results
- Full evaluation data including metrics, governance decision, tokens, cost

**Adversarial Runs**: Red team suite results
- Attack metrics, ASR, vulnerabilities, all attack results

## API Endpoints

### Ingestion
- `POST /api/v1/traces` - Create trace
- `PATCH /api/v1/traces/{trace_id}` - Update trace
- `POST /api/v1/spans` - Create span
- `POST /api/v1/evaluation-runs` - Store evaluation run
- `POST /api/v1/adversarial-runs` - Store adversarial run

### Analytics
- `GET /api/v1/analytics/evaluation-runs` - Query evaluation runs
- `GET /api/v1/analytics/evaluation-runs/{id}` - Get specific run
- `GET /api/v1/analytics/adversarial-runs` - Query adversarial runs
- `GET /api/v1/analytics/summary` - Aggregated metrics

### Tracing
- `GET /api/v1/traces/{trace_id}` - Get trace details
- `GET /api/v1/traces/{trace_id}/spans` - Get all spans for trace
- `GET /api/v1/traces/{trace_id}/flow` - Get flow visualization data

## Getting Started

### Prerequisites
- Python 3.9+
- SQLite (default) or PostgreSQL

### Installation

```bash
cd apps/observability-service
pip install -r requirements.txt
```

### Configuration

Create a `.env` file:

```env
PORT=8003
DATABASE_URL=sqlite:///./observability.db
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Run the Service

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

### Database Migrations

```bash
# Initialize Alembic (already done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

## Integration

### Response Evaluator

The response-evaluator service automatically sends:
- Trace creation at evaluation start
- Token usage and cost estimates
- Evaluation results with all metrics
- Span data for evaluation operations

### Adversarial Tester

The adversarial-tester service automatically sends:
- Trace creation at suite start
- Spans for each individual attack
- Suite results with ASR metrics
- Vulnerability data

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Type checking
mypy .

# Linting
pylint apps/observability-service/
```

## Production Deployment

### PostgreSQL Setup

1. Update `DATABASE_URL` in settings:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/observability
   ```

2. Run migrations:
   ```bash
   alembic upgrade head
   ```

### Docker

```bash
docker build -t observability-service .
docker run -p 8003:8003 observability-service
```

## Monitoring

Health check endpoint:
```bash
curl http://localhost:8003/api/v1/health
```

## Data Retention

By default, all data is retained indefinitely. For production:

1. Implement data pruning (e.g., keep last 30 days)
2. Archive old traces to cold storage
3. Set up automated cleanup jobs

## Security

- Add API authentication for ingestion endpoints
- Use HTTPS in production
- Implement rate limiting (already configured)
- Validate all input data

## License

Internal use only - AI Evaluator Framework
