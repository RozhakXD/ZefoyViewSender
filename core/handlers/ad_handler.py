from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..utils.ui_manager import UIManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time

class AdHandler:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.ui = UIManager()
        self.ad_locators = {
            'close_btn': [
                "//div[@aria-label='Close ad']",
                "//button[@aria-label='Close ad']",
                "//div[@aria-label='Close']",
                "//button[@aria-label='Close']",
                "//div[contains(@id,'dismiss-button')]",
                "//button[contains(@id,'dismiss-button')]",
                "//div[contains(@class,'close-button')]",
                "//button[contains(@class,'close-button')]",
                "//div[contains(@class,'modal') or contains(@class,'popup')]//button[contains(normalize-space(),'×') or contains(normalize-space(),'Close') or contains(@aria-label,'Close')]",
                "//div[contains(@class,'modal')]//button[contains(normalize-space(),'×') or contains(normalize-space(),'Close') or contains(@aria-label,'Close')]",
                "//div[contains(@class,'popup')]//button[contains(normalize-space(),'×') or contains(normalize-space(),'Close') or contains(@aria-label,'Close')]",
                "//button[contains(@class,'close-btn')]",
                "//div[@id='ad_close_btn']",
                "//span[contains(text(), 'Close') or contains(text(), '×') or @aria-label='Close']",
            ],
            'ad_iframe': [
                "//iframe[contains(@id,'ad_iframe') or contains(@name,'ad_frame')]",
                "//iframe[contains(@id,'google_ads_iframe')]",
                "//iframe[contains(@src,'googleads.g.doubleclick.net')]",
                "//iframe[contains(@title,'Advertisement') or contains(@aria-label,'Advertisement')]",
                "//iframe[contains(@name, 'google_ads_frame')]"
            ],
            'ad_overlay': [
                "//div[contains(@class,'ad-overlay') or contains(@class,'ad-backdrop')]",
                "//div[contains(@id,'adContainer') and @aria-modal='true']",
                "//div[starts-with(@id, 'google_ads_gpt_') and contains(@style,'display: block')]",
            ],
            'shadow_dom_hosts': [

            ]
        }

    def handle_ads(self, max_attempts=3):
        self.ui.show_status("🌀 Checking for ads...")
        for attempt in range(1, max_attempts + 1):
            closed_something = False
            try:
                if self._close_popup_ads():
                    closed_something = True
                    self.ui.show_status(f"Attempt {attempt}: Popup/Vignette ad handled.")
                    time.sleep(1)

                if self._handle_iframe_ads():
                    closed_something = True
                    self.ui.show_status(f"Attempt {attempt}: Iframe ad handled.")
                    time.sleep(1)

                if self._handle_shadow_dom_ads():
                    closed_something = True
                    self.ui.show_status(f"Attempt {attempt}: Shadow DOM ad handled.")
                    time.sleep(1)

                if self._close_overlay_ads():
                    closed_something = True
                    self.ui.show_status(f"Attempt {attempt}: Overlay ad handled.")
                    time.sleep(1)

                if closed_something:
                    self.ui.show_status(f"Attempt {attempt} made some progress. Checking again or continuing.")
                    if "#google_vignette" in self.driver.current_url:
                        self.ui.show_status("Google Vignette still detected in URL, retrying handle_ads logic.")
                        time.sleep(1)
                        continue
                    return True

                self.ui.show_status(f"Attempt {attempt}: No ads found or handled by current locators.")
                return True

            except Exception as e:
                self.ui.show_error(f"Attempt {attempt}/{max_attempts} failed to handle ads: {str(e)}")
                if attempt == max_attempts:
                    self.ui.show_error(f"Failed to handle ads after {max_attempts} attempts. Main script might need to proceed or retry.")
                    return False
                time.sleep(2)
        
        self.ui.show_error("Exhausted ad handling attempts without definite success or failure reported.")
        return False

    def _close_popup_ads(self):
        self.ui.show_status("Checking for popup ads / vignette close buttons...")
        for locator in self.ad_locators['close_btn']:
            try:
                close_buttons = self.driver.find_elements(By.XPATH, locator)
                for close_btn in close_buttons:
                    if close_btn.is_displayed() and close_btn.is_enabled():
                        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(close_btn))
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", close_btn)
                        time.sleep(0.2)
                        close_btn.click()
                        self.ui.show_status(f"Popup/Vignette ad closed successfully using locator: {locator}")
                        return True
            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                continue
            except Exception as e_general:
                self.ui.show_error(f"Unexpected error with locator {locator}: {e_general}")
                continue
        return False

    def _handle_iframe_ads(self):
        self.ui.show_status("Checking for iframe ads...")
        try:
            potential_ad_iframes = []
            for iframe_locator_group in self.ad_locators['ad_iframe']:
                try:
                    iframes_found = self.driver.find_elements(By.XPATH, iframe_locator_group)
                    potential_ad_iframes.extend(iframes_found)
                except:
                    continue

            if not potential_ad_iframes:
                return False

            unique_iframes = list(set(potential_ad_iframes))

            for iframe_element in unique_iframes:
                try:
                    if not iframe_element.is_displayed():
                        continue

                    self.driver.switch_to.frame(iframe_element)
                    self.ui.show_status("Switched to an ad iframe.")
                    if self._close_popup_ads():
                        self.ui.show_status("Ad closed successfully within an iframe.")
                        self.driver.switch_to.default_content()
                        return True
                except Exception as e_iframe_switch:
                    self.ui.show_error(f"Error switching to or processing iframe: {e_iframe_switch}")
                finally:
                    self.driver.switch_to.default_content()
        except Exception as e:
            self.ui.show_error(f"Error finding or iterating iframe ads: {str(e)}")
        return False

    def _handle_shadow_dom_ads(self):
        self.ui.show_status("Checking for Shadow DOM ads...")
        for host_locator in self.ad_locators.get('shadow_dom_hosts', []):
            try:
                shadow_hosts = self.driver.find_elements(By.CSS_SELECTOR, host_locator)
                if not shadow_hosts: continue

                for shadow_host_element in shadow_hosts:
                    if not shadow_host_element.is_displayed(): continue

                    js_script_to_click_in_shadow = """
                        const host = arguments[0];
                        if (!host || !host.shadowRoot) return false;
                        
                        const selectors = [
                            '.close-button', 'button[aria-label*="Close"]', 
                            'div[aria-label*="Close"]', '#dismiss-button', 
                            'div[role="button"][aria-label*="Close"]'
                        ]; // Daftar selector CSS untuk dicoba di dalam shadow DOM
                        
                        for (const selector of selectors) {
                            const closeButton = host.shadowRoot.querySelector(selector);
                            if (closeButton) {
                                closeButton.click();
                                return true;
                            }
                        }
                        // Jika ada nested shadow DOM (Shadow DOM di dalam Shadow DOM)
                        // Ini perlu penanganan rekursif atau path yang lebih spesifik.
                        // const nestedShadowHost = host.shadowRoot.querySelector('selector-for-nested-host');
                        // if (nestedShadowHost && nestedShadowHost.shadowRoot) { ... }
                        return false;
                    """
                    try:
                        clicked_in_shadow = self.driver.execute_script(js_script_to_click_in_shadow, shadow_host_element)
                        if clicked_in_shadow:
                            self.ui.show_status(f"Shadow DOM ad closed via JS on host: {host_locator}")
                            return True
                    except Exception as e_js:
                        self.ui.show_error(f"JS execution error in Shadow DOM for host {host_locator}: {e_js}")
            except Exception as e_host:
                self.ui.show_error(f"Error finding Shadow DOM host {host_locator}: {e_host}")
        return False

    def _close_overlay_ads(self):
        self.ui.show_status("Checking for overlay ads...")
        for locator in self.ad_locators['ad_overlay']:
            try:
                overlays = self.driver.find_elements(By.XPATH, locator)
                for overlay_element in overlays:
                    if overlay_element.is_displayed():
                        try:
                            WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(overlay_element))
                            overlay_element.click()
                            self.ui.show_status(f"Overlay ad clicked via locator: {locator}")
                            return True
                        except:
                            pass 
            except:
                continue

        try:
            for locator in self.ad_locators['ad_overlay']:
                js_hide_script = """
                    var elements = document.evaluate(arguments[0], document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
                    var hidden = false;
                    for (var i = 0; i < elements.snapshotLength; i++) {
                        var elem = elements.snapshotItem(i);
                        if (elem.style.display !== 'none') { // Hanya sembunyikan jika belum
                           elem.style.display = 'none';
                           hidden = true;
                        }
                    }
                    return hidden; // True jika sesuatu disembunyikan
                """
                if self.driver.find_elements(By.XPATH, locator):
                    was_hidden = self.driver.execute_script(js_hide_script, locator)
                    if was_hidden:
                        self.ui.show_status(f"Overlay ad matching '{locator}' hidden via JavaScript.")
                        return True
        except Exception as e:
            self.ui.show_error(f"Error hiding overlay ads via JavaScript: {str(e)}")
        return False

    def check_for_ads_presence(self, timeout=3):
        self.ui.show_status(f"Quick check for ad presence (timeout {timeout}s)...")
        if "#google_vignette" in self.driver.current_url:
            self.ui.show_status("Google Vignette detected in URL.")
            return True

        for locator in self.ad_locators['close_btn']:
            try:
                if WebDriverWait(self.driver, 0.5).until(EC.visibility_of_any_elements_located((By.XPATH, locator))):
                    self.ui.show_status(f"Visible ad close button detected by: {locator}")
                    return True
            except TimeoutException:
                pass

        for locator in self.ad_locators['ad_iframe']:
            try:
                iframes = self.driver.find_elements(By.XPATH, locator)
                for iframe_el in iframes:
                    if iframe_el.is_displayed():
                        self.ui.show_status(f"Visible ad iframe detected by: {locator}")
                        return True
            except:
                pass
        
        self.ui.show_status("No obvious ads detected by quick check.")
        return False
