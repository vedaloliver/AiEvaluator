from pydantic import BaseModel, Field
from typing import Optional, Dict
from .governance import GovernanceDecision, MetricThreshold


class TokenUsage(BaseModel):
    """Token usage metrics for LLM calls."""
    prompt_tokens: int = Field(alias="promptTokens")
    completion_tokens: int = Field(alias="completionTokens")
    total_tokens: int = Field(alias="totalTokens")

    class Config:
        populate_by_name = True


class CostEstimate(BaseModel):
    """Cost estimation for LLM calls."""
    amount: float
    currency: str = "USD"
    model_pricing: str = Field(alias="modelPricing")

    class Config:
        populate_by_name = True


class EvaluationScore(BaseModel):
    """Score for a single evaluation metric"""
    score: float  # 0.0 - 1.0 for continuous, 1-5 for ordinal
    rationale: str
    severity: Optional[str] = None  # Only for safety (critical/high/medium/low)
    score_type: Optional[str] = Field(default=None, alias="scoreType")  # 'continuous' or 'ordinal'
    max_score: Optional[int] = Field(default=None, alias="maxScore")  # For ordinal (e.g., 5)

    class Config:
        populate_by_name = True


class EvaluationMetrics(BaseModel):
    """Metrics for all evaluation dimensions"""
    safety: EvaluationScore
    relevance: EvaluationScore
    coherence: EvaluationScore
    fluency: EvaluationScore

    # Custom FCA evaluators (optional for backward compatibility)
    disclaimer_compliance: Optional[EvaluationScore] = Field(default=None, alias="disclaimerCompliance")
    prohibited_language: Optional[EvaluationScore] = Field(default=None, alias="prohibitedLanguage")
    suitability_assessment: Optional[EvaluationScore] = Field(default=None, alias="suitabilityAssessment")
    risk_disclosure: Optional[EvaluationScore] = Field(default=None, alias="riskDisclosure")

    class Config:
        populate_by_name = True
        protected_namespaces = ()


class EvaluationResult(BaseModel):
    """Complete evaluation result"""
    model_id: str = Field(alias="modelId")
    query: str
    response: str
    evaluations: EvaluationMetrics
    governance_decision: GovernanceDecision = Field(alias="governanceDecision")
    timestamp: str  # ISO 8601 format
    duration_ms: Optional[int] = Field(default=None, alias="durationMs")

    # Observability fields
    trace_id: Optional[str] = Field(default=None, alias="traceId")
    span_id: Optional[str] = Field(default=None, alias="spanId")
    token_usage: Optional[TokenUsage] = Field(default=None, alias="tokenUsage")
    cost_estimate: Optional[CostEstimate] = Field(default=None, alias="costEstimate")

    class Config:
        populate_by_name = True
        protected_namespaces = ()


class ThresholdOverride(BaseModel):
    """Partial threshold override structure"""
    safety: Optional[MetricThreshold] = None
    relevance: Optional[MetricThreshold] = None
    coherence: Optional[MetricThreshold] = None
    fluency: Optional[MetricThreshold] = None

    # Custom FCA evaluator thresholds (optional)
    disclaimer_compliance: Optional[MetricThreshold] = Field(default=None, alias="disclaimerCompliance")
    prohibited_language: Optional[MetricThreshold] = Field(default=None, alias="prohibitedLanguage")
    suitability_assessment: Optional[MetricThreshold] = Field(default=None, alias="suitabilityAssessment")
    risk_disclosure: Optional[MetricThreshold] = Field(default=None, alias="riskDisclosure")


class EvaluationRequest(BaseModel):
    """Request to evaluate a single model"""
    scenario_id: str = Field(alias="scenarioId")
    model_id: str = Field(alias="modelId")
    query: str
    thresholds: Optional[ThresholdOverride] = None

    class Config:
        populate_by_name = True
        protected_namespaces = ()


class MultiModelEvaluationRequest(BaseModel):
    """Request to evaluate multiple models"""
    scenario_id: str = Field(alias="scenarioId")
    model_ids: list[str] = Field(alias="modelIds")
    query: str
    thresholds: Optional[ThresholdOverride] = None

    class Config:
        populate_by_name = True
        protected_namespaces = ()


class MultiModelEvaluationResponse(BaseModel):
    """Response for multi-model evaluation"""
    results: list[EvaluationResult]
    timestamp: str  # ISO 8601 format
