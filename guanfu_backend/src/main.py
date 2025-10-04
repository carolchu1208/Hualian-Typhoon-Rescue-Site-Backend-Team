from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from psycopg2 import errors

from .config import settings
from .routers import (
    shelters, reports, volunteer_organizations, accommodations,
    human_resources, medical_stations, mental_health_resources,
    restrooms, shower_stations, water_refill_stations,
    supplies, supply_items
)

# --- 根據環境動態設定 Swagger UI 的伺服器 URL ---
servers = [
    {"url": "http://localhost:8000", "description": "本地開發 (Dev)"},
]
if settings.ENVIRONMENT == "prod":
    servers.insert(0, {"url": settings.PROD_SERVER_URL, "description": "線上服務 (Production)"})

# --- 建立 FastAPI 應用實例 ---
app = FastAPI(
    title=settings.APP_TITLE,
    version="v1.1.0",
    description="光復主站api",
    servers=servers,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # 隱藏model schema
        "docExpansion": "none",  # 預設label收起
    }
)


# ===================================================================
# 全域異常處理器 (Global Exception Handlers)
# ===================================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    自定義 Pydantic 驗證錯誤的處理器，
    將其格式化為更易讀的 {field: [error_message]} 格式，類似 Django REST Framework。
    """
    simplified_errors = {}
    for error in exc.errors():
        # error['loc'] 是一個元組，例如 ('body', 'status')，我們通常取最後一個作為欄位名
        field_name = str(error["loc"][-1]) if error["loc"] else "general"
        error_message = error["msg"]

        # 將錯誤訊息整理成列表
        if field_name not in simplified_errors:
            simplified_errors[field_name] = []
        simplified_errors[field_name].append(error_message)

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=simplified_errors,
    )


@app.exception_handler(IntegrityError)
async def integrity_error_exception_handler(request: Request, exc: IntegrityError):
    """
    攔截所有 SQLAlchemy 的 IntegrityError，並根據具體的錯誤類型回傳友善的錯誤訊息。
    """
    original_error = exc.orig

    # 判斷原始錯誤的具體類型
    if isinstance(original_error, errors.CheckViolation):
        constraint_name = original_error.diag.constraint_name
        detail = f"Input data violates check constraint '{constraint_name}'. Please provide a valid value."
        return JSONResponse(status_code=400, content={"detail": detail})

    if isinstance(original_error, errors.UniqueViolation):
        constraint_name = original_error.diag.constraint_name
        detail = f"A record with this value already exists (violates unique constraint '{constraint_name}')."
        return JSONResponse(status_code=409, content={"detail": detail})

    if isinstance(original_error, errors.NotNullViolation):
        column_name = original_error.diag.column_name
        detail = f"Required field '{column_name}' cannot be null."
        return JSONResponse(status_code=400, content={"detail": detail})

    if isinstance(original_error, errors.ForeignKeyViolation):
        constraint_name = original_error.diag.constraint_name
        detail = f"Foreign key constraint '{constraint_name}' failed. The referenced record may not exist."
        return JSONResponse(status_code=400, content={"detail": detail})

    import logging
    logging.error(f"Unhandled IntegrityError: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected database integrity error occurred."},
    )


# --- 包含所有資源的 routers ---
app.include_router(shelters.router)
app.include_router(reports.router)
app.include_router(volunteer_organizations.router)
app.include_router(accommodations.router)
app.include_router(human_resources.router)
app.include_router(medical_stations.router)
app.include_router(mental_health_resources.router)
app.include_router(restrooms.router)
app.include_router(shower_stations.router)
app.include_router(water_refill_stations.router)
app.include_router(supplies.router)
app.include_router(supply_items.router)
