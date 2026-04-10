'use client';

import { EvaluationResult } from '@ai-evaluator/shared-types';
import MetricsDashboard from '@/components/EvaluationMetrics/MetricsDashboard';

interface ModelDetailsTabProps {
  result: EvaluationResult;
}

export default function ModelDetailsTab({ result }: ModelDetailsTabProps) {
  return (
    <div className="h-full overflow-y-auto">
      <div className="p-6">
        {/* Model Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            {result.modelId}
          </h2>
          {result.durationMs && (
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Evaluation completed in {(result.durationMs / 1000).toFixed(2)} seconds
            </p>
          )}
        </div>

        {/* Overall Metrics Dashboard */}
        <MetricsDashboard result={result} />
      </div>
    </div>
  );
}
