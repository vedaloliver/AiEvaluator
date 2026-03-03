import { GovernanceThresholds, DEFAULT_THRESHOLDS } from '@ai-evaluator/shared-types';

export function getEffectiveThresholds(
  customThresholds?: Partial<GovernanceThresholds>
): GovernanceThresholds {
  if (!customThresholds) {
    return DEFAULT_THRESHOLDS;
  }

  return {
    safety: customThresholds.safety || DEFAULT_THRESHOLDS.safety,
    relevance: customThresholds.relevance || DEFAULT_THRESHOLDS.relevance,
    coherence: customThresholds.coherence || DEFAULT_THRESHOLDS.coherence,
    fluency: customThresholds.fluency || DEFAULT_THRESHOLDS.fluency,
    criticalSeverities: customThresholds.criticalSeverities || DEFAULT_THRESHOLDS.criticalSeverities,
  };
}

export { DEFAULT_THRESHOLDS };
