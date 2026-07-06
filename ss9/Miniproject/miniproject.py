from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

app = FastAPI()

tasks_db = [
    {
        "id": 1,
        "title": "Thiet ke database Shop AI",
        "description": "Xay dung bang va toi uu index",
        "assignee": "QuyDev",
        "priority": 1,
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z"
    },
    {
        "id": 2,
        "title": "Code bo API Authen",
        "description": "Trien khai filter verify JWT token",
        "assignee": "FixerQ",
        "priority": 2,
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z"
    }
]

class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=1)
    priority: int = Field(..., ge=1, le=5)

class TaskStatusUpdateSchema(BaseModel):
    status: str = Field(..., min_length=1)

def response_data(status_code,message,data,error,path):
    return {
        "statusCode":status_code,
        "message":message,
        "data":data,
        "error":error,
        "timestamp":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "path":path
    }

@app.exception_handler(HTTPException)
async def http_handler(request:Request, exc:HTTPException):
    return JSONResponse(status_code=exc.status_code, content=response_data(exc.status_code, exc.detail["message"], None, exc.detail["error"], request.url.path))

@app.exception_handler(RequestValidationError)
async def validation_handler(request:Request, exc:RequestValidationError):
    return JSONResponse(status_code=422, content=response_data(422,"Lỗi: Dữ liệu đầu vào không hợp lệ hoặc sai định dạng quy định!",None,"ERR-VAL-422: Validation error at Request Body fields constraint layout.",request.url.path))

@app.exception_handler(Exception)
async def global_handler(request:Request, exc:Exception):
    return JSONResponse(status_code=500, content=response_data(500,"Lỗi hệ thống!",None,"ERR-500: Internal Server Error",request.url.path))

@app.get("/tasks")
def get_all_tasks(request:Request,status:Optional[str]=None):
    data=tasks_db if status is None else [t for t in tasks_db if t["status"]==status]
    return response_data(200,"Lấy danh sách công việc thành công!",data,None,request.url.path)

@app.post("/tasks",status_code=201)
def create_task(task:TaskCreateSchema,request:Request):
    for t in tasks_db:
        if t["title"].lower()==task.title.lower():
            raise HTTPException(400,{"message":"Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!","error":"ERR-TASK-01: Task conflict: Title field duplicates an existing record."})
    new={
        "id":tasks_db[-1]["id"]+1 if tasks_db else 1,
        "title":task.title,
        "description":task.description,
        "assignee":task.assignee,
        "priority":task.priority,
        "status":"todo",
        "created_at":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    tasks_db.append(new)
    return response_data(201,"Khởi tạo công việc mới thành công!",new,None,request.url.path)

@app.put("/tasks/{task_id}")
def update_task_status(task_id:int,status_in:TaskStatusUpdateSchema,request:Request):
    for t in tasks_db:
        if t["id"]==task_id:
            if t["status"]=="done":
                raise HTTPException(400,{"message":"Lỗi: Công việc đã hoàn thành, không thể cập nhật!","error":"ERR-TASK-04: Task already done."})
            t["status"]=status_in.status
            return response_data(200,"Cập nhật tiến độ công việc thành công!",t,None,request.url.path)
    raise HTTPException(404,{"message":"Lỗi: Không tìm thấy công việc!","error":"ERR-TASK-03: Task ID does not exist."})

def calculate_team_metrics():
    total=len(tasks_db)
    completed=sum(1 for t in tasks_db if t["status"]=="done")
    rate=0 if total==0 else completed/total*100
    return total,completed,rate

@app.get("/tasks/analytics/dashboard")
def get_dashboard_analytics(request:Request):
    total,completed,rate=calculate_team_metrics()
    return response_data(200,"Lấy số liệu thống kê hiệu suất nhóm thành công!",{
        "total_tasks":total,
        "completed_tasks":completed,
        "completion_rate_percentage":rate
    },None,request.url.path)
