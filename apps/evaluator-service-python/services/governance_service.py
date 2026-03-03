from models import (
    GovernanceDecision,
    GovernanceThresholds,
    MetricStatus,
    MetricDecisions,
    EvaluationMetrics,
    SafetyFlag,
    MetricThreshold,
)


class GovernanceService:
    """Service for making governance decisions based on evaluation metrics"""

    def _evaluate_metric(
        self,
        score: float,
        thresholds: MetricThreshold
    ) -> MetricStatus:
        """
        Evaluates a single metric score against thresholds.

        Args:
            score: The metric score (0.0 - 1.0)
            thresholds: Pass and warn thresholds

        Returns:
            MetricStatus: PASS, WARN, or FAIL
        """
        if score >= thresholds.pass_threshold:
            return "PASS"
        if score >= thresholds.warn:
            return "WARN"
        return "FAIL"

    def _check_critical_flags(
        self,
        evaluations: EvaluationMetrics,
        critical_flags: list[SafetyFlag],
        critical_severities: list[str]
    ) -> list[str]:
        """
        Checks if any critical flags are present in the evaluation.

        Args:
            evaluations: The evaluation metrics
            critical_flags: List of critical safety flags to check for
            critical_severities: List of severities considered critical (e.g., ['critical', 'high'])

        Returns:
            List of detected critical flag names
        """
        detected_flags: list[str] = []

        # Check if safety evaluation indicates critical severity
        if evaluations.safety.severity:
            severity_lower = evaluations.safety.severity.lower()
            if severity_lower in [s.lower() for s in critical_severities]:
                # Look for matching flag in rationale
                matching_flag = None
                for flag in critical_flags:
                    if flag.name.lower() in evaluations.safety.rationale.lower():
                        matching_flag = flag
                        break

                if matching_flag:
                    detected_flags.append(matching_flag.name)
                else:
                    detected_flags.append(f"Critical safety concern: {evaluations.safety.severity}")

        # Check for specific flag keywords in rationales
        for flag in critical_flags:
            if flag.severity.lower() in [s.lower() for s in critical_severities]:
                # Search in both safety and relevance rationales
                search_text = f"{evaluations.safety.rationale} {evaluations.relevance.rationale}".lower()
                if flag.name.lower() in search_text or flag.id.lower() in search_text:
                    if flag.name not in detected_flags:
                        detected_flags.append(flag.name)

        return detected_flags

    def make_decision(
        self,
        evaluations: EvaluationMetrics,
        thresholds: GovernanceThresholds,
        critical_flags: list[SafetyFlag] | None = None
    ) -> GovernanceDecision:
        """
        Makes governance decision based on evaluation scores and thresholds.

        Args:
            evaluations: The evaluation metrics
            thresholds: The governance thresholds
            critical_flags: Optional list of critical safety flags

        Returns:
            GovernanceDecision with status, reasons, and metric decisions
        """
        reasons: list[str] = []
        critical_flags_list = critical_flags or []

        # Check for critical flags first (auto-FAIL)
        detected_critical_flags = self._check_critical_flags(
            evaluations,
            critical_flags_list,
            thresholds.critical_severities or ["critical", "high"]
        )

        # Evaluate each metric
        metric_decisions = MetricDecisions(
            safety=self._evaluate_metric(evaluations.safety.score, thresholds.safety),
            relevance=self._evaluate_metric(evaluations.relevance.score, thresholds.relevance),
            coherence=self._evaluate_metric(evaluations.coherence.score, thresholds.coherence),
            fluency=self._evaluate_metric(evaluations.fluency.score, thresholds.fluency),
        )

        # If critical flags detected, return FAIL immediately
        if len(detected_critical_flags) > 0:
            return GovernanceDecision(
                status="FAIL",
                reasons=["Critical safety flags detected"],
                criticalFlags=detected_critical_flags,
                metricDecisions=metric_decisions
            )

        # Track which metrics failed or warned
        failed_metrics: list[str] = []
        warned_metrics: list[str] = []

        for metric_name in ["safety", "relevance", "coherence", "fluency"]:
            status = getattr(metric_decisions, metric_name)
            if status == "FAIL":
                failed_metrics.append(metric_name)
            elif status == "WARN":
                warned_metrics.append(metric_name)

        # Determine overall status
        if len(failed_metrics) > 0:
            overall_status = "FAIL"
            reasons.append(f"Failed metrics: {', '.join(failed_metrics)}")
        elif len(warned_metrics) > 0:
            overall_status = "WARN"
            reasons.append(f"Warning metrics: {', '.join(warned_metrics)}")
        else:
            overall_status = "PASS"
            reasons.append("All metrics passed thresholds")

        return GovernanceDecision(
            status=overall_status,
            reasons=reasons,
            criticalFlags=detected_critical_flags,
            metricDecisions=metric_decisions
        )

    def explain_decision(self, decision: GovernanceDecision) -> str:
        """
        Provides explanation for a governance decision.

        Args:
            decision: The governance decision to explain

        Returns:
            Human-readable explanation string
        """
        explanation = f"Governance Decision: {decision.status}\n\n"

        if len(decision.critical_flags) > 0:
            explanation += f"Critical Flags: {', '.join(decision.critical_flags)}\n"

        if decision.metric_decisions:
            explanation += "\nMetric Decisions:\n"
            explanation += f"  - safety: {decision.metric_decisions.safety}\n"
            explanation += f"  - relevance: {decision.metric_decisions.relevance}\n"
            explanation += f"  - coherence: {decision.metric_decisions.coherence}\n"
            explanation += f"  - fluency: {decision.metric_decisions.fluency}\n"

        explanation += "\nReasons:\n"
        for reason in decision.reasons:
            explanation += f"  - {reason}\n"

        return explanation
