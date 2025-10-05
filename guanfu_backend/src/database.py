from typing import Generator
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from .config import settings

# 讀取設定
ENVIRONMENT = settings.ENVIRONMENT.lower()
DB_USER = settings.DB_USER
DB_PASS = settings.DB_PASS
DB_NAME = settings.DB_NAME
INSTANCE_CONNECTION_NAME = settings.INSTANCE_CONNECTION_NAME
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 依環境切換 Engine
if ENVIRONMENT in ("dev", "prod"):
    # 使用 Cloud SQL 的 Unix Socket（Cloud Run 環境）
    unix_socket_path = f"/cloudsql/{INSTANCE_CONNECTION_NAME}"
    engine = create_engine(
        URL.create(
            drivername="postgresql+psycopg2",
            username=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            query={"host": unix_socket_path},  # Postgres 用 host 指向 socket 路徑
        ),
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )
else:
    # 本機或一般 TCP：優先使用完整 DATABASE_URL
    if not SQLALCHEMY_DATABASE_URL:
        # 備援：若沒提供 DATABASE_URL，可改用 host/port 組裝（預設 localhost:5432）
        engine = create_engine(
            URL.create(
                drivername="postgresql+psycopg2",
                username=DB_USER,
                password=DB_PASS,
                host="localhost",
                port=5432,
                database=DB_NAME,
            ),
            pool_pre_ping=True,
        )
    else:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_pre_ping=True,
        )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
