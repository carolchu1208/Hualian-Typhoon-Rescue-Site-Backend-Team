from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    應用程式設定類別，使用 pydantic-settings 從環境變數或 .env 檔案讀取設定。
    """
    model_config = SettingsConfigDict(env_file=".env.dev", env_file_encoding="utf-8")

    ENVIRONMENT: str
    APP_TITLE: str
    DATABASE_URL: str

    # PROD_SERVER_URL 可以有預設值，因為它不是敏感資訊
    PROD_SERVER_URL: str = "https://guangfu250923.pttapp.cc"


# 建立一個全域的 settings 實例供整個專案引用
settings = Settings()
