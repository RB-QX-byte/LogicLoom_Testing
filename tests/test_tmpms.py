"""
test_tmpms.py
=============
End-to-end automation suite for TM-PMS.

All test data is sourced from ``generate_test_cases.py`` (TC_DATA) –
the same dataset that generates ``Test_Cases_Filled.xlsx``.
No random / mock data is used.
"""

import pytest
import allure
import time
from pages.login_page import LoginPage
from pages.client_page import ClientPage
from pages.sales_order_page import SalesOrderPage
from pages.work_order_page import WorkOrderPage
from generate_test_cases import (
    load_client_data,
    load_sales_order_data,
    load_work_order_data,
)

# ── Load curated test data from TC_DATA ───────────────────────────────────────
CLIENT_DATA_LIST      = load_client_data()        # Client Management – Positive cases
SALES_ORDER_DATA_LIST = load_sales_order_data()   # Sales Orders       – Positive cases
WORK_ORDER_DATA_LIST  = load_work_order_data()    # Work Orders        – Positive cases


@allure.epic("TM-PMS Automation Suite")
@allure.feature("End-to-End Core Workflows")
class TestTMPMS:

    @pytest.mark.run(order=1)
    @allure.story("Login")
    @allure.title("TC-01 – Verify login with valid credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login(self, driver):
        """
        TC-01: Open the application URL and log in with valid credentials.
        Verifies that the user is redirected away from the login page.

        Test Data (from TC_DATA TC-01):
          Email: Prakasht@gmail.com | Password: 1234
        """
        login_page = LoginPage(driver)

        with allure.step("Open the application URL"):
            login_page.navigate()

        with allure.step("Enter valid email and password, click Login"):
            login_page.login("Prakasht@gmail.com", "1234")

        with allure.step("Verify successful redirect (URL must not contain /login)"):
            time.sleep(3)
            current_url = driver.current_url
            print("Redirected to: %s" % current_url)
            assert "login" not in current_url.lower(), (
                "Login failed — still on login page. URL: %s" % current_url
            )

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("client_data", CLIENT_DATA_LIST,
                             ids=[c["test_case_id"] for c in CLIENT_DATA_LIST])
    @allure.story("Client Management")
    @allure.title("Create Client – TC_DATA positive case")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_client(self, driver, client_data):
        """
        TC-02: Create a new client record using curated TC_DATA.
        Verifies redirect to the client list on successful creation.
        """
        client_page = ClientPage(driver)

        with allure.step("Navigate to Client Management"):
            client_page.navigate()

        with allure.step("Click Add New Client"):
            client_page.click_add_new_client()

        with allure.step(
            "[%s] Fill client form: %s" % (client_data["test_case_id"], client_data["client_name"])
        ):
            allure.dynamic.description(
                "Test Case: %s\nTechnique: Positive\nClient: %s"
                % (client_data["test_case_id"], client_data["client_name"])
            )
            client_page.create_client(client_data)

        with allure.step("Verify successful redirect after creation"):
            current_url = driver.current_url
            print("After creation URL: %s" % current_url)
            assert "/create-client" not in current_url, (
                "Client creation failed — still on form. URL: %s" % current_url
            )

    @pytest.mark.run(order=3)
    @pytest.mark.parametrize("order_data", SALES_ORDER_DATA_LIST,
                             ids=[o["test_case_id"] for o in SALES_ORDER_DATA_LIST])
    @allure.story("Sales Orders")
    @allure.title("Create Sales Order – TC_DATA positive case")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_sales_order(self, driver, order_data):
        """
        TC-03: Create a new Sales Order using curated TC_DATA.
        Verifies redirect to the Sales Orders list on successful creation.
        """
        so_page = SalesOrderPage(driver)

        with allure.step("Navigate to Sales Orders"):
            so_page.navigate()

        with allure.step("Click Add New Order"):
            so_page.click_add_new_order()

        with allure.step(
            "[%s] Fill and submit Sales Order: %s"
            % (order_data["test_case_id"], order_data["order_number"])
        ):
            allure.dynamic.description(
                "Test Case: %s\nTechnique: Positive\nOrder: %s"
                % (order_data["test_case_id"], order_data["order_number"])
            )
            so_page.create_sales_order(order_data)

        with allure.step("Verify successful redirect after creation"):
            current_url = driver.current_url
            print("After creation URL: %s" % current_url)
            assert "/create-sale-order" not in current_url, (
                "Sales Order creation failed — still on form. URL: %s" % current_url
            )

    @pytest.mark.run(order=4)
    @pytest.mark.parametrize("work_order_data", WORK_ORDER_DATA_LIST,
                             ids=[w["test_case_id"] for w in WORK_ORDER_DATA_LIST])
    @allure.story("Job Work / Work Orders")
    @allure.title("Create Work Order – TC_DATA positive case")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_job_work(self, driver, work_order_data):
        """
        TC-04: Create a new Job Work / Work Order using curated TC_DATA.
        Verifies redirect to the Work Orders list on successful creation.
        """
        wo_page = WorkOrderPage(driver)

        with allure.step("Navigate to Work Orders"):
            wo_page.navigate()

        with allure.step("Click Add New Work Order"):
            wo_page.click_add_new_work_order()

        with allure.step(
            "[%s] Fill Work Order form" % work_order_data["test_case_id"]
        ):
            allure.dynamic.description(
                "Test Case: %s\nTechnique: Positive\nQty: %s | Rate: %s"
                % (work_order_data["test_case_id"], work_order_data["outsource_qty"], work_order_data["rate"])
            )
            wo_page.create_work_order(work_order_data)

        with allure.step("Verify successful redirect after creation"):
            current_url = driver.current_url
            print("After creation URL: %s" % current_url)
            assert "/create-work-order" not in current_url, (
                "Job Work creation failed — still on form. URL: %s" % current_url
            )

