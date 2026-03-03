import {
  EvaluationRequest,
  EvaluationResult,
  EvaluationMetrics,
  AzureChatMessage,
} from '@ai-evaluator/shared-types';
import { AzureClientService } from './azure-client.service';
import { GovernanceService } from './governance.service';
import { ModelService } from './model.service';
import { getScenarioById } from '../config/scenarios.config';
import { getEffectiveThresholds } from '../config/governance-thresholds.config';

export class EvaluatorService {
  private azureClient: AzureClientService;
  private governanceService: GovernanceService;
  private modelService: ModelService;

  constructor(azureClient: AzureClientService) {
    this.azureClient = azureClient;
    this.governanceService = new GovernanceService();
    this.modelService = new ModelService();
  }

  /**
   * Main evaluation method that orchestrates the entire process
   */
  public async evaluate(request: EvaluationRequest): Promise<EvaluationResult> {
    const startTime = Date.now();

    // 1. Validate inputs
    const scenario = getScenarioById(request.scenarioId);
    if (!scenario) {
      throw new Error(`Scenario not found: ${request.scenarioId}`);
    }

    const model = this.modelService.getModelById(request.modelId);
    if (!model) {
      throw new Error(`Model not found: ${request.modelId}`);
    }

    // 2. Get effective thresholds (merge scenario + request overrides)
    const effectiveThresholds = getEffectiveThresholds({
      ...scenario.customThresholds,
      ...request.thresholds,
    });

    // 3. Generate response from model
    const modelResponse = await this.generateResponse(
      request.modelId,
      scenario.systemPrompt,
      request.query
    );

    // 4. Run all evaluators in parallel
    const evaluations = await this.runEvaluators(
      request.query,
      modelResponse,
      scenario.category
    );

    // 5. Make governance decision
    const governanceDecision = this.governanceService.makeDecision(
      evaluations,
      effectiveThresholds,
      scenario.criticalFlags
    );

    // 6. Construct result
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
   * Generates a response from the specified model
   */
  private async generateResponse(
    modelId: string,
    systemPrompt: string,
    query: string
  ): Promise<string> {
    try {
      const messages: AzureChatMessage[] = [
        {
          role: 'system',
          content: systemPrompt,
        },
        {
          role: 'user',
          content: query,
        },
      ];

      const response = await this.azureClient.invokeModel(modelId, {
        messages,
        temperature: 0.7,
        maxTokens: 1000,
      });

      return response.choices[0].message.content;
    } catch (error) {
      console.error(`Error generating response from ${modelId}:`, error);
      throw new Error(`Failed to generate response: ${error}`);
    }
  }

  /**
   * Runs all evaluators in parallel
   */
  private async runEvaluators(
    query: string,
    response: string,
    context: string
  ): Promise<EvaluationMetrics> {
    try {
      const [safety, relevance, coherence, fluency] = await Promise.all([
        this.azureClient.runEvaluator('safety', { query, response, context }),
        this.azureClient.runEvaluator('relevance', { query, response, context }),
        this.azureClient.runEvaluator('coherence', { query, response, context }),
        this.azureClient.runEvaluator('fluency', { query, response, context }),
      ]);

      return {
        safety: {
          score: safety.score,
          rationale: safety.rationale,
          severity: safety.severity,
        },
        relevance: {
          score: relevance.score,
          rationale: relevance.rationale,
        },
        coherence: {
          score: coherence.score,
          rationale: coherence.rationale,
        },
        fluency: {
          score: fluency.score,
          rationale: fluency.rationale,
        },
      };
    } catch (error) {
      console.error('Error running evaluators:', error);
      throw new Error(`Evaluation failed: ${error}`);
    }
  }

  /**
   * Batch evaluate multiple models
   */
  public async evaluateBatch(
    requests: EvaluationRequest[]
  ): Promise<EvaluationResult[]> {
    // Run evaluations in parallel for better performance
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
          response: 'ERROR: Failed to generate response',
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
}
