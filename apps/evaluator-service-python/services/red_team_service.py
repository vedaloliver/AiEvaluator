"""Red Team Service for adversarial testing"""
import asyncio
from datetime import datetime
from typing import List, Optional
from models import (
    RedTeamRequest,
    RedTeamSuiteResult,
    RedTeamAttackResult,
    RedTeamAttack,
    EvaluationRequest,
)
from .mock_evaluator import MockEvaluatorService
from config.red_team_attacks import (
    RED_TEAM_ATTACKS,
    get_attacks_by_scenario,
    get_attacks_by_category,
    ATTACK_CATEGORIES,
    ATTACK_STRATEGIES,
)


class RedTeamService:
    """Service for running red team adversarial attacks"""

    def __init__(self):
        self.evaluator_service = MockEvaluatorService()

    async def run_attack_suite(self, request: RedTeamRequest) -> RedTeamSuiteResult:
        """
        Run a suite of red team attacks against a model and scenario.

        Args:
            request: Red team request with scenario_id, model_id, and optional filters

        Returns:
            RedTeamSuiteResult with ASR, vulnerabilities, and all attack results
        """
        start_time = datetime.now()

        # Get attacks for the scenario
        attacks = get_attacks_by_scenario(request.scenario_id)

        if not attacks:
            raise ValueError(f"No attacks found for scenario: {request.scenario_id}")

        # Apply filters
        if request.attack_categories:
            attacks = [
                a for a in attacks
                if a.category in request.attack_categories
            ]

        if request.attack_strategies:
            attacks = [
                a for a in attacks
                if a.attack_strategy in request.attack_strategies
            ]

        # Apply limit
        if request.limit and request.limit > 0:
            attacks = attacks[:request.limit]

        # Run all attacks
        attack_results = await self._run_attacks(attacks, request.model_id)

        # Calculate metrics
        total_attacks = len(attack_results)
        successful_attacks = sum(
            1 for r in attack_results if r.vulnerability_detected
        )
        blocked_attacks = total_attacks - successful_attacks
        asr = (successful_attacks / total_attacks) if total_attacks > 0 else 0.0

        # Get vulnerabilities (attacks that got PASS verdict)
        vulnerabilities = [r for r in attack_results if r.vulnerability_detected]

        result = RedTeamSuiteResult(
            scenarioId=request.scenario_id,
            modelId=request.model_id,
            totalAttacks=total_attacks,
            successfulAttacks=successful_attacks,
            blockedAttacks=blocked_attacks,
            attackSuccessRate=round(asr, 3),
            vulnerabilities=vulnerabilities,
            allResults=attack_results,
            timestamp=datetime.now().isoformat()
        )

        return result

    async def _run_attacks(
        self,
        attacks: List[RedTeamAttack],
        model_id: str
    ) -> List[RedTeamAttackResult]:
        """
        Run multiple attacks in parallel.

        Args:
            attacks: List of attacks to run
            model_id: Model ID to test

        Returns:
            List of attack results
        """
        # Create evaluation requests for each attack
        eval_requests = [
            EvaluationRequest(
                scenarioId=attack.scenario_id,
                modelId=model_id,
                query=attack.base_query  # Using base query directly (no transformation in mock mode)
            )
            for attack in attacks
        ]

        # Run evaluations in parallel
        eval_results = await self.evaluator_service.evaluate_batch(eval_requests)

        # Convert to attack results
        attack_results = []
        for i, (attack, eval_result) in enumerate(zip(attacks, eval_results)):
            actual_outcome = eval_result.governance_decision.status
            vulnerability_detected = (
                actual_outcome == "PASS"  # If attack got PASS, governance failed to block it
            )

            attack_result = RedTeamAttackResult(
                attackId=attack.id,
                category=attack.category,
                attackStrategy=attack.attack_strategy,
                transformedQuery=attack.base_query,  # No transformation in simple mode
                evaluationResult=eval_result,
                expectedOutcome=attack.expected_outcome,
                actualOutcome=actual_outcome,
                vulnerabilityDetected=vulnerability_detected
            )
            attack_results.append(attack_result)

        return attack_results

    def get_attack_categories(self) -> List[dict]:
        """Get all available attack categories"""
        return ATTACK_CATEGORIES

    def get_attack_strategies(self) -> List[dict]:
        """Get all available attack strategies"""
        return ATTACK_STRATEGIES

    def get_scenario_attack_count(self, scenario_id: str) -> int:
        """Get count of attacks for a scenario"""
        return len(get_attacks_by_scenario(scenario_id))

    def get_category_attack_count(self, category: str) -> int:
        """Get count of attacks for a category"""
        return len(get_attacks_by_category(category))
