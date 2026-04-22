"""Adversarial Testing Service - independent vulnerability detection"""
import asyncio
import uuid
from datetime import datetime
from typing import List
from models import (
    RedTeamRequest,
    RedTeamSuiteResult,
    RedTeamAttackResult,
    RedTeamAttack,
    DetectedFlag,
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
from config.transformation_strategies import TRANSFORMATION_STRATEGIES, resolve_strategy_key
from services.observability_client import ObservabilityClient
from services.mock_response_service import MockResponseService
from services.flag_detector_service import FlagDetectorService
from services.fca_scorer_service import FCAScorerService
from services.attack_transformer_service import AttackTransformerService


class AdversarialService:
    """Service for running adversarial attack suites against models"""

    def __init__(self):
        self.observability_client = ObservabilityClient(settings.observability_service_url)
        self.mock_service = MockResponseService(attack_success_rate=0.3)
        self.flag_detector = FlagDetectorService()
        self.fca_scorer = FCAScorerService()
        self.transformer = AttackTransformerService()

    async def run_attack_suite(self, request: RedTeamRequest) -> RedTeamSuiteResult:
        """
        Run a suite of adversarial attacks against a model and scenario.

        Args:
            request: Red team request with scenario_id, model_id, and optional filters

        Returns:
            RedTeamSuiteResult with ASR, vulnerabilities, and all attack results
        """
        start_time = datetime.now()

        # Generate trace ID for observability
        trace_id = str(uuid.uuid4())

        # Create trace in observability service (non-blocking)
        try:
            await self.observability_client.create_trace(trace_id)
        except Exception as e:
            print(f"Warning: Failed to create trace: {e}")

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

        # Split requested strategies into conceptual (filter) vs transformation (expand)
        transformation_keys: List[str] = []
        conceptual_strategies: List[str] = []
        if request.attack_strategies:
            for s in request.attack_strategies:
                key = resolve_strategy_key(s)
                if key in TRANSFORMATION_STRATEGIES:
                    transformation_keys.append(key)
                else:
                    conceptual_strategies.append(s)

        if conceptual_strategies:
            attacks = [a for a in attacks if a.attack_strategy in conceptual_strategies]

        # Apply threat type filter
        if hasattr(request, 'threat_types') and request.threat_types:
            attacks = [
                a for a in attacks
                if a.threat_type in request.threat_types
            ]

        # Expand: each attack × each transformation (or once with no transformation)
        if transformation_keys:
            expanded = [(attack, key) for attack in attacks for key in transformation_keys]
        else:
            expanded = [(attack, None) for attack in attacks]

        # Apply limit to expanded list
        if request.limit and request.limit > 0:
            expanded = expanded[:request.limit]

        # Run all attacks
        attack_results = await self._run_attacks(expanded, request.model_id, trace_id)

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
            timestamp=datetime.now().isoformat(),
            traceId=trace_id
        )

        # Store adversarial run in observability service (non-blocking)
        try:
            suite_data = result.model_dump(by_alias=True)
            await self.observability_client.store_adversarial_run(suite_data)
        except Exception as e:
            print(f"Warning: Failed to store adversarial run: {e}")

        # Mark trace as completed (non-blocking)
        try:
            await self.observability_client.update_trace(trace_id, status="completed")
        except Exception as e:
            print(f"Warning: Failed to update trace: {e}")

        return result

    async def _run_attacks(
        self,
        expanded: List[tuple],
        model_id: str,
        trace_id: str
    ) -> List[RedTeamAttackResult]:
        """
        Run multiple attacks independently with flag detection.

        Args:
            expanded: List of (RedTeamAttack, transformation_key | None) tuples
            model_id: Model ID to test
            trace_id: Trace ID for observability

        Returns:
            List of attack results
        """
        tasks = [
            self._evaluate_attack(attack, model_id, trace_id, transformation_key)
            for attack, transformation_key in expanded
        ]

        # Run all evaluations in parallel
        attack_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out errors
        valid_results = []
        for (attack, _), result in zip(expanded, attack_results):
            if isinstance(result, Exception):
                print(f"Error evaluating attack {attack.id}: {type(result).__name__}: {str(result)}")
                import traceback
                traceback.print_exception(type(result), result, result.__traceback__)
                continue
            valid_results.append(result)

        return valid_results

    async def _evaluate_attack(
        self,
        attack: RedTeamAttack,
        model_id: str,
        trace_id: str,
        transformation_key: str | None = None,
    ) -> RedTeamAttackResult:
        """
        Evaluate a single attack independently without calling response evaluator.

        Args:
            attack: Attack to evaluate
            model_id: Model ID to test
            trace_id: Trace ID for observability
            transformation_key: Optional transformation strategy key (e.g. "base64", "rot13")

        Returns:
            RedTeamAttackResult with flag detection and outcome
        """
        span_id = str(uuid.uuid4())
        span_start = datetime.now()

        # Apply transformation if requested
        if transformation_key:
            transformed = self.transformer.transform(attack.base_query, transformation_key)
            query_to_send = transformed.transformed_query
            transformation_applied = transformed.strategy_name
        else:
            query_to_send = attack.base_query
            transformation_applied = None

        # Get mock response from the service
        response = self.mock_service.get_mock_response(model_id, attack.category)

        # Detect critical flags in the response
        detected_flags = self.flag_detector.detect_flags(response)

        # Convert flag objects to model objects
        flag_models = [
            DetectedFlag(
                flagId=flag.flag_id,
                name=flag.name,
                severity=flag.severity,
                detected=flag.detected,
                context=flag.context,
                matchedPattern=flag.matched_pattern
            )
            for flag in detected_flags
        ]

        # Determine outcome based on flag detection
        # If flags are detected, the attack was blocked (FAIL)
        # If no flags, the attack succeeded and found a vulnerability (PASS)
        if detected_flags:
            actual_outcome = "FAIL"  # Flags detected = defense worked
            vulnerability_detected = False
        else:
            actual_outcome = "PASS"  # No flags = potential vulnerability
            vulnerability_detected = True

        print(f"Attack {attack.id} [{transformation_applied or 'direct'}]: {len(detected_flags)} flags detected, outcome: {actual_outcome}")

        # PyRIT-compatible scorer evaluation
        scorer_result = await self.fca_scorer.score(
            response=response,
            attack=attack,
            regex_flags=flag_models,
        )

        # Create attack result
        result = RedTeamAttackResult(
            attackId=attack.id,
            category=attack.category,
            attackStrategy=attack.attack_strategy,
            threatType=attack.threat_type,
            transformedQuery=query_to_send,
            modelResponse=response,
            detectedFlags=flag_models,
            expectedOutcome=attack.expected_outcome,
            actualOutcome=actual_outcome,
            vulnerabilityDetected=vulnerability_detected,
            scorerResult=scorer_result,
        )

        # Calculate span duration
        span_duration = int((datetime.now() - span_start).total_seconds() * 1000)

        # Create span in observability service (non-blocking)
        try:
            await self.observability_client.create_span({
                "spanId": span_id,
                "traceId": trace_id,
                "name": f"attack_{attack.id}",
                "spanType": "adversarial_test",
                "durationMs": span_duration,
                "attributes": {
                    "attackId": attack.id,
                    "attackCategory": attack.category,
                    "attackStrategy": attack.attack_strategy,
                    "threatType": attack.threat_type,
                    "transformationApplied": transformation_applied,
                    "outcome": actual_outcome,
                    "vulnerabilityDetected": vulnerability_detected,
                    "flagsDetected": len(detected_flags),
                    "modelId": model_id,
                    "scenarioId": attack.scenario_id
                }
            })
        except Exception as e:
            print(f"Warning: Failed to create span for attack {attack.id}: {e}")

        return result

    def get_attack_categories(self) -> List[dict]:
        """Get all available attack categories"""
        return ATTACK_CATEGORIES

    def get_attack_strategies(self) -> List[dict]:
        """Get all available attack strategies.

        Returns two groups in one list, distinguished by the ``type`` field:

        - ``"conceptual"`` — high-level attack approach used to label seed
          attacks (direct, social-engineering, implicit).  These are the values
          accepted by the ``attackStrategies`` run-suite filter.
        - ``"transformation"`` — query obfuscation techniques (Base64, ROT13,
          etc.).  Each entry includes a ``pyrit_name`` for use with the Azure
          red team / PyRIT APIs.
        """
        conceptual = [{"type": "conceptual", **s} for s in ATTACK_STRATEGIES]
        transformation = [
            {
                "type": "transformation",
                "id": key,
                "pyrit_name": meta["pyrit_name"],
                "name": meta["name"],
                "description": meta["description"],
                "category": meta.get("category", "transformation"),
            }
            for key, meta in TRANSFORMATION_STRATEGIES.items()
        ]
        return conceptual + transformation

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
