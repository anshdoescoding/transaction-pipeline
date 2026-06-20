from datetime import datetime
from sqlalchemy.orm import Session

from app.worker.celery_app import celery_app
from app.database import SessionLocal
from app.models import Job, Transaction, JobSummary
from app.services.csv_processor import clean_csv
from app.services.anomaly_detector import detect_anomalies


@celery_app.task(name="app.worker.tasks.process_csv_job")
def process_csv_job(file_path, job_id):
    db: Session = SessionLocal()

    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        job.status = "processing"
        db.commit()

        df, raw_rows, clean_rows, missing_category_mask = clean_csv(file_path)
        df = detect_anomalies(df)

        job.row_count_raw = raw_rows
        job.row_count_clean = clean_rows

        for _, row in df.iterrows():
            txn = Transaction(
                job_id=job.id,
                txn_id=row.get("txn_id"),
                date=row.get("date"),
                merchant=row.get("merchant"),
                amount=float(row.get("amount", 0)),
                currency=row.get("currency"),
                status=row.get("status"),
                category=row.get("category"),
                account_id=row.get("account_id"),
                is_anomaly=bool(row.get("is_anomaly")),
                anomaly_reason=row.get("anomaly_reason"),
                llm_failed=False
            )
            db.add(txn)

        total_spend_inr = float(df[df["currency"] == "INR"]["amount"].sum())
        total_spend_usd = float(df[df["currency"] == "USD"]["amount"].sum())

        top_merchants = (
            df.groupby("merchant")["amount"]
            .sum()
            .sort_values(ascending=False)
            .head(3)
            .to_dict()
        )

        anomaly_count = int(df["is_anomaly"].sum())

        risk_level = "low"
        if anomaly_count >= 5:
            risk_level = "high"
        elif anomaly_count >= 2:
            risk_level = "medium"

        narrative = (
            f"Processed {clean_rows} transactions. "
            f"Top merchants were {', '.join(top_merchants.keys())}. "
            f"Detected {anomaly_count} anomalous transactions."
        )

        summary = JobSummary(
            job_id=job.id,
            total_spend_inr=total_spend_inr,
            total_spend_usd=total_spend_usd,
            top_merchants=top_merchants,
            anomaly_count=anomaly_count,
            narrative=narrative,
            risk_level=risk_level
        )

        db.add(summary)

        job.status = "completed"
        job.completed_at = datetime.utcnow()

        db.commit()

        return {"job_id": job.id, "status": "completed"}

    except Exception as e:
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = "failed"
            job.error_message = str(e)
            db.commit()

        return {"job_id": job_id, "status": "failed", "error": str(e)}

    finally:
        db.close()