"""Adversarial Testing API Routes"""
from fastapi import APIRouter, HTTPException
from models import RedTeamRequest, RedTeamSuiteResult
from models.azure_red_team import AzureRedTeamRequest, AzureRedTeamRunResult, TaxonomyUploadResult
from models.taxonomy import ProhibitedActionsTaxonomy
from services.adversarial_service import AdversarialService
from services.azure_red_team_service import AzureRedTeamService, AzureNotConfiguredError

router = APIRouter()
adversarial_service = AdversarialService()
azure_red_team_service = AzureRedTeamService()


@router.post("/adversarial/run-suite", response_model=RedTeamSuiteResult)
async def run_adversarial_suite(request: RedTeamRequest):
    """
    Run an adversarial attack suite against a model and scenario.

    Executes multiple adversarial attacks to test compliance with governance
    thresholds and safety requirements.  Each attack result includes a
    ``scorerResult`` field with a PyRIT-compatible pass/fail verdict.
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
    """Get all available attack categories."""
    return adversarial_service.get_attack_categories()


@router.get("/adversarial/attack-strategies")
async def get_attack_strategies():
    """
    Get all available attack strategies.

    Returns two groups identified by the ``type`` field:
    - ``conceptual`` — attack framing labels used on seed attacks
      (direct, social-engineering, implicit)
    - ``transformation`` — query obfuscation techniques with their PyRIT
      canonical names (Base64, ROT13, Leetspeak, …)
    """
    return adversarial_service.get_attack_strategies()


@router.get("/adversarial/threat-types")
async def get_threat_types():
    """Get all available threat types."""
    return adversarial_service.get_threat_types()


@router.get("/adversarial/scenarios/{scenario_id}/attack-count")
async def get_scenario_attack_count(scenario_id: str):
    count = adversarial_service.get_scenario_attack_count(scenario_id)
    return {"scenarioId": scenario_id, "attackCount": count}


@router.get("/adversarial/categories/{category}/attack-count")
async def get_category_attack_count(category: str):
    count = adversarial_service.get_category_attack_count(category)
    return {"category": category, "attackCount": count}


@router.get("/adversarial/threat-types/{threat_type}/attack-count")
async def get_threat_type_attack_count(threat_type: str):
    count = adversarial_service.get_threat_type_attack_count(threat_type)
    return {"threatType": threat_type, "attackCount": count}


@router.post("/adversarial/taxonomy", response_model=TaxonomyUploadResult)
async def upload_taxonomy(taxonomy: ProhibitedActionsTaxonomy):
    """
    Register an FCA taxonomy with Azure AI Foundry.

    Accepts a ``ProhibitedActionsTaxonomy`` payload.  Returns HTTP 501 when
    Azure is not configured or the SDK feature is not yet available.
    """
    try:
        return await azure_red_team_service.upload_taxonomy(taxonomy)
    except (AzureNotConfiguredError, NotImplementedError) as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Taxonomy upload failed: {str(e)}")


@router.post("/adversarial/run-cloud", response_model=AzureRedTeamRunResult)
async def run_cloud_eval(request: AzureRedTeamRequest):
    """
    Create a PyRIT red team eval run via Azure AI Foundry.

    Requires ``USE_AZURE_RED_TEAM=true`` and a valid
    ``AZURE_AI_PROJECT_ENDPOINT``.  Returns HTTP 501 when Azure is not
    configured or the SDK feature is not yet available.
    """
    try:
        return await azure_red_team_service.run_cloud_eval(request)
    except (AzureNotConfiguredError, NotImplementedError) as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloud eval run failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "adversarial-tester",
        "version": "1.0.0",
    }
