from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    status = Column(String, default="pending")
    row_count_raw = Column(Integer, default=0)
    row_count_clean = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(String, nullable=True)

    transactions = relationship("Transaction", back_populates="job")
    summary = relationship("JobSummary", back_populates="job", uselist=False)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))

    txn_id = Column(String, nullable=True)
    date = Column(String)
    merchant = Column(String)
    amount = Column(Float)
    currency = Column(String)
    status = Column(String)
    category = Column(String)
    account_id = Column(String)

    is_anomaly = Column(Boolean, default=False)
    anomaly_reason = Column(String, nullable=True)

    llm_category = Column(String, nullable=True)
    llm_raw_response = Column(String, nullable=True)
    llm_failed = Column(Boolean, default=False)

    job = relationship("Job", back_populates="transactions")


class JobSummary(Base):
    __tablename__ = "job_summaries"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))

    total_spend_inr = Column(Float, default=0)
    total_spend_usd = Column(Float, default=0)
    top_merchants = Column(JSON)
    anomaly_count = Column(Integer, default=0)
    narrative = Column(String)
    risk_level = Column(String)

    job = relationship("Job", back_populates="summary")