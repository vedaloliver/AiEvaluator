from models import GovernanceThresholds, DEFAULT_THRESHOLDS, ThresholdOverride


def get_effective_thresholds(
    custom_thresholds: ThresholdOverride | None = None
) -> GovernanceThresholds:
    """
    Merge custom thresholds with defaults at the metric level.
    Custom thresholds override defaults where provided.
    """
    if not custom_thresholds:
        return DEFAULT_THRESHOLDS

    # Start with defaults
    effective = GovernanceThresholds(
        safety=DEFAULT_THRESHOLDS.safety,
        relevance=DEFAULT_THRESHOLDS.relevance,
        coherence=DEFAULT_THRESHOLDS.coherence,
        fluency=DEFAULT_THRESHOLDS.fluency,
        critical_severities=DEFAULT_THRESHOLDS.critical_severities,
        disclaimer_compliance=DEFAULT_THRESHOLDS.disclaimer_compliance,
        prohibited_language=DEFAULT_THRESHOLDS.prohibited_language,
        suitability_assessment=DEFAULT_THRESHOLDS.suitability_assessment,
        risk_disclosure=DEFAULT_THRESHOLDS.risk_disclosure
    )

    # Override with custom values if provided
    if custom_thresholds.safety:
        effective.safety = custom_thresholds.safety
    if custom_thresholds.relevance:
        effective.relevance = custom_thresholds.relevance
    if custom_thresholds.coherence:
        effective.coherence = custom_thresholds.coherence
    if custom_thresholds.fluency:
        effective.fluency = custom_thresholds.fluency
    if custom_thresholds.disclaimer_compliance:
        effective.disclaimer_compliance = custom_thresholds.disclaimer_compliance
    if custom_thresholds.prohibited_language:
        effective.prohibited_language = custom_thresholds.prohibited_language
    if custom_thresholds.suitability_assessment:
        effective.suitability_assessment = custom_thresholds.suitability_assessment
    if custom_thresholds.risk_disclosure:
        effective.risk_disclosure = custom_thresholds.risk_disclosure

    return effective
