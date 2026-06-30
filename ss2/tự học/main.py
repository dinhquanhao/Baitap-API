from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello FastAPI"}

@app.get("/about")
def about():
    return {"course": "FastAPI", "lesson": "First API"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Xin chào {name}"}
    