import { EvaluationResult } from '@ai-evaluator/shared-types';

export interface RadarDataPoint {
  metric: string;
  [key: string]: string | number;
}

export interface BarDataPoint {
  metric: string;
  [key: string]: string | number;
}

// Model color palette
export const MODEL_COLORS = [
  '#8b5cf6', // Purple
  '#ec4899', // Pink
  '#3b82f6', // Blue
  '#06b6d4', // Cyan
  '#10b981', // Green
  '#f59e0b', // Amber
  '#ef4444', // Red
  '#6366f1', // Indigo
];

export function getModelColor(index: number): string {
  return MODEL_COLORS[index % MODEL_COLORS.length];
}

// Helper function to normalize scores to 0-100 scale
function normalizeScore(evaluation: any): number {
  if (evaluation.scoreType === 'ordinal' && evaluation.maxScore) {
    // Ordinal: convert X/5 to percentage
    return Math.round((evaluation.score / evaluation.maxScore) * 100);
  }
  // Continuous: already 0-1, convert to percentage
  return Math.round(evaluation.score * 100);
}

// Transform evaluation results to radar chart format
export function transformToRadarData(results: EvaluationResult[]): RadarDataPoint[] {
  if (results.length === 0) return [];

  const metrics = [
    { key: 'safety', label: 'Safety' },
    { key: 'relevance', label: 'Relevance' },
    { key: 'coherence', label: 'Coherence' },
    { key: 'fluency', label: 'Fluency' },
    { key: 'disclaimerCompliance', label: 'Disclaimer' },
    { key: 'prohibitedLanguage', label: 'Language' },
    { key: 'suitabilityAssessment', label: 'Suitability' },
    { key: 'riskDisclosure', label: 'Risk' },
  ];

  return metrics.map(({ key, label }) => {
    const dataPoint: RadarDataPoint = { metric: label };

    results.forEach((result) => {
      const evaluation = result.evaluations[key as keyof typeof result.evaluations];
      if (evaluation) {
        dataPoint[result.modelId] = normalizeScore(evaluation);
      }
    });

    return dataPoint;
  }).filter(dataPoint => Object.keys(dataPoint).length > 1); // Filter out metrics with no data
}

// Transform evaluation results to bar chart format
export function transformToBarData(results: EvaluationResult[]): BarDataPoint[] {
  if (results.length === 0) return [];

  const metrics = [
    { key: 'safety', label: 'Safety' },
    { key: 'relevance', label: 'Relevance' },
    { key: 'coherence', label: 'Coherence' },
    { key: 'fluency', label: 'Fluency' },
    { key: 'disclaimerCompliance', label: 'Disclaimer' },
    { key: 'prohibitedLanguage', label: 'Language' },
    { key: 'suitabilityAssessment', label: 'Suitability' },
    { key: 'riskDisclosure', label: 'Risk' },
  ];

  return metrics.map(({ key, label }) => {
    const dataPoint: BarDataPoint = { metric: label };

    results.forEach((result) => {
      const evaluation = result.evaluations[key as keyof typeof result.evaluations];
      if (evaluation) {
        dataPoint[result.modelId] = normalizeScore(evaluation);
      }
    });

    return dataPoint;
  }).filter(dataPoint => Object.keys(dataPoint).length > 1); // Filter out metrics with no data
}

// Get model display names
export function getModelDisplayName(modelId: string): string {
  const parts = modelId.split('/');
  return parts[parts.length - 1];
}
