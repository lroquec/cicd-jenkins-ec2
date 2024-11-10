import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from urllib3.exceptions import ProtocolError


@pytest.fixture(scope="module")
def driver():
    SELENIUM_HOST = os.environ.get("SELENIUM_HOST", "selenium")
    SELENIUM_PORT = os.environ.get("SELENIUM_PORT", "4444")
    BROWSER = os.environ.get("BROWSER", "chrome").lower()
    MAX_RETRIES = 3

    print(
        f"\nConnecting to Selenium Grid at http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub"
    )
    print(f"Selected browser: {BROWSER}")

    for attempt in range(MAX_RETRIES):
        try:
            if BROWSER == "chrome":
                options = ChromeOptions()
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--headless")  # Headless mode
                options.add_argument("--disable-gpu")  # Necessary in some cases
                options.add_argument("--window-size=1920,1080")

                driver = webdriver.Remote(
                    command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub",
                    options=options,
                )
                print("Successful connection to Selenium Grid")
                break
            # ... rest of the options for other browsers ...
        except ProtocolError as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(5)  # Wait before retrying

    yield driver

    try:
        driver.quit()
    except Exception as e:
        print(f"Error closing the driver: {e}")