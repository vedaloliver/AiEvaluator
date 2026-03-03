from pydantic import BaseModel, Field
from typing import Optional, Dict
from .governance import GovernanceDecision, MetricThreshold


class EvaluationScore(BaseModel):
    """Score for a single evaluation metric"""
    score: float  # 0.0 - 1.0
    rationale: str
    severity: Optional[str] = None  # Only for safety (critical/high/medium/low)


class EvaluationMetrics(BaseModel):
    """Metrics for all evaluation dimensions"""
    safety: EvaluationScore
    relevance: EvaluationScore
    coherence: EvaluationScore
    fluency: EvaluationScore


class EvaluationResult(BaseModel):
    """Complete evaluation result"""
    model_id: str = Field(alias="modelId")
    query: str
    response: str
    evaluations: EvaluationMetrics
    governance_decision: GovernanceDecision = Field(alias="governanceDecision")
    timestamp: str  # ISO 8601 format
    duration_ms: Optional[int] = Field(default=None, alias="durationMs")

    class Config:
        populate_by_name = True
        protected_namespaces = ()


class ThresholdOverride(BaseModel):
    """Partial threshold override structure"""
    safety: Optional[MetricThreshold] = None
    relevance: Optional[MetricThreshold] = None
    coherence: Optional[MetricThreshold] = None
    fluency: Optional[MetricThreshold] = None


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
