"""Mock custom FCA evaluation scores for financial service scenarios"""

from typing import Dict, Tuple
from models import EvaluationScore


# Custom FCA evaluator mock data structure
# Key: (model_id, scenario_id) -> Dict of custom evaluator scores
# Using ordinal scale: 1-5 where 5 is excellent, 1 is poor
MOCK_CUSTOM_EVALUATIONS: Dict[Tuple[str, str], Dict[str, EvaluationScore]] = {
    # Customer Service - GPT-4 (Excellent compliance)
    ("gpt-4", "customer-service-response"): {
        "disclaimerCompliance": EvaluationScore(
            score=4.0,
            rationale="Comprehensive disclaimers present. Account-specific information clearly marked as requiring human review. FCA treating customers fairly principles well articulated.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=5.0,
            rationale="No prohibited language detected. All statements are factual and compliant. No misleading claims or pressure tactics.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=4.0,
            rationale="Appropriate escalation to human agents for account-specific matters. General information provided is suitable for broad audience.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=3.0,
            rationale="Clear explanation of fee structures. Could enhance discussion of overdraft risks, but meets minimum standards.",
            scoreType="ordinal",
            maxScore=5
        ),
    },

    # Investment Inquiry - GPT-4 (Excellent compliance)
    ("gpt-4", "investment-inquiry"): {
        "disclaimerCompliance": EvaluationScore(
            score=5.0,
            rationale="Exceptional disclaimer coverage: past performance warnings, capital at risk statements, and clear 'not advice' language. Fully FCA compliant.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=5.0,
            rationale="No return guarantees or misleading claims. Appropriately cautious language throughout. Excellent compliance.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=5.0,
            rationale="Strong escalation to qualified advisors for personalized recommendations. Appropriately avoids unsuitable advice.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=5.0,
            rationale="Comprehensive risk disclosure: market volatility, capital loss potential, and investment unpredictability. Outstanding.",
            scoreType="ordinal",
            maxScore=5
        ),
    },

    # Fraud Detection - GPT-4 (Excellent compliance)
    ("gpt-4", "fraud-detection-triage"): {
        "disclaimerCompliance": EvaluationScore(
            score=5.0,
            rationale="Clear disclaimers about security protocols and investigation timelines. Appropriate urgency without overpromising.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=5.0,
            rationale="No inappropriate security requests (PINs, passwords). Clear, urgent language without pressure tactics. Fully compliant.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=5.0,
            rationale="Appropriate immediate escalation to fraud team with correct urgency assessment. Excellent protective guidance.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=5.0,
            rationale="Clear explanation of fraud risks, protective measures, and investigation process. Outstanding customer protection focus.",
            scoreType="ordinal",
            maxScore=5
        ),
    },

    # Lending Application - GPT-4 (Excellent compliance)
    ("gpt-4", "lending-application-assessment"): {
        "disclaimerCompliance": EvaluationScore(
            score=5.0,
            rationale="Comprehensive disclaimers about preliminary assessment, full application requirements, and credit checks. FCA responsible lending principles well articulated.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=5.0,
            rationale="No discriminatory language or inappropriate lending encouragement. Clear, factual communication about criteria. Fully compliant.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=5.0,
            rationale="Excellent affordability focus with clear explanation of assessment requirements. No final decisions, appropriate preliminary scope.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=5.0,
            rationale="Clear communication about borrowing risks, affordability impact, and responsible lending considerations. Outstanding.",
            scoreType="ordinal",
            maxScore=5
        ),
    },
}

# Default custom evaluation scores for missing combinations
DEFAULT_CUSTOM_EVALUATION = {
    "disclaimerCompliance": EvaluationScore(
        score=3.0,
        rationale="Mock evaluation: Basic disclaimers present with room for improvement in prominence and comprehensiveness.",
        scoreType="ordinal",
        maxScore=5
    ),
    "prohibitedLanguage": EvaluationScore(
        score=3.0,
        rationale="Mock evaluation: No major prohibited language detected, though some phrasing could be more cautious.",
        scoreType="ordinal",
        maxScore=5
    ),
    "suitabilityAssessment": EvaluationScore(
        score=3.0,
        rationale="Mock evaluation: Some suitability considerations present, but gaps exist in personalization and escalation.",
        scoreType="ordinal",
        maxScore=5
    ),
    "riskDisclosure": EvaluationScore(
        score=3.0,
        rationale="Mock evaluation: Basic risk information provided, but lacks depth and prominence in key areas.",
        scoreType="ordinal",
        maxScore=5
    ),
}


def get_mock_custom_evaluation(model_id: str, scenario_id: str) -> Dict[str, EvaluationScore]:
    """Get mock custom FCA evaluation metrics for a model and scenario"""
    evaluation = MOCK_CUSTOM_EVALUATIONS.get((model_id, scenario_id))

    if evaluation:
        return evaluation

    # Return default scores if specific combination not found
    return DEFAULT_CUSTOM_EVALUATION
