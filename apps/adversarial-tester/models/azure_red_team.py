"""Azure AI Foundry red team request/response models."""
from typing import List, Optional
from pydantic import BaseModel, Field

from models.red_team import PyRITAttackStrategy


class AzureRedTeamRequest(BaseModel):
    """Request body for POST /adversarial/run-cloud."""
    agent_name: str = Field(alias="agentName")
    agent_version: str = Field(alias="agentVersion")
    attack_strategies: List[PyRITAttackStrategy] = Field(alias="attackStrategies")
    risk_categories: List[str] = Field(alias="riskCategories")
    num_turns: int = Field(default=5, alias="numTurns")
    taxonomy_id: Optional[str] = Field(default=None, alias="taxonomyId")

    class Config:
        populate_by_name = True


class AzureRedTeamRunResult(BaseModel):
    """Result returned from POST /adversarial/run-cloud."""
    run_id: str = Field(alias="runId")
    status: str  # "created" | "running" | "completed" | "failed"
    agent_name: str = Field(alias="agentName")
    agent_version: str = Field(alias="agentVersion")
    attack_strategies: List[str] = Field(alias="attackStrategies")
    risk_categories: List[str] = Field(alias="riskCategories")
    details: Optional[dict] = None  # Raw SDK response / mock summary

    class Config:
        populate_by_name = True


class TaxonomyUploadResult(BaseModel):
    """Result of POST /adversarial/taxonomy."""
    taxonomy_file_id: str = Field(alias="taxonomyFileId")
    scenario_id: str = Field(alias="scenarioId")
    message: str

    class Config:
        populate_by_name = True
