from fastapi import FastAPI

app = FastAPI(title="Hệ thống Phân tích Đơn hàng E-commerce")

mock_orders = [
    {"id": 1, "customer_name": "Nguyen Van A", "total_amount": 500000, "status": "delivered"},
    {"id": 2, "customer_name": "Tran Thi B", "total_amount": 200000, "status": "pending"},
    {"id": 3, "customer_name": "Nguyen Van A", "total_amount": 350000, "status": "delivered"},
    {"id": 4, "customer_name": "Le Van C", "total_amount": 350000, "status": "delivered"},
    {"id": 5, "customer_name": "Tran Thi B", "total_amount": 500000, "status": "delivered"},
    {"id": 6, "customer_name": "Pham Van D", "total_amount": 150000, "status": "cancelled"},
]


@app.get("/orders/revenue-report")
def get_revenue_report():
    orders = mock_orders

    if not orders:
        return {
            "total_revenue": 0,
            "successful_revenue": 0,
            "average_order_value": 0,
        }

    total_revenue = 0
    successful_revenue = 0

    for order in orders:
        total_revenue += order["total_amount"]
        if order["status"] == "delivered":
            successful_revenue += order["total_amount"]

    average_order_value = float(f"{total_revenue / len(orders):.2f}")

    return {
        "total_revenue": total_revenue,
        "successful_revenue": successful_revenue,
        "average_order_value": average_order_value,
    }


@app.get("/orders/status-breakdown")
def get_status_breakdown():
    orders = mock_orders

    breakdown = {
        "pending": 0,
        "delivered": 0,
        "cancelled": 0,
    }

    for order in orders:
        status = order["status"]
        breakdown[status] = breakdown.get(status, 0) + 1

    return {"breakdown": breakdown}


@app.get("/orders/top-customers")
def get_top_customers():
    orders = mock_orders

    delivered_orders = [o for o in orders if o["status"] == "delivered"]

    if not delivered_orders:
        return {"message": "No VIP customers found"}

    spending = {}
    for order in delivered_orders:
        name = order["customer_name"]
        spending[name] = spending.get(name, 0) + order["total_amount"]

    sorted_customers = sorted(spending.items(), key=lambda item: item[1], reverse=True)

    top_3 = sorted_customers[:3]

    top_customers = [
        {"customer_name": name, "total_spent": total_spent}
        for name, total_spent in top_3
    ]

    return {"top_customers": top_customers}