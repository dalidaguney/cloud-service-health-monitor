# Cloud Service Health Monitor

A Python application that periodically checks website and API availability, measures request duration, and logs failed checks.

## Features

- Checks multiple URLs sequentially.
- Reports `UP` for HTTP status codes from 200 to 299 and `DOWN` for other codes.
- Handles connection errors and timeouts.
- Displays check duration in milliseconds.
- Shows the local date and time when each check finishes.
- Records failed checks in `monitor.log`.
- Waits for a configurable interval between check rounds.
- Stops gracefully with Control + C.

## Technologies

- Python
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

## Usage

With the virtual environment activated, run:

```bash
python monitor.py
```

Press **Control + C** in the terminal to stop monitoring.

## Configuration

Edit the `urls` list in `monitor.py` to choose which services to monitor:

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

The application waits this many seconds after all URLs have been checked. The total duration of a round includes both the checks and the waiting interval.

## Example Output

```text
https://www.google.com
Status: UP
Status Code: 200
Response Time: 523 ms
Checked At: 2026-09-26 23:06:59
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
- Successful checks are not yet stored.
- Uptime percentages are not yet calculated.
- Reported duration includes network activity and response download time; it is not a measurement of server processing time alone.
- A successful response from one URL does not guarantee that every feature of a service is working.
- Monitoring runs locally while the script is active; cloud deployment is planned.

## Planned Improvements

- FastAPI backend for managing monitored services and accessing results
- Persistent check history in a database
- Uptime calculations and a dashboard
- Docker support
- CI/CD workflows and cloud deployment
