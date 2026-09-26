import logging
import time
from datetime import datetime, timezone

import requests

# Save error messages to monitor.log in the current working directory.
# Each entry contains a timestamp, a log level, and a message.
# New records are added without deleting older ones.
logging.basicConfig(
    filename="monitor.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Use a named logger for this module.
# It uses the file and format configured above.
logger = logging.getLogger(__name__)


def check_service(url):
    # Start measuring before sending the request.
    # perf_counter measures elapsed time and is not affected
    # by changes to the computer's clock.
    start = time.perf_counter()

    try:
        # Send a GET request and store the response.
        # Requests follows redirects by default.
        #
        # timeout=10 limits connection and data waiting periods.
        # It does not set a strict total duration for the request.
        response = requests.get(url, timeout=10)
        status_code = response.status_code

        # Our monitoring rule treats HTTP codes 200-299 as UP.
        # All other HTTP status codes are treated as DOWN.
        # This checks one URL, not every feature of the service.
        if 200 <= status_code < 300:
            status = "UP"
        else:
            status = "DOWN"

            # The server responded with an unsuccessful status code.
            # Record the URL and code so we can investigate later.
            logger.error(
                "Service check failed | URL: %s | Status Code: %s",
                url,
                status_code,
            )

    except requests.exceptions.RequestException as error:
        # Handle connection errors, timeouts, and other request failures.
        # Catching these errors allows monitoring to continue.
        #
        # No usable response was returned, so there is no HTTP code
        # to display. N/A means "not available".
        status = "DOWN"
        status_code = "N/A"

        # Show the error immediately and also save it to the log file.
        # The %s placeholders receive the URL and error details.
        print(f"Error: {error}")
        logger.error(
            "Service check failed | URL: %s | Error: %s",
            url,
            error,
        )

    # Calculate the elapsed time and convert seconds to milliseconds.
    # This includes the request and any error reporting above.
    # For a failed request, it measures the failed attempt.
    elapsed_ms = (time.perf_counter() - start) * 1000

    # Get the current time with timezone information.
    # Convert it to the computer's local timezone for display.
    #
    # %Y-%m-%d: year-month-day
    # %H:%M:%S: hour:minute:second
    # %z: UTC offset, such as +0300
    checked_at = datetime.now(timezone.utc).astimezone().strftime(
        "%Y-%m-%d %H:%M:%S %z"
    )

    # Display results for both successful and failed checks.
    # An f-string inserts values inside the braces.
    # :.0f rounds the displayed duration to a whole number.
    print(url)
    print(f"Status: {status}")
    print(f"Status Code: {status_code}")
    print(f"Response Time: {elapsed_ms:.0f} ms")
    print(f"Checked At: {checked_at}")


# Wait this many seconds after all URLs have been checked.
# A complete round includes the checks plus this waiting time.
CHECK_INTERVAL_SECONDS = 30

# Add or remove addresses here to choose which services to monitor.
# Include https:// or http:// in each URL.
urls = [
    "https://www.google.com",
    "https://www.python.org",
]

try:
    # Keep running until the user stops the program.
    while True:
        # Check URLs one at a time using the same function.
        for url in urls:
            check_service(url)
            print()

        # Wait once after the whole list has been checked.
        print(
            f"Waiting {CHECK_INTERVAL_SECONDS} seconds "
            "before the next round..."
        )
        time.sleep(CHECK_INTERVAL_SECONDS)

except KeyboardInterrupt:
    # Control + C interrupts the program.
    # Handle it with a short message instead of a traceback.
    print("\nMonitoring stopped.")
