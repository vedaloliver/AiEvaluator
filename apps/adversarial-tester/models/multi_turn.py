"""Conversation turn and history models for multi-turn attacks"""
from pydantic import BaseModel
from typing import List, Optional
from models.judge import JudgeEvaluation


class ConversationTurn(BaseModel):
    """A single turn in a multi-turn conversation"""
    turn_number: int
    role: str  # "user" | "assistant"
    content: str
    flags_detected: List[str] = []
    judge_evaluation: Optional[JudgeEvaluation] = None

    class Config:
        populate_by_name = True


class ConversationHistory(BaseModel):
    """Full conversation history for a multi-turn attack"""
    attack_id: str
    turns: List[ConversationTurn]
    violation_turn: Optional[int] = None  # first turn where violation occurred
    total_turns: int

    class Config:
        populate_by_name = True
