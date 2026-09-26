from fastapi import FastAPI

from database import create_tables, get_recent_checks
from monitor import check_service


app = FastAPI(title="Cloud Service Health Monitor")

# Create the database table when the API starts.
create_tables()


@app.get("/")
def read_root():
    return {"message": "Cloud Service Health Monitor API is running"}


@app.get("/check")
def check_url(url: str):
    return check_service(url)


@app.get("/checks")
def list_checks(limit: int = 20):
    return get_recent_checks(limit)