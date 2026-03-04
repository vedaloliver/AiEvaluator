import { GovernanceDecision } from './governance';

export interface EvaluationScore {
  score: number;
  rationale: string;
  severity?: string;
  scoreType?: 'continuous' | 'ordinal';
  maxScore?: number;
}

export interface EvaluationMetrics {
  safety: EvaluationScore;
  relevance: EvaluationScore;
  coherence: EvaluationScore;
  fluency: EvaluationScore;

  // Custom FCA evaluators (optional for backward compatibility)
  disclaimerCompliance?: EvaluationScore;
  prohibitedLanguage?: EvaluationScore;
  suitabilityAssessment?: EvaluationScore;
  riskDisclosure?: EvaluationScore;
}

export interface EvaluationResult {
  modelId: string;
  query: string;
  response: string;
  evaluations: EvaluationMetrics;
  governanceDecision: GovernanceDecision;
  timestamp: string;
  durationMs?: number;
}

export interface EvaluationRequest {
  scenarioId: string;
  modelId: string;
  query: string;
  thresholds?: Partial<{
    safety: { pass: number; warn: number };
    relevance: { pass: number; warn: number };
    coherence: { pass: number; warn: number };
    fluency: { pass: number; warn: number };
    disclaimerCompliance: { pass: number; warn: number };
    prohibitedLanguage: { pass: number; warn: number };
    suitabilityAssessment: { pass: number; warn: number };
    riskDisclosure: { pass: number; warn: number };
  }>;
}

export interface MultiModelEvaluationRequest {
  scenarioId: string;
  modelIds: string[];
  query: string;
  thresholds?: Partial<{
    safety: { pass: number; warn: number };
    relevance: { pass: number; warn: number };
    coherence: { pass: number; warn: number };
    fluency: { pass: number; warn: number };
    disclaimerCompliance: { pass: number; warn: number };
    prohibitedLanguage: { pass: number; warn: number };
    suitabilityAssessment: { pass: number; warn: number };
    riskDisclosure: { pass: number; warn: number };
  }>;
}

export interface MultiModelEvaluationResponse {
  results: EvaluationResult[];
  timestamp: string;
}
