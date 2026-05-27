import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class SalesOrderPage(BasePage):
    """Page Object for the Sales Order creation and listing pages."""

    # Locators
    ORDER_NUMBER       = (By.XPATH, "//main//input[@name='order_number']")
    ORDER_REFERENCE_NO = (By.XPATH, "//main//input[@name='order_reference_no']")
    ADDRESS_TEXTAREA   = (By.XPATH, "//main//textarea[@name='address']")
    CLIENT_SELECT      = (By.XPATH, "//main//label[contains(.,'Client')]/..//input[contains(@id,'react-select-')]")
    ADD_NEW_ORDER_BTN  = (By.XPATH, "//main//button[contains(.,'Add New Order')]")
    ADD_ROW_BTN        = (By.XPATH, "//button[normalize-space()='ADD']")

    def __init__(self, driver):
        super().__init__(driver)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self):
        """Navigate to the Sales Orders list page via the sidebar link."""
        print("Navigating to Sales Orders page...")
        link = self.wait_for_element_clickable((By.LINK_TEXT, "Sales Orders"))
        self.driver.execute_script("arguments[0].click();", link)
        time.sleep(2)

    def click_add_new_order(self):
        """Click the Add New Order button to open the creation form."""
        print("Clicking Add New Order...")
        self.js_click_element(self.ADD_NEW_ORDER_BTN)
        time.sleep(3)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _fill_date_field(self, name, date_str):
        """Set a date input value using the native value setter (React-compatible)."""
        try:
            locator = (By.XPATH, "//main//input[@name='%s' and @type='date']" % name)
            el = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
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

    def _fill_grid_text(self, field_name, value):
        """Set a text or numeric input in the grid table body (skips read-only fields)."""
        if not value:
            return
        try:
            locator = (By.XPATH, "//main//tbody//input[@name='%s']" % field_name)
            el = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(locator)
            )
            if el.get_attribute("readonly") or el.get_attribute("disabled"):
                return
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            js = (
                "var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
                "s.call(arguments[0],arguments[1]);"
                "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
                "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));"
            )
            self.driver.execute_script(js, el, str(value))
            print("  -> Grid '%s' = '%s'" % (field_name, value))
        except Exception as e:
            print("  [warn] Grid field '%s': %s" % (field_name, e))

    def _fill_grid_date(self, field_name, date_str):
        """Set a date input inside the grid table body."""
        try:
            locator = (By.XPATH, "//main//tbody//input[@name='%s']" % field_name)
            el = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(locator)
            )
            js = (
                "var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
                "s.call(arguments[0],arguments[1]);"
                "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
                "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));"
            )
            self.driver.execute_script(js, el, date_str)
            print("  -> Grid date '%s' = '%s'" % (field_name, date_str))
        except Exception as e:
            print("  [warn] Grid date '%s': %s" % (field_name, e))

    # ------------------------------------------------------------------
    # Form actions
    # ------------------------------------------------------------------

    def create_sales_order(self, order_data):
        """
        Fill and submit the Sales Order creation form.

        Header field order:
          Client → Project Type → Project Manager → Branch → text fields

        Branch is selected LAST among header dropdowns because selecting
        Project Type or Project Manager can reset Branch. Selecting Branch
        last ensures it persists until submission.

        Grid row flow (after ADD button):
          Category → Item Code/Name → grid text fields → Tax → Submit
        """
        print("Creating Sales Order %s for %s..." % (order_data["order_number"], order_data["client_name"]))

        # Client (triggers Branch options to load via API)
        self.select_react_dropdown_option(self.CLIENT_SELECT, order_data["client_name"])
        time.sleep(5.0)

        # Project Type and Project Manager (independent of Branch)
        self.select_react_dropdown_by_placeholder("Select Project Type", "")
        time.sleep(1.0)

        self.select_react_dropdown_by_placeholder("Select Project Manager", "")
        time.sleep(1.0)

        # Branch LAST — prevents PT/PM selection from clearing Branch value
        self.select_react_dropdown_by_placeholder("Select Branch", "")
        time.sleep(1.5)

        # Header text fields and dates
        self.enter_text(self.ORDER_NUMBER, order_data["order_number"])
        self.enter_text(self.ORDER_REFERENCE_NO, order_data["order_reference_no"])
        self._fill_date_field("order_date", order_data["order_date"])
        self._fill_date_field("delivery_date", order_data["delivery_date"])
        self.enter_text(self.ADDRESS_TEXTAREA, order_data["address"])
        time.sleep(0.5)

        # Only click ADD if no item row already exists in the grid (e.g. quantity input is missing)
        try:
            existing_inputs = self.driver.find_elements(By.XPATH, "//main//tbody//input[@name='quantity']")
            if not existing_inputs:
                add_btn = WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable(self.ADD_ROW_BTN)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_btn)
                time.sleep(0.3)
                self.driver.execute_script("arguments[0].click();", add_btn)
                print("  -> ADD row clicked (grid was empty).")
                time.sleep(1.5)
            else:
                print("  -> Grid already has an item row by default. Skipping ADD click.")
        except Exception as e:
            print("  [warn] ADD button check: %s" % e)

        # Grid row: Category → Item (in that order)
        self.select_react_dropdown_by_placeholder("Category", "", parent_xpath="//tbody")
        time.sleep(1.5)

        self.select_react_dropdown_by_placeholder("Item", "", parent_xpath="//tbody")
        time.sleep(1.5)

        # Grid text fields
        self._fill_grid_text("item_line_code",     order_data["item_line_code"])
        self._fill_grid_text("customer_item_name", order_data["customer_item_name"])
        self._fill_grid_text("item_code",          order_data["item_code"])
        self._fill_grid_text("material",           order_data["material"])
        self._fill_grid_text("size",               order_data["size"])
        self._fill_grid_text("description",        order_data["description"])
        self._fill_grid_text("quantity",           order_data["quantity"])
        self._fill_grid_text("unit_price",         order_data["unit_price"])
        self._fill_grid_date("expected_delivery_date", order_data["expected_delivery_date"])

        # Tax (grid row) — select last so form considers row complete
        self.select_react_dropdown_by_placeholder("Select Tax", "", parent_xpath="//tbody")
        time.sleep(0.5)

        # Submit
        print("  -> Submitting Sales Order...")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        try:
            create_btn = None
            for locator in [
                (By.XPATH, "//button[@type='submit' and (contains(.,'Create') or contains(.,'Save'))]"),
                (By.XPATH, "//button[@type='submit']"),
                (By.XPATH, "//main//button[contains(.,'Create')]"),
            ]:
                els = self.driver.find_elements(*locator)
                visible = [e for e in els if e.is_displayed()]
                if visible:
                    create_btn = visible[0]
                    break

            if not create_btn:
                print("  [error] Submit button not found!")
                return

            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_btn)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", create_btn)
            print("  -> Submitted (button: '%s')" % create_btn.text.strip())
            time.sleep(4)
        except Exception as e:
            print("  [error] Could not submit: %s" % e)
