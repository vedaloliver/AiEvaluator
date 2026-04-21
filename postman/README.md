# Postman Collection - Financial Budget Testing

This collection provides comprehensive API testing for the AI Evaluator Framework.

## Services Covered

### 1. Response Evaluator (Port 3001)
- Evaluate individual AI responses with governance thresholds
- Test financial advice scenarios with FCA compliance
- Get evaluation metrics (safety, relevance, coherence, fluency)
- Includes token usage and cost tracking

### 2. Adversarial Tester / Red Team (Port 3002)
- Run red team attack suites against models
- Test for security vulnerabilities
- Measure Attack Success Rate (ASR)
- Filter by attack categories and strategies

### 3. Observability Service (Port 8003)
- View aggregated analytics and metrics
- Query evaluation and adversarial run history
- Trace end-to-end execution flows
- Analyze costs, tokens, and latency

## Quick Start

### 1. Import Collection & Environment

1. Open Postman
2. Import `Financial-Budget-Testing.postman_collection.json`
3. Import `Financial-Budget-Testing.postman_environment.json`
4. Select "Financial Budget Testing - Local" environment

### 2. Start Services

```bash
# Terminal 1: Response Evaluator
cd apps/response-evaluator
python -m uvicorn main:app --port 3001

# Terminal 2: Adversarial Tester
cd apps/adversarial-tester
python -m uvicorn main:app --port 3002

# Terminal 3: Observability Service
cd apps/observability-service
python main.py  # Runs on port 8003
```

### 3. Run Health Checks

Execute the "Health Check" requests in each folder to verify services are running.

## Usage Workflows

### Workflow 1: Evaluate a Single Response

1. Run any scenario under **Response Evaluator** folder:
   - Scenario 1: Monthly Spending Habits
   - Scenario 2: Savings Budget Advice
   - Scenario 3: Investment Recommendations
   - Scenario 4: Credit Card Debt Management

2. Response includes:
   - `traceId` - For distributed tracing
   - `spanId` - Span identifier
   - `tokenUsage` - Prompt/completion/total tokens
   - `costEstimate` - Estimated cost in USD
   - `governanceDecision` - Pass/Warn/Fail verdict
   - Full evaluation metrics

3. Copy the `traceId` from the response

4. Go to **Observability Service** → "Get Trace by ID"
   - Set `TRACE_ID` variable to the copied trace ID
   - Run the request to see trace details

### Workflow 2: Red Team Testing

1. Run **Adversarial Tester** → "Red Team Suite: Monthly Spending"
   - Runs 10 attacks against the model
   - Returns ASR and vulnerability list

2. Response includes:
   - `traceId` - For distributed tracing
   - `attackSuccessRate` - Percentage of attacks that bypassed governance
   - `vulnerabilities` - List of successful attacks
   - `allResults` - Complete attack results

3. View red team analytics:
   - Go to **Observability Service** → "Get Adversarial Runs"
   - See all red team suite runs with ASR metrics

### Workflow 3: View Analytics Dashboard

1. Run **Observability Service** → "Get Analytics Summary"
   - Returns aggregated metrics:
     - Total evaluation runs
     - Average latency
     - Total cost and tokens
     - Average ASR across red team suites

2. Query specific runs:
   - "Get Evaluation Runs" - Recent evaluation history
   - "Get Adversarial Runs" - Recent red team tests
   - Use query parameters to filter by model or scenario

3. Visualize trace flows:
   - "Get Trace Flow Visualization" - Hierarchical span tree
   - "Get Trace Spans" - All spans for a trace

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EVALUATOR_URL` | http://localhost:3001 | Response Evaluator service |
| `ADVERSARIAL_TESTER_URL` | http://localhost:3002 | Adversarial Tester service |
| `OBSERVABILITY_URL` | http://localhost:8003 | Observability service |
| `SCENARIO_ID` | fca-consumer-duty | Financial scenario ID |
| `MODEL_ID` | gpt-4o | LLM model identifier |
| `TRACE_ID` | (empty) | Set from response for trace lookups |

## Postman Tests & Automation

### Test Scripts Included

The collection includes basic test scripts:
- Verify HTTP 200 status
- Check response has required fields
- Validate JSON structure

### Running Collection with Newman

```bash
npm install -g newman
newman run Financial-Budget-Testing.postman_collection.json \
  -e Financial-Budget-Testing.postman_environment.json
```

## Response Examples

### Evaluation Response
```json
{
  "modelId": "gpt-4o",
  "query": "Can you review my spending...",
  "response": "Based on your income...",
  "evaluations": { ... },
  "governanceDecision": {
    "decision": "PASS",
    "status": "PASS"
  },
  "timestamp": "2024-04-20T14:30:00Z",
  "durationMs": 1250,
  "traceId": "abc-123-def-456",
  "spanId": "xyz-789",
  "tokenUsage": {
    "promptTokens": 450,
    "completionTokens": 320,
    "totalTokens": 770
  },
  "costEstimate": {
    "amount": 0.00385,
    "currency": "USD",
    "modelPricing": "$2.5/$10.0 per 1M tokens"
  }
}
```

### Red Team Suite Response
```json
{
  "scenarioId": "fca-consumer-duty",
  "modelId": "gpt-4o",
  "totalAttacks": 10,
  "successfulAttacks": 2,
  "blockedAttacks": 8,
  "attackSuccessRate": 0.2,
  "vulnerabilities": [ ... ],
  "timestamp": "2024-04-20T14:35:00Z",
  "traceId": "def-456-ghi-789"
}
```

### Analytics Summary Response
```json
{
  "evaluationRuns": {
    "totalRuns": 45,
    "avgLatencyMs": 1235.5,
    "totalCost": 0.1245,
    "totalTokens": 34520
  },
  "adversarialRuns": {
    "totalSuites": 8,
    "avgAttackSuccessRate": 0.15
  }
}
```

## Troubleshooting

### Services Not Responding
- Check all services are running: `curl http://localhost:3001/api/v1/health`
- Verify ports are not in use: `netstat -an | grep LISTEN`

### CORS Errors
- Check CORS settings in each service's `.env` file
- Response evaluator: `CORS_ORIGINS=*`
- Observability: `CORS_ORIGINS=http://localhost:3000,http://localhost:3001`

### Trace ID Not Found
- Ensure observability service is running before evaluation
- Check database exists: `ls apps/observability-service/observability.db`
- Verify traceId is in the evaluation response

### Port Conflicts
If ports are already in use, update environment variables:
- Change ports in service `.env` files
- Update Postman environment variables accordingly

## Next Steps

1. **Frontend Testing**: Open `http://localhost:3000/observability` to view dashboard
2. **Custom Scenarios**: Modify request bodies to test different queries
3. **Model Comparison**: Run same query with different `modelId` values
4. **Performance Testing**: Use Newman to run collection multiple times

## Support

For issues or questions:
- Check service logs in terminal windows
- Review API documentation in each service's README
- Verify all dependencies are installed: `pip install -r requirements.txt`
