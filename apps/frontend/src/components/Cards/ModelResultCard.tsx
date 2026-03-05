'use client';

import { useState } from 'react';
import { EvaluationResult } from '@ai-evaluator/shared-types';
import { getModelDisplayName } from '@/lib/chart-utils';

interface ModelResultCardProps {
  result: EvaluationResult;
  index: number;
}

export default function ModelResultCard({ result, index }: ModelResultCardProps) {
  const [responseExpanded, setResponseExpanded] = useState(false);
  const [reasonsExpanded, setReasonsExpanded] = useState(false);
  const builtInMetrics = [
    { label: 'Safety', value: result.evaluations.safety.score, key: 'safety', evaluation: result.evaluations.safety },
    { label: 'Relevance', value: result.evaluations.relevance.score, key: 'relevance', evaluation: result.evaluations.relevance },
    { label: 'Coherence', value: result.evaluations.coherence.score, key: 'coherence', evaluation: result.evaluations.coherence },
    { label: 'Fluency', value: result.evaluations.fluency.score, key: 'fluency', evaluation: result.evaluations.fluency },
  ];

  const customMetrics = [
    { label: 'Disclaimer', evaluation: result.evaluations.disclaimerCompliance, key: 'disclaimerCompliance' },
    { label: 'Language', evaluation: result.evaluations.prohibitedLanguage, key: 'prohibitedLanguage' },
    { label: 'Suitability', evaluation: result.evaluations.suitabilityAssessment, key: 'suitabilityAssessment' },
    { label: 'Risk', evaluation: result.evaluations.riskDisclosure, key: 'riskDisclosure' },
  ].filter(m => m.evaluation); // Only include if present

  const normalizeScore = (evaluation: any) => {
    if (!evaluation) return 0;
    if (evaluation.scoreType === 'ordinal' && evaluation.maxScore) {
      return Math.round((evaluation.score / evaluation.maxScore) * 100);
    }
    return Math.round(evaluation.score * 100);
  };

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
        <h3 className="font-semibold text-gray-900 dark:text-white text-sm">
          {getModelDisplayName(result.modelId)}
        </h3>
        <div
          className={`px-3 py-1 rounded-full text-xs font-semibold border ${getDecisionColor(
            result.governanceDecision.status
          )}`}
        >
          {result.governanceDecision.status}
        </div>
      </div>

      {/* Built-in Metrics */}
      <div className="mb-4">
        <h4 className="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-2">
          Built-in Metrics
        </h4>
        <div className="grid grid-cols-2 gap-3">
          {builtInMetrics.map((metric) => (
            <div
              key={metric.key}
              className="bg-white/5 dark:bg-black/20 rounded-lg p-2 border border-white/10"
            >
              <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">
                {metric.label}
              </div>
              <div className={`text-lg font-bold ${getScoreColor(Math.round(metric.value * 100))}`}>
                {Math.round(metric.value * 100)}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Custom FCA Metrics */}
      {customMetrics.length > 0 && (
        <div className="mb-4">
          <h4 className="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-2">
            Custom FCA Metrics
          </h4>
          <div className="grid grid-cols-2 gap-3">
            {customMetrics.map((metric) => {
              const normalized = normalizeScore(metric.evaluation);
              const displayScore = metric.evaluation.scoreType === 'ordinal'
                ? `${metric.evaluation.score}/${metric.evaluation.maxScore}`
                : `${normalized}%`;
              return (
                <div
                  key={metric.key}
                  className="bg-white/5 dark:bg-black/20 rounded-lg p-2 border border-white/10"
                >
                  <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">
                    {metric.label}
                  </div>
                  <div className={`text-lg font-bold ${getScoreColor(normalized)}`}>
                    {displayScore}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Response Accordion */}
      <div className="mt-3 pt-3 border-t border-white/10">
        <button
          onClick={() => setResponseExpanded(!responseExpanded)}
          className="w-full flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
        >
          <span className="font-medium">Response</span>
          <span className="transform transition-transform duration-200" style={{ transform: responseExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}>
            ▼
          </span>
        </button>
        {responseExpanded && (
          <div className="mt-2 text-xs text-gray-600 dark:text-gray-400 whitespace-pre-wrap">
            {result.response}
          </div>
        )}
      </div>

      {/* Reasons Accordion */}
      {result.governanceDecision.reasons && result.governanceDecision.reasons.length > 0 && (
        <div className="mt-3 pt-3 border-t border-white/10">
          <button
            onClick={() => setReasonsExpanded(!reasonsExpanded)}
            className="w-full flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
          >
            <span className="font-medium">Reasons</span>
            <span className="transform transition-transform duration-200" style={{ transform: reasonsExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}>
              ▼
            </span>
          </button>
          {reasonsExpanded && (
            <ul className="mt-2 text-xs text-gray-600 dark:text-gray-400 list-disc list-inside space-y-0.5">
              {result.governanceDecision.reasons.map((reason, idx) => (
                <li key={idx}>{reason}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
