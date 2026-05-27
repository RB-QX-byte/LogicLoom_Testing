import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base Page Object providing shared browser interaction utilities."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ------------------------------------------------------------------
    # Core element interactions
    # ------------------------------------------------------------------

    def wait_for_element_visible(self, locator, timeout=15):
        """Wait until the element is visible and return it."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=15):
        """Wait until the element is clickable and return it."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click_element(self, locator, timeout=15):
        """Click an element after waiting for it to be clickable."""
        el = self.wait_for_element_clickable(locator, timeout)
        el.click()

    def js_click_element(self, locator, timeout=15):
        """Click an element using JavaScript (bypasses overlay issues)."""
        el = self.wait_for_element_visible(locator, timeout)
        self.driver.execute_script("arguments[0].click();", el)

    def enter_text(self, locator, text, timeout=15):
        """
        Fill a React-controlled input or textarea via the native value setter.
        Dispatches input and change events so React registers the new value.
        """
        print("  -> Filling '%s' into %s..." % (text, locator))
        el = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center', behavior:'instant'});", el
        )
        time.sleep(0.2)
        tag = el.tag_name.lower()
        proto = "HTMLTextAreaElement" if tag == "textarea" else "HTMLInputElement"
        js = (
            "var setter = Object.getOwnPropertyDescriptor(window.%s.prototype,'value').set;" % proto
            + "setter.call(arguments[0],arguments[1]);"
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
            "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));"
        )
        self.driver.execute_script(js, el, str(text))
        time.sleep(0.1)

    def get_text(self, locator, timeout=15):
        """Return the visible text of an element."""
        return self.wait_for_element_visible(locator, timeout).text.strip()

    # ------------------------------------------------------------------
    # React-Select helpers
    # ------------------------------------------------------------------

    def _find_visible_options(self):
        """Return all currently visible React-Select option elements."""
        for selector in ["[role='option']", "[class*='-option']", "[class*='__option']"]:
            try:
                opts = self.driver.find_elements(By.CSS_SELECTOR, selector)
                visible = [o for o in opts if o.is_displayed() and o.text.strip()]
                if visible:
                    return visible
            except Exception:
                pass
        return []

    def _open_react_select_and_pick(self, inp_element, search_text=""):
        """
        Open a React-Select dropdown and select an option.

        Strategy:
        - Locate the control div (visible dropdown box) by walking up the DOM.
        - Open the menu via native click, ActionChains click, or JS mousedown.
        - Optionally filter options by typing search_text.
        - Select the best-matching option via ActionChains (CDP events).
        - Close the menu by moving focus outside the RS container via JS.
        """
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center',behavior:'instant'});",
                inp_element
            )
            time.sleep(0.4)

            # Locate the control div (the visible clickable dropdown box)
            control = self.driver.execute_script("""
                var el = arguments[0];
                while (el && el !== document.body) {
                    var cls = el.className;
                    if (cls && typeof cls==='string' && cls.includes('-control'))
                        return el;
                    el = el.parentElement;
                }
                return arguments[0].parentElement;
            """, inp_element)

            # Open the dropdown menu
            opened = False
            try:
                if control:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});", control
                    )
                    control.click()
                else:
                    inp_element.click()
                opened = True
                time.sleep(0.8)
            except Exception:
                pass

            if not opened or not self._find_visible_options():
                try:
                    target_el = control if control else inp_element
                    ActionChains(self.driver).move_to_element(target_el).click().perform()
                    time.sleep(0.8)
                except Exception as e:
                    print("  [dropdown] Open failed: %s" % e)

            if not self._find_visible_options():
                try:
                    self.driver.execute_script("""
                        var el = arguments[0];
                        var ctrl = el;
                        while (ctrl && ctrl !== document.body) {
                            var cls = ctrl.className;
                            if (cls && typeof cls==='string' && cls.includes('-control')) break;
                            ctrl = ctrl.parentElement;
                        }
                        if (!ctrl || ctrl===document.body) ctrl = el.parentElement || el;
                        ctrl.dispatchEvent(new MouseEvent('mousedown',
                            {bubbles:true,cancelable:true,view:window,buttons:1}));
                        ctrl.dispatchEvent(new MouseEvent('mouseup',
                            {bubbles:true,cancelable:true,view:window,buttons:1}));
                        ctrl.dispatchEvent(new MouseEvent('click',
                            {bubbles:true,cancelable:true,view:window,buttons:1}));
                    """, inp_element)
                    time.sleep(0.8)
                except Exception as e2:
                    print("  [dropdown] JS open fallback failed: %s" % e2)

            # Wait up to 10 s for options to appear (allows for slow API responses)
            opts = []
            for _ in range(20):
                opts = self._find_visible_options()
                if opts:
                    break
                time.sleep(0.5)

            if not opts:
                print("  [dropdown] No options for '%s'" % search_text)
                return False

            # Filter by search text if provided
            if search_text:
                try:
                    self.driver.switch_to.active_element.send_keys(search_text)
                    time.sleep(3.0)
                    opts = self._find_visible_options()
                except Exception as te:
                    print("  [dropdown] Type failed: %s" % te)

            if not opts:
                print("  [dropdown] No options after search '%s'" % search_text)
                return False

            # Pick best match
            if search_text:
                target = next(
                    (o for o in opts if search_text.lower() in o.text.lower()),
                    opts[0]
                )
            else:
                target = opts[0]

            print("  [dropdown] %d opts. Selecting: '%s'" % (len(opts), target.text.strip()[:60]))

            # Select via JS simulated click and MouseEvents (highly reliable in headless Chrome)
            try:
                self.driver.execute_script("""
                    var el = arguments[0];
                    el.scrollIntoView({block: 'center', behavior: 'instant'});
                    el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, cancelable: true, view: window}));
                    el.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, cancelable: true, view: window}));
                    el.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
                """, target)
                time.sleep(0.6)
            except Exception as ce:
                print("  [dropdown] JS click failed: %s" % ce)
                try:
                    target.click()
                    time.sleep(0.6)
                except Exception as fe:
                    print("  [dropdown] Fallback standard click failed: %s" % fe)
                    return False

            # Close the menu if still open after selection.
            # Use direct blur() on the RS hidden input — fires onInputBlur
            # regardless of which element is currently active, guaranteeing
            # React Hook Form's field.onBlur() and any dependent form effects run.
            if self._find_visible_options():
                try:
                    self.driver.execute_script("arguments[0].blur();", inp_element)
                    time.sleep(0.4)
                    # Fallback: focus a neutral element if menu still did not close
                    if self._find_visible_options():
                        self.driver.execute_script("""
                            var el = document.querySelector("input[name='is_active']")
                                  || document.querySelector("input[name='expected_receipt_date']")
                                  || document.querySelector("input[name='date']");
                            if (el) {
                                el.focus();
                            } else {
                                document.body.setAttribute('tabindex', '-1');
                                document.body.focus();
                            }
                        """)
                        time.sleep(0.4)
                except Exception as fe:
                    print("  [dropdown] Menu close failed: %s" % fe)


            return True

        except Exception as e:
            print("  [dropdown] Error: %s" % e)
            return False

    def select_react_dropdown_option(self, input_locator, option_text, timeout=15):
        """Find a React-Select input by locator and pick the specified option."""
        print("  -> Dropdown '%s'..." % option_text)
        try:
            inp = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(input_locator)
            )
            return self._open_react_select_and_pick(inp, option_text)
        except Exception as e:
            print("  [warn] select_react_dropdown_option: %s" % e)
            return False

    def select_react_dropdown_by_placeholder(self, placeholder_text, option_text="", timeout=10, parent_xpath=""):
        """
        Find a React-Select dropdown by its visible placeholder text and pick an option.
        Resolves the placeholder element ID to the corresponding hidden input.
        """
        print("  -> Dropdown placeholder='%s' option='%s'..." % (placeholder_text, option_text))
        try:
            prefix = parent_xpath if parent_xpath else ""
            ph_el = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "%s//*[contains(@id,'-placeholder') and contains(text(),'%s')]" % (prefix, placeholder_text)
                ))
            )
            ph_id = ph_el.get_attribute("id")
            inp_id = ph_id.replace("-placeholder", "-input")
            inp = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, inp_id))
            )
            return self._open_react_select_and_pick(inp, option_text)
        except Exception as e:
            print("  [warn] select_react_dropdown_by_placeholder('%s'): %s" % (placeholder_text, e))
            return False
