"""Hàm hỗ trợ tạo response JSON theo cấu trúc chuẩn của toàn bộ API."""
from typing import Any, Optional

from fastapi.responses import JSONResponse


def api_response(
    status_code: int,
    message: str,
    data: Any = None,
    error: Optional[str] = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "error": error,
            "message": message,
            "data": data,
        },
    )
