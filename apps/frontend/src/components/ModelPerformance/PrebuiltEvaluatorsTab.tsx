'use client';

import { EvaluationResult } from '@ai-evaluator/shared-types';
import MetricCard from '@/components/EvaluationMetrics/MetricCard';

interface PrebuiltEvaluatorsTabProps {
  result: EvaluationResult;
}

export default function PrebuiltEvaluatorsTab({ result }: PrebuiltEvaluatorsTabProps) {
  const { evaluations, governanceDecision } = result;

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-6">
        <div className="mb-6">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
            Built-in Evaluators
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Standard evaluation metrics for safety, relevance, coherence, and fluency
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <MetricCard
            name="Safety"
            evaluation={evaluations.safety}
            status={governanceDecision.metricDecisions?.safety}
          />
          <MetricCard
            name="Relevance"
            evaluation={evaluations.relevance}
            status={governanceDecision.metricDecisions?.relevance}
          />
          <MetricCard
            name="Coherence"
            evaluation={evaluations.coherence}
            status={governanceDecision.metricDecisions?.coherence}
          />
          <MetricCard
            name="Fluency"
            evaluation={evaluations.fluency}
            status={governanceDecision.metricDecisions?.fluency}
          />
        </div>
      </div>
    </div>
  );
}
