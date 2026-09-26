# Cloud Service Health Monitor

A Python application that periodically checks website and API availability, measures request duration, and logs failed checks.

## Features

- Checks multiple URLs sequentially.
- Reports `UP` for HTTP status codes from 200 to 299 and `DOWN` for other codes.
- Handles connection errors and timeouts.
- Displays response time in milliseconds.
- Shows the local date and time with timezone information.
- Records failed checks in `monitor.log`.
- Waits for a configurable interval between check rounds.
- Provides a FastAPI endpoint for checking a service.
- Provides interactive API documentation with Swagger UI.
- Stops gracefully with Control + C.

## Technologies

- Python
- FastAPI
- Uvicorn
- requests
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

## Monitoring Script Usage

With the virtual environment activated, run:

```bash
python monitor.py
```

The script checks every URL in the `urls` list, waits for the configured interval, and starts the next round.

Press **Control + C** in the terminal to stop monitoring.

## FastAPI API

Start the API server with:

```bash
uvicorn app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

The root endpoint confirms that the API is running:

```text
http://127.0.0.1:8000/
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Check a Service Through the API

Use the `/check` endpoint with a URL query parameter:

```text
http://127.0.0.1:8000/check?url=https://www.google.com
```

The endpoint returns JSON containing:

- URL
- Service status
- HTTP status code
- Response time in milliseconds
- Check time

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

## Configuration

Edit the `urls` list in `monitor.py` to choose which services the monitoring script checks:

```python
urls = [
    "https://www.google.com",
    "https://www.python.org",
]
```

Set the waiting interval using:

```python
CHECK_INTERVAL_SECONDS = 30
```

The application waits this many seconds after all URLs have been checked. A complete monitoring round includes the check durations and this waiting time.

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

If no HTTP response is received, the application displays `DOWN` with a status code of `N/A`. In that case, the displayed duration represents the failed attempt rather than a received response.

## Current Limitations

- Checks run sequentially.
- Successful checks are not yet stored in a database.
- Uptime percentages are not yet calculated.
- The API currently checks a URL but does not save its result.
- Reported duration includes network activity and response download time; it is not a measurement of server processing time alone.
- Monitoring runs locally while the script is active.
- A successful response from one URL does not guarantee that every feature of a service is working.

## Planned Improvements

- SQLite database for persistent check history
- Service management endpoints for adding and removing URLs
- Uptime percentage calculations
- HTML dashboard
- Docker support
- PostgreSQL support
- CI/CD workflows
- Cloud deployment
