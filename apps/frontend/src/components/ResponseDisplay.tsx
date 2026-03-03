'use client';

import { EvaluationResult } from '@ai-evaluator/shared-types';
import MetricsDashboard from './EvaluationMetrics/MetricsDashboard';
import GovernanceDecisionBadge from './EvaluationMetrics/GovernanceDecisionBadge';

interface ResponseDisplayProps {
  results: EvaluationResult[];
}

export default function ResponseDisplay({ results }: ResponseDisplayProps) {
  if (results.length === 0) {
    return null;
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          Evaluation Results
        </h2>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          {results.length} model{results.length > 1 ? 's' : ''} evaluated
        </span>
      </div>

      {results.map((result, index) => (
        <div key={`${result.modelId}-${index}`} className="space-y-4">
          {/* Model Header */}
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                {result.modelId}
              </h3>
              {result.durationMs && (
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  Completed in {(result.durationMs / 1000).toFixed(2)}s
                </span>
              )}
            </div>
            <GovernanceDecisionBadge status={result.governanceDecision.status} />
          </div>

          {/* Model Response */}
          <div className="card p-6">
            <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
              Model Response
            </h4>
            <div className="prose dark:prose-invert max-w-none">
              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                {result.response}
              </p>
            </div>
          </div>

          {/* Metrics Dashboard */}
          <MetricsDashboard result={result} />

          {/* Divider between results */}
          {index < results.length - 1 && (
            <hr className="my-8 border-gray-300 dark:border-gray-700" />
          )}
        </div>
      ))}
    </div>
  );
}
