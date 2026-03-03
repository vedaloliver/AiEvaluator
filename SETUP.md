# Setup Guide

## Prerequisites

- Node.js >= 18.0.0
- pnpm >= 8.0.0
- Azure AI Foundry account with API access

## Installation Steps

### 1. Install Dependencies

```bash
pnpm install
```

This will install dependencies for all workspaces (root, frontend, evaluator-service, and shared-types).

### 2. Build Shared Types

The shared-types package must be built before running the applications:

```bash
pnpm --filter shared-types build
```

Or build everything:

```bash
pnpm build
```

### 3. Configure Environment Variables

#### Evaluator Service

Copy the example environment file:

```bash
cp apps/evaluator-service/.env.example apps/evaluator-service/.env
```

Edit `apps/evaluator-service/.env` with your Azure credentials:

```env
AZURE_AI_FOUNDRY_ENDPOINT=https://your-endpoint.azure.com
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
EVALUATOR_SERVICE_PORT=3001
```

#### Frontend

Copy the example environment file:

```bash
cp apps/frontend/.env.example apps/frontend/.env.local
```

Edit `apps/frontend/.env.local` (should work with defaults):

```env
NEXT_PUBLIC_API_URL=http://localhost:3000
EVALUATOR_SERVICE_URL=http://localhost:3001
```

### 4. Start Development Servers

Start both services concurrently:

```bash
pnpm dev
```

Or start them separately:

```bash
# Terminal 1 - Evaluator Service
pnpm dev:evaluator

# Terminal 2 - Frontend
pnpm dev:frontend
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Evaluator Service API**: http://localhost:3001
- **API Documentation**: http://localhost:3001/ (lists all endpoints)

## Verification

### Test Evaluator Service

```bash
curl http://localhost:3001/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "service": "evaluator-service",
  "version": "1.0.0"
}
```

### Test Frontend API

```bash
curl http://localhost:3000/api/scenarios
```

## Troubleshooting

### Port Already in Use

If ports 3000 or 3001 are in use, you can change them:

- Frontend: Set `PORT=3002` in environment or use `PORT=3002 pnpm dev:frontend`
- Evaluator Service: Change `EVALUATOR_SERVICE_PORT` in `.env`

### Azure Authentication Errors

Ensure your Azure credentials are correct:
1. Verify the Azure AI Foundry endpoint is accessible
2. Check that your service principal has the correct permissions
3. Test credentials using Azure CLI: `az login --service-principal`

### Module Resolution Errors

If you see TypeScript errors about missing modules:

```bash
# Clean all build outputs
pnpm clean

# Rebuild shared types
pnpm --filter shared-types build

# Restart dev servers
pnpm dev
```

### CORS Errors

The evaluator service has CORS enabled by default. If you're running the frontend on a different port, CORS should work automatically.

## Building for Production

### Build All Packages

```bash
pnpm build
```

This will:
1. Build shared-types
2. Build evaluator-service
3. Build frontend

### Start Production Servers

```bash
# Evaluator Service
cd apps/evaluator-service
pnpm start

# Frontend (separate terminal)
cd apps/frontend
pnpm start
```

## Project Structure

```
AiEvaluator/
├── apps/
│   ├── frontend/              # Next.js application (port 3000)
│   └── evaluator-service/     # Express API (port 3001)
├── packages/
│   └── shared-types/          # Shared TypeScript types
├── package.json               # Root workspace config
└── pnpm-workspace.yaml        # Workspace definition
```

## Key Features

1. **Multi-Model Comparison**: Evaluate multiple AI models side-by-side
2. **Governance Framework**: Configurable thresholds with PASS/WARN/FAIL decisions
3. **Regulatory Scenarios**: Pre-defined scenarios for Financial, Medical, Legal, and HR domains
4. **Evaluation Metrics**: Safety, Relevance, Coherence, and Fluency scores
5. **Visual Dashboard**: Color-coded metrics and governance decisions

## Next Steps

- Customize governance thresholds in `apps/evaluator-service/src/config/governance-thresholds.config.ts`
- Add new scenarios in `apps/evaluator-service/src/config/scenarios.config.ts`
- Configure additional models in `apps/evaluator-service/src/services/model.service.ts`
