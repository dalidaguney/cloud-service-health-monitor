# Cloud Service Health Monitor

A Python application that checks website and API availability, measures response time, logs failed checks, and stores every result in SQLite.

## Features

- Checks multiple URLs sequentially.
- Reports `UP` for HTTP status codes from 200 to 299.
- Reports `DOWN` for other status codes, connection errors, and timeouts.
- Measures response time in milliseconds.
- Shows the local date and time with timezone information.
- Logs failed checks in `monitor.log`.
- Stores check results in the local SQLite database `monitor.db`.
- Provides a FastAPI endpoint for checking a service.
- Provides an endpoint for listing recent check results.
- Includes interactive API documentation with Swagger UI.
- Stops the monitoring script gracefully with Control + C.

## Technologies

- Python
- FastAPI
- Uvicorn
- requests
- SQLite through Python's standard `sqlite3` library
- Python standard library: time, datetime, and logging

## Installation

Install Python 3, then open a terminal in the project directory.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Monitoring Script

With the virtual environment activated, run:

```bash
python monitor.py
```

The script checks every URL in the `urls` list, saves each result to SQLite, waits for the configured interval, and starts the next round.

Press **Control + C** in the terminal to stop monitoring.

## FastAPI Server

Start the API server with:

```bash
uvicorn app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Check a service

Use the `/check` endpoint with a URL query parameter:

```text
http://127.0.0.1:8000/check?url=https://www.google.com
```

Example response:

```json
{
  "url": "https://www.google.com",
  "status": "UP",
  "status_code": 200,
  "response_time_ms": 523,
  "checked_at": "2026-09-26 23:54:07 +0300"
}
```

Every API check is also saved in `monitor.db`.

### List recent checks

Use the `/checks` endpoint to view saved results:

```text
http://127.0.0.1:8000/checks
```

The default response contains the 20 most recent checks. You can change the number with the `limit` parameter:

```text
http://127.0.0.1:8000/checks?limit=5
```

### Root endpoint

The root endpoint confirms that the API is running:

```text
http://127.0.0.1:8000/
```

Example response:

```json
{
  "message": "Cloud Service Health Monitor API is running"
}
```

## Database

The application creates a `checks` table in `monitor.db` automatically when the API starts or when a check is performed.

Each saved record contains:

- Record ID
- URL
- Service status
- HTTP status code
- Response time in milliseconds
- Check time

The database file is local and is excluded from Git with `.gitignore`.

## Configuration

Edit the `urls` list in `monitor.py` to choose which services the monitoring script checks:

```python
urls = [
    "https://www.google.com",
    "https://www.python.org",
]
```

Set the waiting interval with:

```python
CHECK_INTERVAL_SECONDS = 30
```

The application waits this many seconds after all URLs have been checked.

## Example Output

```text
https://www.google.com
Status: UP
Status Code: 200
Response Time: 523 ms
Checked At: 2026-09-26 23:06:59 +0300
```

Actual results depend on the network connection and the monitored service.

## Error Logging

Failed checks are appended to `monitor.log` in the directory where the application is run.

Each entry includes:

- Timestamp
- Log level
- URL
- HTTP status code or connection error details

If no HTTP response is received, the application displays `DOWN` with a status code of `N/A`. The displayed duration represents the failed attempt.

## Current Limitations

- Checks run sequentially.
- Uptime percentages are not calculated yet.
- URLs cannot be added or removed through the API yet.
- Monitoring runs locally while the script is active.
- A successful response from one URL does not guarantee that every feature of a service is working.

## Planned Improvements

- Uptime percentage calculations
- Service management endpoints for adding and removing URLs
- HTML dashboard
- Docker support
- PostgreSQL support
- CI/CD workflows
- Cloud deployment
