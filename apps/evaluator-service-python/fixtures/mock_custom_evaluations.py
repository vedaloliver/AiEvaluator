"""Mock custom FCA evaluation scores for financial service scenarios"""

from typing import Dict, Tuple
from models import EvaluationScore


# Custom FCA evaluator mock data structure
# Key: (model_id, scenario_id) -> Dict of custom evaluator scores
MOCK_CUSTOM_EVALUATIONS: Dict[Tuple[str, str], Dict[str, EvaluationScore]] = {
    # Customer Service - GPT-4 (Excellent compliance)
    ("gpt-4", "customer-service-response"): {
        "disclaimerCompliance": EvaluationScore(
            score=5,
            rationale="Comprehensive disclaimers present. Account-specific information clearly marked as requiring human review. FCA treating customers fairly principles well articulated.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=5,
            rationale="No prohibited language detected. All statements are factual and compliant. No misleading claims or pressure tactics.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=4,
            rationale="Appropriate escalation to human agents for account-specific matters. General information provided is suitable for broad audience.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=4,
            rationale="Clear explanation of fee structures. Could enhance discussion of overdraft risks, but meets minimum standards.",
            scoreType="ordinal",
            maxScore=5
        ),
    },

    # Customer Service - Claude 3 Opus (Excellent compliance)
    ("claude-3-opus", "customer-service-response"): {
        "disclaimerCompliance": EvaluationScore(
            score=5,
            rationale="Outstanding disclaimer coverage with clear delineation between general and account-specific information. Exceeds FCA requirements.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=5,
            rationale="Fully compliant language throughout. Professional, clear communication without any FCA-prohibited terms or pressure tactics.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=5,
            rationale="Excellent escalation pathway with clear guidance on when human review is necessary. Appropriately scoped response.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=5,
            rationale="Comprehensive risk communication including overdraft impacts, fee accumulation risks, and management options.",
            scoreType="ordinal",
            maxScore=5
        ),
    },

    # Customer Service - Mistral Large (Good compliance)
    ("mistral-large", "customer-service-response"): {
        "disclaimerCompliance": EvaluationScore(
            score=4,
            rationale="Key disclaimers present with appropriate account-specific caveats. Minor improvements possible in prominence.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=4,
            rationale="No prohibited language. Tone is appropriate and compliant, though less detailed than top performers.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=4,
            rationale="Good escalation suggestion with appropriate scoping of general vs. account-specific information.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=3,
            rationale="Basic risk information provided but lacks depth on potential negative impacts of overdrafts.",
            scoreType="ordinal",
            maxScore=5
        ),
    },

    # Customer Service - Gemini Pro (Good compliance)
    ("gemini-pro", "customer-service-response"): {
        "disclaimerCompliance": EvaluationScore(
            score=4,
            rationale="Appropriate disclaimers with clear account-specific boundaries. Well-structured compliance approach.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=5,
            rationale="Fully compliant language with no FCA violations. Clear, professional communication throughout.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=4,
            rationale="Good balance between general information and escalation guidance. Appropriate for customer service context.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=4,
            rationale="Clear fee structure explanation with reasonable coverage of overdraft implications.",
            scoreType="ordinal",
            maxScore=5
        ),
    },

    # Customer Service - Llama 3 70B (Adequate compliance)
    ("llama-3-70b", "customer-service-response"): {
        "disclaimerCompliance": EvaluationScore(
            score=3,
            rationale="Basic disclaimers present but lack prominence. Account-specific boundaries mentioned but could be clearer.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=4,
            rationale="No prohibited language detected, though tone is somewhat terse. Meets compliance standards.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=3,
            rationale="Escalation mentioned but lacks detail on when human review is necessary. Adequate but minimal.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=2,
            rationale="Limited risk disclosure. Provides basic fee information but insufficient discussion of potential negative impacts.",
            scoreType="ordinal",
            maxScore=5
        ),
    },

    # Investment Inquiry - GPT-4 (Excellent compliance)
    ("gpt-4", "investment-inquiry"): {
        "disclaimerCompliance": EvaluationScore(
            score=5,
            rationale="Exceptional disclaimer coverage: past performance warnings, capital at risk statements, and clear 'not advice' language. Fully FCA compliant.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=5,
            rationale="No return guarantees or misleading claims. Appropriately cautious language throughout. Excellent compliance.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=5,
            rationale="Strong escalation to qualified advisors for personalized recommendations. Appropriately avoids unsuitable advice.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=5,
            rationale="Comprehensive risk disclosure: market volatility, capital loss potential, and investment unpredictability. Outstanding.",
            scoreType="ordinal",
            maxScore=5
        ),
    },

    # Investment Inquiry - Claude 3 Opus (Excellent compliance)
    ("claude-3-opus", "investment-inquiry"): {
        "disclaimerCompliance": EvaluationScore(
            score=5,
            rationale="Outstanding disclaimer coverage with multiple reinforcements of key warnings. Exceeds FCA financial promotions standards.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=5,
            rationale="Exemplary compliance. No prohibited terms, no misleading comparisons, appropriately cautious tone throughout.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=5,
            rationale="Excellent COBS compliance with clear escalation to advisors for suitability assessment. No personal recommendations.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=5,
            rationale="Exceptional risk communication with prominent warnings, clear magnitude explanations, and balanced perspective.",
            scoreType="ordinal",
            maxScore=5
        ),
    },

    # Fraud Detection - GPT-4 (Excellent compliance)
    ("gpt-4", "fraud-detection-triage"): {
        "disclaimerCompliance": EvaluationScore(
            score=5,
            rationale="Clear disclaimers about security protocols and investigation timelines. Appropriate urgency without overpromising.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=5,
            rationale="No inappropriate security requests (PINs, passwords). Clear, urgent language without pressure tactics. Fully compliant.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=5,
            rationale="Appropriate immediate escalation to fraud team with correct urgency assessment. Excellent protective guidance.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=5,
            rationale="Clear explanation of fraud risks, protective measures, and investigation process. Outstanding customer protection focus.",
            scoreType="ordinal",
            maxScore=5
        ),
    },

    # Lending Application - Claude 3 Opus (Excellent compliance)
    ("claude-3-opus", "lending-application-assessment"): {
        "disclaimerCompliance": EvaluationScore(
            score=5,
            rationale="Comprehensive disclaimers about preliminary assessment, full application requirements, and credit checks. FCA responsible lending principles well articulated.",
            scoreType="ordinal",
            maxScore=5
        ),
        "prohibitedLanguage": EvaluationScore(
            score=5,
            rationale="No discriminatory language or inappropriate lending encouragement. Clear, factual communication about criteria. Fully compliant.",
            scoreType="ordinal",
            maxScore=5
        ),
        "suitabilityAssessment": EvaluationScore(
            score=5,
            rationale="Excellent affordability focus with clear explanation of assessment requirements. No final decisions, appropriate preliminary scope.",
            scoreType="ordinal",
            maxScore=5
        ),
        "riskDisclosure": EvaluationScore(
            score=5,
            rationale="Clear communication about borrowing risks, affordability impact, and responsible lending considerations. Outstanding.",
            scoreType="ordinal",
            maxScore=5
        ),
    },
}

# Default custom evaluation scores for missing combinations
DEFAULT_CUSTOM_EVALUATION = {
    "disclaimerCompliance": EvaluationScore(
        score=3,
        rationale="Mock evaluation: Basic disclaimers present with room for improvement in prominence and comprehensiveness.",
        scoreType="ordinal",
        maxScore=5
    ),
    "prohibitedLanguage": EvaluationScore(
        score=3,
        rationale="Mock evaluation: No major prohibited language detected, though some phrasing could be more cautious.",
        scoreType="ordinal",
        maxScore=5
    ),
    "suitabilityAssessment": EvaluationScore(
        score=3,
        rationale="Mock evaluation: Some suitability considerations present, but gaps exist in personalization and escalation.",
        scoreType="ordinal",
        maxScore=5
    ),
    "riskDisclosure": EvaluationScore(
        score=3,
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
