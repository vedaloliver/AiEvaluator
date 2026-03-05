"""Built-in evaluator service for safety, relevance, coherence, and fluency metrics"""

from models import EvaluationMetrics


class BuiltInEvaluatorService:
    """Handles evaluation of built-in metrics (safety, relevance, coherence, fluency)"""

    async def evaluate(
        self, model_id: str, scenario_id: str, query: str, response: str
    ) -> EvaluationMetrics:
        """
        Get built-in evaluations from mock data.

        In production, this would call Azure AI Foundry built-in evaluators.
        Currently returns mock data for testing and development.

        Args:
            model_id: The model identifier (e.g., "gpt-4", "claude-3-opus")
            scenario_id: The scenario identifier (e.g., "customer-service-response")
            query: The input query/prompt
            response: The model's response to evaluate

        Returns:
            EvaluationMetrics containing scores for built-in metrics
        """
        from fixtures.mock_evaluations import get_mock_evaluation

        return get_mock_evaluation(model_id, scenario_id)
