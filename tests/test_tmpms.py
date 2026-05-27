import pytest
import allure
import time
from pages.login_page import LoginPage
from pages.client_page import ClientPage
from pages.sales_order_page import SalesOrderPage
from pages.work_order_page import WorkOrderPage
from utils.data_generator import (
    generate_mock_clients,
    generate_mock_sales_orders,
    generate_mock_work_orders,
)

COUNT = 10
CLIENT_DATA_LIST      = generate_mock_clients(COUNT)
CLIENT_NAMES          = [c["client_name"] for c in CLIENT_DATA_LIST]
SALES_ORDER_DATA_LIST = generate_mock_sales_orders(CLIENT_NAMES, COUNT)
WORK_ORDER_DATA_LIST  = generate_mock_work_orders(CLIENT_NAMES, COUNT)


@allure.epic("TM-PMS Automation Suite")
@allure.feature("End-to-End Core Workflows")
class TestTMPMS:

    @pytest.mark.run(order=1)
    @allure.story("Login")
    @allure.title("TC-01 - Verify login with valid credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login(self, driver):
        """
        TC-01: Open the application URL and log in with valid credentials.
        Verifies that the user is redirected away from the login page.
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
    @pytest.mark.parametrize("client_data", CLIENT_DATA_LIST)
    @allure.story("Client Management")
    @allure.title("TC-02 - Create Client")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_client(self, driver, client_data):
        """
        TC-02: Create a new client record with all required fields.
        Verifies redirect to the client list on successful creation.
        """
        client_page = ClientPage(driver)

        with allure.step("Navigate to Client Management"):
            client_page.navigate()

        with allure.step("Click Add New Client"):
            client_page.click_add_new_client()

        with allure.step("Fill client form for: %s" % client_data["client_name"]):
            client_page.create_client(client_data)

        with allure.step("Verify successful redirect after creation"):
            current_url = driver.current_url
            print("After creation URL: %s" % current_url)
            assert "/create-client" not in current_url, (
                "Client creation failed — still on form. URL: %s" % current_url
            )

    @pytest.mark.run(order=3)
    @pytest.mark.parametrize("order_data", SALES_ORDER_DATA_LIST)
    @allure.story("Sales Orders")
    @allure.title("TC-03 - Create Sales Order")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_sales_order(self, driver, order_data):
        """
        TC-03: Create a new Sales Order with all required fields.
        Verifies redirect to the Sales Orders list on successful creation.
        """
        so_page = SalesOrderPage(driver)

        with allure.step("Navigate to Sales Orders"):
            so_page.navigate()

        with allure.step("Click Add New Order"):
            so_page.click_add_new_order()

        with allure.step("Fill and submit Sales Order: %s" % order_data["order_number"]):
            so_page.create_sales_order(order_data)

        with allure.step("Verify successful redirect after creation"):
            current_url = driver.current_url
            print("After creation URL: %s" % current_url)
            assert "/create-sale-order" not in current_url, (
                "Sales Order creation failed — still on form. URL: %s" % current_url
            )

    @pytest.mark.run(order=4)
    @pytest.mark.parametrize("idx", range(COUNT))
    @allure.story("Job Work / Work Orders")
    @allure.title("TC-04 - Create Job Work (Work Order)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_job_work(self, driver, idx):
        """
        TC-04: Create a new Job Work / Work Order.
        Selects Branch, Tax, and Vendor dropdowns, fills dates and remark,
        adds an item line, and verifies redirect to the Work Orders list.
        """
        wo_page = WorkOrderPage(driver)
        wo_data = WORK_ORDER_DATA_LIST[idx]

        with allure.step("Navigate to Work Orders"):
            wo_page.navigate()

        with allure.step("Click Add New Work Order"):
            wo_page.click_add_new_work_order()

        with allure.step("Fill Work Order (iteration %d)" % (idx + 1)):
            wo_page.create_work_order(wo_data)

        with allure.step("Verify successful redirect after creation"):
            current_url = driver.current_url
            print("After creation URL: %s" % current_url)
            assert "/create-work-order" not in current_url, (
                "Job Work creation failed — still on form. URL: %s" % current_url
            )
