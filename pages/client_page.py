import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ClientPage(BasePage):
    # ---- Standard input field selectors (scoped to //main) ----
    CLIENT_NAME            = (By.XPATH, "//main//input[@name='client_name']")
    CONTACT_PERSON_NAME    = (By.XPATH, "//main//input[@name='contact_person_name']")
    CONTACT_PERSON_EMAIL   = (By.XPATH, "//main//input[@name='contact_person_email']")
    CONTACT_PERSON_MOBILE  = (By.XPATH, "//main//input[@name='contact_person_mobile_number']")
    GSTIN_NUMBER           = (By.XPATH, "//main//input[@name='GSTIN_number']")
    PAN_NUMBER             = (By.XPATH, "//main//input[@name='pan_no']")
    TDS_PERCENTAGE         = (By.XPATH, "//main//input[@name='tds_percentage']")
    EMAIL_ID               = (By.XPATH, "//main//input[@name='email_id']")
    MOBILE_NUMBER          = (By.XPATH, "//main//input[@name='mobile_number']")
    PHONE_NUMBER           = (By.XPATH, "//main//input[@name='phone_number']")
    PINCODE                = (By.XPATH, "//main//input[@name='pincode']")
    VENDOR_CODE            = (By.XPATH, "//main//input[@name='vendor_code']")

    # ---- Buttons ----
    ADD_NEW_CLIENT_BTN = (By.XPATH, "//main//button[contains(., 'Add New Client')]")
    CREATE_BUTTON      = (By.XPATH, "//main//button[@type='submit']")

    # ---- Ship-to section ----
    # "Add" button inside the Ship To Details card
    SHIP_TO_ADD_BTN = (By.XPATH, "//main//h5[contains(.,'Ship To')]/..//button[normalize-space()='Add']")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate(self):
        """Navigates to the Client Masters page via sidebar menu link."""
        print("Navigating to Client Management via sidebar link...")
        client_link = self.wait_for_element_clickable((By.LINK_TEXT, "Client Management"))
        self.driver.execute_script("arguments[0].click();", client_link)
        time.sleep(2)

    def click_add_new_client(self):
        """Opens the Create Client form."""
        print("Clicking '+ Add New Client' via JS...")
        self.js_click_element(self.ADD_NEW_CLIENT_BTN)
        time.sleep(3)

    def _fill_ship_to_row(self, location, address, pincode, row_index=1):
        """
        Fill a Ship-To row in the table by row index (1-based).
        Uses placeholder-based XPath since ship-to fields have no name attribute.
        """
        try:
            # Locate the specific row's inputs by position
            loc_input = (By.XPATH,
                f"(//main//table//input[@placeholder='Enter ship to location'])[{row_index}]"
            )
            addr_input = (By.XPATH,
                f"(//main//table//input[@placeholder='Enter ship to address'])[{row_index}]"
            )
            pin_input = (By.XPATH,
                f"(//main//table//input[@placeholder='Enter pincode'])[{row_index}]"
            )

            self.enter_text(loc_input, location)
            self.enter_text(addr_input, address)
            self.enter_text(pin_input, pincode)
        except Exception as e:
            print(f"  [warn] Ship-to row {row_index} fill failed: {e}")

    def create_client(self, client_data):
        """Fills out the client creation form and submits it."""
        print(f"Creating client: {client_data['client_name']}...")

        # 1. Fill all core text inputs
        self.enter_text(self.CLIENT_NAME, client_data["client_name"])
        self.enter_text(self.CONTACT_PERSON_NAME, client_data["contact_person_name"])
        self.enter_text(self.CONTACT_PERSON_EMAIL, client_data["contact_person_email"])
        self.enter_text(self.CONTACT_PERSON_MOBILE, client_data["contact_person_mobile_number"])
        self.enter_text(self.GSTIN_NUMBER, client_data["GSTIN_number"])
        self.enter_text(self.PAN_NUMBER, client_data["pan_no"])
        self.enter_text(self.TDS_PERCENTAGE, client_data["tds_percentage"])
        self.enter_text(self.EMAIL_ID, client_data["email_id"])
        self.enter_text(self.MOBILE_NUMBER, client_data["mobile_number"])
        self.enter_text(self.PHONE_NUMBER, client_data["phone_number"])
        self.enter_text(self.PINCODE, client_data["pincode"])
        self.enter_text(self.VENDOR_CODE, client_data["vendor_code"])

        # 2. Country, State, City dropdowns
        print("  Selecting Country...")
        self.select_react_dropdown_by_placeholder("Select Country", "India")
        time.sleep(2.5)

        print("  Selecting State...")
        self.select_react_dropdown_by_placeholder("Select State", "Maharashtra")
        time.sleep(2.0)

        print("  Selecting City...")
        self.select_react_dropdown_by_placeholder("Select City", "Mumbai")
        time.sleep(1.0)

        # 3. Ship-to details — click Add first to ensure a row exists, then fill it
        print("  Filling Ship-To details...")
        try:
            # The HTML shows a default row already exists, but click Add to be safe
            add_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.SHIP_TO_ADD_BTN)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_btn)
            time.sleep(0.3)
            # Only click Add if no row already exists
            existing = self.driver.find_elements(
                By.XPATH,
                "//main//table//input[@placeholder='Enter ship to location']"
            )
            if not existing:
                self.driver.execute_script("arguments[0].click();", add_btn)
                time.sleep(0.5)
        except Exception as e:
            print(f"  [warn] Ship-to Add button: {e}")

        self._fill_ship_to_row(
            client_data["ship_to_location"],
            client_data["ship_to_address"],
            client_data["pincode"],
            row_index=1
        )

        # 4. Submit
        print("  Clicking Create button...")
        # Scroll to bottom first — submit button is at the end of a long form
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        try:
            # Try multiple selectors for the submit button
            create_btn = None
            for locator in [
                (By.XPATH, "//button[@type='submit' and (contains(.,'Create') or contains(.,'Save') or contains(.,'Submit'))]"),
                (By.XPATH, "//button[@type='submit']"),
                (By.XPATH, "//button[contains(.,'Create Client')]"),
                (By.XPATH, "//button[contains(.,'Create')]"),
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
            print(f"  Submitted form (button text: '{create_btn.text.strip()}'")
            time.sleep(4)
        except Exception as e:
            print(f"  [error] Submit failed: {e}")
