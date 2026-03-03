'use client';

import { EvaluationResult } from '@ai-evaluator/shared-types';
import MetricCard from './MetricCard';
import GovernanceDecisionBadge from './GovernanceDecisionBadge';

interface MetricsDashboardProps {
  result: EvaluationResult;
}

export default function MetricsDashboard({ result }: MetricsDashboardProps) {
  const { evaluations, governanceDecision } = result;

  return (
    <div className="space-y-4">
      {/* Overall Governance Decision */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white">
            Governance Decision
          </h3>
          <GovernanceDecisionBadge status={governanceDecision.status} size="lg" />
        </div>

        {/* Reasons */}
        <div className="space-y-2">
          <h4 className="font-semibold text-gray-700 dark:text-gray-300">
            Decision Reasons:
          </h4>
          <ul className="list-disc list-inside space-y-1">
            {governanceDecision.reasons.map((reason, index) => (
              <li key={index} className="text-sm text-gray-600 dark:text-gray-400">
                {reason}
              </li>
            ))}
          </ul>
        </div>

        {/* Critical Flags */}
        {governanceDecision.criticalFlags.length > 0 && (
          <div className="mt-4 p-3 bg-fail-light rounded-lg">
            <h4 className="font-semibold text-fail-dark mb-2">
              Critical Flags Detected:
            </h4>
            <ul className="list-disc list-inside space-y-1">
              {governanceDecision.criticalFlags.map((flag, index) => (
                <li key={index} className="text-sm text-fail-dark">
                  {flag}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Individual Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {governanceDecision.metricDecisions && (
          <>
            <MetricCard
              name="Safety"
              evaluation={evaluations.safety}
              status={governanceDecision.metricDecisions.safety}
            />
            <MetricCard
              name="Relevance"
              evaluation={evaluations.relevance}
              status={governanceDecision.metricDecisions.relevance}
            />
            <MetricCard
              name="Coherence"
              evaluation={evaluations.coherence}
              status={governanceDecision.metricDecisions.coherence}
            />
            <MetricCard
              name="Fluency"
              evaluation={evaluations.fluency}
              status={governanceDecision.metricDecisions.fluency}
            />
          </>
        )}
      </div>
    </div>
  );
}
