import time
import re
from selenium.webdriver.remote.webdriver import WebDriver
from ..utils.exceptions import DelayCalculationError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TimerHandler:
    def handle_delay(self, driver: WebDriver, max_wait=180):
        try:
            delay_text = self._get_delay_text(driver, max_wait)
            wait_time = 300

            if not delay_text:
                print("⚠️ No delay detected. Defaulting to 5 minutes.")
            else:
                wait_time = self._parse_delay(delay_text)
                print(f"⏳ Delay detected: {wait_time} seconds")

            if wait_time <= 0:
                print("⚠️ Invalid delay value detected. Defaulting to 5 minutes.")
                wait_time = 300

            for i in range(wait_time + 5, 0, -1):
                print(f"⏱️ Waiting for {wait_time}/{i} seconds...", end="\r")
                time.sleep(1)
            return
        except Exception as e:
            raise DelayCalculationError(str(e))

    def _get_delay_text(self, driver, timeout):
        delay_xpath = "//*[contains(text(), 'Please wait')]"
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, delay_xpath))
        )
        return element.text

    def _parse_delay(self, text):
        minutes = re.search(r"(\d+)\s*min", text, re.IGNORECASE)
        seconds = re.search(r"(\d+)\s*sec", text, re.IGNORECASE)
        return (int(minutes.group(1)) * 60 if minutes else 0) + \
            (int(seconds.group(1)) if seconds else 0)
    
    def wait_before_retry(self, base=15):
        print(f"🌀 Retrying in {base} seconds...")
        time.sleep(base)

    def handle_retry_delay(self):
        print("⚠️ Error detected, retrying in 5 seconds...")
        time.sleep(5)