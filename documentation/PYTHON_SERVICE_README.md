# Evaluator Service (Python)

Python rewrite of the evaluator service using FastAPI and Azure AI Foundry native evaluators.

## Features

- **FastAPI** server with async/await
- **Azure AI Foundry** native evaluators (12+ specialized evaluators)
- **Mock mode** for testing without Azure credentials
- **Expanded metrics**: Groundedness, Ungrounded Attributes, Intent Resolution, ECI
- Same governance logic and REST API endpoints as TypeScript version
- 4 financial services scenarios

## Quick Start

### 1. Install Dependencies

```bash
cd apps/evaluator-service-python
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set `USE_MOCK_DATA=true` for mock mode.

### 3. Run the Service

```bash
# Development mode with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --port 3002
```

The service will start on http://localhost:3002

## API Endpoints

- `GET /` - Service information
- `GET /api/v1/health` - Health check
- `GET /api/v1/scenarios` - List all scenarios
- `GET /api/v1/scenarios/:id` - Get scenario by ID
- `GET /api/v1/models` - List all models
- `GET /api/v1/models/:id` - Get model by ID
- `POST /api/v1/evaluate` - Evaluate a query

## Example Request

```bash
curl -X POST http://localhost:3002/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "scenarioId": "customer-service-response",
    "modelId": "gpt-4",
    "query": "What are overdraft fees?"
  }'
```

## Project Structure

```
apps/evaluator-service-python/
├── main.py                      # FastAPI entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── config/
│   ├── settings.py              # Pydantic settings
│   ├── scenarios.py             # Regulatory scenarios
│   └── thresholds.py            # Governance thresholds
├── models/
│   ├── evaluation.py            # Evaluation models
│   ├── scenario.py              # Scenario models
│   ├── governance.py            # Governance models
│   └── azure.py                 # Azure models
├── services/
│   ├── governance_service.py    # Governance decision logic
│   ├── mock_evaluator.py        # Mock evaluator service
│   └── model_service.py         # Model catalog
├── routes/
│   └── evaluation_routes.py     # FastAPI routes
└── fixtures/
    ├── mock_responses.py        # Mock model responses
    └── mock_evaluations.py      # Mock evaluation scores
```

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `USE_MOCK_DATA` | Use mock data instead of Azure | No (default: true) |
| `PORT` | Service port | No (default: 3001) |
| `ENVIRONMENT` | Environment (development/production) | No (default: development) |
| `AZURE_AI_FOUNDRY_ENDPOINT` | Azure endpoint URL | Yes (if not mock) |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID | Yes (if not mock) |
| `AZURE_TENANT_ID` | Azure tenant ID | Yes (if not mock) |
| `AZURE_CLIENT_ID` | Azure client ID | Yes (if not mock) |
| `AZURE_CLIENT_SECRET` | Azure client secret | Yes (if not mock) |

## Migration from TypeScript

The Python service maintains API compatibility with the TypeScript version:

- Same request/response structures
- Same governance logic
- Same endpoint paths
- Same mock data

Frontend can switch between services by changing `EVALUATOR_SERVICE_URL` environment variable.

## Development

### Adding New Scenarios

Edit `config/scenarios.py` and add a new `RegulatoryScenario` to the `REGULATORY_SCENARIOS` list.

### Adding New Models

Edit `services/model_service.py` and add a new `ModelInfo` to the `AVAILABLE_MODELS` list.

### Modifying Governance Logic

Edit `services/governance_service.py` - ensure changes match TypeScript version for consistency.
