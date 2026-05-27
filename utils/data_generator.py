import random
import time
from datetime import datetime, timedelta

# RUN_ID is fixed at import time so all generated data stays consistent within one test session
RUN_ID = int(time.time()) % 10000


def generate_mock_clients(count=10):
    """Generate a list of unique mock client records."""
    clients = []
    for i in range(1, count + 1):
        digits = "%04d" % ((RUN_ID + i) % 10000)
        gstin  = "27INTQA%sF1Z5" % digits
        pan    = "INTQA%sF" % digits

        mobile    = "9%d" % random.randint(100000000, 999999999)
        cp_mobile = "9%d" % random.randint(100000000, 999999999)
        phone     = "022%d" % random.randint(1000000, 9999999)

        clients.append({
            "client_name":                  "Intern Client %d Ltd %02d" % (RUN_ID, i),
            "contact_person_name":          "Contact Person %d" % i,
            "contact_person_email":         "contact%d@intern%d.com" % (i, RUN_ID),
            "contact_person_mobile_number": cp_mobile,
            "GSTIN_number":                 gstin,
            "pan_no":                       pan,
            "tds_percentage":               "%.1f" % (1.5 + i * 0.1),
            "email_id":                     "billing%d@intern%d.com" % (i, RUN_ID),
            "mobile_number":                mobile,
            "phone_number":                 phone,
            "pincode":                      "400%03d" % (100 + i),
            "vendor_code":                  "V-%d-%02d" % (RUN_ID, i),
            "ship_to_location":             "Warehouse Wing %s" % chr(65 + (i % 6)),
            "ship_to_address":              "Plot No %d, Industrial Area Sector %d" % (10 + i, i % 5 + 1),
        })
    return clients


def generate_mock_sales_orders(client_names, count=10):
    """Generate a list of unique mock sales order records."""
    orders = []
    base_date = datetime.now()
    for i in range(1, count + 1):
        order_date    = base_date + timedelta(days=i)
        delivery_date = order_date + timedelta(days=15)
        exp_delivery  = delivery_date - timedelta(days=2)

        client = client_names[i - 1] if i - 1 < len(client_names) else "Intern Client %d Ltd %02d" % (RUN_ID, i)

        orders.append({
            "client_name":          client,
            "order_number":         "SO-%04d-%02d" % (RUN_ID, i),
            "order_reference_no":   "REF-%d-%02d" % (RUN_ID, i),
            "order_date":           order_date.strftime("%Y-%m-%d"),
            "delivery_date":        delivery_date.strftime("%Y-%m-%d"),
            "item_line_code":       "LINE-%d" % (100 + i),
            "customer_item_name":   "Finished Gear Box Model %s" % chr(65 + (i % 8)),
            "item_code":            "ITEM-%d" % (500 + i),
            "material":             "Alloy Steel Grade A",
            "size":                 "100x200x%dmm" % (50 + i * 2),
            "description":          "Heavy-duty industrial gearbox component serial %03d" % i,
            "quantity":             str(random.randint(10, 100)),
            "unit_price":           str(random.randint(150, 500)),
            "expected_delivery_date": exp_delivery.strftime("%Y-%m-%d"),
            "address":              "Delivery Point Hub %d, Logistics Park" % (i % 3 + 1),
        })
    return orders


def generate_mock_work_orders(client_names, count=10):
    """Generate a list of unique mock work order records."""
    work_orders = []
    base_date = datetime.now()
    for i in range(1, count + 1):
        order_date   = base_date + timedelta(days=i)
        receipt_date = order_date + timedelta(days=20)

        work_orders.append({
            "date":                  order_date.strftime("%Y-%m-%d"),
            "expected_receipt_date": receipt_date.strftime("%Y-%m-%d"),
            "outsource_qty":         str(random.randint(5, 50)),
            "rate":                  str(random.randint(45, 120)),
            "remark":                "Outsourced heat treatment process run %02d - high priority" % i,
        })
    return work_orders
