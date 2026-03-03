'use client';

import { EvaluationResult } from '@ai-evaluator/shared-types';
import { getModelDisplayName } from '@/lib/chart-utils';

interface ModelResultCardProps {
  result: EvaluationResult;
  index: number;
}

export default function ModelResultCard({ result, index }: ModelResultCardProps) {
  const metrics = [
    { label: 'Safety', value: result.evaluations.safety.score, key: 'safety' },
    { label: 'Relevance', value: result.evaluations.relevance.score, key: 'relevance' },
    { label: 'Coherence', value: result.evaluations.coherence.score, key: 'coherence' },
    { label: 'Fluency', value: result.evaluations.fluency.score, key: 'fluency' },
  ];

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-pass dark:text-pass';
    if (score >= 60) return 'text-warn dark:text-warn';
    return 'text-fail dark:text-fail';
  };

  const getDecisionColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'pass':
        return 'bg-pass-light text-pass-dark border-pass';
      case 'warn':
        return 'bg-warn-light text-warn-dark border-warn';
      case 'fail':
        return 'bg-fail-light text-fail-dark border-fail';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div
      className="glass-card p-3 animate-slide-in"
      style={{ animationDelay: `${index * 100}ms` }}
    >
      {/* Model Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-semibold text-gray-900 dark:text-white text-sm">
            {getModelDisplayName(result.modelId)}
          </h3>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
            {result.modelId}
          </p>
        </div>
        <div
          className={`px-3 py-1 rounded-full text-xs font-semibold border ${getDecisionColor(
            result.governanceDecision.status
          )}`}
        >
          {result.governanceDecision.status}
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        {metrics.map((metric) => (
          <div
            key={metric.key}
            className="bg-white/5 dark:bg-black/20 rounded-lg p-2 border border-white/10"
          >
            <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">
              {metric.label}
            </div>
            <div className={`text-lg font-bold ${getScoreColor(metric.value)}`}>
              {Math.round(metric.value)}
            </div>
          </div>
        ))}
      </div>

      {/* Response Preview */}
      <div className="bg-white/5 dark:bg-black/20 rounded-lg p-3 border border-white/10">
        <div className="text-xs text-gray-500 dark:text-gray-400 mb-2">Response</div>
        <p className="text-xs text-gray-700 dark:text-gray-300 line-clamp-3">
          {result.response}
        </p>
      </div>

      {/* Reasons */}
      {result.governanceDecision.reasons && result.governanceDecision.reasons.length > 0 && (
        <div className="mt-3 pt-3 border-t border-white/10">
          <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Reasons</div>
          <ul className="text-xs text-gray-600 dark:text-gray-400 list-disc list-inside space-y-0.5">
            {result.governanceDecision.reasons.map((reason, idx) => (
              <li key={idx}>{reason}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
