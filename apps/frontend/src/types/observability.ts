/**
 * TypeScript types for Observability data
 */

export interface Trace {
  traceId: string;
  startTime: string;
  endTime?: string;
  rootSpanId?: string;
  status: 'in_progress' | 'completed' | 'error';
}

export interface Span {
  spanId: string;
  traceId: string;
  parentSpanId?: string;
  name: string;
  spanType: 'llm_call' | 'evaluation' | 'retrieval' | 'reasoning' | 'adversarial_test';
  startTime: string;
  durationMs?: number;
  attributes?: Record<string, any>;
}

export interface TokenUsage {
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
}

export interface CostEstimate {
  amount: number;
  currency: string;
  modelPricing: string;
}

export interface EvaluationRun {
  id: number;
  traceId?: string;
  modelId: string;
  scenarioId: string;
  query: string;
  response: string;
  evaluations: Record<string, any>;
  governanceDecision: Record<string, any>;
  durationMs: number;
  promptTokens?: number;
  completionTokens?: number;
  totalTokens?: number;
  estimatedCost?: number;
  costCurrency: string;
  timestamp: string;
}

export interface AdversarialRun {
  id: number;
  traceId?: string;
  scenarioId: string;
  modelId: string;
  totalAttacks: number;
  successfulAttacks: number;
  blockedAttacks: number;
  attackSuccessRate: number;
  vulnerabilities: any[];
  allResults: any[];
  timestamp: string;
}

export interface AnalyticsSummary {
  evaluationRuns: {
    totalRuns: number;
    avgLatencyMs: number;
    totalCost: number;
    totalTokens: number;
  };
  adversarialRuns: {
    totalSuites: number;
    avgAttackSuccessRate: number;
  };
}

export interface TrendData {
  timestamp: string;
  value: number;
  label: string;
}

export interface FlowVisualization {
  traceId: string;
  startTime: string;
  endTime?: string;
  status: string;
  rootSpans: SpanNode[];
  totalSpans: number;
}

export interface SpanNode extends Span {
  children: SpanNode[];
}

export interface RunFilters {
  modelId?: string;
  scenarioId?: string;
  startDate?: string;
  endDate?: string;
  limit?: number;
  offset?: number;
}

export interface TrendFilters {
  startDate?: string;
  endDate?: string;
  modelId?: string;
  groupBy?: 'hour' | 'day' | 'week';
}
