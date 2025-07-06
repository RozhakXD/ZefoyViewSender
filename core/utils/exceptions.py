class ZefoyBaseException(Exception):
    def __init__(self, message="Zefoy automation error occurred"):
        self.message = message
        super().__init__(self.message)

class AutomationError(ZefoyBaseException):
    def __init__(self, message="Automation process failed"):
        super().__init__(message)

class ElementNotFoundError(ZefoyBaseException):
    def __init__(self, element_description):
        message = f"Element not found: {element_description}"
        super().__init__(message)

class DelayCalculationError(ZefoyBaseException):
    def __init__(self, delay_info):
        message = f"Delay calculation failed: {delay_info}"
        super().__init__(message)

class AdHandlerError(ZefoyBaseException):
    def __init__(self, message="Failed to handle advertisements"):
        super().__init__(message)

class CaptchaError(ZefoyBaseException):
    def __init__(self, message="CAPTCHA verification failed"):
        super().__init__(message)

class ConfigError(ZefoyBaseException):
    def __init__(self, config_key=None):
        message = "Configuration error" + (f" (key: {config_key})" if config_key else "")
        super().__init__(message)

class RateLimitError(ZefoyBaseException):
    def __init__(self, retry_after=None):
        message = "Rate limit exceeded"
        if retry_after:
            message += f", please wait {retry_after} seconds"
        super().__init__(message)

class SessionExpiredError(ZefoyBaseException):
    def __init__(self, message="Session has expired"):
        super().__init__(message)

class BrowserError(ZefoyBaseException):
    def __init__(self, message="Browser operation failed"):
        super().__init__(message)