"""Custom FCA evaluator service for financial compliance metrics"""

from typing import Dict
from models import EvaluationScore


class CustomFCAEvaluatorService:
    """Handles evaluation of custom FCA metrics"""

    # Required FCA evaluators for financial scenarios
    REQUIRED_FCA_EVALUATORS = [
        "disclaimerCompliance",
        "prohibitedLanguage",
        "suitabilityAssessment",
        "riskDisclosure",
    ]

    async def evaluate(
        self, model_id: str, scenario_id: str, query: str, response: str
    ) -> Dict[str, EvaluationScore]:
        """
        Get FCA evaluations from mock data.

        In production, this would call Azure code-based custom evaluators.
        Currently returns mock data for testing and development.

        Args:
            model_id: The model identifier (e.g., "gpt-4", "claude-3-opus")
            scenario_id: The scenario identifier (e.g., "customer-service-response")
            query: The input query/prompt
            response: The model's response to evaluate

        Returns:
            Dictionary of FCA metric names to EvaluationScore objects
        """
        from fixtures.mock_custom_evaluations import get_mock_custom_evaluation

        return get_mock_custom_evaluation(model_id, scenario_id)

    def validate_complete(self, fca_metrics: Dict[str, EvaluationScore]) -> None:
        """
        Validate that all 4 required FCA metrics are present.

        Args:
            fca_metrics: Dictionary of FCA metric names to EvaluationScore objects

        Raises:
            ValueError: If any required FCA metrics are missing or None
        """
        missing = [
            metric
            for metric in self.REQUIRED_FCA_EVALUATORS
            if metric not in fca_metrics or fca_metrics[metric] is None
        ]

        if missing:
            raise ValueError(
                f"Financial scenarios require all FCA evaluators. Missing: {', '.join(missing)}"
            )
