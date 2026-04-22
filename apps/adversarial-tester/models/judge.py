"""LLM Judge evaluation models"""
from pydantic import BaseModel
from typing import List


class JudgeEvaluation(BaseModel):
    """Result of LLM-as-judge evaluation"""
    violated: bool
    confidence: float  # 0.0–1.0
    risk_category: str  # which risk category was violated
    reasoning: str  # explanation of verdict
    detected_issues: List[str]  # specific issues found
    evaluation_method: str  # "regex_match" | "llm_judge" | "combined"

    class Config:
        populate_by_name = True
