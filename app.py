from fastapi import FastAPI

from database import create_tables
from monitor import check_service

app = FastAPI(title="Cloud Service Health Monitor")

# Make sure the database table exists when the API starts.
create_tables()


@app.get("/")
def read_root():
    return {"message": "Cloud Service Health Monitor API is running"}


@app.get("/check")
def check_url(url: str):
    return check_service(url)
