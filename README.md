# TM-PMS Automation Suite

**Automation Testing Assignment — LogicLoom Technologies**

| | |
|---|---|
| **Application URL** | https://tmpms.disctesting.in/login |
| **Login** | Prakasht@gmail.com / 1234 |
| **Tool Stack** | Python · Selenium · Pytest · Allure · pytest-html |
| **Python Version** | 3.12+ |

---

## Project Structure

```
LogicLoom_Testing/
├── pages/
│   ├── base_page.py          # Shared browser interaction utilities (POM base class)
│   ├── login_page.py         # Login page object
│   ├── client_page.py        # Client Management page object
│   ├── sales_order_page.py   # Sales Orders page object
│   └── work_order_page.py    # Work Orders (Job Work) page object
├── tests/
│   ├── test_tmpms.py         # Main E2E suite: Login → Client → Sales Order → Job Work
│   └── test_work_order_only.py  # Work Order boundary & edge-case suite (10 TCs)
├── utils/
│   └── data_generator.py     # Dynamic test data generator (unique per run)
├── reports/                  # Auto-generated HTML reports and failure screenshots
├── conftest.py               # Pytest fixtures: Chrome WebDriver, failure hooks
├── pyproject.toml            # Dependencies and pytest config
└── Test_Cases_TMPMS.md       # Manual test case documentation
```

---

## Automated Test Coverage

### `tests/test_tmpms.py` — End-to-End Core Workflows

| Test | Description | Iterations |
|---|---|---|
| TC-01 — Login | Valid credentials → redirect to dashboard | 1 |
| TC-02 — Create Client | All required fields; redirect to client list | 10 |
| TC-03 — Create Sales Order | Dropdowns + item grid; redirect to orders list | 10 |
| TC-04 — Create Job Work | Branch/Tax/Vendor + item grid; redirect to WO list | 10 |

### `tests/test_work_order_only.py` — Work Order Boundary Suite

| Test ID | Scenario |
|---|---|
| TC-WO-01 | Required fields only (no optional fields) |
| TC-WO-02 | All fields including remark and receipt date |
| TC-WO-03 | Boundary date: order date = today |
| TC-WO-04 | Boundary date: 1 day ahead |
| TC-WO-05 | Boundary date: 1 year ahead |
| TC-WO-06 | Boundary quantity: minimum (1) |
| TC-WO-07 | Boundary quantity: large (500) |
| TC-WO-08 | Boundary rate: minimum (1) |
| TC-WO-09 | Boundary rate: high (99999) |
| TC-WO-10 | Edge case: long remark (~500 chars) |

---

## Running the Tests

### Install dependencies

```bash
pip install -e .
```

### Run the full E2E suite (generates HTML report automatically)

```bash
pytest tests/test_tmpms.py -v --headless=false
```

### Run Work Order boundary suite

```bash
pytest tests/test_work_order_only.py -v --headless=false
```

### Run all tests with Allure report

```bash
pytest tests/ -v --headless=false --alluredir=allure-results
allure serve allure-results
```

### Run in headless mode (CI/CD)

```bash
pytest tests/ -v
```

---

## Reports

After every run, the following are auto-generated:

- **HTML Report:** `reports/report.html` — open in any browser
- **Failure Screenshots:** `reports/screenshots/` — PNG per failed test
- **Allure Report:** run `allure serve allure-results` (requires Allure CLI)
