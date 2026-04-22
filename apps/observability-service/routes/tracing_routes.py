"""API routes for distributed tracing."""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends

from database.connection import get_repository
from database.repository import ObservabilityRepository
from models.responses import TraceResponse, SpanResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/traces/{trace_id}", response_model=TraceResponse)
async def get_trace(trace_id: str, repo: ObservabilityRepository = Depends(get_repository)):
    """Get a trace by ID."""
    try:
        trace = repo.get_trace(trace_id)
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
        logger.error(f"Error getting trace: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/traces/{trace_id}/spans", response_model=List[SpanResponse])
async def get_trace_spans(trace_id: str, repo: ObservabilityRepository = Depends(get_repository)):
    """Get all spans for a trace."""
    try:
        spans = repo.get_spans_by_trace(trace_id)
        return [
            SpanResponse(
                spanId=span.span_id,
                traceId=span.trace_id,
                parentSpanId=span.parent_span_id,
                name=span.name,
                spanType=span.span_type,
                startTime=span.start_time,
                durationMs=span.duration_ms,
                attributes=span.attributes
            )
            for span in spans
        ]
    except Exception as e:
        logger.error(f"Error getting trace spans: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/traces/{trace_id}/flow")
async def get_trace_flow(trace_id: str, repo: ObservabilityRepository = Depends(get_repository)):
    """Get execution flow visualization data for a trace."""
    try:
        trace = repo.get_trace(trace_id)
        if not trace:
            raise HTTPException(status_code=404, detail=f"Trace {trace_id} not found")

        spans = repo.get_spans_by_trace(trace_id)

        # Build hierarchical flow structure
        span_map = {}
        root_spans = []

        for span in spans:
            span_data = {
                "spanId": span.span_id,
                "traceId": span.trace_id,
                "parentSpanId": span.parent_span_id,
                "name": span.name,
                "spanType": span.span_type,
                "startTime": span.start_time.isoformat(),
                "durationMs": span.duration_ms,
                "attributes": span.attributes,
                "children": []
            }
            span_map[span.span_id] = span_data

            if span.parent_span_id is None:
                root_spans.append(span_data)

        # Build parent-child relationships
        for span in spans:
            if span.parent_span_id and span.parent_span_id in span_map:
                span_map[span.parent_span_id]["children"].append(span_map[span.span_id])

        return {
            "traceId": trace.trace_id,
            "startTime": trace.start_time.isoformat(),
            "endTime": trace.end_time.isoformat() if trace.end_time else None,
            "status": trace.status,
            "rootSpans": root_spans,
            "totalSpans": len(spans)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting trace flow: {e}")
        raise HTTPException(status_code=500, detail=str(e))
