from fastapi import FastAPI

from monitor import check_service

app = FastAPI(title="Cloud Service Health Monitor")
@app.get("/")
def read_root():
    return {"message": "Cloud Service Health Monitor API is running"}

@app.get("/check")
def check_url(url: str):
    return check_service(url)
