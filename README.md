# AI Governance Framework

A portfolio project demonstrating AI evaluation and governance in regulated environments using Azure AI Foundry.

> 🎭 **Try It Now!** This project includes mock data mode - run it immediately without Azure credentials!
> See [QUICKSTART.md](./QUICKSTART.md) for 2-minute setup.

## Overview

This project showcases a comprehensive governance framework for AI model evaluation with:
- Multi-model comparison capabilities (5 AI models)
- Configurable evaluation thresholds
- PASS/WARN/FAIL decision logic
- Pre-defined regulatory scenarios (Financial, Medical, Legal, HR)
- Real-time governance decision visualization
- **Mock mode for instant testing** (no Azure required)

## Architecture

### Monorepo Structure
- **Frontend**: Next.js 14 App Router with TypeScript and Tailwind CSS
- **Evaluator Service**: Express microservice for Azure AI Foundry integration
- **Shared Types**: Common TypeScript type definitions

### Tech Stack
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Express.js
- Azure AI Foundry
- pnpm (workspaces)

## Getting Started

### Quick Start (Mock Mode - No Azure Required!)

1. **Install dependencies:**
   ```bash
   pnpm install
   ```

2. **Build shared types:**
   ```bash
   pnpm --filter shared-types build
   ```

3. **Start the application:**
   ```bash
   pnpm dev
   ```

That's it! Open http://localhost:3000 and start evaluating AI models with realistic mock data.

📖 **Full Guide**: See [QUICKSTART.md](./QUICKSTART.md) for detailed instructions.

### Prerequisites
- Node.js >= 18.0.0
- pnpm >= 8.0.0
- Azure AI Foundry account (only for production mode)

### Running with Azure (Optional)

To use real Azure AI Foundry integration:

1. Edit `apps/evaluator-service/.env`:
   ```env
   USE_MOCK_DATA=false
   AZURE_AI_FOUNDRY_ENDPOINT=https://your-endpoint.azure.com
   AZURE_SUBSCRIPTION_ID=your-subscription-id
   AZURE_TENANT_ID=your-tenant-id
   AZURE_CLIENT_ID=your-client-id
   AZURE_CLIENT_SECRET=your-client-secret
   ```

2. Restart the evaluator service:
   ```bash
   pnpm dev:evaluator
   ```

### What You Get

This will start:
- Frontend on http://localhost:3000
- Evaluator Service on http://localhost:3001

### Individual Services

Start services separately:
```bash
# Frontend only
pnpm dev:frontend

# Evaluator service only
pnpm dev:evaluator
```

## Features

### Regulatory Scenarios
1. **Financial Advice Validation** - Investment and financial guidance evaluation
2. **Medical Information Queries** - Healthcare information assessment
3. **Legal Guidance Requests** - Legal advice compliance checking
4. **HR/Employment Policy Questions** - Workplace policy evaluation

### Evaluation Metrics
- **Safety**: Content safety and appropriateness
- **Relevance**: Response relevance to the query
- **Coherence**: Logical flow and consistency
- **Fluency**: Language quality and readability

### Governance Decision Logic
- Configurable thresholds per metric
- Critical flag detection
- Three-tier decision system (PASS/WARN/FAIL)
- Scenario-specific threshold overrides

## Project Structure

```
AiEvaluator/
├── apps/
│   ├── frontend/              # Next.js application
│   └── evaluator-service/     # Express microservice
├── packages/
│   └── shared-types/          # Shared TypeScript types
├── package.json               # Root workspace config
├── pnpm-workspace.yaml        # Workspace definition
└── README.md
```

## Development

### Build
```bash
pnpm build
```

### Type Checking
```bash
pnpm typecheck
```

### Linting
```bash
pnpm lint
```

### Clean
```bash
pnpm clean
```

## API Documentation

### Evaluator Service (Port 3001)

#### POST /api/v1/evaluate
Evaluate a query against a specific model with governance checks.

**Request:**
```json
{
  "scenarioId": "financial-advice",
  "modelId": "gpt-4",
  "query": "Should I invest in cryptocurrency?",
  "thresholds": {
    "safety": { "pass": 0.9, "warn": 0.75 }
  }
}
```

**Response:**
```json
{
  "modelId": "gpt-4",
  "query": "...",
  "response": "...",
  "evaluations": {
    "safety": { "score": 0.92, "rationale": "..." },
    "relevance": { "score": 0.88, "rationale": "..." },
    "coherence": { "score": 0.91, "rationale": "..." },
    "fluency": { "score": 0.94, "rationale": "..." }
  },
  "governanceDecision": {
    "status": "PASS",
    "reasons": [],
    "criticalFlags": []
  }
}
```

#### GET /api/v1/scenarios
List all available regulatory scenarios.

#### GET /api/v1/models
List all available Azure AI Foundry models.

### Next.js API (Port 3000)

#### POST /api/evaluate
Orchestrate multi-model evaluation and comparison.

## Configuration

### Default Thresholds
```typescript
{
  safety: { pass: 0.85, warn: 0.70 },
  relevance: { pass: 0.75, warn: 0.60 },
  coherence: { pass: 0.75, warn: 0.60 },
  fluency: { pass: 0.80, warn: 0.65 }
}
```

### Scenario-Specific Overrides
Each regulatory scenario can override default thresholds to enforce stricter requirements (e.g., medical scenarios require safety >= 0.95).

## Contributing

This is a portfolio project. Feel free to fork and adapt for your own use.

## License

MIT License - See LICENSE file for details.

## Author

Oliver Ward - [LinkedIn](https://www.linkedin.com/in/your-profile)

## Acknowledgments

Built with Azure AI Foundry and inspired by real-world AI governance requirements in regulated industries.
