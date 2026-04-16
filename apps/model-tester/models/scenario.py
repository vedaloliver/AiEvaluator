from pydantic import BaseModel, Field
from typing import Optional, Literal
from .governance import GovernanceThresholds, SafetyFlag


ScenarioCategory = Literal["financial", "medical", "legal", "hr"]


class RegulatoryScenario(BaseModel):
    """Complete regulatory scenario definition"""
    id: str
    name: str
    category: ScenarioCategory
    description: str
    example_query: str = Field(alias="exampleQuery")
    system_prompt: str = Field(alias="systemPrompt")
    critical_flags: list[SafetyFlag] = Field(alias="criticalFlags")
    custom_thresholds: Optional[GovernanceThresholds] = Field(default=None, alias="customThresholds")

    class Config:
        populate_by_name = True

    def to_list_item(self) -> "ScenarioListItem":
        """Convert to list item for API responses"""
        return ScenarioListItem(
            id=self.id,
            name=self.name,
            category=self.category,
            description=self.description,
            example_query=self.example_query
        )


class ScenarioListItem(BaseModel):
    """Simplified scenario for list endpoints"""
    id: str
    name: str
    category: ScenarioCategory
    description: str
    example_query: str = Field(alias="exampleQuery")

    class Config:
        populate_by_name = True
