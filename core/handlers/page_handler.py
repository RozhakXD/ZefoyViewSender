from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..utils.exceptions import ElementNotFoundError
import time

class PageHandler:
    def __init__(self, driver):
        self.driver = driver
        self.locators = {
            'url_input': "//div[contains(@class, 't-views-menu')]//input[@type='search' and @placeholder='Enter Video URL']",
            'search_btn': "//div[contains(@class, 't-views-menu')]//button[@type='submit' and contains(., 'Search')]",
            'views_section': "//div[contains(@class, 'colsmenu')]//h5[normalize-space(text())='Views']/following-sibling::button",
            'views_btn': "//div[@id='c2VuZC9mb2xeb3dlcnNfdGlrdG9V']//form//button[@type='submit' and contains(@class, 'wbutton')]"
        }

    def navigate_to_views_section(self):
        self._click_element(self.locators['views_section'])

    def submit_video_url(self, video_url):
        self._input_text(self.locators['url_input'], video_url)
        self._click_element(self.locators['search_btn'])

    def send_views(self):
        try:
            self._click_element(self.locators['search_btn'])
        except:
            pass
        for selector in [self.locators['views_btn'], "//form//button[contains(@class, 'wbutton') and contains(., 'Submit')]", "//form//button[contains(@class, 'wbutton')]"]:
            try:
                self._click_element(selector)
                time.sleep(5)
                break
            except:
                pass
        self._verify_success()

    def _click_element(self, xpath, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
        except Exception as e:
            raise ElementNotFoundError(f"Element not found: {xpath} - {str(e)}")

    def _input_text(self, xpath, text, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.clear()
            element.send_keys(text)
        except Exception as e:
            raise ElementNotFoundError(f"Input field not found: {xpath} - {str(e)}")

    def _verify_success(self, timeout=20):
        success_xpath = "//*[contains(text(), 'Successfully')]"
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, success_xpath))
            )
        except:
            self.send_views()
            raise ElementNotFoundError("Success message not found. Please check the operation.")
