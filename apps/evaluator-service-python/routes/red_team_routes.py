"""Red Team API Routes"""
from fastapi import APIRouter, HTTPException
from models import RedTeamRequest, RedTeamSuiteResult
from services.red_team_service import RedTeamService

router = APIRouter()
red_team_service = RedTeamService()


@router.post("/red-team/run-suite", response_model=RedTeamSuiteResult)
async def run_red_team_suite(request: RedTeamRequest):
    """
    Run a red team attack suite against a model and scenario.

    This endpoint executes multiple adversarial attacks to test the model's
    compliance with governance thresholds and safety requirements.

    Returns:
        RedTeamSuiteResult with attack success rate, vulnerabilities, and detailed results
    """
    try:
        result = await red_team_service.run_attack_suite(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Red team suite failed: {str(e)}")


@router.get("/red-team/attack-categories")
async def get_attack_categories():
    """
    Get all available attack categories.

    Returns:
        List of attack categories with descriptions
    """
    return red_team_service.get_attack_categories()


@router.get("/red-team/attack-strategies")
async def get_attack_strategies():
    """
    Get all available attack strategies.

    Returns:
        List of attack strategies with descriptions
    """
    return red_team_service.get_attack_strategies()


@router.get("/red-team/scenarios/{scenario_id}/attack-count")
async def get_scenario_attack_count(scenario_id: str):
    """
    Get the count of attacks available for a specific scenario.

    Args:
        scenario_id: The scenario identifier

    Returns:
        Count of attacks for the scenario
    """
    count = red_team_service.get_scenario_attack_count(scenario_id)
    return {"scenarioId": scenario_id, "attackCount": count}


@router.get("/red-team/categories/{category}/attack-count")
async def get_category_attack_count(category: str):
    """
    Get the count of attacks available for a specific category.

    Args:
        category: The attack category

    Returns:
        Count of attacks for the category
    """
    count = red_team_service.get_category_attack_count(category)
    return {"category": category, "attackCount": count}
