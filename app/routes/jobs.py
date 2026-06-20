import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job, Transaction, JobSummary
from app.worker.tasks import process_csv_job

router = APIRouter(prefix="/jobs", tags=["Jobs"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        return {"error": "Only CSV files are allowed"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job = Job(filename=file.filename, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)

    process_csv_job(file_path, job.id)

    return {
        "job_id": job.id,
        "status": job.status,
        "message": "CSV uploaded and processing started"
    }


@router.get("/")
def list_jobs(status: str = None, db: Session = Depends(get_db)):
    query = db.query(Job)

    if status:
        query = query.filter(Job.status == status)

    jobs = query.order_by(Job.created_at.desc()).all()

    return jobs


@router.get("/{job_id}/status")
def job_status(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {"error": "Job not found"}

    response = {
        "job_id": job.id,
        "status": job.status,
        "filename": job.filename,
        "row_count_raw": job.row_count_raw,
        "row_count_clean": job.row_count_clean,
        "error_message": job.error_message
    }

    if job.status == "completed" and job.summary:
        response["summary"] = {
            "anomaly_count": job.summary.anomaly_count,
            "risk_level": job.summary.risk_level,
            "narrative": job.summary.narrative
        }

    return response


@router.get("/{job_id}/results")
def job_results(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {"error": "Job not found"}

    transactions = db.query(Transaction).filter(Transaction.job_id == job_id).all()
    anomalies = [t for t in transactions if t.is_anomaly]
    summary = db.query(JobSummary).filter(JobSummary.job_id == job_id).first()

    category_breakdown = {}
    for txn in transactions:
        category_breakdown[txn.category] = category_breakdown.get(txn.category, 0) + txn.amount

    return {
        "job_id": job.id,
        "status": job.status,
        "cleaned_transactions": transactions,
        "flagged_anomalies": anomalies,
        "per_category_spend_breakdown": category_breakdown,
        "llm_generated_summary": summary
    }