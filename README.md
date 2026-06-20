# Transaction Processing Pipeline

## Overview

The Transaction Processing Pipeline is a backend application built using FastAPI that processes transaction datasets uploaded in CSV format. The system performs automated data validation, cleaning, anomaly detection, spending analysis, and summary generation. Processed results are stored in a SQLite database and can be accessed through RESTful API endpoints.

This project demonstrates backend development, data engineering workflows, database integration, and analytical reporting in a scalable and modular architecture.

---

## Key Features

- CSV transaction file upload
- Automated data cleaning and validation
- Missing value handling
- Duplicate transaction removal
- Anomaly detection based on spending patterns
- Category-wise spending analysis
- Transaction summary generation
- SQLite database integration
- Job tracking and status monitoring
- Interactive API documentation with Swagger UI

---

## Technology Stack

| Component | Technology |
|------------|------------|
| Backend Framework | FastAPI |
| Language | Python |
| Data Processing | Pandas |
| Database | SQLite |
| ORM | SQLAlchemy |
| API Server | Uvicorn |
| Documentation | Swagger UI |

---

## Project Structure

```text
transaction-pipeline/
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── worker/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── __init__.py
│
├── transactions.csv
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd transaction-pipeline
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Interactive API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Upload Transaction File

```http
POST /jobs/upload
```

Uploads a CSV file and initiates a transaction processing job.

---

### Get Job Status

```http
GET /jobs/{job_id}/status
```

Returns the current processing status and metadata for a specific job.

---

### Get Processing Results

```http
GET /jobs/{job_id}/results
```

Returns:

- Cleaned transactions
- Flagged anomalies
- Category-wise spending breakdown
- Generated analytical summary

---

### List All Jobs

```http
GET /jobs/
```

Retrieves all processing jobs available in the system.

---

## Processing Workflow

1. Upload transaction CSV file
2. Validate incoming data
3. Clean and standardize records
4. Remove duplicate transactions
5. Detect anomalous spending patterns
6. Store processed records in SQLite
7. Generate analytical summaries
8. Expose results through REST APIs

---

## Sample Output

```json
{
  "anomaly_count": 5,
  "risk_level": "high",
  "top_merchants": {
    "IRCTC": 450697.69,
    "Jio Recharge": 270255.97,
    "Flipkart": 227539.88
  },
  "narrative": "Processed 85 transactions. Top merchants were IRCTC, Jio Recharge, and Flipkart. Detected 5 anomalous transactions."
}
```

---

## Results Generated

The system provides:

- Cleaned transaction records
- Anomaly detection reports
- Spending analytics by category
- Merchant-wise spending insights
- Risk assessment summary
- Processing statistics

---

## Future Enhancements

- Machine Learning-based anomaly detection
- Real-time transaction streaming
- Interactive analytics dashboard
- User authentication and authorization
- PostgreSQL integration
- Advanced fraud detection capabilities

---

## Author

**Ansh Kaushik**

B.Tech Student | AI & Data Science Enthusiast

---

## License

This project was developed as part of a backend engineering and data processing assignment for educational and evaluation purposes.
