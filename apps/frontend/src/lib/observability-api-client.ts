/**
 * API Client for Observability Service
 */

import {
  EvaluationRun,
  AdversarialRun,
  AnalyticsSummary,
  TrendData,
  Trace,
  FlowVisualization,
  RunFilters,
  TrendFilters,
} from '@/types/observability';

const OBSERVABILITY_URL = process.env.NEXT_PUBLIC_OBSERVABILITY_URL || 'http://localhost:8003';

export class ObservabilityApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = OBSERVABILITY_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Get evaluation runs with filters
   */
  async getEvaluationRuns(filters: RunFilters = {}): Promise<EvaluationRun[]> {
    const params = new URLSearchParams();
    if (filters.modelId) params.append('modelId', filters.modelId);
    if (filters.scenarioId) params.append('scenarioId', filters.scenarioId);
    if (filters.startDate) params.append('startDate', filters.startDate);
    if (filters.endDate) params.append('endDate', filters.endDate);
    if (filters.limit) params.append('limit', filters.limit.toString());
    if (filters.offset) params.append('offset', filters.offset.toString());

    const response = await fetch(`${this.baseUrl}/api/v1/analytics/evaluation-runs?${params}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch evaluation runs: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get a specific evaluation run by ID
   */
  async getEvaluationRun(runId: number): Promise<EvaluationRun> {
    const response = await fetch(`${this.baseUrl}/api/v1/analytics/evaluation-runs/${runId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch evaluation run: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get adversarial runs with filters
   */
  async getAdversarialRuns(filters: RunFilters = {}): Promise<AdversarialRun[]> {
    const params = new URLSearchParams();
    if (filters.modelId) params.append('modelId', filters.modelId);
    if (filters.scenarioId) params.append('scenarioId', filters.scenarioId);
    if (filters.startDate) params.append('startDate', filters.startDate);
    if (filters.endDate) params.append('endDate', filters.endDate);
    if (filters.limit) params.append('limit', filters.limit.toString());
    if (filters.offset) params.append('offset', filters.offset.toString());

    const response = await fetch(`${this.baseUrl}/api/v1/analytics/adversarial-runs?${params}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch adversarial runs: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get a specific adversarial run by ID
   */
  async getAdversarialRun(runId: number): Promise<AdversarialRun> {
    const response = await fetch(`${this.baseUrl}/api/v1/analytics/adversarial-runs/${runId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch adversarial run: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get analytics summary
   */
  async getAnalyticsSummary(filters: {
    startDate?: string;
    endDate?: string;
    modelId?: string;
  } = {}): Promise<AnalyticsSummary> {
    const params = new URLSearchParams();
    if (filters.startDate) params.append('startDate', filters.startDate);
    if (filters.endDate) params.append('endDate', filters.endDate);
    if (filters.modelId) params.append('modelId', filters.modelId);

    const response = await fetch(`${this.baseUrl}/api/v1/analytics/summary?${params}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch analytics summary: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get trace by ID
   */
  async getTrace(traceId: string): Promise<Trace> {
    const response = await fetch(`${this.baseUrl}/api/v1/traces/${traceId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch trace: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get trace flow visualization data
   */
  async getTraceFlow(traceId: string): Promise<FlowVisualization> {
    const response = await fetch(`${this.baseUrl}/api/v1/traces/${traceId}/flow`);
    if (!response.ok) {
      throw new Error(`Failed to fetch trace flow: ${response.statusText}`);
    }
    return response.json();
  }
}

// Export singleton instance
export const observabilityApiClient = new ObservabilityApiClient();
