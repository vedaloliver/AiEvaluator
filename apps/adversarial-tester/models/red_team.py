"""Red Team Models for adversarial testing"""
from enum import Enum
from pydantic import BaseModel, Field
from typing import Literal, Optional, List


class PyRITAttackStrategy(str, Enum):
    """PyRIT canonical attack strategy names."""
    Base64 = "Base64"
    ROT13 = "ROT13"
    Caesar = "Caesar"
    Leetspeak = "Leetspeak"
    Flip = "Flip"
    CharSwap = "CharSwap"
    UnicodeConfusable = "UnicodeConfusable"
    SuffixAppend = "SuffixAppend"
    CharacterSpace = "CharacterSpace"


class PyRITScorerResult(BaseModel):
    """PyRIT-compatible scorer result attached to each attack evaluation."""
    score: Literal["pass", "fail"]
    risk_category: str
    reasoning: str
    severity: Literal["low", "medium", "high"]
    evaluation_method: str


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


class DetectedFlag(BaseModel):
    """Flag detected during attack evaluation"""
    flag_id: str = Field(alias="flagId")
    name: str
    severity: str
    detected: bool
    context: Optional[str] = None
    matched_pattern: Optional[str] = Field(default=None, alias="matchedPattern")

    class Config:
        populate_by_name = True


class RedTeamAttackResult(BaseModel):
    """Result of a single red team attack"""
    attack_id: str = Field(alias="attackId")
    category: str
    attack_strategy: str = Field(alias="attackStrategy")
    threat_type: Optional[str] = Field(default=None, alias="threatType")
    transformed_query: str = Field(alias="transformedQuery")

    # Direct attack evaluation (independent of response evaluator)
    model_response: str = Field(alias="modelResponse")
    detected_flags: List[DetectedFlag] = Field(default=[], alias="detectedFlags")

    # Outcome assessment
    expected_outcome: str = Field(alias="expectedOutcome")
    actual_outcome: str = Field(alias="actualOutcome")  # PASS/FAIL based on flag detection
    vulnerability_detected: bool = Field(alias="vulnerabilityDetected")  # True if no flags detected (attack succeeded)

    # PyRIT-compatible scorer result (populated by FCAScorerService)
    scorer_result: Optional[PyRITScorerResult] = Field(default=None, alias="scorerResult")

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

    # Observability field
    trace_id: Optional[str] = Field(default=None, alias="traceId")

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
