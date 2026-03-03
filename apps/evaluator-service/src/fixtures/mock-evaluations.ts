/**
 * Mock evaluation scores for financial service scenarios
 * Combines all scenario evaluations
 */

import { EvaluationMetrics } from '@ai-evaluator/shared-types';
import { MOCK_EVALUATIONS_CUSTOMER_SERVICE } from './mock-evaluations-part1';
import { MOCK_EVALUATIONS_OTHER_SCENARIOS } from './mock-evaluations-part2';

interface MockEvaluation {
  modelId: string;
  scenarioId: string;
  evaluations: EvaluationMetrics;
}

// Combine all mock evaluations
export const MOCK_EVALUATIONS: MockEvaluation[] = [
  ...MOCK_EVALUATIONS_CUSTOMER_SERVICE,
  ...MOCK_EVALUATIONS_OTHER_SCENARIOS,
];

export function getMockEvaluation(
  modelId: string,
  scenarioId: string
): EvaluationMetrics {
  const mock = MOCK_EVALUATIONS.find(
    (e) => e.modelId === modelId && e.scenarioId === scenarioId
  );

  // Return mock data if available, otherwise return default scores
  return (
    mock?.evaluations || {
      safety: {
        score: 0.75,
        rationale: 'Mock evaluation: Response demonstrates adequate safety measures with some compliance considerations present.',
        severity: 'medium',
      },
      relevance: {
        score: 0.72,
        rationale: 'Mock evaluation: Response addresses the query with reasonable relevance to the financial service context.',
      },
      coherence: {
        score: 0.74,
        rationale: 'Mock evaluation: Reasonably coherent structure with acceptable logical flow.',
      },
      fluency: {
        score: 0.78,
        rationale: 'Mock evaluation: Good language quality and professional communication style.',
      },
    }
  );
}
