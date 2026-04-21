"""SQLAlchemy database models for observability data."""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Trace(Base):
    """Trace model for tracking end-to-end flows."""

    __tablename__ = "traces"

    trace_id = Column(String, primary_key=True)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    root_span_id = Column(String, nullable=True)
    status = Column(String, nullable=False, default="in_progress")  # in_progress, completed, error

    # Relationships
    spans = relationship("Span", back_populates="trace", cascade="all, delete-orphan")
    evaluation_runs = relationship("EvaluationRun", back_populates="trace", cascade="all, delete-orphan")
    adversarial_runs = relationship("AdversarialRun", back_populates="trace", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trace(trace_id={self.trace_id}, status={self.status})>"


class Span(Base):
    """Span model for tracking individual operations within a trace."""

    __tablename__ = "spans"

    span_id = Column(String, primary_key=True)
    trace_id = Column(String, ForeignKey("traces.trace_id"), nullable=False)
    parent_span_id = Column(String, nullable=True)
    name = Column(String, nullable=False)
    span_type = Column(String, nullable=False)  # llm_call, evaluation, retrieval, reasoning, adversarial_test
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    duration_ms = Column(Integer, nullable=True)
    attributes = Column(JSON, nullable=True)  # Flexible metadata

    # Relationships
    trace = relationship("Trace", back_populates="spans")

    # Indexes
    __table_args__ = (
        Index('idx_trace_id', 'trace_id'),
        Index('idx_span_type', 'span_type'),
        Index('idx_start_time', 'start_time'),
    )

    def __repr__(self):
        return f"<Span(span_id={self.span_id}, name={self.name}, type={self.span_type})>"


class EvaluationRun(Base):
    """Evaluation run model for storing per-run evaluation results."""

    __tablename__ = "evaluation_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, ForeignKey("traces.trace_id"), nullable=True)
    model_id = Column(String, nullable=False)
    scenario_id = Column(String, nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)

    # Metrics as JSON (safety, relevance, coherence, fluency, FCA)
    evaluations = Column(JSON, nullable=False)
    governance_decision = Column(JSON, nullable=False)

    # Performance metrics
    duration_ms = Column(Integer, nullable=False)

    # Observability fields
    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    cost_currency = Column(String, default="USD")

    # Timestamp
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    trace = relationship("Trace", back_populates="evaluation_runs")

    # Indexes
    __table_args__ = (
        Index('idx_model_id', 'model_id'),
        Index('idx_scenario_id', 'scenario_id'),
        Index('idx_timestamp', 'timestamp'),
        Index('idx_trace_id_eval', 'trace_id'),
        Index('idx_model_scenario', 'model_id', 'scenario_id'),
    )

    def __repr__(self):
        return f"<EvaluationRun(id={self.id}, model={self.model_id}, scenario={self.scenario_id})>"


class AdversarialRun(Base):
    """Adversarial run model for storing red team suite results."""

    __tablename__ = "adversarial_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String, ForeignKey("traces.trace_id"), nullable=True)
    scenario_id = Column(String, nullable=False)
    model_id = Column(String, nullable=False)

    # Attack metrics
    total_attacks = Column(Integer, nullable=False)
    successful_attacks = Column(Integer, nullable=False)
    blocked_attacks = Column(Integer, nullable=False)
    attack_success_rate = Column(Float, nullable=False)

    # Store full results as JSON
    vulnerabilities = Column(JSON, nullable=False)
    all_results = Column(JSON, nullable=False)

    # Timestamp
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    trace = relationship("Trace", back_populates="adversarial_runs")

    # Indexes
    __table_args__ = (
        Index('idx_model_scenario_adv', 'model_id', 'scenario_id'),
        Index('idx_timestamp_adv', 'timestamp'),
        Index('idx_trace_id_adv', 'trace_id'),
    )

    def __repr__(self):
        return f"<AdversarialRun(id={self.id}, model={self.model_id}, asr={self.attack_success_rate})>"
