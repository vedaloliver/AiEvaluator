# Quick Start Guide - Mock Mode

Get the AI Governance Framework running in 2 minutes with mock data!

## Prerequisites

- Node.js >= 18.0.0
- pnpm >= 8.0.0

## Quick Start (Mock Data - No Azure Required)

### 1. Install Dependencies

```bash
pnpm install
```

### 2. Build Shared Types

```bash
pnpm --filter shared-types build
```

### 3. Start the Application

```bash
pnpm dev
```

That's it! The application is now running with mock data:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:3001

## What You'll See

The mock data includes realistic responses from 5 AI models:

### Models Available
1. **GPT-4** (OpenAI) - Premium model
2. **Claude 3 Opus** (Anthropic) - Top-tier reasoning
3. **Mistral Large** (Mistral AI) - Multilingual powerhouse
4. **Gemini Pro** (Google) - Multimodal capabilities
5. **Llama 3 70B** (Meta) - Open-source option

### Scenarios Available
1. **Financial Advice Validation** - Investment guidance evaluation
2. **Medical Information Queries** - Healthcare information assessment
3. **Legal Guidance Requests** - Legal advice compliance
4. **HR/Employment Policy** - Workplace policy evaluation

## Try It Out

1. Open http://localhost:3000
2. Select a scenario (e.g., "Financial Advice Validation")
3. Choose 2-4 models to compare
4. Submit the pre-filled query or write your own
5. Watch the evaluation results appear!

## Mock Data Features

The mock data demonstrates:
- ✅ Different governance decisions (PASS/WARN/FAIL)
- ✅ Varied evaluation scores across models
- ✅ Realistic AI responses with proper disclaimers
- ✅ Critical safety flag detection
- ✅ Model performance differences

### Example Results You'll See:

**GPT-4 on Financial Advice:**
- Safety: 95% (PASS) - Excellent disclaimers
- Relevance: 88% (PASS)
- Overall: PASS ✓

**Llama 3 70B on Financial Advice:**
- Safety: 82% (WARN) - Good but borderline
- Relevance: 80% (PASS)
- Overall: WARN ⚠

## Next Steps

### To Switch to Real Azure Integration:

1. Edit `apps/evaluator-service/.env`:
   ```env
   USE_MOCK_DATA=false
   AZURE_AI_FOUNDRY_ENDPOINT=https://your-endpoint.azure.com
   # ... add your Azure credentials
   ```

2. Restart the evaluator service:
   ```bash
   pnpm dev:evaluator
   ```

## Troubleshooting

### "Cannot find module '@ai-evaluator/shared-types'"

```bash
pnpm --filter shared-types build
```

### Port Already in Use

Stop the existing process or change ports:
```bash
# Stop existing processes
lsof -ti:3000 | xargs kill
lsof -ti:3001 | xargs kill

# Then restart
pnpm dev
```

### Changes Not Appearing

```bash
# Clean and rebuild
pnpm clean
pnpm --filter shared-types build
pnpm dev
```

## Development Tips

### Test Different Scenarios

Mock responses are scenario-specific:
- Financial scenarios show more conservative responses
- Medical scenarios have stricter safety scores
- Each model has different characteristics

### Understand the Mock Data

Check these files to see how mock data is structured:
- `apps/evaluator-service/src/fixtures/mock-responses.ts` - Model responses
- `apps/evaluator-service/src/fixtures/mock-evaluations.ts` - Evaluation scores

### Customize Mock Data

You can edit the fixtures files to:
- Add new model responses
- Adjust evaluation scores
- Test edge cases (e.g., failing scenarios)
- Add new scenarios

## What's Next?

1. **Explore the UI** - Try all 4 scenarios with different models
2. **Review the Code** - See how governance decisions are made
3. **Customize** - Modify thresholds, add scenarios
4. **Deploy** - When ready, connect to Azure for real evaluations

## Need Help?

- See `SETUP.md` for detailed setup instructions
- See `PROJECT_STATUS.md` for architecture details
- See `README.md` for feature documentation
