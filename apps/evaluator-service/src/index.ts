import express, { Application } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import { AzureClientService } from './services/azure-client.service';
import { EvaluatorService } from './services/evaluator.service';
import { MockEvaluatorService } from './services/mock-evaluator.service';
import { EvaluationController } from './controllers/evaluation.controller';
import { createEvaluationRoutes } from './routes/evaluation.routes';
import { errorHandler, notFoundHandler } from './middleware/error-handler';
import { AzureAIConfig } from '@ai-evaluator/shared-types';

// Load environment variables
dotenv.config();

// Check if using mock data
const USE_MOCK_DATA = process.env.USE_MOCK_DATA === 'true';

let evaluatorService: EvaluatorService | MockEvaluatorService;
let evaluationController: EvaluationController;

if (USE_MOCK_DATA) {
  console.log('🎭 Running in MOCK MODE - Using test fixtures instead of Azure');
  evaluatorService = new MockEvaluatorService();
  evaluationController = new EvaluationController(evaluatorService as any);
} else {
  // Validate required environment variables for Azure
  const requiredEnvVars = [
    'AZURE_AI_FOUNDRY_ENDPOINT',
    'AZURE_SUBSCRIPTION_ID',
    'AZURE_TENANT_ID',
    'AZURE_CLIENT_ID',
    'AZURE_CLIENT_SECRET',
  ];

  const missingEnvVars = requiredEnvVars.filter(
    (varName) => !process.env[varName]
  );

  if (missingEnvVars.length > 0) {
    console.error(
      `❌ Missing required environment variables: ${missingEnvVars.join(', ')}`
    );
    console.error('💡 Tip: Set USE_MOCK_DATA=true in .env to use mock data instead');
    console.error('Please check your .env file');
    process.exit(1);
  }

  // Create Azure configuration
  const azureConfig: AzureAIConfig = {
    endpoint: process.env.AZURE_AI_FOUNDRY_ENDPOINT!,
    subscriptionId: process.env.AZURE_SUBSCRIPTION_ID!,
    tenantId: process.env.AZURE_TENANT_ID!,
    clientId: process.env.AZURE_CLIENT_ID!,
    clientSecret: process.env.AZURE_CLIENT_SECRET!,
  };

  // Initialize services with Azure
  const azureClient = new AzureClientService(azureConfig);
  evaluatorService = new EvaluatorService(azureClient);
  evaluationController = new EvaluationController(evaluatorService);
}

// Create Express app
const app: Application = express();
const PORT = parseInt(process.env.EVALUATOR_SERVICE_PORT || '3001', 10);

// Middleware
app.use(helmet()); // Security headers
app.use(cors()); // Enable CORS
app.use(express.json({ limit: '10mb' })); // Parse JSON bodies
app.use(express.urlencoded({ extended: true }));
app.use(
  morgan(process.env.NODE_ENV === 'production' ? 'combined' : 'dev')
); // Logging

// API Routes
app.use('/api/v1', createEvaluationRoutes(evaluationController));

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    service: 'AI Evaluator Service',
    version: '1.0.0',
    status: 'running',
    endpoints: {
      health: '/api/v1/health',
      evaluate: 'POST /api/v1/evaluate',
      scenarios: 'GET /api/v1/scenarios',
      models: 'GET /api/v1/models',
    },
  });
});

// Error handling
app.use(notFoundHandler);
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  console.log(`\n🚀 Evaluator Service running on port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);

  if (USE_MOCK_DATA) {
    console.log(`🎭 Mode: MOCK DATA (using test fixtures)`);
    console.log(`   Set USE_MOCK_DATA=false to use real Azure integration`);
  } else {
    console.log(`☁️  Mode: Azure AI Foundry`);
    console.log(`🔗 Azure Endpoint: ${process.env.AZURE_AI_FOUNDRY_ENDPOINT}`);
  }

  console.log(`\n📍 Available endpoints:`);
  console.log(`   - http://localhost:${PORT}/`);
  console.log(`   - http://localhost:${PORT}/api/v1/health`);
  console.log(`   - http://localhost:${PORT}/api/v1/scenarios`);
  console.log(`   - http://localhost:${PORT}/api/v1/models`);
  console.log(`   - http://localhost:${PORT}/api/v1/evaluate`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
});
