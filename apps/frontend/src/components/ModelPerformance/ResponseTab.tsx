'use client';

import { EvaluationResult } from '@ai-evaluator/shared-types';
import GovernanceDecisionBadge from '@/components/EvaluationMetrics/GovernanceDecisionBadge';

interface ResponseTabProps {
  result: EvaluationResult;
}

export default function ResponseTab({ result }: ResponseTabProps) {
  const { response, governanceDecision, query } = result;

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-6 space-y-6">
        {/* Query Section */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
            <span>❓</span>
            Query
          </h3>
          <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
            {query}
          </p>
        </div>

        {/* Response Section */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
            <span>💬</span>
            Model Response
          </h3>
          <div className="prose dark:prose-invert max-w-none">
            <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
              {response}
            </p>
          </div>
        </div>

        {/* Governance Decision Section */}
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
              <span>⚖️</span>
              Governance Decision
            </h3>
            <GovernanceDecisionBadge status={governanceDecision.status} size="lg" />
          </div>

          {/* Decision Reasons */}
          <div className="space-y-2 mb-4">
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
            <div className="p-4 bg-fail-light rounded-lg">
              <h4 className="font-semibold text-fail-dark mb-2 flex items-center gap-2">
                <span>⚠️</span>
                Critical Flags Detected
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
      </div>
    </div>
  );
}
