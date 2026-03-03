from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from models import EvaluationRequest, EvaluationResult
from services.mock_evaluator import MockEvaluatorService
from services.model_service import ModelService
from config.scenarios import get_all_scenarios, get_scenario_by_id


router = APIRouter()

# Initialize services
mock_evaluator = MockEvaluatorService()
model_service = ModelService()


@router.post("/evaluate", response_model=EvaluationResult)
async def evaluate(request: EvaluationRequest):
    """
    POST /api/v1/evaluate
    Evaluates a single query against a model
    """
    try:
        result = await mock_evaluator.evaluate(request)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation failed: {str(e)}"
        )


@router.get("/scenarios")
async def get_scenarios():
    """
    GET /api/v1/scenarios
    Lists all available regulatory scenarios
    """
    try:
        scenarios = get_all_scenarios()

        # Return simplified scenario list
        scenario_list = [scenario.to_list_item() for scenario in scenarios]

        return {"scenarios": scenario_list}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    """
    GET /api/v1/scenarios/:id
    Gets a specific scenario by ID
    """
    try:
        scenario = get_scenario_by_id(scenario_id)

        if not scenario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scenario not found: {scenario_id}"
            )

        return scenario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/models")
async def get_models():
    """
    GET /api/v1/models
    Lists all available models
    """
    try:
        models = model_service.get_all_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/models/{model_id}")
async def get_model(model_id: str):
    """
    GET /api/v1/models/:id
    Gets a specific model by ID
    """
    try:
        model = model_service.get_model_by_id(model_id)

        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model not found: {model_id}"
            )

        return model
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health")
async def health_check():
    """
    GET /api/v1/health
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "evaluator-service-python",
        "version": "1.0.0"
    }
