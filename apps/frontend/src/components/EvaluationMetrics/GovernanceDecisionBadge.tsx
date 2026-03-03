'use client';

import { GovernanceStatus } from '@ai-evaluator/shared-types';
import clsx from 'clsx';

interface GovernanceDecisionBadgeProps {
  status: GovernanceStatus;
  size?: 'sm' | 'md' | 'lg';
}

export default function GovernanceDecisionBadge({
  status,
  size = 'md',
}: GovernanceDecisionBadgeProps) {
  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1',
    lg: 'text-base px-4 py-2',
  };

  const statusConfig = {
    PASS: {
      bgColor: 'bg-pass-light',
      textColor: 'text-pass-dark',
      borderColor: 'border-pass',
      icon: '✓',
      label: 'PASS',
    },
    WARN: {
      bgColor: 'bg-warn-light',
      textColor: 'text-warn-dark',
      borderColor: 'border-warn',
      icon: '⚠',
      label: 'WARN',
    },
    FAIL: {
      bgColor: 'bg-fail-light',
      textColor: 'text-fail-dark',
      borderColor: 'border-fail',
      icon: '✗',
      label: 'FAIL',
    },
  };

  const config = statusConfig[status];

  return (
    <span
      className={clsx(
        'inline-flex items-center gap-1 rounded-full font-semibold border-2',
        config.bgColor,
        config.textColor,
        config.borderColor,
        sizeClasses[size]
      )}
    >
      <span>{config.icon}</span>
      <span>{config.label}</span>
    </span>
  );
}
