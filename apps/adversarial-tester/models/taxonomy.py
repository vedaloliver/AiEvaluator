"""Prohibited actions taxonomy models"""
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class TaxonomyTier(str, Enum):
    PROHIBITED = "prohibited"  # never allowed
    HIGH_RISK = "high_risk"  # allowed with human-in-loop
    IRREVERSIBLE = "irreversible"  # allowed with disclosure + confirmation


class TaxonomyAction(BaseModel):
    """A single action entry in the taxonomy"""
    id: str
    name: str
    description: str
    tier: TaxonomyTier
    regulatory_basis: Optional[str] = None
    examples: List[str] = []

    class Config:
        populate_by_name = True


class ProhibitedActionsTaxonomy(BaseModel):
    """Complete taxonomy for a scenario"""
    scenario_id: str
    prohibited: List[TaxonomyAction]
    high_risk: List[TaxonomyAction]
    irreversible: List[TaxonomyAction]
    version: str
    last_updated: str

    class Config:
        populate_by_name = True
