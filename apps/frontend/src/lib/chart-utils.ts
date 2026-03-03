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

// Transform evaluation results to radar chart format
export function transformToRadarData(results: EvaluationResult[]): RadarDataPoint[] {
  if (results.length === 0) return [];

  const metrics = [
    { key: 'safety', label: 'Safety' },
    { key: 'relevance', label: 'Relevance' },
    { key: 'coherence', label: 'Coherence' },
    { key: 'fluency', label: 'Fluency' },
  ];

  return metrics.map(({ key, label }) => {
    const dataPoint: RadarDataPoint = { metric: label };

    results.forEach((result) => {
      const evaluation = result.evaluations[key as keyof typeof result.evaluations];
      dataPoint[result.modelId] = Math.round(evaluation.score);
    });

    return dataPoint;
  });
}

// Transform evaluation results to bar chart format
export function transformToBarData(results: EvaluationResult[]): BarDataPoint[] {
  if (results.length === 0) return [];

  const metrics = [
    { key: 'safety', label: 'Safety' },
    { key: 'relevance', label: 'Relevance' },
    { key: 'coherence', label: 'Coherence' },
    { key: 'fluency', label: 'Fluency' },
  ];

  return metrics.map(({ key, label }) => {
    const dataPoint: BarDataPoint = { metric: label };

    results.forEach((result) => {
      const evaluation = result.evaluations[key as keyof typeof result.evaluations];
      dataPoint[result.modelId] = Math.round(evaluation.score);
    });

    return dataPoint;
  });
}

// Get model display names
export function getModelDisplayName(modelId: string): string {
  const parts = modelId.split('/');
  return parts[parts.length - 1];
}
