"""
Mock Evaluator Service

This service provides mock evaluation results without calling Azure AI Foundry.
Use this for development and testing the UI without Azure credentials.
"""

import asyncio
import random
import uuid
from datetime import datetime
from models import EvaluationRequest, EvaluationResult, EvaluationMetrics, EvaluationScore
from .governance_service import GovernanceService
from .model_service import ModelService
from .built_in_evaluator_service import BuiltInEvaluatorService
from .custom_fca_evaluator_service import CustomFCAEvaluatorService
from .token_service import calculate_tokens_and_cost
from .observability_client import ObservabilityClient
from config.scenarios import get_scenario_by_id
from config.thresholds import get_effective_thresholds
from config.settings import settings
from fixtures.mock_responses import get_mock_response


class MockEvaluatorService:
    """Mock evaluator service for testing without Azure"""

    def __init__(self):
        self.governance_service = GovernanceService()
        self.model_service = ModelService()
        self.built_in_service = BuiltInEvaluatorService()
        self.fca_service = CustomFCAEvaluatorService()
        self.observability_client = ObservabilityClient(settings.observability_service_url)

    async def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        """Main evaluation method using mock data"""
        start_time = datetime.now()

        # Generate trace and span IDs for observability
        trace_id = str(uuid.uuid4())
        span_id = str(uuid.uuid4())

        # Create trace in observability service (non-blocking)
        try:
            await self.observability_client.create_trace(trace_id)
        except Exception as e:
            # Log but don't fail evaluation
            print(f"Warning: Failed to create trace: {e}")

        # Simulate API delay (800-1500ms)
        await self._simulate_delay(800, 1500)

        # Validate inputs
        scenario = get_scenario_by_id(request.scenario_id)
        if not scenario:
            raise ValueError(f"Scenario not found: {request.scenario_id}")

        model = self.model_service.get_model_by_id(request.model_id)
        if not model:
            raise ValueError(f"Model not found: {request.model_id}")

        # Get effective thresholds (merge scenario custom + request overrides)
        effective_thresholds = get_effective_thresholds(request.thresholds)

        # Override with scenario custom thresholds if present
        if scenario.custom_thresholds:
            effective_thresholds = get_effective_thresholds(request.thresholds)
            # Merge scenario thresholds
            if scenario.custom_thresholds.safety:
                effective_thresholds.safety = scenario.custom_thresholds.safety
            if scenario.custom_thresholds.relevance:
                effective_thresholds.relevance = scenario.custom_thresholds.relevance
            if scenario.custom_thresholds.coherence:
                effective_thresholds.coherence = scenario.custom_thresholds.coherence
            if scenario.custom_thresholds.fluency:
                effective_thresholds.fluency = scenario.custom_thresholds.fluency
            # Merge FCA thresholds for financial scenarios
            if scenario.custom_thresholds.disclaimer_compliance:
                effective_thresholds.disclaimer_compliance = scenario.custom_thresholds.disclaimer_compliance
            if scenario.custom_thresholds.prohibited_language:
                effective_thresholds.prohibited_language = scenario.custom_thresholds.prohibited_language
            if scenario.custom_thresholds.suitability_assessment:
                effective_thresholds.suitability_assessment = scenario.custom_thresholds.suitability_assessment
            if scenario.custom_thresholds.risk_disclosure:
                effective_thresholds.risk_disclosure = scenario.custom_thresholds.risk_disclosure

        # Get mock response
        model_response = get_mock_response(request.model_id, request.scenario_id)

        # Calculate tokens and cost
        token_usage, cost_estimate = calculate_tokens_and_cost(
            query=request.query,
            system_prompt=scenario.system_prompt,
            response=model_response,
            model_id=request.model_id
        )

        # Get built-in evaluations (safety, relevance, coherence, fluency)
        evaluations = await self.built_in_service.evaluate(
            request.model_id, request.scenario_id, request.query, model_response
        )

        # Get and merge custom FCA evaluations for financial scenarios
        if scenario.category == "financial":
            fca_metrics = await self.fca_service.evaluate(
                request.model_id, request.scenario_id, request.query, model_response
            )

            # Validate all 4 FCA evaluators are present
            self.fca_service.validate_complete(fca_metrics)

            # Merge into evaluations
            evaluations.disclaimer_compliance = fca_metrics.get("disclaimerCompliance")
            evaluations.prohibited_language = fca_metrics.get("prohibitedLanguage")
            evaluations.suitability_assessment = fca_metrics.get("suitabilityAssessment")
            evaluations.risk_disclosure = fca_metrics.get("riskDisclosure")

        # Make governance decision
        governance_decision = self.governance_service.make_decision(
            evaluations,
            effective_thresholds,
            scenario.critical_flags
        )

        # Calculate duration
        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

        # Construct result with observability data
        result = EvaluationResult(
            modelId=request.model_id,
            query=request.query,
            response=model_response,
            evaluations=evaluations,
            governanceDecision=governance_decision,
            timestamp=datetime.now().isoformat(),
            durationMs=duration_ms,
            traceId=trace_id,
            spanId=span_id,
            tokenUsage=token_usage,
            costEstimate=cost_estimate
        )

        # Create span in observability service (non-blocking)
        try:
            await self.observability_client.create_span({
                "spanId": span_id,
                "traceId": trace_id,
                "name": "evaluate",
                "spanType": "evaluation",
                "durationMs": duration_ms,
                "attributes": {
                    "modelId": request.model_id,
                    "scenarioId": request.scenario_id,
                    "decision": governance_decision.status
                }
            })
        except Exception as e:
            # Log but don't fail evaluation
            print(f"Warning: Failed to create span: {e}")

        # Store evaluation run in observability service (non-blocking)
        try:
            eval_data = result.model_dump(by_alias=True)
            eval_data["scenarioId"] = request.scenario_id  # Add scenario_id
            await self.observability_client.store_evaluation_run(eval_data)
        except Exception as e:
            # Log but don't fail evaluation
            print(f"Warning: Failed to store evaluation run: {e}")

        # Mark trace as completed (non-blocking)
        try:
            await self.observability_client.update_trace(trace_id, status="completed")
        except Exception as e:
            # Log but don't fail evaluation
            print(f"Warning: Failed to update trace: {e}")

        return result

    async def evaluate_batch(
        self,
        requests: list[EvaluationRequest]
    ) -> list[EvaluationResult]:
        """Batch evaluate multiple models with mock data"""
        # Run evaluations in parallel
        tasks = [self.evaluate(request) for request in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Map results, handling errors
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Return a failed result
                print(f"Evaluation failed for request {i}: {result}")
                processed_results.append(
                    EvaluationResult(
                        modelId=requests[i].model_id,
                        query=requests[i].query,
                        response="ERROR: Mock evaluation failed",
                        evaluations=EvaluationMetrics(
                            safety=EvaluationScore(score=0.0, rationale="Evaluation failed"),
                            relevance=EvaluationScore(score=0.0, rationale="Evaluation failed"),
                            coherence=EvaluationScore(score=0.0, rationale="Evaluation failed"),
                            fluency=EvaluationScore(score=0.0, rationale="Evaluation failed")
                        ),
                        governanceDecision={
                            "status": "FAIL",
                            "reasons": [f"Error: {str(result)}"],
                            "criticalFlags": []
                        },
                        timestamp=datetime.now().isoformat()
                    )
                )
            else:
                processed_results.append(result)

        return processed_results

    async def _simulate_delay(self, min_ms: int, max_ms: int) -> None:
        """Simulates network delay"""
        delay_ms = random.uniform(min_ms, max_ms)
        await asyncio.sleep(delay_ms / 1000.0)
