from fastapi import FastAPI

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

@app.get("/courses")
def get_courses(keyword: str=None, min_fee: int=None, max_fee: int=None):
    result = courses
    if keyword:
        result = [c for c in result if keyword.lower() in c["name"].lower() or keyword.lower() in c["code"].lower()]
    if min_fee is not None:
        result = [c for c in result if c["fee"] >= min_fee]
    if max_fee is not None:
        result = [c for c in result if c["fee"] <= max_fee]
    return result

@app.get("/courses/{course_id}")
def get_course(course_id:int):
    for c in courses:
        if c["id"] == course_id:
            return c
    return {"message":"Không tìm thấy khóa học"}

@app.post("/courses")
def create_course(course:dict):
    courses.append(course)
    return {"message":"Thêm khóa học thành công","data":course}

@app.put("/courses/{course_id}")
def update_course(course_id:int,new_course:dict):
    for i in range(len(courses)):
        if courses[i]["id"]==course_id:
            courses[i]=new_course
            return {"message":"Cập nhật thành công","data":new_course}
    return {"message":"Không tìm thấy khóa học"}

@app.delete("/courses/{course_id}")
def delete_course(course_id:int):
    for i in range(len(courses)):
        if courses[i]["id"]==course_id:
            d=courses.pop(i)
            return {"message":"Xóa thành công","data":d}
    return {"message":"Không tìm thấy khóa học"}
