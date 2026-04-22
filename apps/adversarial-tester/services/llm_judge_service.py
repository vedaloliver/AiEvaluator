"""LLM-as-judge evaluation service.

Dispatches to the mock implementation when ``use_mock_data=True`` (default).

Real implementation would call the Azure AI Evaluation SDK evaluators
(e.g. azure.ai.evaluation.ViolenceEvaluator, HateUnfairnessEvaluator, etc.)
but that requires Azure credentials and is not yet wired up.
"""
from typing import List, Optional

from config.settings import settings
from models.judge import JudgeEvaluation
from models import RedTeamAttack, DetectedFlag


class LLMJudgeService:
    """Public judge service — delegates to mock or real backend."""

    def __init__(self) -> None:
        if settings.use_mock_data:
            from mocks.llm_judge import MockLLMJudgeService
            self._backend = MockLLMJudgeService()
        else:
            # Real Azure AI Evaluation backend (not yet implemented).
            # When ready, import and instantiate the Azure evaluator here.
            raise NotImplementedError(
                "Real LLM judge is not yet implemented. "
                "Set USE_MOCK_DATA=true to use the deterministic mock."
            )

    async def evaluate(
        self,
        attack: RedTeamAttack,
        response: str,
        regex_flags: List[DetectedFlag],
        transformation_applied: Optional[str] = None,
    ) -> JudgeEvaluation:
        return await self._backend.evaluate(
            attack=attack,
            response=response,
            regex_flags=regex_flags,
            transformation_applied=transformation_applied,
        )
