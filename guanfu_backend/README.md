
# 災害物資需求 API 服務

這是一個基於 FastAPI 和 PostgreSQL 的後端 API 服務，旨在提供一個穩定、可擴展的平台，用於管理和查詢災難應變相關的資源，例如庇護所、醫療站、人力與物資需求等。

本專案的設計重點在於清晰的架構分離、環境組態管理以及自動化的 API 文件生成。

## ✨ 核心功能

*   **RESTful API**: 提供一整套符合 RESTful 風格的 API，用於對各項資源進行增、刪、改、查 (CRUD) 操作。
*   **環境分流**: 支援 **開發 (dev)** 與 **生產 (prod)** 環境，透過環境變數無縫切換資料庫連線和其他設定。
*   **資料庫整合**: 使用 SQLAlchemy ORM 來對接一個 **已存在的 PostgreSQL 資料庫**，不干預現有資料表結構。
*   **資料驗證**: 透過 Pydantic 模型進行嚴格的請求與回應資料驗證，確保資料的正確性。
*   **自動化 API 文件**: 自動生成符合 OpenAPI 規格的互動式 API 文件 (Swagger UI & ReDoc)。
*   **模組化路由**: 將不同資源的 API 端點模組化，易於維護和擴展。

## 📂 專案結構

```
.
├── .env.dev             # 開發環境變數範本
├── .env.prod            # 生產環境變數範本
├── README.md            # 專案說明文件
├── poetry.lock     # 專案依賴套件
└── src/
    ├── __init__.py
    ├── config.py        # 核心設定檔，讀取環境變數
    ├── crud.py          # 通用的資料庫 CRUD 操作函式
    ├── database.py      # 資料庫連線與 Session 管理
    ├── main.py          # FastAPI 應用程式主入口
    ├── models.py        # SQLAlchemy ORM 模型 (對應資料庫資料表)
    ├── schemas.py       # Pydantic 資料驗證模型 (用於 API 請求/回應)
    └── routers/
        ├── __init__.py
        ├── shelters.py  # 庇護所 API 路由
        ├── reports.py   # 回報事件 API 路由
        └── ...          # 其他資源的 API 路由檔案
```

## 🛠️ 技術棧

*   **Web 框架**: FastAPI
*   **資料庫**: PostgreSQL
*   **ORM**: SQLAlchemy
*   **資料驗證**: Pydantic
*   **設定管理**: Pydantic-Settings
*   **PostgreSQL 驅動**: psycopg2
*   **ASGI 伺服器**: 沒決定