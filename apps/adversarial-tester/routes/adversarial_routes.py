"""Adversarial Testing API Routes"""
from fastapi import APIRouter, HTTPException
from models import RedTeamRequest, RedTeamSuiteResult
from services.adversarial_service import AdversarialService

router = APIRouter()
adversarial_service = AdversarialService()


@router.post("/adversarial/run-suite", response_model=RedTeamSuiteResult)
async def run_adversarial_suite(request: RedTeamRequest):
    """
    Run an adversarial attack suite against a model and scenario.

    This endpoint executes multiple adversarial attacks to test the model's
    compliance with governance thresholds and safety requirements.

    Returns:
        RedTeamSuiteResult with attack success rate, vulnerabilities, and detailed results
    """
    try:
        result = await adversarial_service.run_attack_suite(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Adversarial suite failed: {str(e)}")


@router.get("/adversarial/attack-categories")
async def get_attack_categories():
    """
    Get all available attack categories.

    Returns:
        List of attack categories with descriptions
    """
    return adversarial_service.get_attack_categories()


@router.get("/adversarial/attack-strategies")
async def get_attack_strategies():
    """
    Get all available attack strategies.

    Returns:
        List of attack strategies with descriptions
    """
    return adversarial_service.get_attack_strategies()


@router.get("/adversarial/threat-types")
async def get_threat_types():
    """
    Get all available threat types.

    Returns:
        List of threat types with descriptions
    """
    return adversarial_service.get_threat_types()


@router.get("/adversarial/scenarios/{scenario_id}/attack-count")
async def get_scenario_attack_count(scenario_id: str):
    """
    Get the count of attacks available for a specific scenario.

    Args:
        scenario_id: The scenario identifier

    Returns:
        Count of attacks for the scenario
    """
    count = adversarial_service.get_scenario_attack_count(scenario_id)
    return {"scenarioId": scenario_id, "attackCount": count}


@router.get("/adversarial/categories/{category}/attack-count")
async def get_category_attack_count(category: str):
    """
    Get the count of attacks available for a specific category.

    Args:
        category: The attack category

    Returns:
        Count of attacks for the category
    """
    count = adversarial_service.get_category_attack_count(category)
    return {"category": category, "attackCount": count}


@router.get("/adversarial/threat-types/{threat_type}/attack-count")
async def get_threat_type_attack_count(threat_type: str):
    """
    Get the count of attacks available for a specific threat type.

    Args:
        threat_type: The threat type

    Returns:
        Count of attacks for the threat type
    """
    count = adversarial_service.get_threat_type_attack_count(threat_type)
    return {"threatType": threat_type, "attackCount": count}


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "model-tester",
        "version": "1.0.0"
    }
