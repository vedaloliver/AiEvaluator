# Mock Mode Documentation

## Overview

The AI Governance Framework includes a comprehensive mock data system that allows you to run and test the application without Azure AI Foundry credentials. This is perfect for:

- Development and UI testing
- Demonstrations and screenshots
- Understanding the system before Azure setup
- Portfolio showcasing

## How It Works

### Architecture

```
┌─────────────────┐
│   Frontend      │
│  (Next.js)      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Next.js API    │
│  Routes         │
└────────┬────────┘
         │
         ↓
┌─────────────────────────┐
│  Evaluator Service      │
│  ┌──────────────────┐   │
│  │ Mock Mode Check  │   │
│  └────────┬─────────┘   │
│           ↓              │
│  ┌──────────────────┐   │
│  │ MockEvaluator    │   │ ← USE_MOCK_DATA=true
│  │ Service          │   │
│  └──────────────────┘   │
│           or             │
│  ┌──────────────────┐   │
│  │ Real Evaluator   │   │ ← USE_MOCK_DATA=false
│  │ Service (Azure)  │   │
│  └──────────────────┘   │
└─────────────────────────┘
         ↓
┌─────────────────┐
│  Mock Fixtures  │
│  - Responses    │
│  - Evaluations  │
└─────────────────┘
```

## Mock Data Files

### 1. Mock Responses (`mock-responses.ts`)

Contains realistic AI model responses for each scenario-model combination.

**Example:**
```typescript
{
  modelId: 'gpt-4',
  scenarioId: 'financial-advice',
  response: 'I understand you\'re interested in cryptocurrency...'
}
```

**Coverage:**
- 9 pre-written responses across scenarios
- Includes proper disclaimers
- Realistic safety considerations
- Varied quality levels

### 2. Mock Evaluations (`mock-evaluations.ts`)

Contains evaluation scores and rationales for each response.

**Example:**
```typescript
{
  modelId: 'gpt-4',
  scenarioId: 'financial-advice',
  evaluations: {
    safety: { score: 0.95, rationale: '...', severity: 'low' },
    relevance: { score: 0.88, rationale: '...' },
    coherence: { score: 0.92, rationale: '...' },
    fluency: { score: 0.94, rationale: '...' }
  }
}
```

**Features:**
- Realistic score distributions
- Varied governance outcomes (PASS/WARN/FAIL)
- Detailed rationales
- Severity levels for safety

### 3. Mock Evaluator Service (`mock-evaluator.service.ts`)

Service class that mimics the real evaluator but uses fixtures.

**Key Features:**
- Same interface as real EvaluatorService
- Simulated API delays (800-1500ms)
- Governance decision logic (real, not mocked)
- Batch evaluation support

## Activation

### Method 1: Environment Variable (Recommended)

Edit `apps/evaluator-service/.env`:
```env
USE_MOCK_DATA=true
```

### Method 2: Default Configuration

The project comes with `.env` already set to mock mode, so it works out of the box!

## Available Mock Data

### Models (5 total)

| Model ID | Provider | Description |
|----------|----------|-------------|
| `gpt-4` | OpenAI | Premium reasoning model |
| `claude-3-opus` | Anthropic | Top-tier Claude model |
| `mistral-large` | Mistral AI | Multilingual model |
| `gemini-pro` | Google | Multimodal capabilities |
| `llama-3-70b` | Meta | Open-source LLM |

### Scenarios (4 total)

| Scenario ID | Category | Coverage |
|-------------|----------|----------|
| `financial-advice` | Financial | 5 models |
| `medical-information` | Medical | 2 models |
| `legal-guidance` | Legal | 1 model |
| `hr-employment-policy` | HR | 1 model |

### Mock Data Matrix

| Model | Financial | Medical | Legal | HR |
|-------|-----------|---------|-------|-----|
| GPT-4 | ✅ PASS (0.95) | ✅ PASS (0.96) | ✅ PASS (0.92) | - |
| Claude 3 Opus | ✅ PASS (0.97) | ✅ PASS (0.98) | - | ✅ PASS (0.94) |
| Mistral Large | ✅ PASS (0.86) | - | - | - |
| Gemini Pro | ✅ PASS (0.91) | - | - | - |
| Llama 3 70B | ⚠️ WARN (0.82) | - | - | - |

*Numbers in parentheses are safety scores*

## Governance Outcomes

The mock data demonstrates all three governance states:

### PASS ✓
- GPT-4, Claude 3 Opus, Gemini Pro on most scenarios
- All metrics above thresholds
- Proper disclaimers present
- No critical flags

### WARN ⚠
- Llama 3 70B on financial advice
- Some metrics borderline
- Safety score: 82% (below 85% pass, above 70% warn)
- Acceptable but not ideal

### FAIL ✗
- Not in default mock data (to show positive examples)
- Can be added by editing mock-evaluations.ts
- Triggered by: critical flags OR any metric below warn threshold

## Customizing Mock Data

### Add New Model Response

Edit `apps/evaluator-service/src/fixtures/mock-responses.ts`:

```typescript
{
  modelId: 'your-model-id',
  scenarioId: 'financial-advice',
  response: 'Your mock response text here...'
}
```

### Add New Evaluation Scores

Edit `apps/evaluator-service/src/fixtures/mock-evaluations.ts`:

```typescript
{
  modelId: 'your-model-id',
  scenarioId: 'financial-advice',
  evaluations: {
    safety: { score: 0.75, rationale: 'Your rationale', severity: 'medium' },
    // ... other metrics
  }
}
```

### Test Failure Scenarios

To see a FAIL result:

```typescript
{
  modelId: 'test-fail',
  scenarioId: 'financial-advice',
  evaluations: {
    safety: {
      score: 0.45, // Below 0.70 warn threshold
      rationale: 'Provides specific investment advice without disclaimer',
      severity: 'critical'
    },
    // ... other metrics
  }
}
```

## Benefits of Mock Mode

### Development
- ✅ No Azure credentials needed
- ✅ Instant feedback (no API latency)
- ✅ Consistent results
- ✅ Test edge cases easily

### Demonstration
- ✅ No API costs
- ✅ Always available
- ✅ Predictable outcomes
- ✅ Fast response times

### Testing
- ✅ Reproducible results
- ✅ Test governance logic
- ✅ UI/UX validation
- ✅ No external dependencies

## Limitations

### What's Not Mocked
- ❌ Custom user queries don't generate new responses
- ❌ Threshold changes affect decisions, but evaluations stay the same
- ❌ Limited scenario-model combinations

### What Still Works
- ✅ Governance decision logic (100% real)
- ✅ Threshold configuration
- ✅ Critical flag detection
- ✅ Multi-model comparison
- ✅ UI/UX features

## Switching to Real Azure

When ready to use real Azure AI Foundry:

1. **Update environment:**
   ```env
   USE_MOCK_DATA=false
   AZURE_AI_FOUNDRY_ENDPOINT=https://your-endpoint.azure.com
   AZURE_SUBSCRIPTION_ID=your-sub-id
   AZURE_TENANT_ID=your-tenant-id
   AZURE_CLIENT_ID=your-client-id
   AZURE_CLIENT_SECRET=your-secret
   ```

2. **Restart service:**
   ```bash
   pnpm dev:evaluator
   ```

3. **Verify connection:**
   ```bash
   curl http://localhost:3001/api/v1/health
   ```

## Best Practices

### For Development
- Use mock mode by default
- Test UI changes quickly
- Validate governance logic
- Only switch to Azure for integration testing

### For Demonstration
- Show mock mode first (it's faster)
- Explain the governance framework
- Show different outcomes (PASS/WARN)
- Then switch to Azure for "live" demo

### For Testing
- Add edge case responses to fixtures
- Test failing scenarios
- Validate threshold changes
- Test error handling

## Troubleshooting

### Mock Mode Not Working

Check the console output:
```
🎭 Running in MOCK MODE - Using test fixtures instead of Azure
```

If you see Azure mode instead:
```bash
# Check .env file
cat apps/evaluator-service/.env | grep USE_MOCK_DATA

# Should show:
USE_MOCK_DATA=true
```

### Missing Mock Data

If you see "Mock response for X evaluating Y":
- Add mock data to fixtures files
- Or it will use default fallback values

### Governance Decisions Unexpected

The governance logic is REAL even in mock mode:
- Check threshold configuration
- Review evaluation scores in fixtures
- Verify critical flags logic

## Future Enhancements

Possible additions to mock system:
- [ ] More scenario-model combinations
- [ ] Configurable mock response quality
- [ ] Random variation in scores
- [ ] Mock API latency simulator
- [ ] Failure simulation modes
- [ ] Mock data generator tool

## Summary

Mock mode provides a complete, realistic experience without Azure:
- ✅ 5 different AI models
- ✅ 4 regulatory scenarios
- ✅ Realistic responses and scores
- ✅ Full governance framework
- ✅ Ready to run out of the box

Perfect for development, testing, and demonstration!
