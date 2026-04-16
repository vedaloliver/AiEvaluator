"""Red Team Models for adversarial testing"""
from pydantic import BaseModel, Field
from typing import Optional, List
from .evaluation import EvaluationResult


class AttackStrategy(BaseModel):
    """Attack transformation strategy"""
    id: str
    name: str
    description: str


class AttackCategory(BaseModel):
    """Category of adversarial attack"""
    id: str
    name: str
    description: str


class RedTeamAttack(BaseModel):
    """Individual red team attack definition"""
    id: str
    scenario_id: str = Field(alias="scenarioId")
    category: str  # prohibited-actions, sensitive-data-leakage, compliance-bypass, discriminatory-language
    threat_type: str = Field(alias="threatType")  # prompt-injection, information-evasion, biased-opinion
    base_query: str = Field(alias="baseQuery")
    attack_strategy: str = Field(alias="attackStrategy")  # base64, jailbreak, social-engineering, leetspeak
    expected_outcome: str = Field(alias="expectedOutcome")  # FAIL (governance should block), PASS (vulnerability)
    description: Optional[str] = None

    class Config:
        populate_by_name = True


class RedTeamAttackResult(BaseModel):
    """Result of a single red team attack"""
    attack_id: str = Field(alias="attackId")
    category: str
    attack_strategy: str = Field(alias="attackStrategy")
    transformed_query: str = Field(alias="transformedQuery")
    evaluation_result: EvaluationResult = Field(alias="evaluationResult")
    expected_outcome: str = Field(alias="expectedOutcome")
    actual_outcome: str = Field(alias="actualOutcome")  # PASS/WARN/FAIL
    vulnerability_detected: bool = Field(alias="vulnerabilityDetected")  # True if attack succeeded (PASS verdict)

    class Config:
        populate_by_name = True


class RedTeamSuiteResult(BaseModel):
    """Result of running a red team attack suite"""
    scenario_id: str = Field(alias="scenarioId")
    model_id: str = Field(alias="modelId")
    total_attacks: int = Field(alias="totalAttacks")
    successful_attacks: int = Field(alias="successfulAttacks")  # Attacks that got PASS (vulnerabilities)
    blocked_attacks: int = Field(alias="blockedAttacks")  # Attacks that got FAIL/WARN (governance working)
    attack_success_rate: float = Field(alias="attackSuccessRate")  # ASR = successful / total
    vulnerabilities: List[RedTeamAttackResult]
    all_results: List[RedTeamAttackResult] = Field(alias="allResults")
    timestamp: str

    class Config:
        populate_by_name = True


class RedTeamRequest(BaseModel):
    """Request to run red team attack suite"""
    scenario_id: str = Field(alias="scenarioId")
    model_id: str = Field(alias="modelId")
    attack_categories: Optional[List[str]] = Field(default=None, alias="attackCategories")  # Filter by categories
    attack_strategies: Optional[List[str]] = Field(default=None, alias="attackStrategies")  # Filter by strategies
    threat_types: Optional[List[str]] = Field(default=None, alias="threatTypes")  # Filter by threat types
    limit: Optional[int] = None  # Limit number of attacks to run

    class Config:
        populate_by_name = True
