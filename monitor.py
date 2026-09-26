import logging
import time
from datetime import datetime, timezone

import requests

# Save error messages to monitor.log in the current working directory.
logging.basicConfig(
    filename="monitor.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Use a named logger for this module.
logger = logging.getLogger(__name__)


def check_service(url):
    # Start measuring the request duration.
    start = time.perf_counter()

    try:
        # Send a GET request to the service.
        response = requests.get(url, timeout=10)
        status_code = response.status_code

        # Treat HTTP status codes from 200 to 299 as UP.
        if 200 <= status_code < 300:
            status = "UP"
        else:
            status = "DOWN"

            # Save unsuccessful HTTP responses to the log.
            logger.error(
                "Service check failed | URL: %s | Status Code: %s",
                url,
                status_code,
            )

    except requests.exceptions.RequestException as error:
        # Handle connection errors and timeouts.
        status = "DOWN"
        status_code = "N/A"

        print(f"Error: {error}")

        # Save the request error to the log.
        logger.error(
            "Service check failed | URL: %s | Error: %s",
            url,
            error,
        )

    # Calculate the duration in milliseconds.
    elapsed_ms = (time.perf_counter() - start) * 1000

    # Get the local date and time with timezone information.
    checked_at = datetime.now(timezone.utc).astimezone().strftime(
        "%Y-%m-%d %H:%M:%S %z"
    )

    # Display the result in the terminal.
    print(url)
    print(f"Status: {status}")
    print(f"Status Code: {status_code}")
    print(f"Response Time: {elapsed_ms:.0f} ms")
    print(f"Checked At: {checked_at}")

    # Return the result so another file, such as app.py,
    # can use it as an API response.
    return {
        "url": url,
        "status": status,
        "status_code": status_code,
        "response_time_ms": round(elapsed_ms),
        "checked_at": checked_at,
    }


# Wait this many seconds after all URLs have been checked.
CHECK_INTERVAL_SECONDS = 30

# Services monitored by the script.
urls = [
    "https://www.google.com",
    "https://www.python.org",
]


# Run the monitoring loop only when this file is executed directly.
# It will not start automatically when app.py imports check_service.
if __name__ == "__main__":
    try:
        while True:
            for url in urls:
                check_service(url)
                print()

            print(
                f"Waiting {CHECK_INTERVAL_SECONDS} seconds "
                "before the next round..."
            )
            time.sleep(CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
