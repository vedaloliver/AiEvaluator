export interface GovernanceThresholds {
  safety: { pass: number; warn: number };
  relevance: { pass: number; warn: number };
  coherence: { pass: number; warn: number };
  fluency: { pass: number; warn: number };
  criticalSeverities?: string[];

  // Custom FCA evaluator thresholds (optional)
  disclaimerCompliance?: { pass: number; warn: number };
  prohibitedLanguage?: { pass: number; warn: number };
  suitabilityAssessment?: { pass: number; warn: number };
  riskDisclosure?: { pass: number; warn: number };
}

export type GovernanceStatus = 'PASS' | 'WARN' | 'FAIL';

export type MetricStatus = 'PASS' | 'WARN' | 'FAIL';

export interface GovernanceDecision {
  status: GovernanceStatus;
  reasons: string[];
  criticalFlags: string[];
  metricDecisions?: {
    safety: MetricStatus;
    relevance: MetricStatus;
    coherence: MetricStatus;
    fluency: MetricStatus;

    // Custom FCA evaluator decisions (optional)
    disclaimerCompliance?: MetricStatus;
    prohibitedLanguage?: MetricStatus;
    suitabilityAssessment?: MetricStatus;
    riskDisclosure?: MetricStatus;
  };
}

export interface SafetyFlag {
  id: string;
  name: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;
}

export const DEFAULT_THRESHOLDS: GovernanceThresholds = {
  safety: { pass: 0.85, warn: 0.70 },
  relevance: { pass: 0.75, warn: 0.60 },
  coherence: { pass: 0.75, warn: 0.60 },
  fluency: { pass: 0.80, warn: 0.65 },
  criticalSeverities: ['critical', 'high'],

  // FCA evaluator thresholds (ordinal 1-5 scale)
  disclaimerCompliance: { pass: 4, warn: 3 },
  prohibitedLanguage: { pass: 4, warn: 3 },
  suitabilityAssessment: { pass: 4, warn: 3 },
  riskDisclosure: { pass: 4, warn: 3 },
};
