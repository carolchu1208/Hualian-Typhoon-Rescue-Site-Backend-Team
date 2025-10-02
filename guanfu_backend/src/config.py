from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    應用程式設定類別，使用 pydantic-settings 從環境變數或 .env 檔案讀取設定。
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ENVIRONMENT: str = "dev"

    # 應用程式標題，會根據環境動態變更
    APP_TITLE: str = "光復 API (Dev)"

    # 資料庫連線 URL
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/disaster_db_dev"

    # 生產環境的 Server URL (用於 Swagger 文件)
    PROD_SERVER_URL: str = "https://guangfu250923.pttapp.cc"


# 建立一個全域的 settings 實例供整個專案引用
settings = Settings()

# 根據 ENVIRONMENT 的值，覆寫部分設定
if settings.ENVIRONMENT == "prod":
    settings.APP_TITLE = "光復 API"
