"""API routes for analytics and querying observability data."""

import logging
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from database.connection import get_db_session
from database.repository import ObservabilityRepository
from models.responses import (
    EvaluationRunResponse,
    AdversarialRunResponse,
    AnalyticsSummaryResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def get_repository(db: Session = Depends(get_db_session)) -> ObservabilityRepository:
    """Dependency to get repository instance."""
    try:
        return ObservabilityRepository(db)
    finally:
        db.close()


@router.get("/analytics/evaluation-runs", response_model=List[EvaluationRunResponse])
async def get_evaluation_runs(
    model_id: Optional[str] = Query(None, alias="modelId"),
    scenario_id: Optional[str] = Query(None, alias="scenarioId"),
    start_date: Optional[datetime] = Query(None, alias="startDate"),
    end_date: Optional[datetime] = Query(None, alias="endDate"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    repo: ObservabilityRepository = Depends(get_repository)
):
    """Get evaluation runs with filters."""
    try:
        runs = repo.get_evaluation_runs(
            model_id=model_id,
            scenario_id=scenario_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset
        )
        return [
            EvaluationRunResponse(
                id=run.id,
                traceId=run.trace_id,
                modelId=run.model_id,
                scenarioId=run.scenario_id,
                query=run.query,
                response=run.response,
                evaluations=run.evaluations,
                governanceDecision=run.governance_decision,
                durationMs=run.duration_ms,
                promptTokens=run.prompt_tokens,
                completionTokens=run.completion_tokens,
                totalTokens=run.total_tokens,
                estimatedCost=run.estimated_cost,
                costCurrency=run.cost_currency,
                timestamp=run.timestamp
            )
            for run in runs
        ]
    except Exception as e:
        logger.error(f"Error getting evaluation runs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/evaluation-runs/{run_id}", response_model=EvaluationRunResponse)
async def get_evaluation_run(run_id: int, repo: ObservabilityRepository = Depends(get_repository)):
    """Get a specific evaluation run by ID."""
    try:
        run = repo.get_evaluation_run_by_id(run_id)
        if not run:
            raise HTTPException(status_code=404, detail=f"Evaluation run {run_id} not found")

        return EvaluationRunResponse(
            id=run.id,
            traceId=run.trace_id,
            modelId=run.model_id,
            scenarioId=run.scenario_id,
            query=run.query,
            response=run.response,
            evaluations=run.evaluations,
            governanceDecision=run.governance_decision,
            durationMs=run.duration_ms,
            promptTokens=run.prompt_tokens,
            completionTokens=run.completion_tokens,
            totalTokens=run.total_tokens,
            estimatedCost=run.estimated_cost,
            costCurrency=run.cost_currency,
            timestamp=run.timestamp
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting evaluation run: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/adversarial-runs", response_model=List[AdversarialRunResponse])
async def get_adversarial_runs(
    model_id: Optional[str] = Query(None, alias="modelId"),
    scenario_id: Optional[str] = Query(None, alias="scenarioId"),
    start_date: Optional[datetime] = Query(None, alias="startDate"),
    end_date: Optional[datetime] = Query(None, alias="endDate"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    repo: ObservabilityRepository = Depends(get_repository)
):
    """Get adversarial runs with filters."""
    try:
        runs = repo.get_adversarial_runs(
            model_id=model_id,
            scenario_id=scenario_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset
        )
        return [
            AdversarialRunResponse(
                id=run.id,
                traceId=run.trace_id,
                scenarioId=run.scenario_id,
                modelId=run.model_id,
                totalAttacks=run.total_attacks,
                successfulAttacks=run.successful_attacks,
                blockedAttacks=run.blocked_attacks,
                attackSuccessRate=run.attack_success_rate,
                vulnerabilities=run.vulnerabilities,
                allResults=run.all_results,
                timestamp=run.timestamp
            )
            for run in runs
        ]
    except Exception as e:
        logger.error(f"Error getting adversarial runs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/adversarial-runs/{run_id}", response_model=AdversarialRunResponse)
async def get_adversarial_run(run_id: int, repo: ObservabilityRepository = Depends(get_repository)):
    """Get a specific adversarial run by ID."""
    try:
        run = repo.get_adversarial_run_by_id(run_id)
        if not run:
            raise HTTPException(status_code=404, detail=f"Adversarial run {run_id} not found")

        return AdversarialRunResponse(
            id=run.id,
            traceId=run.trace_id,
            scenarioId=run.scenario_id,
            modelId=run.model_id,
            totalAttacks=run.total_attacks,
            successfulAttacks=run.successful_attacks,
            blockedAttacks=run.blocked_attacks,
            attackSuccessRate=run.attack_success_rate,
            vulnerabilities=run.vulnerabilities,
            allResults=run.all_results,
            timestamp=run.timestamp
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting adversarial run: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(
    start_date: Optional[datetime] = Query(None, alias="startDate"),
    end_date: Optional[datetime] = Query(None, alias="endDate"),
    model_id: Optional[str] = Query(None, alias="modelId"),
    repo: ObservabilityRepository = Depends(get_repository)
):
    """Get aggregated analytics summary."""
    try:
        metrics = repo.get_aggregated_metrics(
            start_date=start_date,
            end_date=end_date,
            model_id=model_id
        )
        return AnalyticsSummaryResponse(
            evaluationRuns=metrics["evaluation_runs"],
            adversarialRuns=metrics["adversarial_runs"]
        )
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
