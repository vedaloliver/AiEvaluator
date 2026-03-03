import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { EvaluatorService } from '../services/evaluator.service';
import { ModelService } from '../services/model.service';
import { getAllScenarios } from '../config/scenarios.config';
import { createError } from '../middleware/error-handler';

// Request validation schemas
const ThresholdSchema = z.object({
  pass: z.number().min(0).max(1),
  warn: z.number().min(0).max(1),
});

const EvaluationRequestSchema = z.object({
  scenarioId: z.string(),
  modelId: z.string(),
  query: z.string().min(1).max(5000),
  thresholds: z
    .object({
      safety: ThresholdSchema.optional(),
      relevance: ThresholdSchema.optional(),
      coherence: ThresholdSchema.optional(),
      fluency: ThresholdSchema.optional(),
    })
    .optional(),
});

export class EvaluationController {
  private evaluatorService: EvaluatorService;
  private modelService: ModelService;

  constructor(evaluatorService: EvaluatorService) {
    this.evaluatorService = evaluatorService;
    this.modelService = new ModelService();
  }

  /**
   * POST /api/v1/evaluate
   * Evaluates a single query against a model
   */
  public evaluate = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      // Validate request body
      const validationResult = EvaluationRequestSchema.safeParse(req.body);
      if (!validationResult.success) {
        throw createError(
          'Invalid request body',
          400,
          validationResult.error.errors
        );
      }

      const evaluationRequest = validationResult.data;

      // Perform evaluation
      const result = await this.evaluatorService.evaluate(evaluationRequest);

      res.json(result);
    } catch (error) {
      next(error);
    }
  };

  /**
   * GET /api/v1/scenarios
   * Lists all available regulatory scenarios
   */
  public getScenarios = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const scenarios = getAllScenarios();

      // Return simplified scenario list
      const scenarioList = scenarios.map((scenario) => ({
        id: scenario.id,
        name: scenario.name,
        category: scenario.category,
        description: scenario.description,
        exampleQuery: scenario.exampleQuery,
      }));

      res.json({ scenarios: scenarioList });
    } catch (error) {
      next(error);
    }
  };

  /**
   * GET /api/v1/scenarios/:id
   * Gets a specific scenario by ID
   */
  public getScenario = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const { id } = req.params;
      const scenarios = getAllScenarios();
      const scenario = scenarios.find((s) => s.id === id);

      if (!scenario) {
        throw createError(`Scenario not found: ${id}`, 404);
      }

      res.json(scenario);
    } catch (error) {
      next(error);
    }
  };

  /**
   * GET /api/v1/models
   * Lists all available models
   */
  public getModels = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const models = this.modelService.getAllModels();
      res.json({ models });
    } catch (error) {
      next(error);
    }
  };

  /**
   * GET /api/v1/models/:id
   * Gets a specific model by ID
   */
  public getModel = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      const { id } = req.params;
      const model = this.modelService.getModelById(id);

      if (!model) {
        throw createError(`Model not found: ${id}`, 404);
      }

      res.json(model);
    } catch (error) {
      next(error);
    }
  };

  /**
   * GET /api/v1/health
   * Health check endpoint
   */
  public healthCheck = async (
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> => {
    try {
      res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        service: 'evaluator-service',
        version: '1.0.0',
      });
    } catch (error) {
      next(error);
    }
  };
}
