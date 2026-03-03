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
        critical_severities=DEFAULT_THRESHOLDS.critical_severities
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

    return effective
