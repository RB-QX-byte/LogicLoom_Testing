from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for the Login page."""

    EMAIL_INPUT    = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON   = (By.XPATH, "//button[@type='submit']")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate(self, url="https://tmpms.disctesting.in/login"):
        """Open the login page."""
        self.driver.get(url)

    def login(self, email, password):
        """Enter credentials and click the Login button."""
        print("  -> Logging in as %s..." % email)
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
