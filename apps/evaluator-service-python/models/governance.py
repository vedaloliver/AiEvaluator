from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict


class MetricThreshold(BaseModel):
    """Threshold for a single metric"""
    pass_threshold: float = Field(alias="pass")
    warn: float


class GovernanceThresholds(BaseModel):
    """Thresholds for all governance metrics"""
    safety: MetricThreshold
    relevance: MetricThreshold
    coherence: MetricThreshold
    fluency: MetricThreshold
    critical_severities: Optional[list[str]] = Field(default=None, alias="criticalSeverities")

    class Config:
        populate_by_name = True


GovernanceStatus = Literal["PASS", "WARN", "FAIL"]
MetricStatus = Literal["PASS", "WARN", "FAIL"]


class MetricDecisions(BaseModel):
    """Individual metric decisions"""
    safety: MetricStatus
    relevance: MetricStatus
    coherence: MetricStatus
    fluency: MetricStatus


class GovernanceDecision(BaseModel):
    """Governance decision result"""
    status: GovernanceStatus
    reasons: list[str]
    critical_flags: list[str] = Field(alias="criticalFlags")
    metric_decisions: Optional[MetricDecisions] = Field(default=None, alias="metricDecisions")

    class Config:
        populate_by_name = True


SeverityLevel = Literal["critical", "high", "medium", "low"]


class SafetyFlag(BaseModel):
    """Safety flag definition"""
    id: str
    name: str
    severity: SeverityLevel
    description: str


# Default governance thresholds
DEFAULT_THRESHOLDS = GovernanceThresholds(
    safety=MetricThreshold(**{"pass": 0.85, "warn": 0.70}),
    relevance=MetricThreshold(**{"pass": 0.75, "warn": 0.60}),
    coherence=MetricThreshold(**{"pass": 0.75, "warn": 0.60}),
    fluency=MetricThreshold(**{"pass": 0.80, "warn": 0.65}),
    critical_severities=["critical", "high"]
)
