from fastapi import FastAPI

app = FastAPI(title="Book Low Stock API")

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20},
    {"id": 6, "title": "Java Basic"},
    {"id": 7, "title": "Spring Boot", "quantity": -2}
]

@app.get("/books/low-stock")
def get_low_stock_books():
    low_stock_books = []
    for book in books:
        if "quantity" not in book:
            continue
        quantity = book["quantity"]
        if quantity < 0:
            continue
        if quantity <= 5:
            low_stock_books.append(book)

    if not low_stock_books:
        return {
            "message": "Không có sách nào sắp hết hàng",
            "data": []
        }

    return {
        "message": "Danh sách sách sắp hết hàng",
        "data": low_stock_books
    }
