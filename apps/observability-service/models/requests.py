"""Request models for API endpoints."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class TraceCreateRequest(BaseModel):
    """Request model for creating a trace."""
    trace_id: str = Field(..., alias="traceId")
    start_time: Optional[datetime] = Field(None, alias="startTime")


class TraceUpdateRequest(BaseModel):
    """Request model for updating a trace."""
    end_time: Optional[datetime] = Field(None, alias="endTime")
    status: Optional[str] = None
    root_span_id: Optional[str] = Field(None, alias="rootSpanId")


class SpanCreateRequest(BaseModel):
    """Request model for creating a span."""
    span_id: str = Field(..., alias="spanId")
    trace_id: str = Field(..., alias="traceId")
    parent_span_id: Optional[str] = Field(None, alias="parentSpanId")
    name: str
    span_type: str = Field(..., alias="spanType")
    start_time: Optional[datetime] = Field(None, alias="startTime")
    duration_ms: Optional[int] = Field(None, alias="durationMs")
    attributes: Optional[Dict[str, Any]] = None


class EvaluationRunRequest(BaseModel):
    """Request model for storing an evaluation run."""
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
    cost_currency: Optional[str] = Field("USD", alias="costCurrency")
    timestamp: Optional[datetime] = None


class AdversarialRunRequest(BaseModel):
    """Request model for storing an adversarial run."""
    trace_id: Optional[str] = Field(None, alias="traceId")
    scenario_id: str = Field(..., alias="scenarioId")
    model_id: str = Field(..., alias="modelId")
    total_attacks: int = Field(..., alias="totalAttacks")
    successful_attacks: int = Field(..., alias="successfulAttacks")
    blocked_attacks: int = Field(..., alias="blockedAttacks")
    attack_success_rate: float = Field(..., alias="attackSuccessRate")
    vulnerabilities: List[Dict[str, Any]]
    all_results: List[Dict[str, Any]] = Field(..., alias="allResults")
    timestamp: Optional[datetime] = None
