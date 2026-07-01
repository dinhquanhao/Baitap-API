
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

enrollments = [
    {
        "id": 1,
        "student_id": "SV001",
        "course_id": 1
    },
    {
        "id": 2,
        "student_id": "SV002",
        "course_id": 1
    }
]

class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: int

@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate):
    for e in enrollments:
        if (
            e["student_id"] == enrollment.student_id
            and e["course_id"] == enrollment.course_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Student has already enrolled in this course"
            )

    new_enrollment = {
        "id": len(enrollments) + 1,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }

    enrollments.append(new_enrollment)

    return {
        "message": "Enroll successfully",
        "data": new_enrollment
    }

'''
Phần 1 - Test case

| STT | Dữ liệu gửi lên | Kết quả hiện tại | Kết quả đúng mong muốn | Lỗi phát hiện |
|-----|-----------------|------------------|-------------------------|---------------|
| 1 | student_id="SV001", course_id=1 | Vẫn đăng ký được | Báo lỗi 400 - Student has already enrolled in this course | Không kiểm tra đăng ký trùng |
| 2 | student_id="SV002", course_id=1 | Vẫn đăng ký được | Báo lỗi 400 - Student has already enrolled in this course | Không kiểm tra đăng ký trùng |

Sau khi sửa:
- Đăng ký trùng -> HTTP 400
- Đăng ký mới -> HTTP 201 Created
'''
