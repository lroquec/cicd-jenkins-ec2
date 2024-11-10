import os
from selenium.webdriver.common.by import By

os.environ['OTEL_TRACES_EXPORTER'] = 'none'


def test_app_loads_correctly(driver):
    APP_HOST = os.environ.get("APP_HOST", "myapp")
    APP_PORT = os.environ.get("APP_PORT", "5000")

    app_url = f"http://{APP_HOST}:{APP_PORT}"
    print(f"\nAttempting to access: {app_url}")

    try:
        print("Starting page get...")
        driver.get(app_url)
        print("Get completed")

        print("Waiting for the body element...")
        driver.implicitly_wait(5)
        body = driver.find_element(By.TAG_NAME, "body")
        print(f"Body found. Full text:\n{body.text}")

        print("Verifying 'very simple' text...")
        assert (
            "very simple" in body.text
        ), f"'very simple' text not found. Current text: {body.text}"
        print("Test completed successfully")

    except Exception as e:
        print(f"Error during the test: {str(e)}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")
        print("Page source:")
        print(driver.page_source)
        raise