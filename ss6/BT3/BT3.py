# BT3.py

from fastapi import FastAPI

app = FastAPI()

rooms = [
    {"id": 1, "code": "R101", "name": "Room 101", "capacity": 30, "status": "AVAILABLE"},
    {"id": 2, "code": "R102", "name": "Room 102", "capacity": 20, "status": "AVAILABLE"},
    {"id": 3, "code": "R103", "name": "Room 103", "capacity": 40, "status": "MAINTENANCE"}
]

room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING"
    }
]


# ==================================
# GET Danh sách phòng học
# ==================================
@app.get("/rooms")
def get_rooms(
    keyword: str = None,
    status: str = None,
    min_capacity: int = None
):
    result = rooms

    if keyword:
        result = [
            room for room in result
            if keyword.lower() in room["code"].lower()
            or keyword.lower() in room["name"].lower()
        ]

    if status:
        result = [
            room for room in result
            if room["status"] == status
        ]

    if min_capacity is not None:
        result = [
            room for room in result
            if room["capacity"] >= min_capacity
        ]

    return result


# ==================================
# GET Chi tiết phòng
# ==================================
@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            return room

    return {"message": "Room not found"}


# ==================================
# POST Thêm phòng
# ==================================
@app.post("/rooms")
def create_room(room: dict):

    for r in rooms:
        if r["code"] == room["code"]:
            return {"message": "Code already exists"}

    if room["name"] == "":
        return {"message": "Name cannot be empty"}

    if room["capacity"] <= 0:
        return {"message": "Capacity must be greater than 0"}

    if room["status"] not in ["AVAILABLE", "IN_USE", "MAINTENANCE"]:
        return {"message": "Invalid status"}

    rooms.append(room)

    return {
        "message": "Add room successfully",
        "data": room
    }


# ==================================
# PUT Cập nhật phòng
# ==================================
@app.put("/rooms/{room_id}")
def update_room(room_id: int, new_room: dict):

    if new_room["name"] == "":
        return {"message": "Name cannot be empty"}

    if new_room["capacity"] <= 0:
        return {"message": "Capacity must be greater than 0"}

    if new_room["status"] not in ["AVAILABLE", "IN_USE", "MAINTENANCE"]:
        return {"message": "Invalid status"}

    for i in range(len(rooms)):
        if rooms[i]["id"] == room_id:
            rooms[i] = new_room
            return {
                "message": "Update successfully",
                "data": new_room
            }

    return {"message": "Room not found"}


# ==================================
# DELETE Phòng
# ==================================
@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):

    for i in range(len(rooms)):
        if rooms[i]["id"] == room_id:
            deleted_room = rooms.pop(i)
            return {
                "message": "Delete successfully",
                "data": deleted_room
            }

    return {"message": "Room not found"}


# ==================================
# GET Danh sách lịch đặt phòng
# ==================================
@app.get("/room-bookings")
def get_bookings():
    return room_bookings


# ==================================
# POST Đặt phòng
# ==================================
@app.post("/room-bookings")
def create_booking(booking: dict):

    room = None

    for r in rooms:
        if r["id"] == booking["room_id"]:
            room = r
            break

    if room is None:
        return {"message": "Room not found"}

    if room["status"] != "AVAILABLE":
        return {"message": "Room is not available"}

    if booking["student_count"] <= 0:
        return {"message": "Student count must be greater than 0"}

    if booking["student_count"] > room["capacity"]:
        return {"message": "Room capacity is not enough"}

    if booking["slot"] not in ["MORNING", "AFTERNOON", "EVENING"]:
        return {"message": "Invalid slot"}

    for b in room_bookings:
        if (
            b["room_id"] == booking["room_id"]
            and b["date"] == booking["date"]
            and b["slot"] == booking["slot"]
        ):
            return {"message": "Room booking already exists"}

    room_bookings.append(booking)

    return {
        "message": "Booking successfully",
        "data": booking
    }