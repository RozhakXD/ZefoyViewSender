from core.utils.exceptions import AutomationError
from core.automator import ZefoyAutomator
from core.utils.ui_manager import UIManager

if __name__ == "__main__":
    ui = UIManager()
    ui.show_banner()

    try:
        automator = ZefoyAutomator()
        ui.show_status("Automation started successfully!")
        automator.run()
    except AutomationError as e:
        ui.show_error(f"Automation failed: {str(e)}")
    except KeyboardInterrupt:
        ui.show_status("Process interrupted by user")
        exit(0)
    except Exception as e:
        ui.show_error(f"Unexpected error: {str(e)}")
    finally:
        automator.driver.quit()
        ui.show_status("Browser closed. Exiting program.")