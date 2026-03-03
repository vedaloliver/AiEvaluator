/**
 * Mock Evaluator Service
 *
 * This service provides mock evaluation results without calling Azure AI Foundry.
 * Use this for development and testing the UI without Azure credentials.
 */

import {
  EvaluationRequest,
  EvaluationResult,
  EvaluationMetrics,
} from '@ai-evaluator/shared-types';
import { GovernanceService } from './governance.service';
import { ModelService } from './model.service';
import { getScenarioById } from '../config/scenarios.config';
import { getEffectiveThresholds } from '../config/governance-thresholds.config';
import { getMockResponse } from '../fixtures/mock-responses';
import { getMockEvaluation } from '../fixtures/mock-evaluations';

export class MockEvaluatorService {
  private governanceService: GovernanceService;
  private modelService: ModelService;

  constructor() {
    this.governanceService = new GovernanceService();
    this.modelService = new ModelService();
  }

  /**
   * Main evaluation method using mock data
   */
  public async evaluate(request: EvaluationRequest): Promise<EvaluationResult> {
    const startTime = Date.now();

    // Simulate API delay
    await this.simulateDelay(800, 1500);

    // Validate inputs
    const scenario = getScenarioById(request.scenarioId);
    if (!scenario) {
      throw new Error(`Scenario not found: ${request.scenarioId}`);
    }

    const model = this.modelService.getModelById(request.modelId);
    if (!model) {
      throw new Error(`Model not found: ${request.modelId}`);
    }

    // Get effective thresholds
    const effectiveThresholds = getEffectiveThresholds({
      ...scenario.customThresholds,
      ...request.thresholds,
    });

    // Get mock response
    const modelResponse = getMockResponse(request.modelId, request.scenarioId);

    // Get mock evaluations
    const evaluations = getMockEvaluation(request.modelId, request.scenarioId);

    // Make governance decision
    const governanceDecision = this.governanceService.makeDecision(
      evaluations,
      effectiveThresholds,
      scenario.criticalFlags
    );

    // Construct result
    const result: EvaluationResult = {
      modelId: request.modelId,
      query: request.query,
      response: modelResponse,
      evaluations,
      governanceDecision,
      timestamp: new Date().toISOString(),
      durationMs: Date.now() - startTime,
    };

    return result;
  }

  /**
   * Batch evaluate multiple models with mock data
   */
  public async evaluateBatch(
    requests: EvaluationRequest[]
  ): Promise<EvaluationResult[]> {
    // Run evaluations in parallel
    const results = await Promise.allSettled(
      requests.map((request) => this.evaluate(request))
    );

    // Map results, handling errors
    return results.map((result, index) => {
      if (result.status === 'fulfilled') {
        return result.value;
      } else {
        console.error(
          `Evaluation failed for request ${index}:`,
          result.reason
        );
        // Return a failed result
        return {
          modelId: requests[index].modelId,
          query: requests[index].query,
          response: 'ERROR: Mock evaluation failed',
          evaluations: {
            safety: { score: 0, rationale: 'Evaluation failed' },
            relevance: { score: 0, rationale: 'Evaluation failed' },
            coherence: { score: 0, rationale: 'Evaluation failed' },
            fluency: { score: 0, rationale: 'Evaluation failed' },
          },
          governanceDecision: {
            status: 'FAIL',
            reasons: [`Error: ${result.reason}`],
            criticalFlags: [],
          },
          timestamp: new Date().toISOString(),
        };
      }
    });
  }

  /**
   * Simulates network delay
   */
  private async simulateDelay(minMs: number, maxMs: number): Promise<void> {
    const delay = Math.random() * (maxMs - minMs) + minMs;
    return new Promise((resolve) => setTimeout(resolve, delay));
  }
}
