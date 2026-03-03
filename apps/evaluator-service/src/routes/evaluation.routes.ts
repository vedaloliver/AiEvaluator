import { Router } from 'express';
import { EvaluationController } from '../controllers/evaluation.controller';
import { rateLimiter } from '../middleware/rate-limiter';

export function createEvaluationRoutes(
  controller: EvaluationController
): Router {
  const router = Router();

  // Apply rate limiting to evaluation endpoint
  router.post('/evaluate', rateLimiter, controller.evaluate);

  // Scenario endpoints
  router.get('/scenarios', controller.getScenarios);
  router.get('/scenarios/:id', controller.getScenario);

  // Model endpoints
  router.get('/models', controller.getModels);
  router.get('/models/:id', controller.getModel);

  // Health check
  router.get('/health', controller.healthCheck);

  return router;
}
