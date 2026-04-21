"""Repository for database CRUD operations."""

import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from database.models import Trace, Span, EvaluationRun, AdversarialRun

logger = logging.getLogger(__name__)


class ObservabilityRepository:
    """Repository for observability data operations."""

    def __init__(self, db: Session):
        self.db = db

    # ========== Trace Operations ==========

    def create_trace(self, trace_id: str, start_time: Optional[datetime] = None) -> Trace:
        """Create a new trace."""
        trace = Trace(
            trace_id=trace_id,
            start_time=start_time or datetime.utcnow(),
            status="in_progress"
        )
        self.db.add(trace)
        self.db.commit()
        self.db.refresh(trace)
        logger.info(f"Created trace: {trace_id}")
        return trace

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """Get a trace by ID with all related spans."""
        return self.db.query(Trace).filter(Trace.trace_id == trace_id).first()

    def update_trace(
        self,
        trace_id: str,
        end_time: Optional[datetime] = None,
        status: Optional[str] = None,
        root_span_id: Optional[str] = None
    ) -> Optional[Trace]:
        """Update a trace."""
        trace = self.get_trace(trace_id)
        if not trace:
            logger.warning(f"Trace not found: {trace_id}")
            return None

        if end_time is not None:
            trace.end_time = end_time
        if status is not None:
            trace.status = status
        if root_span_id is not None:
            trace.root_span_id = root_span_id

        self.db.commit()
        self.db.refresh(trace)
        logger.info(f"Updated trace: {trace_id}")
        return trace

    # ========== Span Operations ==========

    def create_span(
        self,
        span_id: str,
        trace_id: str,
        name: str,
        span_type: str,
        parent_span_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        duration_ms: Optional[int] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> Span:
        """Create a new span."""
        span = Span(
            span_id=span_id,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            name=name,
            span_type=span_type,
            start_time=start_time or datetime.utcnow(),
            duration_ms=duration_ms,
            attributes=attributes
        )
        self.db.add(span)
        self.db.commit()
        self.db.refresh(span)
        logger.info(f"Created span: {span_id} ({name})")
        return span

    def get_spans_by_trace(self, trace_id: str) -> List[Span]:
        """Get all spans for a trace."""
        return self.db.query(Span).filter(Span.trace_id == trace_id).order_by(Span.start_time).all()

    # ========== Evaluation Run Operations ==========

    def save_evaluation_run(self, data: Dict[str, Any]) -> int:
        """Save an evaluation run."""
        evaluation_run = EvaluationRun(
            trace_id=data.get("trace_id"),
            model_id=data["model_id"],
            scenario_id=data["scenario_id"],
            query=data["query"],
            response=data["response"],
            evaluations=data["evaluations"],
            governance_decision=data["governance_decision"],
            duration_ms=data["duration_ms"],
            prompt_tokens=data.get("prompt_tokens"),
            completion_tokens=data.get("completion_tokens"),
            total_tokens=data.get("total_tokens"),
            estimated_cost=data.get("estimated_cost"),
            cost_currency=data.get("cost_currency", "USD"),
            timestamp=data.get("timestamp", datetime.utcnow())
        )
        self.db.add(evaluation_run)
        self.db.commit()
        self.db.refresh(evaluation_run)
        logger.info(f"Saved evaluation run: {evaluation_run.id}")
        return evaluation_run.id

    def get_evaluation_runs(
        self,
        model_id: Optional[str] = None,
        scenario_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[EvaluationRun]:
        """Get evaluation runs with filters."""
        query = self.db.query(EvaluationRun)

        if model_id:
            query = query.filter(EvaluationRun.model_id == model_id)
        if scenario_id:
            query = query.filter(EvaluationRun.scenario_id == scenario_id)
        if start_date:
            query = query.filter(EvaluationRun.timestamp >= start_date)
        if end_date:
            query = query.filter(EvaluationRun.timestamp <= end_date)

        return query.order_by(EvaluationRun.timestamp.desc()).limit(limit).offset(offset).all()

    def get_evaluation_run_by_id(self, run_id: int) -> Optional[EvaluationRun]:
        """Get a specific evaluation run by ID."""
        return self.db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()

    # ========== Adversarial Run Operations ==========

    def save_adversarial_run(self, data: Dict[str, Any]) -> int:
        """Save an adversarial run."""
        adversarial_run = AdversarialRun(
            trace_id=data.get("trace_id"),
            scenario_id=data["scenario_id"],
            model_id=data["model_id"],
            total_attacks=data["total_attacks"],
            successful_attacks=data["successful_attacks"],
            blocked_attacks=data["blocked_attacks"],
            attack_success_rate=data["attack_success_rate"],
            vulnerabilities=data["vulnerabilities"],
            all_results=data["all_results"],
            timestamp=data.get("timestamp", datetime.utcnow())
        )
        self.db.add(adversarial_run)
        self.db.commit()
        self.db.refresh(adversarial_run)
        logger.info(f"Saved adversarial run: {adversarial_run.id}")
        return adversarial_run.id

    def get_adversarial_runs(
        self,
        model_id: Optional[str] = None,
        scenario_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AdversarialRun]:
        """Get adversarial runs with filters."""
        query = self.db.query(AdversarialRun)

        if model_id:
            query = query.filter(AdversarialRun.model_id == model_id)
        if scenario_id:
            query = query.filter(AdversarialRun.scenario_id == scenario_id)
        if start_date:
            query = query.filter(AdversarialRun.timestamp >= start_date)
        if end_date:
            query = query.filter(AdversarialRun.timestamp <= end_date)

        return query.order_by(AdversarialRun.timestamp.desc()).limit(limit).offset(offset).all()

    def get_adversarial_run_by_id(self, run_id: int) -> Optional[AdversarialRun]:
        """Get a specific adversarial run by ID."""
        return self.db.query(AdversarialRun).filter(AdversarialRun.id == run_id).first()

    # ========== Analytics Operations ==========

    def get_aggregated_metrics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        model_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get aggregated metrics across all runs."""
        eval_query = self.db.query(EvaluationRun)
        adv_query = self.db.query(AdversarialRun)

        if start_date:
            eval_query = eval_query.filter(EvaluationRun.timestamp >= start_date)
            adv_query = adv_query.filter(AdversarialRun.timestamp >= start_date)
        if end_date:
            eval_query = eval_query.filter(EvaluationRun.timestamp <= end_date)
            adv_query = adv_query.filter(AdversarialRun.timestamp <= end_date)
        if model_id:
            eval_query = eval_query.filter(EvaluationRun.model_id == model_id)
            adv_query = adv_query.filter(AdversarialRun.model_id == model_id)

        # Evaluation metrics
        eval_stats = eval_query.with_entities(
            func.count(EvaluationRun.id).label("total_runs"),
            func.avg(EvaluationRun.duration_ms).label("avg_latency"),
            func.sum(EvaluationRun.estimated_cost).label("total_cost"),
            func.sum(EvaluationRun.total_tokens).label("total_tokens")
        ).first()

        # Adversarial metrics
        adv_stats = adv_query.with_entities(
            func.count(AdversarialRun.id).label("total_suites"),
            func.avg(AdversarialRun.attack_success_rate).label("avg_asr")
        ).first()

        return {
            "evaluation_runs": {
                "total_runs": eval_stats.total_runs or 0,
                "avg_latency_ms": float(eval_stats.avg_latency) if eval_stats.avg_latency else 0,
                "total_cost": float(eval_stats.total_cost) if eval_stats.total_cost else 0,
                "total_tokens": int(eval_stats.total_tokens) if eval_stats.total_tokens else 0
            },
            "adversarial_runs": {
                "total_suites": adv_stats.total_suites or 0,
                "avg_attack_success_rate": float(adv_stats.avg_asr) if adv_stats.avg_asr else 0
            }
        }
