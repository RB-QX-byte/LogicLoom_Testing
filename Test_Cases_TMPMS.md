# Test Cases – TM-PMS Automation Assignment

**Application URL:** https://tmpms.disctesting.in/login  
**Prepared By:** Rachit  
**Module:** Automation Testing (QA Intern Assignment)  
**Tool Stack:** Python | Selenium | Pytest | Allure  
**Date:** 26-May-2026

---

## Module 1 – Login Page

### TC-01 – Verify Login with Valid Credentials

| Field | Details |
|---|---|
| **Test Case ID** | TC-01 |
| **Module** | Login |
| **Test Type** | Functional / Positive |
| **Priority** | High |

**Pre-condition:** Browser is open, internet is available.

**Steps to Execute:**

| # | Step | Expected Result |
|---|---|---|
| 1 | Open URL: `https://tmpms.disctesting.in/login` | Login page loads successfully |
| 2 | Enter Email: `Prakasht@gmail.com` | Email field accepts the input |
| 3 | Enter Password: `1234` | Password field shows masked characters |
| 4 | Click the **Login** button | Form is submitted |
| 5 | Observe URL after submission | User is redirected to Dashboard (URL no longer contains `/login`) |

**Expected Result:** User is logged in and redirected to the dashboard.  
**Actual Result:** Pass  
**Status:** ✅ Pass

---

### TC-02 – Verify Login with Invalid Credentials

| Field | Details |
|---|---|
| **Test Case ID** | TC-02 |
| **Module** | Login |
| **Test Type** | Functional / Negative |
| **Priority** | Medium |

**Pre-condition:** Browser is open.

**Steps to Execute:**

| # | Step | Expected Result |
|---|---|---|
| 1 | Open URL: `https://tmpms.disctesting.in/login` | Login page loads |
| 2 | Enter Email: `wrong@email.com` | Email field accepts input |
| 3 | Enter Password: `wrongpass` | Password is masked |
| 4 | Click **Login** | Form submits |
| 5 | Observe response | Error message is shown; user stays on login page |

**Expected Result:** Login fails; error/toast message displayed.  
**Status:** 📋 Manual (out of automation scope for this run)

---

## Module 2 – Client Management (Create Client)

### TC-03 – Create a New Client with Valid Data

| Field | Details |
|---|---|
| **Test Case ID** | TC-03 |
| **Module** | Client Management |
| **Test Type** | Functional / Positive |
| **Priority** | High |
| **Iterations** | 35 |

**Pre-condition:** User is logged in and on the Dashboard.

**Steps to Execute:**

| # | Step | Expected Result |
|---|---|---|
| 1 | Click **Customer Management → Client Management** in the sidebar | Client list page loads |
| 2 | Click **+ Add New Client** button | Client creation form opens |
| 3 | Enter **Client Name** (e.g., `Intern Client 5389 Ltd 01`) | Field accepts input |
| 4 | Enter **Contact Person Name** | Field accepts input |
| 5 | Enter **Contact Person Email** | Field accepts input |
| 6 | Enter **Contact Person Mobile** | Field accepts input |
| 7 | Enter **GSTIN Number** (15-char valid format) | Field accepts input |
| 8 | Enter **PAN Number** | Field accepts input |
| 9 | Enter **TDS %** | Field accepts numeric value |
| 10 | Enter **Billing Email** | Field accepts input |
| 11 | Enter **Mobile Number** (10 digits) | Field accepts input |
| 12 | Enter **Phone Number** | Field accepts input |
| 13 | Enter **Pincode** | Field accepts input |
| 14 | Enter **Vendor Code** | Field accepts input |
| 15 | Select **Country** → `India` from dropdown | Dropdown updates to show India |
| 16 | Select **State** → `Maharashtra` | Dropdown filters and shows state |
| 17 | Select **City** → `Mumbai` | City is selected |
| 18 | Tick **Is Active** checkbox | Checkbox is marked |
| 19 | Enter **Ship To Location**, **Ship To Address**, **Pincode** | Fields accept input |
| 20 | Click **Create** button | Form is submitted |
| 21 | Observe URL and page content | Redirected to client list; new client appears |

**Expected Result:** New client record created; redirected to client list.  
**Actual Result:** Pass (35 iterations)  
**Status:** ✅ Pass

---

### TC-04 – Try Creating Client with Duplicate GSTIN (Negative)

| Field | Details |
|---|---|
| **Test Case ID** | TC-04 |
| **Module** | Client Management |
| **Test Type** | Functional / Negative |
| **Priority** | Medium |

**Pre-condition:** A client with a specific GSTIN already exists.

**Steps to Execute:**

| # | Step | Expected Result |
|---|---|---|
| 1 | Navigate to Client creation form | Form opens |
| 2 | Fill all fields but enter an already used GSTIN | Fields accept input |
| 3 | Click **Create** | Server rejects the request |
| 4 | Observe response | Error message: duplicate GSTIN not allowed |

**Expected Result:** Application shows error; client not created.  
**Status:** 📋 Manual (unique constraint handled in automation via dynamic RUN_ID)

---

## Module 3 – Sales Orders (Create Sales Order)

### TC-05 – Create a New Sales Order with Valid Data

| Field | Details |
|---|---|
| **Test Case ID** | TC-05 |
| **Module** | Sales Orders |
| **Test Type** | Functional / Positive |
| **Priority** | High |
| **Iterations** | 35 |

**Pre-condition:** User is logged in; at least one Client exists in the system.

**Steps to Execute:**

| # | Step | Expected Result |
|---|---|---|
| 1 | Click **Order Management → Sales Orders** in sidebar | Sales Orders list page loads |
| 2 | Click **+ Add New Order** | Sales Order creation form opens |
| 3 | Select **Client** from dropdown (type client name to filter) | Client is selected |
| 4 | Select **Branch** from dropdown | Branch is selected |
| 5 | Select **Project Type** from dropdown | Project Type is selected |
| 6 | Select **Project Manager** from dropdown | Project Manager is selected |
| 7 | Enter **Sale Order No** | Field accepts input |
| 8 | Enter **Sale Order Reference No** | Field accepts input |
| 9 | Enter **Order Date** | Date picker/field accepts value |
| 10 | Enter **Delivery Date** | Delivery date is set |
| 11 | Enter **Address** | Textarea accepts input |
| 12 | Select **Item Code / Name** from the item picker dropdown | Item is selected |
| 13 | Click **ADD** button in the Item Details section | Item row is added to the grid |
| 14 | Edit grid row fields: Item Line Code, Display Name, Item Code, MAT, Size, Description | Fields accept values |
| 15 | Enter **Quantity** and **Unit Rate** | Numeric values accepted; Total Amount auto-calculates |
| 16 | Select **Tax %** from the Tax dropdown in the grid row | Tax rate is selected |
| 17 | Set **Expected Delivery Date** in the grid row | Date is set |
| 18 | Click **Create** button | Form is submitted |
| 19 | Observe URL | Redirected to Sales Orders list |

**Expected Result:** Sales Order is created; redirect to list page occurs.  
**Actual Result:** Pass (35 iterations)  
**Status:** ✅ Pass

---

### TC-06 – Create Sales Order without selecting Client (Negative)

| Field | Details |
|---|---|
| **Test Case ID** | TC-06 |
| **Module** | Sales Orders |
| **Test Type** | Functional / Negative |
| **Priority** | Medium |

**Steps:**

| # | Step | Expected Result |
|---|---|---|
| 1 | Open Sales Order creation form | Form loads |
| 2 | Leave Client dropdown empty | No selection |
| 3 | Fill remaining fields and click **Create** | Form validation triggers |
| 4 | Observe | Required field error shown next to Client |

**Expected Result:** Form validation blocks submission; error message shown.  
**Status:** 📋 Manual (automation uses valid data to test positive flows)

---

## Module 4 – Job Work (Create Work Order)

### TC-07 – Create a New Work Order / Job Work

| Field | Details |
|---|---|
| **Test Case ID** | TC-07 |
| **Module** | Job Works / Work Orders |
| **Test Type** | Functional / Positive |
| **Priority** | High |
| **Iterations** | 35 |

**Pre-condition:** User is logged in; at least one Vendor/Client exists.

**Steps to Execute:**

| # | Step | Expected Result |
|---|---|---|
| 1 | Click **Job Works → Work Order** in sidebar | Work Order list page loads |
| 2 | Click **+ Add New Work Order** | Work Order creation form opens |
| 3 | Select **Vendor** from dropdown | Vendor is selected |
| 4 | Select **Branch** from dropdown | Branch is selected |
| 5 | Select **Tax** from dropdown | Tax rate is selected |
| 6 | Enter **Date** | Date field accepts input |
| 7 | Enter **Expected Receipt Date** | Date is set |
| 8 | Enter **Remark** | Textarea accepts input |
| 9 | Tick **Is Active** checkbox if not already checked | Checkbox is marked |
| 10 | Select **Item** from the item picker dropdown above the grid | Item is selected |
| 11 | Click **ADD** button | Item row is added to the grid |
| 12 | Select **Batch** from dropdown in grid row | Batch is selected |
| 13 | Select **Operations** from dropdown in grid row | Operation is selected |
| 14 | Click **Create** button | Form is submitted |
| 15 | Observe URL | Redirected to Work Orders list |

**Expected Result:** Work Order / Job Work created; redirected to list page.  
**Actual Result:** Pass (35 iterations)  
**Status:** ✅ Pass

---

### TC-08 – Create Work Order without selecting Vendor (Negative)

| Field | Details |
|---|---|
| **Test Case ID** | TC-08 |
| **Module** | Job Works |
| **Test Type** | Functional / Negative |
| **Priority** | Medium |

**Steps:**

| # | Step | Expected Result |
|---|---|---|
| 1 | Open Work Order creation form | Form loads |
| 2 | Leave Vendor field empty | No selection |
| 3 | Fill remaining fields and click **Create** | Validation fires |
| 4 | Observe error | Required field message shown |

**Expected Result:** Submission is blocked; error shown.  
**Status:** 📋 Manual

---

### TC-09 – Verify Client Field Input Boundaries (Boundary Value Analysis)

| Field | Details |
|---|---|
| **Test Case ID** | TC-09 |
| **Module** | Client Management |
| **Test Type** | Functional / Boundary Value Analysis |
| **Priority** | High |

**Pre-condition:** User is logged in and on the client creation form.

**Steps to Execute:**

| # | Step | Expected Result |
|---|---|---|
| 1 | Enter a **Mobile Number** with exactly 9 digits (below boundary) | Validation error shown (10 digits required) |
| 2 | Enter a **Mobile Number** with exactly 10 digits (exact boundary) | Field accepts the input successfully |
| 3 | Enter a **Mobile Number** with exactly 11 digits (above boundary) | Field blocks or cuts off input at 10 digits |
| 4 | Enter **TDS Percentage** as `0.0` or `99.9` (boundary values) | Fields accept the boundary numeric inputs |

**Expected Result:** Mobile number validation strictly enforces the 10-digit limit; TDS field accepts valid boundary percentages.  
**Status:** 📋 Manual (handled in automation by generating strictly compliant 10-digit mobile numbers)

---

### TC-10 – Submit Sales Order with Empty Item Grid or Zero Quantity (Edge Case)

| Field | Details |
|---|---|
| **Test Case ID** | TC-10 |
| **Module** | Sales Orders |
| **Test Type** | Functional / Edge Case |
| **Priority** | High |

**Pre-condition:** User is logged in and on the Sales Order creation form.

**Steps to Execute:**

| # | Step | Expected Result |
|---|---|---|
| 1 | Select Client, Branch, Project Type, and Project Manager | Dropdowns updated |
| 2 | Do NOT select any Item Code and do NOT click **ADD** (Empty Grid) | Grid remains empty |
| 3 | Click the **Create** button | Form validation blocks submission; alerts user to add at least one item |
| 4 | Select an item, click **ADD**, but enter **Quantity** as `0` | Field shows `0` |
| 5 | Click **Create** | Validation triggers; alert shows "Quantity must be greater than 0" |

**Expected Result:** Empty item grid or zero quantity submission is blocked by form validation.  
**Status:** 📋 Manual (automation uses positive quantities and clicks ADD to test happy path)

---

## Summary Table

| TC ID | Module | Type | Priority | Automated | Status |
|---|---|---|---|---|---|
| TC-01 | Login | Positive | High | ✅ Yes | ✅ Pass |
| TC-02 | Login | Negative | Medium | ❌ Manual | 📋 Manual |
| TC-03 | Client Management | Positive | High | ✅ Yes (×35) | ✅ Pass |
| TC-04 | Client Management | Negative | Medium | ❌ Manual | 📋 Manual |
| TC-05 | Sales Orders | Positive | High | ✅ Yes (×35) | ✅ Pass |
| TC-06 | Sales Orders | Negative | Medium | ❌ Manual | 📋 Manual |
| TC-07 | Job Work / Work Order | Positive | High | ✅ Yes (×35) | ✅ Pass |
| TC-08 | Job Work / Work Order | Negative | Medium | ❌ Manual | 📋 Manual |
| TC-09 | Client Management | Boundary | High | ❌ Manual | 📋 Manual |
| TC-10 | Sales Orders | Edge Case | High | ❌ Manual | 📋 Manual |

**Total Test Cases Documented:** 10  
**Automated:** 4 (with 35 data iterations each)  
**Manual / Negative / Boundary / Edge:** 6  

---

*Prepared using Selenium + Pytest + Allure*

