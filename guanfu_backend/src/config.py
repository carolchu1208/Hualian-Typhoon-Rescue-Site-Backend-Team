from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    應用程式設定類別，使用 pydantic-settings 從環境變數或 .env 檔案讀取設定。

    注意：env_file 可能包含其他工具（如 Docker）使用的環境變數，
    Settings 類別只會讀取它需要的欄位，其餘會被忽略。
    """
    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        extra="ignore"  # 忽略不在 Settings 中定義的環境變數
    )

    ENVIRONMENT: str
    APP_TITLE: str
    DATABASE_URL: str

    # PROD_SERVER_URL 可以有預設值，因為它不是敏感資訊
    PROD_SERVER_URL: str = "https://guangfu250923.pttapp.cc"


# 建立一個全域的 settings 實例供整個專案引用
settings = Settings()
