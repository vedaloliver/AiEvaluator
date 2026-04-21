"""Response models for API endpoints."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class TraceResponse(BaseModel):
    """Response model for trace data."""
    trace_id: str = Field(..., alias="traceId")
    start_time: datetime = Field(..., alias="startTime")
    end_time: Optional[datetime] = Field(None, alias="endTime")
    root_span_id: Optional[str] = Field(None, alias="rootSpanId")
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True


class SpanResponse(BaseModel):
    """Response model for span data."""
    span_id: str = Field(..., alias="spanId")
    trace_id: str = Field(..., alias="traceId")
    parent_span_id: Optional[str] = Field(None, alias="parentSpanId")
    name: str
    span_type: str = Field(..., alias="spanType")
    start_time: datetime = Field(..., alias="startTime")
    duration_ms: Optional[int] = Field(None, alias="durationMs")
    attributes: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class EvaluationRunResponse(BaseModel):
    """Response model for evaluation run data."""
    id: int
    trace_id: Optional[str] = Field(None, alias="traceId")
    model_id: str = Field(..., alias="modelId")
    scenario_id: str = Field(..., alias="scenarioId")
    query: str
    response: str
    evaluations: Dict[str, Any]
    governance_decision: Dict[str, Any] = Field(..., alias="governanceDecision")
    duration_ms: int = Field(..., alias="durationMs")
    prompt_tokens: Optional[int] = Field(None, alias="promptTokens")
    completion_tokens: Optional[int] = Field(None, alias="completionTokens")
    total_tokens: Optional[int] = Field(None, alias="totalTokens")
    estimated_cost: Optional[float] = Field(None, alias="estimatedCost")
    cost_currency: str = Field(..., alias="costCurrency")
    timestamp: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class AdversarialRunResponse(BaseModel):
    """Response model for adversarial run data."""
    id: int
    trace_id: Optional[str] = Field(None, alias="traceId")
    scenario_id: str = Field(..., alias="scenarioId")
    model_id: str = Field(..., alias="modelId")
    total_attacks: int = Field(..., alias="totalAttacks")
    successful_attacks: int = Field(..., alias="successfulAttacks")
    blocked_attacks: int = Field(..., alias="blockedAttacks")
    attack_success_rate: float = Field(..., alias="attackSuccessRate")
    vulnerabilities: List[Dict[str, Any]]
    all_results: List[Dict[str, Any]] = Field(..., alias="allResults")
    timestamp: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class AnalyticsSummaryResponse(BaseModel):
    """Response model for analytics summary."""
    evaluation_runs: Dict[str, Any] = Field(..., alias="evaluationRuns")
    adversarial_runs: Dict[str, Any] = Field(..., alias="adversarialRuns")


class TrendDataResponse(BaseModel):
    """Response model for trend data."""
    timestamp: datetime
    value: float
    label: str
