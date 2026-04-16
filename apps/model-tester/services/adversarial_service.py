"""Adversarial Testing Service - calls Response Evaluator to test model vulnerabilities"""
import asyncio
import httpx
from datetime import datetime
from typing import List
from models import (
    RedTeamRequest,
    RedTeamSuiteResult,
    RedTeamAttackResult,
    RedTeamAttack,
    EvaluationResult,
)
from config.settings import settings
from config.attacks import (
    RED_TEAM_ATTACKS,
    get_attacks_by_scenario,
    get_attacks_by_category,
    get_attacks_by_threat_type,
    ATTACK_CATEGORIES,
    ATTACK_STRATEGIES,
    THREAT_TYPES,
)


class AdversarialService:
    """Service for running adversarial attack suites against models"""

    def __init__(self):
        self.response_evaluator_url = settings.response_evaluator_url

    async def run_attack_suite(self, request: RedTeamRequest) -> RedTeamSuiteResult:
        """
        Run a suite of adversarial attacks against a model and scenario.

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

        # Apply threat type filter (new)
        if hasattr(request, 'threat_types') and request.threat_types:
            attacks = [
                a for a in attacks
                if a.threat_type in request.threat_types
            ]

        # Apply limit
        if request.limit and request.limit > 0:
            attacks = attacks[:request.limit]

        # Run all attacks by calling response evaluator
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
        Run multiple attacks by calling the response evaluator service.

        Args:
            attacks: List of attacks to run
            model_id: Model ID to test

        Returns:
            List of attack results
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            tasks = []
            for attack in attacks:
                task = self._evaluate_attack(client, attack, model_id)
                tasks.append(task)

            # Run all evaluations in parallel
            eval_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert to attack results
        attack_results = []
        for attack, eval_result in zip(attacks, eval_results):
            # Handle errors
            if isinstance(eval_result, Exception):
                print(f"Error evaluating attack {attack.id}: {eval_result}")
                continue

            actual_outcome = eval_result.governance_decision.status
            vulnerability_detected = (
                actual_outcome == "PASS"  # If attack got PASS, governance failed to block it
            )

            attack_result = RedTeamAttackResult(
                attackId=attack.id,
                category=attack.category,
                attackStrategy=attack.attack_strategy,
                transformedQuery=attack.base_query,
                evaluationResult=eval_result,
                expectedOutcome=attack.expected_outcome,
                actualOutcome=actual_outcome,
                vulnerabilityDetected=vulnerability_detected
            )
            attack_results.append(attack_result)

        return attack_results

    async def _evaluate_attack(
        self,
        client: httpx.AsyncClient,
        attack: RedTeamAttack,
        model_id: str
    ) -> EvaluationResult:
        """
        Call the response evaluator service to evaluate a single attack.

        Args:
            client: HTTP client
            attack: Attack to evaluate
            model_id: Model ID to test

        Returns:
            EvaluationResult from the response evaluator
        """
        url = f"{self.response_evaluator_url}/api/v1/evaluate"
        payload = {
            "scenarioId": attack.scenario_id,
            "modelId": model_id,
            "query": attack.base_query
        }

        response = await client.post(url, json=payload)
        response.raise_for_status()

        # Parse response into EvaluationResult
        data = response.json()
        return EvaluationResult(**data)

    def get_attack_categories(self) -> List[dict]:
        """Get all available attack categories"""
        return ATTACK_CATEGORIES

    def get_attack_strategies(self) -> List[dict]:
        """Get all available attack strategies"""
        return ATTACK_STRATEGIES

    def get_threat_types(self) -> List[dict]:
        """Get all available threat types"""
        return THREAT_TYPES

    def get_scenario_attack_count(self, scenario_id: str) -> int:
        """Get count of attacks for a scenario"""
        return len(get_attacks_by_scenario(scenario_id))

    def get_category_attack_count(self, category: str) -> int:
        """Get count of attacks for a category"""
        return len(get_attacks_by_category(category))

    def get_threat_type_attack_count(self, threat_type: str) -> int:
        """Get count of attacks for a threat type"""
        return len(get_attacks_by_threat_type(threat_type))
