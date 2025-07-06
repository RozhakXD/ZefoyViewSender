from selenium import webdriver
from .handlers.page_handler import PageHandler
from .handlers.timer_handler import TimerHandler
from .handlers.ad_handler import AdHandler
from .utils.config_manager import ConfigManager
import time

class ZefoyAutomator:
    def __init__(self):
        self.config = ConfigManager.load_config()
        self.driver = webdriver.Chrome()
        self.page_handler = PageHandler(self.driver)
        self.timer_handler = TimerHandler()
        self.ad_handler = AdHandler(self.driver)

        self.driver.get('https://zefoy.com/')
        self._wait_for_manual_captcha()

    def _wait_for_manual_captcha(self):
        input("Please complete the CAPTCHA and press Enter to continue...")
        time.sleep(5)

    def run(self):
        while True:
            try:
                self.driver.refresh()
                self.page_handler.navigate_to_views_section()
                self._process_views()
            except Exception as e:
                print(f"⚠️ Error occurred: {str(e)[:100]}")
                continue

    def _process_views(self):
        try:
            self.page_handler.submit_video_url(self.config['video_url'])
            self.timer_handler.handle_delay(self.driver)
            
            if self.ad_handler.check_for_ads_presence(timeout=5):
                print("Ads detected, attempting to handle them...")
                if self.ad_handler.handle_ads(max_attempts=3):
                    print("Ads handled successfully (or no unhandled ads found).")
                else:
                    print("Failed to handle ads after multiple attempts.")
            else:
                print("No ads initially detected by check_for_ads_presence.")

            self.page_handler.send_views()
            print("Successfully sent views!           ")
            self.timer_handler.wait_before_retry()

            return
        except Exception:
            self.timer_handler.handle_retry_delay()
            raise
