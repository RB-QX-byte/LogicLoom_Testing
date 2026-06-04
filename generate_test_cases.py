"""
Test Case Generator – TM-PMS (Quality-focused, curated set)
Each module has exactly ONE representative test case per technique:
  Positive | Negative | EP (×2) | BVA (×2) | Decision Table | Error Guessing | Edge Case
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# ── Styles ───────────────────────────────────────────────────────────────────
HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
FILLS = {
    "Positive":       PatternFill("solid", fgColor="D9EAD3"),   # green
    "Negative":       PatternFill("solid", fgColor="FFD7D7"),   # red
    "EP":             PatternFill("solid", fgColor="DDEEFF"),   # blue
    "BVA":            PatternFill("solid", fgColor="FFF2CC"),   # yellow
    "Decision Table": PatternFill("solid", fgColor="E8D5F5"),   # purple
    "Error Guessing": PatternFill("solid", fgColor="FFE8C8"),   # orange
    "Edge Case":      PatternFill("solid", fgColor="D9F2F9"),   # sky blue
}

HEADER_FONT = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
NORMAL_FONT = Font(name="Calibri", size=10)
thin = Side(style="thin", color="CCCCCC")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP   = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

# ── Columns (exact template match) ───────────────────────────────────────────
COLUMNS = [
    "Sr.No", "Test case ID", "Module", "Sub Module",
    "Test Case", "Test Cases Description",
    "Test Data", "Prerequisite", "Steps to Reproduce",
    "Expected Result", "Actual Result",
    "Test Mode (Positive/Negative)", "Severity", "Priority",
]
COL_WIDTHS = [6, 14, 22, 22, 42, 52, 42, 42, 72, 55, 18, 24, 12, 10]

# ── Test Cases ────────────────────────────────────────────────────────────────
# Each tuple: module | sub_module | tc_name | description | test_data | prereq | steps | expected | actual | mode | technique | severity | priority
TC_DATA = [

    # ════════════════════════════════════════════════════════════════
    # MODULE 1 – LOGIN
    # ════════════════════════════════════════════════════════════════

    (   # 1 – POSITIVE
        "Login", "Login Form",
        "[Positive] Login with valid credentials",
        "Verify a registered user can log in with correct email and password and is redirected to the Dashboard.",
        "Email: Prakasht@gmail.com\nPassword: 1234",
        "Browser is open. Application URL is reachable: https://tmpms.disctesting.in/login",
        "1. Open https://tmpms.disctesting.in/login\n2. Enter Email: Prakasht@gmail.com\n3. Enter Password: 1234\n4. Click the Login button",
        "User is logged in successfully. Redirected to Dashboard. URL no longer contains /login.",
        "Pass", "Positive", "Positive", "Critical", "High",
    ),
    (   # 2 – NEGATIVE
        "Login", "Login Form",
        "[Negative] Login with wrong password",
        "Verify that login fails when a valid email is entered but the password is incorrect.",
        "Email: Prakasht@gmail.com (valid)\nPassword: wrongpass (incorrect)",
        "Browser is open. Login page is loaded.",
        "1. Open login page\n2. Enter Email: Prakasht@gmail.com\n3. Enter Password: wrongpass\n4. Click Login",
        "Login fails. Error message like 'Invalid credentials' is shown. User remains on the login page.",
        "To be executed", "Negative", "Negative", "High", "High",
    ),
    (   # 3 – EP: Valid class
        "Login", "Login Form",
        "[EP] Email – valid format class (registered email)",
        "Equivalence Partitioning – Valid Class: Any correctly formatted, registered email should allow login.",
        "Email: Prakasht@gmail.com (valid class – correct format, registered)\nPassword: 1234",
        "Login page is open.",
        "1. Open login page\n2. Enter a correctly formatted registered email\n3. Enter correct password\n4. Click Login",
        "Login succeeds. User is redirected to Dashboard. All valid-class emails must work the same way.",
        "Pass", "Positive", "EP", "High", "High",
    ),
    (   # 4 – EP: Invalid class
        "Login", "Login Form",
        "[EP] Email – invalid format class (missing @ symbol)",
        "Equivalence Partitioning – Invalid Class: Any email without '@' represents the entire invalid-format partition. System must reject all emails in this class.",
        "Email: PrakashatGmail.com (no @ – invalid format class)\nPassword: 1234",
        "Login page is open.",
        "1. Open login page\n2. Enter Email: PrakashatGmail.com\n3. Enter Password: 1234\n4. Click Login",
        "Validation error 'Enter a valid email address' appears. Form is not submitted. All emails without '@' are in this invalid class.",
        "To be executed", "Negative", "EP", "Medium", "High",
    ),
    (   # 5 – BVA (treating password length as boundary)
        "Login", "Login Form",
        "[BVA] Login with single-character password (minimum length boundary)",
        "Boundary Value Analysis: A 1-character password tests the minimum length boundary. System should reject it if minimum length is > 1, or accept it if no minimum exists.",
        "Email: Prakasht@gmail.com\nPassword: 1 (only 1 character – minimum boundary)",
        "Login page is open.",
        "1. Open login page\n2. Enter Email: Prakasht@gmail.com\n3. Enter Password: 1 (single character)\n4. Click Login",
        "If password minimum length is > 1: validation error shown. If no minimum enforced: login attempt is made and fails with 'Invalid credentials'. Either way, system should NOT crash.",
        "To be executed", "Negative", "BVA", "Medium", "Medium",
    ),
    (   # 6 – Decision Table
        "Login", "Login Form",
        "[Decision Table] Invalid email + Invalid password (both wrong)",
        "Decision Table Testing: Testing the combination where BOTH email and password are incorrect. This covers the 'both invalid' cell of the email × password decision table.",
        "Email: nobody@nowhere.com (unregistered)\nPassword: wrongpass (incorrect)\n\nDecision Table:\n| Email   | Password | Result |\n| Valid   | Valid    | Login  |\n| Valid   | Invalid  | Fail   |\n| Invalid | Valid    | Fail   |\n| Invalid | Invalid  | Fail   | ← This TC",
        "Login page is open.",
        "1. Open login page\n2. Enter Email: nobody@nowhere.com\n3. Enter Password: wrongpass\n4. Click Login",
        "Login fails. Error message displayed. User stays on login page. Both invalid inputs must produce the same 'fail' outcome.",
        "To be executed", "Negative", "Decision Table", "High", "High",
    ),
    (   # 7 – Error Guessing
        "Login", "Login Form",
        "[Error Guessing] Click Login with both fields completely empty",
        "Error Guessing: A common user mistake is clicking Login without entering anything. The system must handle this gracefully with proper validation — not crash or freeze.",
        "Email: (blank)\nPassword: (blank)",
        "Login page is open.",
        "1. Open login page\n2. Do not enter anything in Email or Password\n3. Directly click the Login button",
        "Validation errors appear on both fields (e.g., 'Email is required', 'Password is required'). The page must NOT navigate away or crash.",
        "To be executed", "Negative", "Error Guessing", "Medium", "High",
    ),
    (   # 8 – Edge Case
        "Login", "Login Form",
        "[Edge Case] Email entered in all uppercase letters",
        "Edge Case: Email addresses are typically case-insensitive. Testing with all-caps email checks if the system treats 'PRAKASHT@GMAIL.COM' the same as 'Prakasht@gmail.com'.",
        "Email: PRAKASHT@GMAIL.COM (all uppercase)\nPassword: 1234",
        "Login page is open.",
        "1. Open login page\n2. Enter Email in all caps: PRAKASHT@GMAIL.COM\n3. Enter Password: 1234\n4. Click Login",
        "System should log in successfully (email is case-insensitive). If login fails, it means the system is case-sensitive — which should be documented as a bug.",
        "To be executed", "Positive", "Edge Case", "Low", "Medium",
    ),

    # ════════════════════════════════════════════════════════════════
    # MODULE 2 – CLIENT MANAGEMENT
    # ════════════════════════════════════════════════════════════════

    (   # 9 – POSITIVE
        "Client Management", "Create Client",
        "[Positive] Create client with all valid required fields",
        "Verify that a new client is created successfully when all mandatory fields are correctly filled with valid data.",
        "Client Name: ABC Pvt Ltd\nContact Person: Rahul Sharma\nContact Email: rahul@abc.com\nContact Mobile: 9876543210\nGSTIN: 27AAPFU0939F1ZV\nPAN: AAPFU0939F\nTDS%: 5\nBilling Email: billing@abc.com\nMobile: 9876543210\nPhone: 0221234567\nPincode: 400001\nVendor Code: VC001\nCountry: India | State: Maharashtra | City: Mumbai",
        "User is logged in. Dashboard is visible.",
        "1. Click Customer Management → Client Management in sidebar\n2. Click '+ Add New Client'\n3. Fill all fields with the provided valid test data\n4. Select Country: India → State: Maharashtra → City: Mumbai\n5. Fill Ship To Location, Address, Pincode\n6. Click Create",
        "Client is created successfully. User is redirected to the client list. The new client 'ABC Pvt Ltd' appears in the list.",
        "Pass", "Positive", "Positive", "Critical", "High",
    ),
    (   # 10 – NEGATIVE
        "Client Management", "Create Client",
        "[Negative] Create client without entering Client Name",
        "Verify that the form blocks submission when the mandatory Client Name field is left empty.",
        "Client Name: (blank – left empty)\nAll other fields: filled with valid data",
        "User is logged in. Client creation form is open.",
        "1. Navigate to Client Management → Add New Client\n2. Leave Client Name field completely empty\n3. Fill all other fields with valid data\n4. Click Create",
        "Form is not submitted. Validation error 'Client Name is required' (or similar) appears next to the field.",
        "To be executed", "Negative", "Negative", "High", "High",
    ),
    (   # 11 – EP: Valid class
        "Client Management", "Create Client",
        "[EP] Mobile Number – valid class (10 numeric digits)",
        "Equivalence Partitioning – Valid Class: Any mobile number with exactly 10 numeric digits belongs to the valid partition and must be accepted by the system.",
        "Mobile Number: 9876543210 (10 digits, all numeric – valid class)",
        "User is logged in. Client creation form is open.",
        "1. Open Client creation form\n2. Enter Mobile Number: 9876543210\n3. Fill all other required fields with valid data\n4. Click Create",
        "Mobile number is accepted. Client is created successfully. All 10-digit numeric values are in the valid equivalence class.",
        "Pass", "Positive", "EP", "Medium", "High",
    ),
    (   # 12 – EP: Invalid class
        "Client Management", "Create Client",
        "[EP] Mobile Number – invalid class (alphabetic input)",
        "Equivalence Partitioning – Invalid Class: Any non-numeric input in the Mobile field represents the 'wrong data type' invalid partition. System must reject all values in this class.",
        "Mobile Number: ABCDEFGHIJ (letters instead of digits – invalid class)",
        "User is logged in. Client creation form is open.",
        "1. Open Client creation form\n2. Enter Mobile Number: ABCDEFGHIJ\n3. Fill all other fields with valid data\n4. Click Create",
        "Validation error shown. Non-numeric input is rejected. All alphabetic inputs belong to the same invalid class and must produce the same error.",
        "To be executed", "Negative", "EP", "Medium", "High",
    ),
    (   # 13 – BVA: Below boundary
        "Client Management", "Create Client",
        "[BVA] Mobile Number – 9 digits (one below the 10-digit boundary)",
        "Boundary Value Analysis: 9 digits is one unit below the minimum valid boundary of 10 digits. This must be rejected.",
        "Mobile Number: 987654321 (9 digits – one below lower boundary)",
        "User is logged in. Client creation form is open.",
        "1. Open Client creation form\n2. Enter Mobile Number: 987654321 (9 digits only)\n3. Fill all other fields\n4. Click Create",
        "Validation error shown. A 9-digit mobile number is below the accepted boundary and must be rejected.",
        "To be executed", "Negative", "BVA", "Medium", "High",
    ),
    (   # 14 – BVA: Exact boundary
        "Client Management", "Create Client",
        "[BVA] Mobile Number – 10 digits (exact valid boundary)",
        "Boundary Value Analysis: 10 digits is the exact valid boundary. The system must accept this without any errors.",
        "Mobile Number: 9876543210 (10 digits – exact boundary)",
        "User is logged in. Client creation form is open.",
        "1. Open Client creation form\n2. Enter Mobile Number: 9876543210 (exactly 10 digits)\n3. Fill all other fields\n4. Click Create",
        "Mobile number accepted without any error. Client is created successfully.",
        "Pass", "Positive", "BVA", "Medium", "High",
    ),
    (   # 15 – Decision Table
        "Client Management", "Create Client",
        "[Decision Table] Valid GSTIN + Invalid Mobile vs Invalid GSTIN + Valid Mobile",
        "Decision Table Testing: Tests two rule combinations to verify the system validates each field independently and shows the correct error for whichever field is invalid.\n\nRule Table:\n| GSTIN   | Mobile  | Outcome         |\n| Valid   | Valid   | Client Created  |\n| Valid   | Invalid | Mobile Error    | ← Test A\n| Invalid | Valid   | GSTIN Error     | ← Test B\n| Invalid | Invalid | Both Errors     |",
        "Test A: GSTIN=27AAPFU0939F1ZV (valid) + Mobile=ABCD (invalid letters)\nTest B: GSTIN=123 (too short) + Mobile=9876543210 (valid)",
        "User is logged in. Client creation form is open.",
        "-- Test A --\n1. Open form\n2. Enter GSTIN: 27AAPFU0939F1ZV (valid)\n3. Enter Mobile: ABCD (invalid)\n4. Fill other fields\n5. Click Create → Expect Mobile error only\n\n-- Test B --\n1. Open form again\n2. Enter GSTIN: 123 (invalid)\n3. Enter Mobile: 9876543210 (valid)\n4. Fill other fields\n5. Click Create → Expect GSTIN error only",
        "Test A: Only Mobile field shows an error. GSTIN is accepted.\nTest B: Only GSTIN field shows an error. Mobile is accepted.\nThis confirms fields are validated independently.",
        "To be executed", "Negative", "Decision Table", "High", "High",
    ),
    (   # 16 – Error Guessing
        "Client Management", "Create Client",
        "[Error Guessing] Try creating second client with same GSTIN (duplicate)",
        "Error Guessing: GSTIN is a unique tax identifier. Creating two clients with the same GSTIN is a real-world mistake. System must detect and reject duplicates.",
        "GSTIN: 27AAPFU0939F1ZV (same GSTIN as an already existing client)",
        "User is logged in. A client with GSTIN 27AAPFU0939F1ZV already exists in the system.",
        "1. Navigate to Client Management → Add New Client\n2. Enter all valid fields\n3. Enter GSTIN: 27AAPFU0939F1ZV (already used by another client)\n4. Click Create",
        "System rejects the form. Error like 'GSTIN already exists' or 'Duplicate entry not allowed' is shown. No new duplicate client is created.",
        "To be executed", "Negative", "Error Guessing", "High", "High",
    ),
    (   # 17 – Edge Case
        "Client Management", "Create Client",
        "[Edge Case] Client Name with only special characters",
        "Edge Case: What happens when Client Name is filled with only special characters like @#$%? This is a non-standard but possible user input.",
        "Client Name: @#$%^&*!\nAll other fields: valid",
        "User is logged in. Client creation form is open.",
        "1. Open Client creation form\n2. Enter Client Name: @#$%^&*!\n3. Fill all other fields with valid data\n4. Click Create",
        "System should either show a validation error 'Special characters not allowed in Client Name' OR if accepted, the client name must display correctly in the list. System must NOT crash.",
        "To be executed", "Negative", "Edge Case", "Medium", "Medium",
    ),

    # ════════════════════════════════════════════════════════════════
    # MODULE 3 – SALES ORDERS
    # ════════════════════════════════════════════════════════════════

    (   # 18 – POSITIVE
        "Sales Orders", "Create Sales Order",
        "[Positive] Create sales order with all valid data",
        "Verify that a Sales Order is created successfully when all required fields are filled with valid data.",
        "Client: (existing client)\nBranch: (available branch)\nProject Type: (available)\nProject Manager: (available)\nOrder No: SO-001\nRef No: REF-001\nOrder Date: 2026-06-03\nDelivery Date: 2026-07-03\nAddress: 123 Test Street, Mumbai\nItem: (existing item)\nQty: 10 | Unit Rate: 500 | Tax: 18%\nExpected Delivery Date: 2026-07-03",
        "User is logged in. At least one Client, Branch, Project Type, Project Manager, and Item exist in the system.",
        "1. Click Order Management → Sales Orders in sidebar\n2. Click '+ Add New Order'\n3. Select Client from dropdown\n4. Select Branch, Project Type, Project Manager\n5. Enter Order No: SO-001, Ref No: REF-001\n6. Set Order Date: 2026-06-03, Delivery Date: 2026-07-03\n7. Enter Address\n8. Select Item → Click ADD button\n9. Enter Qty: 10 and Unit Rate: 500\n10. Select Tax: 18%\n11. Set Expected Delivery Date\n12. Click Create",
        "Sales Order is created successfully. User is redirected to the Sales Orders list. The new order SO-001 appears in the list.",
        "Pass", "Positive", "Positive", "Critical", "High",
    ),
    (   # 19 – NEGATIVE
        "Sales Orders", "Create Sales Order",
        "[Negative] Create sales order without selecting a Client",
        "Verify that form validation blocks submission when the mandatory Client field is left empty.",
        "Client: (not selected – dropdown left empty)\nAll other fields: filled with valid data",
        "User is logged in. Sales Order creation form is open.",
        "1. Navigate to Sales Orders → Add New Order\n2. Leave the Client dropdown empty (do not select anything)\n3. Fill all other fields with valid data\n4. Click Create",
        "Form is not submitted. Validation error 'Please select a Client' appears near the Client dropdown.",
        "To be executed", "Negative", "Negative", "High", "High",
    ),
    (   # 20 – EP: Valid class
        "Sales Orders", "Create Sales Order",
        "[EP] Quantity – valid class (any positive integer)",
        "Equivalence Partitioning – Valid Class: Any positive integer (1, 5, 25, 100...) belongs to the valid quantity partition. All values in this class must be accepted.",
        "Quantity: 25 (positive integer – represents valid class)\nUnit Rate: 200",
        "User is logged in. Sales Order form is open with an item added to the grid.",
        "1. Open Sales Order form and fill header fields\n2. Select item and click ADD\n3. Enter Quantity: 25\n4. Enter Unit Rate: 200\n5. Click Create",
        "Quantity 25 is accepted. Sales Order is created. Total Amount = 5000 (25 × 200).",
        "To be executed", "Positive", "EP", "Medium", "High",
    ),
    (   # 21 – EP: Invalid class
        "Sales Orders", "Create Sales Order",
        "[EP] Quantity – invalid class (negative number)",
        "Equivalence Partitioning – Invalid Class: Any negative number is logically invalid as a quantity. All negative values belong to the same invalid partition and must be rejected.",
        "Quantity: -5 (negative – invalid class)\nUnit Rate: 200",
        "User is logged in. Sales Order form with item in grid.",
        "1. Open Sales Order form\n2. Add item to grid\n3. Enter Quantity: -5\n4. Enter Unit Rate: 200\n5. Click Create",
        "Validation error shown. Negative quantity is rejected. All negative values produce the same error (same invalid class).",
        "To be executed", "Negative", "EP", "High", "High",
    ),
    (   # 22 – BVA: Just below minimum
        "Sales Orders", "Create Sales Order",
        "[BVA] Quantity – 0 (one below the minimum valid boundary of 1)",
        "Boundary Value Analysis: 0 is one unit below the minimum valid quantity boundary (which is 1). This must be rejected by the system.",
        "Quantity: 0 (one below minimum boundary)\nUnit Rate: 200",
        "User is logged in. Sales Order form with item added to grid.",
        "1. Open Sales Order form\n2. Add item to grid\n3. Enter Quantity: 0\n4. Enter Unit Rate: 200\n5. Click Create",
        "Validation error 'Quantity must be greater than 0' is shown. Form is not submitted.",
        "To be executed", "Negative", "BVA", "High", "High",
    ),
    (   # 23 – BVA: Exact minimum boundary
        "Sales Orders", "Create Sales Order",
        "[BVA] Quantity – 1 (exact minimum boundary, must be accepted)",
        "Boundary Value Analysis: 1 is the minimum valid boundary for quantity. The system must accept this value without any error.",
        "Quantity: 1 (exact minimum boundary – must be valid)\nUnit Rate: 200",
        "User is logged in. Sales Order form with item added to grid.",
        "1. Open Sales Order form\n2. Add item to grid\n3. Enter Quantity: 1\n4. Enter Unit Rate: 200\n5. Click Create",
        "Quantity 1 is accepted. Sales Order is created. Total Amount = 200 (1 × 200).",
        "To be executed", "Positive", "BVA", "Medium", "High",
    ),
    (   # 24 – Decision Table
        "Sales Orders", "Create Sales Order",
        "[Decision Table] Item in grid + Qty 0 vs Item in grid + Valid Qty",
        "Decision Table Testing: Tests that the item grid and quantity work together as a pair. Both conditions must be valid for order creation to succeed.\n\nRule Table:\n| Item Added | Qty Valid | Outcome           |\n| Yes        | Yes       | Order Created     |\n| Yes        | No (0)    | Qty Error         | ← Test A\n| No         | –         | 'Add Item' Error  | ← Test B",
        "Test A: Item added to grid + Quantity = 0\nTest B: No item added + Quantity = 10 (moot)",
        "User is logged in. Sales Order form is open.",
        "-- Test A --\n1. Open Sales Order form, fill header\n2. Select item and click ADD\n3. Enter Quantity: 0\n4. Click Create → Expect Quantity error\n\n-- Test B --\n1. Open Sales Order form, fill header\n2. Do NOT click ADD or select any item\n3. Click Create → Expect 'add an item' error",
        "Test A: Only Quantity error appears. Item grid is fine.\nTest B: Error 'Please add at least one item' appears.\nThis confirms both conditions are validated independently.",
        "To be executed", "Negative", "Decision Table", "High", "High",
    ),
    (   # 25 – Error Guessing
        "Sales Orders", "Create Sales Order",
        "[Error Guessing] Set Delivery Date earlier than Order Date",
        "Error Guessing: A common real-world data entry mistake — setting delivery before order. This is a logical impossibility and the system should catch it.",
        "Order Date: 2026-06-03\nDelivery Date: 2026-05-01 (before Order Date)",
        "User is logged in. Sales Order creation form is open.",
        "1. Open Sales Order form\n2. Set Order Date: 2026-06-03\n3. Set Delivery Date: 2026-05-01 (a date BEFORE the Order Date)\n4. Fill all other fields with valid data\n5. Click Create",
        "System shows validation error 'Delivery date cannot be before Order date'. Form is not submitted. This is a logical date-order check.",
        "To be executed", "Negative", "Error Guessing", "High", "High",
    ),
    (   # 26 – Edge Case
        "Sales Orders", "Create Sales Order",
        "[Edge Case] Total Amount auto-calculates on Qty × Rate input",
        "Edge Case: The Total Amount field should auto-calculate in real-time when Quantity and Unit Rate are entered, without the user needing to type it manually.",
        "Quantity: 10\nUnit Rate: 500\nExpected Auto-Calculated Total: 5000",
        "User is logged in. Sales Order form is open with an item already added to the grid.",
        "1. Open Sales Order form\n2. Add an item to the grid\n3. Enter Quantity: 10\n4. Enter Unit Rate: 500\n5. Observe the Total Amount field without clicking anywhere else",
        "Total Amount field auto-displays 5000 (10 × 500) immediately after input. User does not need to manually calculate or enter the total.",
        "To be executed", "Positive", "Edge Case", "Medium", "High",
    ),

    # ════════════════════════════════════════════════════════════════
    # MODULE 4 – JOB WORK / WORK ORDERS
    # ════════════════════════════════════════════════════════════════

    (   # 27 – POSITIVE
        "Job Work / Work Orders", "Create Work Order",
        "[Positive] Create work order with all valid required fields",
        "Verify that a Work Order (Job Work) is created successfully when all required fields are filled with valid data.",
        "Branch: (available)\nTax: 18%\nWork Order Date: 2026-06-03\nExpected Receipt Date: 2026-07-03\nVendor: (existing vendor)\nItem: (existing item)\nOutsource Qty: 10 | Rate: 100",
        "User is logged in. At least one Vendor, Branch, Tax option, and Item exist in the system.",
        "1. Click Job Works → Work Order in sidebar\n2. Click '+ Add New Work Order'\n3. Select Branch\n4. Select Tax: 18%\n5. Set Work Order Date: 2026-06-03\n6. Set Expected Receipt Date: 2026-07-03\n7. Select Vendor\n8. Select Item Code/Name\n9. Enter Outsource Qty: 10\n10. Enter Rate: 100\n11. Click Create",
        "Work Order is created successfully. User is redirected to the Work Orders list. The new work order appears in the list.",
        "Pass", "Positive", "Positive", "Critical", "High",
    ),
    (   # 28 – NEGATIVE
        "Job Work / Work Orders", "Create Work Order",
        "[Negative] Create work order without selecting a Vendor",
        "Verify that form validation prevents submission when the mandatory Vendor field is left empty.",
        "Vendor: (not selected – dropdown left empty)\nAll other fields: filled with valid data",
        "User is logged in. Work Order creation form is open.",
        "1. Navigate to Job Works → Add New Work Order\n2. Leave the Vendor dropdown empty\n3. Fill all other fields with valid data\n4. Click Create",
        "Form is not submitted. Validation error 'Please select a Vendor' appears near the Vendor dropdown.",
        "To be executed", "Negative", "Negative", "High", "High",
    ),
    (   # 29 – EP: Valid class
        "Job Work / Work Orders", "Create Work Order",
        "[EP] Rate – valid class (any positive number)",
        "Equivalence Partitioning – Valid Class: Any positive rate value (1, 50, 250, 5000...) belongs to the valid partition. All values in this class must be accepted.",
        "Rate: 250 (positive number – represents valid class)\nOutsource Qty: 5",
        "User is logged in. Work Order form with Vendor and Item selected.",
        "1. Open Work Order form\n2. Fill all required fields, select Vendor and Item\n3. Enter Outsource Qty: 5\n4. Enter Rate: 250\n5. Click Create",
        "Rate of 250 is accepted. Work Order is created successfully.",
        "To be executed", "Positive", "EP", "Medium", "High",
    ),
    (   # 30 – EP: Invalid class
        "Job Work / Work Orders", "Create Work Order",
        "[EP] Rate – invalid class (alphabetic/text input)",
        "Equivalence Partitioning – Invalid Class: Any non-numeric input (letters, symbols) in the Rate field belongs to the invalid data-type partition. System must reject the entire class.",
        "Rate: pqr (letters – invalid class, non-numeric)\nOutsource Qty: 5",
        "User is logged in. Work Order form with Vendor and Item selected.",
        "1. Open Work Order form\n2. Fill all required fields, select Vendor and Item\n3. Type: pqr in Rate field\n4. Click Create",
        "Validation error shown. Alphabetic input in Rate field is rejected. All non-numeric Rate inputs produce the same error.",
        "To be executed", "Negative", "EP", "Medium", "High",
    ),
    (   # 31 – BVA: Just below minimum
        "Job Work / Work Orders", "Create Work Order",
        "[BVA] Outsource Qty – 0 (one below the minimum valid boundary of 1)",
        "Boundary Value Analysis: 0 is one unit below the minimum valid quantity boundary. A work order for 0 items makes no business sense and must be rejected.",
        "Outsource Qty: 0 (one below minimum boundary)\nRate: 100",
        "User is logged in. Work Order form with Vendor and Item selected.",
        "1. Open Work Order form\n2. Fill all required fields, select Vendor and Item\n3. Enter Outsource Qty: 0\n4. Enter Rate: 100\n5. Click Create",
        "Validation error shown. Qty of 0 is rejected as it is below the minimum valid boundary.",
        "To be executed", "Negative", "BVA", "High", "High",
    ),
    (   # 32 – BVA: Exact minimum
        "Job Work / Work Orders", "Create Work Order",
        "[BVA] Outsource Qty – 1 (exact minimum boundary, must be accepted)",
        "Boundary Value Analysis: 1 is the minimum valid boundary for outsource quantity. The system must accept this without any error.",
        "Outsource Qty: 1 (exact minimum boundary)\nRate: 100",
        "User is logged in. Work Order form with Vendor and Item selected.",
        "1. Open Work Order form\n2. Fill all required fields, select Vendor and Item\n3. Enter Outsource Qty: 1\n4. Enter Rate: 100\n5. Click Create",
        "Outsource Qty of 1 is accepted. Work Order is created successfully.",
        "To be executed", "Positive", "BVA", "Medium", "High",
    ),
    (   # 33 – Decision Table
        "Job Work / Work Orders", "Create Work Order",
        "[Decision Table] Branch + Vendor field combinations",
        "Decision Table Testing: Both Branch and Vendor are mandatory. Tests all invalid combinations to confirm both fields are independently validated.\n\nRule Table:\n| Branch   | Vendor   | Outcome         |\n| Selected | Selected | WO Created      |\n| Selected | Empty    | Vendor Error    | ← Test A\n| Empty    | Selected | Branch Error    | ← Test B\n| Empty    | Empty    | Both Errors     | ← Test C",
        "Test A: Branch selected, Vendor empty\nTest B: Branch empty, Vendor selected\nTest C: Both empty",
        "User is logged in. Work Order creation form is open.",
        "-- Test A --\n1. Open Work Order form\n2. Select Branch, leave Vendor empty\n3. Fill other fields, click Create\n→ Expect: Only Vendor error\n\n-- Test B --\n1. Open Work Order form\n2. Leave Branch empty, select Vendor\n3. Fill other fields, click Create\n→ Expect: Only Branch error\n\n-- Test C --\n1. Open Work Order form\n2. Leave both Branch and Vendor empty\n3. Click Create\n→ Expect: Both errors",
        "Test A: Vendor error shown, Branch is fine.\nTest B: Branch error shown, Vendor is fine.\nTest C: Both field errors shown simultaneously.\nConfirms independent validation of each required dropdown.",
        "To be executed", "Negative", "Decision Table", "High", "High",
    ),
    (   # 34 – Error Guessing
        "Job Work / Work Orders", "Create Work Order",
        "[Error Guessing] Enter special characters / script in Remark field",
        "Error Guessing: Testing if the Remark field is vulnerable to unexpected input like HTML/script tags. The system should sanitize or safely handle such input without executing it or crashing.",
        "Remark: <script>alert('test')</script> @#$%\nAll other fields: valid",
        "User is logged in. Work Order creation form is open.",
        "1. Open Work Order form\n2. Fill all required fields (Branch, Tax, Vendor, Item, Qty, Rate)\n3. In the Remark field, enter: <script>alert('test')</script> @#$%\n4. Click Create",
        "System should safely handle the input. The script must NOT execute (no popup alert). Work Order is either created with the text stored as-is, OR a validation error appears. System must NOT crash or show a server error.",
        "To be executed", "Negative", "Error Guessing", "High", "Medium",
    ),
    (   # 35 – Edge Case
        "Job Work / Work Orders", "Create Work Order",
        "[Edge Case] Expected Receipt Date set before the Work Order Date",
        "Edge Case: Setting the receipt date before the work order date is a logical contradiction. Goods cannot be received before an order is even placed.",
        "Work Order Date: 2026-06-03\nExpected Receipt Date: 2026-05-01 (before Work Order Date)",
        "User is logged in. Work Order creation form is open.",
        "1. Open Work Order form\n2. Set Work Order Date: 2026-06-03\n3. Set Expected Receipt Date: 2026-05-01 (a date before the Work Order Date)\n4. Fill all other required fields\n5. Click Create",
        "System shows validation error 'Expected Receipt Date cannot be before Work Order Date'. Form is not submitted. The date logic is enforced.",
        "To be executed", "Negative", "Edge Case", "Medium", "Medium",
    ),
]

# ── Build Workbook ────────────────────────────────────────────────────────────
def build():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test Case Formate"

    # Header
    for ci, name in enumerate(COLUMNS, 1):
        c = ws.cell(row=1, column=ci, value=name)
        c.fill   = HEADER_FILL
        c.font   = HEADER_FONT
        c.alignment = CENTER
        c.border = BORDER

    for i, w in enumerate(COL_WIDTHS):
        ws.column_dimensions["ABCDEFGHIJKLMN"[i]].width = w

    ws.freeze_panes = "A2"

    # Rows
    for sr, tc in enumerate(TC_DATA, 1):
        (module, sub, name, desc, data, pre, steps,
         exp, actual, mode, tech, sev, pri) = tc
        ri = sr + 1
        fill = FILLS.get(tech, FILLS["Positive"])
        vals = [sr, f"TC-{sr:02d}", module, sub, name, desc,
                data, pre, steps, exp, actual, mode, sev, pri]
        for ci, v in enumerate(vals, 1):
            c = ws.cell(row=ri, column=ci, value=v)
            c.fill = fill; c.font = NORMAL_FONT
            c.alignment = WRAP; c.border = BORDER
        ws.row_dimensions[ri].height = 120

    ws.auto_filter.ref = f"A1:N{len(TC_DATA)+1}"

    # ── Legend sheet ──────────────────────────────────────────────────────────
    ls = wb.create_sheet("Legend & Technique Summary")
    ls.column_dimensions["A"].width = 28
    ls.column_dimensions["B"].width = 20
    ls.column_dimensions["C"].width = 65

    legend = [
        ("Color Code",        "Technique",         "What it tests"),
        ("🟢 Green",          "Positive Testing",   "Happy path — system works correctly with valid inputs"),
        ("🔴 Light Red",      "Negative Testing",   "System correctly blocks invalid/missing inputs"),
        ("🔵 Blue",           "Equivalence Part.",  "Divides inputs into valid & invalid classes; 1 test per class represents the whole class"),
        ("🟡 Yellow",         "Boundary Value Analysis", "Tests at exact boundary, one below, and one above (e.g. min-1, min, max)"),
        ("🟣 Purple",         "Decision Table",     "Tests combinations of multiple conditions to verify independent validation"),
        ("🟠 Orange",         "Error Guessing",     "Based on experience — tests what a real user might do wrong (blank submit, duplicates, bad dates)"),
        ("🩵 Sky Blue",       "Edge Case",          "Unusual but valid/borderline scenarios that test system robustness"),
    ]
    lh_font = Font(bold=True, name="Calibri", size=11)
    for ri, (col, tech, desc) in enumerate(legend, 1):
        ls.cell(ri, 1, col).font  = lh_font if ri == 1 else NORMAL_FONT
        ls.cell(ri, 2, tech).font = lh_font if ri == 1 else NORMAL_FONT
        ls.cell(ri, 3, desc).font = lh_font if ri == 1 else NORMAL_FONT

    out = r"c:\Users\rachi\OneDrive\Documents\LogicLoom_Testing\Test_Cases_Filled.xlsx"
    wb.save(out)
    print(f"[DONE] Saved: {out}")
    print(f"Total TCs: {len(TC_DATA)}\n")

    from collections import Counter
    module_counts  = Counter(tc[0]  for tc in TC_DATA)
    tech_counts    = Counter(tc[10] for tc in TC_DATA)
    print("Per Module:")
    for m, c in module_counts.items():  print(f"  {m:30s}: {c} TCs")
    print("\nPer Technique:")
    for t, c in sorted(tech_counts.items()): print(f"  {t:20s}: {c} TCs")


def load_tc_data():
    """Return TC_DATA as a list of dictionaries.

    Each dict contains keys: sr_no, test_case_id, module, sub_module,
    name, description, test_data, prerequisite, steps, expected_result,
    actual_result, mode, technique, severity, priority.
    """
    rows = []
    for idx, tc in enumerate(TC_DATA, 1):
        (module, sub, name, desc, data, pre, steps,
         exp, actual, mode, tech, sev, pri) = tc
        rows.append({
            "sr_no": idx,
            "test_case_id": f"TC-{idx:02d}",
            "module": module,
            "sub_module": sub,
            "name": name,
            "description": desc,
            "test_data": data,
            "prerequisite": pre,
            "steps": steps,
            "expected_result": exp,
            "actual_result": actual,
            "mode": mode,
            "technique": tech,
            "severity": sev,
            "priority": pri,
        })
    return rows


# ── Per-Module Parsers & Loaders ──────────────────────────────────────────────

def _parse_client_testdata(raw):
    """Parse a Client Management test_data string into a structured dict.

    Returns keys expected by ClientPage.create_client():
        client_name, contact_person_name, contact_person_email,
        contact_person_mobile_number, GSTIN_number, pan_no,
        tds_percentage, email_id, mobile_number, phone_number,
        pincode, vendor_code, ship_to_location, ship_to_address.
    """
    out = {
        "client_name": "",
        "contact_person_name": "",
        "contact_person_email": "",
        "contact_person_mobile_number": "",
        "GSTIN_number": "",
        "pan_no": "",
        "tds_percentage": "0",
        "email_id": "",
        "mobile_number": "",
        "phone_number": "",
        "pincode": "",
        "vendor_code": "",
        "ship_to_location": "Warehouse A",
        "ship_to_address": "Plot No 10, Industrial Area Sector 1",
    }
    for line in raw.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip().lower()
        v = v.strip()
        # skip placeholders / notes
        if not v or v.startswith("(") or v.lower().startswith("all other"):
            continue
        if "client name" in k:
            out["client_name"] = v
        elif "contact email" in k:
            out["contact_person_email"] = v
        elif "contact mobile" in k:
            out["contact_person_mobile_number"] = v
        elif "contact person" in k:
            out["contact_person_name"] = v
        elif k == "gstin":
            out["GSTIN_number"] = v
        elif k == "pan":
            out["pan_no"] = v
        elif "tds" in k:
            out["tds_percentage"] = v.split()[0]   # strip any "%"
        elif "billing email" in k:
            out["email_id"] = v
        elif "mobile" in k and "contact" not in k:
            out["mobile_number"] = v
        elif "phone" in k:
            out["phone_number"] = v
        elif "pincode" in k:
            out["pincode"] = v
        elif "vendor code" in k:
            out["vendor_code"] = v
    return out


def load_client_data():
    """Return Client Management positive test cases as structured dicts.

    Filters technique == 'Positive' (the happy-path cases that have
    complete data and are expected to successfully create a client record).
    """
    result = []
    for tc in load_tc_data():
        if tc["module"] != "Client Management":
            continue
        if tc["technique"] != "Positive":
            continue
        parsed = _parse_client_testdata(tc["test_data"])
        parsed["test_case_id"] = tc["test_case_id"]
        parsed["name"]         = tc["name"]
        parsed["mode"]         = tc["mode"]
        parsed["severity"]     = tc["severity"]
        result.append(parsed)
    return result


def _parse_sales_order_testdata(raw):
    """Parse a Sales Orders test_data string into a structured dict.

    Returns keys expected by SalesOrderPage.create_sales_order():
        client_name, order_number, order_reference_no, order_date,
        delivery_date, quantity, unit_price, expected_delivery_date, address.

    order_number and order_reference_no receive a short timestamp suffix so
    they are unique across repeated test runs.
    """
    import time as _time
    from datetime import datetime, timedelta
    _run_tag = str(int(_time.time()) % 100000)   # 5-digit epoch suffix
    today = datetime.now()
    out = {
        "client_name":            "",
        "order_number":           "SO-" + _run_tag,
        "order_reference_no":     "REF-" + _run_tag,
        "order_date":             today.strftime("%Y-%m-%d"),
        "delivery_date":          (today + timedelta(days=30)).strftime("%Y-%m-%d"),
        "item_line_code":         "",
        "customer_item_name":     "",
        "item_code":              "",
        "material":               "",
        "size":                   "",
        "description":            "",
        "quantity":               "10",
        "unit_price":             "500",
        "expected_delivery_date": (today + timedelta(days=28)).strftime("%Y-%m-%d"),
        "address":                "",
    }
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        # pipe-separated values (e.g. "Qty: 10 | Unit Rate: 500 | Tax: 18%")
        if "|" in line:
            for part in line.split("|"):
                part = part.strip()
                if ":" not in part:
                    continue
                pk, _, pv = part.partition(":")
                pk = pk.strip().lower()
                pv = pv.strip()
                if "qty" in pk:
                    out["quantity"] = pv.split()[0]
                elif "unit rate" in pk:
                    out["unit_price"] = pv.split()[0]
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip().lower()
        v = v.strip()
        if not v or v.startswith("(") or v.lower().startswith("all other"):
            continue
        if "client" in k:
            out["client_name"] = v
        elif "order no" in k:
            # Store prefix only; unique suffix applied in load_sales_order_data()
            out["_order_no_raw"] = v.split("-")[0] if "-" in v else v
        elif "ref no" in k:
            out["_ref_no_raw"] = v.split("-")[0] if "-" in v else v
        elif "order date" in k:
            out["order_date"] = v
        elif "expected delivery" in k:
            out["expected_delivery_date"] = v
        elif "delivery date" in k:
            out["delivery_date"] = v
        elif "address" in k:
            out["address"] = v
    return out


def load_sales_order_data():
    """Return Sales Order positive test cases as structured dicts.

    Filters technique == 'Positive' (complete data, expected to succeed).
    order_number and order_reference_no get a timestamp suffix so each
    test run produces a unique order number and won't clash with existing data.
    """
    import time as _t
    _tag = str(int(_t.time()) % 100000)   # 5-digit epoch suffix, fixed once per import
    result = []
    for tc in load_tc_data():
        if tc["module"] != "Sales Orders":
            continue
        if tc["technique"] != "Positive":
            continue
        parsed = _parse_sales_order_testdata(tc["test_data"])
        # Build unique order/ref numbers: e.g. "SO-86852" and "REF-86852"
        prefix_no  = parsed.pop("_order_no_raw", "SO")
        prefix_ref = parsed.pop("_ref_no_raw",   "REF")
        parsed["order_number"]       = "%s-%s" % (prefix_no, _tag)
        parsed["order_reference_no"] = "%s-%s" % (prefix_ref, _tag)
        parsed["test_case_id"] = tc["test_case_id"]
        parsed["name"]         = tc["name"]
        parsed["mode"]         = tc["mode"]
        parsed["severity"]     = tc["severity"]
        result.append(parsed)
    return result


def _parse_work_order_testdata(raw):
    """Parse a Work Order test_data string into a structured dict.

    Returns keys expected by WorkOrderPage.create_work_order():
        date, expected_receipt_date, outsource_qty, rate, remark.
    """
    from datetime import datetime, timedelta
    today = datetime.now()
    out = {
        "date":                  (today + timedelta(days=1)).strftime("%Y-%m-%d"),
        "expected_receipt_date": (today + timedelta(days=21)).strftime("%Y-%m-%d"),
        "outsource_qty":         "1",
        "rate":                  "100",
        "remark":                "",
    }
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        # pipe-separated (e.g. "Outsource Qty: 10 | Rate: 100")
        if "|" in line:
            for part in line.split("|"):
                part = part.strip()
                if ":" not in part:
                    continue
                pk, _, pv = part.partition(":")
                pk = pk.strip().lower()
                pv = pv.strip()
                digits = "".join(ch for ch in pv if ch.isdigit())
                if "outsource qty" in pk or "outsource" in pk:
                    out["outsource_qty"] = digits or out["outsource_qty"]
                elif "rate" in pk:
                    out["rate"] = digits or out["rate"]
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip().lower()
        v = v.strip()
        if not v or v.startswith("("):
            continue
        if "work order date" in k:
            out["date"] = v
        elif "expected receipt date" in k:
            out["expected_receipt_date"] = v
        elif "remark" in k:
            out["remark"] = v
        elif k == "rate":
            digits = "".join(ch for ch in v if ch.isdigit())
            out["rate"] = digits or out["rate"]
    return out


def load_work_order_data():
    """Return Work Order positive test cases as structured dicts.

    Filters technique == 'Positive' (complete data, expected to succeed).
    """
    result = []
    for tc in load_tc_data():
        if tc["module"] != "Job Work / Work Orders":
            continue
        if tc["technique"] != "Positive":
            continue
        parsed = _parse_work_order_testdata(tc["test_data"])
        parsed["test_case_id"] = tc["test_case_id"]
        parsed["name"]         = tc["name"]
        parsed["mode"]         = tc["mode"]
        parsed["severity"]     = tc["severity"]
        result.append(parsed)
    return result


if __name__ == "__main__":
    build()

