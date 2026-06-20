from fastapi import FastAPI
from app.database import Base, engine
from app.routes import jobs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Transaction Processing Pipeline")

app.include_router(jobs.router)

@app.get("/")
def home():
    return {"message": "Transaction Processing API is running"}