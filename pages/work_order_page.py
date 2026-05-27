import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class WorkOrderPage(BasePage):
    """Page Object for the Work Order creation and listing pages."""

    # Locators
    ADD_NEW_WORK_ORDER_BTN = (By.XPATH,
        "//main//button[contains(.,'Add New Work Order') or contains(.,'New Work')]"
    )
    CREATE_BUTTON  = (By.XPATH, "//main//button[@type='submit']")
    REMARK_TEXTAREA = (By.XPATH, "//main//textarea[@name='remark']")

    def __init__(self, driver):
        super().__init__(driver)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self):
        """Navigate to the Work Orders list page via the sidebar link."""
        print("Navigating to Work Orders...")
        link = self.wait_for_element_clickable((By.LINK_TEXT, "Work Order"))
        self.driver.execute_script("arguments[0].click();", link)
        time.sleep(2)

    def click_add_new_work_order(self):
        """Click Add New Work Order to open the creation form."""
        print("Clicking Add New Work Order...")
        self.js_click_element(self.ADD_NEW_WORK_ORDER_BTN)
        time.sleep(3)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _fill_date(self, name, date_str):
        """Set a date input value using the native value setter (React-compatible)."""
        if not date_str:
            return
        try:
            locator = (By.XPATH, "//main//input[@name='%s']" % name)
            el = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located(locator)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", el
            )
            js = (
                "var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
                "s.call(arguments[0],arguments[1]);"
                "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
                "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));"
            )
            self.driver.execute_script(js, el, date_str)
            print("  -> Date '%s' = %s" % (name, date_str))
        except Exception as e:
            print("  [warn] Date '%s' not filled: %s" % (name, e))

    def _fill_grid_field(self, name, value):
        """Set a numeric input inside the item grid by its name attribute."""
        if not value:
            return
        try:
            locator = (By.XPATH, "//main//tbody//input[@name='%s']" % name)
            el = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located(locator)
            )
            if el.get_attribute("readonly") or el.get_attribute("disabled"):
                return
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", el
            )
            js = (
                "var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
                "s.call(arguments[0],arguments[1]);"
                "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
                "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));"
            )
            self.driver.execute_script(js, el, str(value))
            print("  -> Grid '%s' = '%s'" % (name, value))
        except Exception as e:
            print("  [warn] Grid '%s' not filled: %s" % (name, e))

    # ------------------------------------------------------------------
    # Form actions
    # ------------------------------------------------------------------

    def create_work_order(self, wo_data):
        """
        Fill and submit the Work Order creation form.

        Field fill order:
          Branch → Tax → Date → Remark → Vendor → Item → Grid quantities → Submit

        Notes:
          - Job Work Type and Status are pre-set by the application.
          - Vendor is selected after Branch because Branch selection resets
            dependent dropdowns including Vendor.
          - Batch No and Operations auto-populate when an Item is selected.
        """
        print("Creating Work Order...")

        self.select_react_dropdown_by_placeholder("Select Branch", "")
        time.sleep(1.0)

        self.select_react_dropdown_by_placeholder("Select Tax", "")
        time.sleep(0.8)

        self._fill_date("date", wo_data["date"])
        self._fill_date("expected_receipt_date", wo_data.get("expected_receipt_date", ""))

        remark = wo_data.get("remark", "")
        if remark:
            self.enter_text(self.REMARK_TEXTAREA, remark)
        time.sleep(0.3)

        self.select_react_dropdown_by_placeholder("Select Vendor", "")
        time.sleep(5.0)

        self.select_react_dropdown_by_placeholder("Select Item Code / Name", "")
        time.sleep(3.0)

        self._fill_grid_field("outsource_qty", wo_data.get("outsource_qty", "1"))
        self._fill_grid_field("rate", wo_data.get("rate", "100"))

        try:
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.CREATE_BUTTON)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", btn
            )
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", btn)
            print("  -> Work Order submitted.")
            time.sleep(4)
        except Exception as e:
            print("  [error] Submit failed: %s" % e)
