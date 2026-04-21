"""API routes for ingesting observability data."""

import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database.connection import get_db_session
from database.repository import ObservabilityRepository
from models.requests import (
    TraceCreateRequest,
    TraceUpdateRequest,
    SpanCreateRequest,
    EvaluationRunRequest,
    AdversarialRunRequest,
)
from models.responses import TraceResponse, SpanResponse

logger = logging.getLogger(__name__)
router = APIRouter()


def get_repository(db: Session = Depends(get_db_session)) -> ObservabilityRepository:
    """Dependency to get repository instance."""
    try:
        return ObservabilityRepository(db)
    finally:
        db.close()


@router.post("/traces", response_model=TraceResponse, status_code=201)
async def create_trace(request: TraceCreateRequest, repo: ObservabilityRepository = Depends(get_repository)):
    """Create a new trace."""
    try:
        trace = repo.create_trace(
            trace_id=request.trace_id,
            start_time=request.start_time
        )
        return TraceResponse(
            traceId=trace.trace_id,
            startTime=trace.start_time,
            endTime=trace.end_time,
            rootSpanId=trace.root_span_id,
            status=trace.status
        )
    except Exception as e:
        logger.error(f"Error creating trace: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/traces/{trace_id}", response_model=TraceResponse)
async def update_trace(
    trace_id: str,
    request: TraceUpdateRequest,
    repo: ObservabilityRepository = Depends(get_repository)
):
    """Update a trace."""
    try:
        trace = repo.update_trace(
            trace_id=trace_id,
            end_time=request.end_time,
            status=request.status,
            root_span_id=request.root_span_id
        )
        if not trace:
            raise HTTPException(status_code=404, detail=f"Trace {trace_id} not found")

        return TraceResponse(
            traceId=trace.trace_id,
            startTime=trace.start_time,
            endTime=trace.end_time,
            rootSpanId=trace.root_span_id,
            status=trace.status
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating trace: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/spans", response_model=SpanResponse, status_code=201)
async def create_span(request: SpanCreateRequest, repo: ObservabilityRepository = Depends(get_repository)):
    """Create a new span."""
    try:
        span = repo.create_span(
            span_id=request.span_id,
            trace_id=request.trace_id,
            name=request.name,
            span_type=request.span_type,
            parent_span_id=request.parent_span_id,
            start_time=request.start_time,
            duration_ms=request.duration_ms,
            attributes=request.attributes
        )
        return SpanResponse(
            spanId=span.span_id,
            traceId=span.trace_id,
            parentSpanId=span.parent_span_id,
            name=span.name,
            spanType=span.span_type,
            startTime=span.start_time,
            durationMs=span.duration_ms,
            attributes=span.attributes
        )
    except Exception as e:
        logger.error(f"Error creating span: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluation-runs", status_code=201)
async def store_evaluation_run(
    request: EvaluationRunRequest,
    repo: ObservabilityRepository = Depends(get_repository)
):
    """Store an evaluation run."""
    try:
        run_id = repo.save_evaluation_run(request.model_dump(by_alias=False))
        return {"id": run_id, "message": "Evaluation run stored successfully"}
    except Exception as e:
        logger.error(f"Error storing evaluation run: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/adversarial-runs", status_code=201)
async def store_adversarial_run(
    request: AdversarialRunRequest,
    repo: ObservabilityRepository = Depends(get_repository)
):
    """Store an adversarial run."""
    try:
        run_id = repo.save_adversarial_run(request.model_dump(by_alias=False))
        return {"id": run_id, "message": "Adversarial run stored successfully"}
    except Exception as e:
        logger.error(f"Error storing adversarial run: {e}")
        raise HTTPException(status_code=500, detail=str(e))
