from fastapi import FastAPI

app = FastAPI()

# Danh sách sách mẫu
books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Nguyen Van A",
        "category": "programming",
        "year": 2020,
        "is_available": True    
    },
    {
        "id": 2,
        "title": "FastAPI Tutorial",
        "author": "Tran Van B",
        "category": "web",
        "year": 2023,
        "is_available": False
    },
    {
        "id": 3,
        "title": "Database Design",
        "author": "Le Thi C",
        "category": "database",
        "year": 2021,
        "is_available": True
    },
    {
        "id": 4,
        "title": "Computer Network",
        "author": "Pham Van D",
        "category": "network",
        "year": 2019,
        "is_available": True
    },
    {
        "id": 5,
        "title": "Django Framework",
        "author": "Nguyen Van E",
        "category": "web",
        "year": 2022,
        "is_available": False
    },
    {
        "id": 6,
        "title": "FastAPI Basic",
        "author": "Nguyen Van A",
        "category": "web",
        "year": 2024,
        "is_available": True
    }
]

@app.get("/")
def home():
    return {"message": "Library API is running"}

# API 1: Thống kê dữ liệu sách
@app.get("/books/statistics")
def book_statistics():
    total_books = len(books)
    available_books = len(
        [book for book in books if book["is_available"]]
    )
    borrowed_books = len(
        [book for book in books if not book["is_available"]]
    )

    return {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books
    }


# API 2: Lấy danh sách thể loại không trùng nhau
@app.get("/books/categories")
def get_categories():
    categories = list(
        set(book["category"] for book in books)
    )

    return {
        "categories": categories
    }


# API 3: Lấy sách mới nhất
@app.get("/books/latest")
def get_latest_book():
    if len(books) == 0:
        return {
            "message": "No books available"
        }

    latest_book = max(
        books,
        key=lambda book: book["year"]
    )

    return latest_book

