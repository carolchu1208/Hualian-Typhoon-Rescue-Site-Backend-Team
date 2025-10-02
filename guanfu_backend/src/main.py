from fastapi import FastAPI
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
    servers.insert(0, {"url": settings.PROD_SERVER_URL, "description": "正式環境"})

# --- 建立 FastAPI 應用實例 ---
app = FastAPI(
    title=settings.APP_TITLE,  # 從設定檔讀取標題
    version="v1.1.0",
    description="後端 API。提供建立物資需求、查詢需求清單、物資配送登記。",
    servers=servers  # 使用動態產生的 servers 列表
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
