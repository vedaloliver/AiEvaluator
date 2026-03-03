'use client';

import { EvaluationScore, MetricStatus } from '@ai-evaluator/shared-types';
import clsx from 'clsx';

interface MetricCardProps {
  name: string;
  evaluation: EvaluationScore;
  status: MetricStatus;
}

export default function MetricCard({ name, evaluation, status }: MetricCardProps) {
  const statusConfig = {
    PASS: {
      bgColor: 'bg-pass-light',
      borderColor: 'border-pass',
      textColor: 'text-pass-dark',
    },
    WARN: {
      bgColor: 'bg-warn-light',
      borderColor: 'border-warn',
      textColor: 'text-warn-dark',
    },
    FAIL: {
      bgColor: 'bg-fail-light',
      borderColor: 'border-fail',
      textColor: 'text-fail-dark',
    },
  };

  const config = statusConfig[status];
  const scorePercentage = Math.round(evaluation.score * 100);

  return (
    <div className={clsx('card p-4 border-l-4', config.borderColor)}>
      <div className="flex justify-between items-start mb-2">
        <h4 className="font-semibold text-gray-900 dark:text-white capitalize">
          {name}
        </h4>
        <span
          className={clsx(
            'text-2xl font-bold',
            config.textColor
          )}
        >
          {scorePercentage}%
        </span>
      </div>

      {/* Score bar */}
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-3">
        <div
          className={clsx('h-2 rounded-full transition-all duration-500', {
            'bg-pass': status === 'PASS',
            'bg-warn': status === 'WARN',
            'bg-fail': status === 'FAIL',
          })}
          style={{ width: `${scorePercentage}%` }}
        />
      </div>

      {/* Status badge */}
      <div className="mb-2">
        <span
          className={clsx(
            'badge text-xs',
            config.bgColor,
            config.textColor
          )}
        >
          {status}
        </span>
      </div>

      {/* Rationale */}
      <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
        {evaluation.rationale}
      </p>

      {/* Severity (for safety metric) */}
      {evaluation.severity && (
        <div className="mt-2">
          <span className="text-xs font-medium text-gray-500 dark:text-gray-400">
            Severity: <span className="uppercase">{evaluation.severity}</span>
          </span>
        </div>
      )}
    </div>
  );
}
