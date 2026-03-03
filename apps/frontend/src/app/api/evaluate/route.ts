import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';
import {
  MultiModelEvaluationRequest,
  EvaluationRequest,
  EvaluationResult,
} from '@ai-evaluator/shared-types';

const EVALUATOR_SERVICE_URL =
  process.env.EVALUATOR_SERVICE_URL || 'http://localhost:3001';

export async function POST(request: NextRequest) {
  try {
    const body: MultiModelEvaluationRequest = await request.json();

    // Validate request
    if (!body.scenarioId || !body.modelIds || body.modelIds.length === 0 || !body.query) {
      return NextResponse.json(
        {
          error: {
            message: 'Missing required fields: scenarioId, modelIds, query',
            statusCode: 400,
          },
        },
        { status: 400 }
      );
    }

    // Create individual evaluation requests for each model
    const evaluationPromises = body.modelIds.map((modelId) => {
      const evalRequest: EvaluationRequest = {
        scenarioId: body.scenarioId,
        modelId,
        query: body.query,
        thresholds: body.thresholds,
      };

      return axios
        .post<EvaluationResult>(
          `${EVALUATOR_SERVICE_URL}/api/v1/evaluate`,
          evalRequest,
          {
            timeout: 120000,
          }
        )
        .then((response) => response.data)
        .catch((error) => {
          console.error(`Evaluation failed for model ${modelId}:`, error);
          // Return a failed result instead of throwing
          return {
            modelId,
            query: body.query,
            response: 'ERROR: Evaluation failed',
            evaluations: {
              safety: { score: 0, rationale: `Error: ${error.message}` },
              relevance: { score: 0, rationale: 'Evaluation failed' },
              coherence: { score: 0, rationale: 'Evaluation failed' },
              fluency: { score: 0, rationale: 'Evaluation failed' },
            },
            governanceDecision: {
              status: 'FAIL' as const,
              reasons: [`Evaluation error: ${error.message}`],
              criticalFlags: [],
            },
            timestamp: new Date().toISOString(),
          } as EvaluationResult;
        });
    });

    // Wait for all evaluations to complete
    const results = await Promise.all(evaluationPromises);

    return NextResponse.json({
      results,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Evaluation orchestration error:', error);
    return NextResponse.json(
      {
        error: {
          message: error instanceof Error ? error.message : 'Internal server error',
          statusCode: 500,
        },
      },
      { status: 500 }
    );
  }
}
