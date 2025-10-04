# 開發環境設定指南

本文件從零開始設定 Python 開發環境，即使沒有 Python 經驗也能啟動專案。

## 為什麼使用 uv？

Python 在套件管理方面可能因不同專案需要不同版本的套件，如果直接安裝在系統層級，容易造成版本衝突，甚至影響作業系統的穩定性。

**uv** 是一個現代化的 Python 套件管理工具，它可以：

- 自動管理 Python 版本
- 為每個專案建立獨立的虛擬環境
- 比傳統工具（pip、poetry）快 10-100 倍
- 避免污染系統的 Python 環境

## 前置需求

- macOS 作業系統
- Homebrew（macOS 套件管理工具）

## 安裝步驟

### 1. 安裝 uv

使用 Homebrew 安裝 uv：

```bash
brew install uv
```

安裝完成後，驗證安裝：

```bash
uv --version
```

### 3. 設定 Python 環境

**重要：** 請先切換到 `guanfu_backend` 目錄作為專案根目錄：

```bash
cd guanfu_backend
```

本專案使用 Poetry 作為套件管理工具，但我們可以透過 uv 來加速套件安裝：

```bash
# 讓 uv 自動安裝 Python 3.13（本專案需要 3.11+）
uv python install 3.13

# 建立虛擬環境
uv venv

# 啟動虛擬環境
# macOS/Linux:
source .venv/bin/activate

# 註：pyproject.toml 已加入 [tool.poetry] packages 設定
# 以支援 uv pip install -e . 的 editable install 模式

# 使用 uv 安裝套件（比 poetry 更快）
uv pip install -e .

# 停止虛擬環境（當要切換專案或結束開發時）
deactivate
```

**注意：**

- 啟動虛擬環境：`source .venv/bin/activate`
- 停止虛擬環境：`deactivate`
- 當您看到命令提示字元前面出現 `(.venv)` 時，表示虛擬環境已啟動

### 4. 設定環境變數

複製環境變數範本並填入正確的資料庫連線資訊：

```bash
cp .env.example .env.dev
```

編輯 `.env.dev` 檔案，填入資料庫連線資訊：

```
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

**重要：** 請將 `username`、`password`、`database_name` 替換為您的實際資料庫連線資訊。

### 5. 啟動 PostgreSQL 資料庫

本專案使用 Docker Compose 來執行 PostgreSQL 資料庫，這樣可以確保所有開發者使用相同的資料庫版本和設定。

**使用 Docker Compose 啟動資料庫：**

```bash
# 啟動 PostgreSQL 容器（在背景執行）
docker-compose --env-file .env.dev up -d

# 確認容器是否正在執行
docker ps

# 查看資料庫日誌（如果需要）
docker logs postgres
```

**停止資料庫：**

```bash
# 停止並移除容器
docker-compose down
```

**注意事項：**
- 資料庫設定（使用者名稱、密碼、資料庫名稱）定義在 `.env.dev` 檔案中
- 資料會持久化儲存在 `postgres-data/` 資料夾中
- 如果本地已有其他服務佔用 5432 埠號，需要先停止該服務

**替代方案：使用本地 PostgreSQL**

如果您不想使用 Docker，也可以使用 Homebrew 安裝的本地 PostgreSQL：

```bash
# 啟動本地 PostgreSQL
brew services start postgresql@16

# 確認是否正在接受連線
pg_isready
```

### 6. 啟動開發伺服器

```bash
uvicorn src.main:app --reload
```

伺服器啟動後，開啟瀏覽器訪問：

- API 文件：http://localhost:8000/docs
- 替代文件：http://localhost:8000/redoc

## 常用指令

### 啟動/停止虛擬環境

```bash
# 啟動（每次開始開發前都要執行）
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 停止
deactivate
```

### 安裝新套件

```bash
# 使用 uv 安裝（推薦，速度更快）
uv pip install <package-name>

# 或使用 poetry（會更新 pyproject.toml）
poetry add <package-name>
```

### 查看已安裝套件

```bash
uv pip list
```

### 更新套件

```bash
# 更新所有套件
uv pip install --upgrade -e .

# 更新特定套件
uv pip install --upgrade <package-name>
```

## 專案結構說明

```
guanfu_backend/
├── src/                    # 主要程式碼目錄
│   ├── main.py            # FastAPI 應用程式入口
│   ├── models.py          # 資料庫模型定義
│   ├── schemas.py         # API 資料驗證結構
│   ├── crud.py            # 資料庫操作函式
│   ├── database.py        # 資料庫連線設定
│   ├── config.py          # 應用程式設定
│   └── routers/           # API 路由處理器
├── docs/                  # 專案文件
├── pyproject.toml         # 專案設定與套件依賴
├── poetry.lock            # 套件版本鎖定檔案
└── .env                   # 環境變數（不會提交到 Git）
```

## 常見問題

### Q: 為什麼不直接使用 Poetry？

A: Poetry 是優秀的套件管理工具，但 uv 的安裝速度快得多，且能更好地隔離不同專案的 Python 環境。本專案同時支援兩者。

### Q: 虛擬環境是什麼？

A: 虛擬環境是一個獨立的 Python 執行環境，讓每個專案都有自己的套件版本，互不干擾。

### Q: 每次開啟終端機都要重新啟動虛擬環境嗎？

A: 是的，每次開啟新的終端機視窗並想要執行此專案時，都需要先啟動虛擬環境。

### Q: 如何確認虛擬環境已啟動？

A: 命令提示字元前會顯示 `(.venv)`，例如：`(.venv) user@computer:~/project$`

### Q: uv 和 pip 有什麼不同？

A: uv 是 pip 的現代化替代品，功能相同但速度快得多，且內建更好的依賴解析機制。

## 下一步

- 閱讀 [API 開發指南](./api-development.md)（待建立）
- 了解 [資料庫結構](../../table_spec.md)
- 查看 [FastAPI 官方文件](https://fastapi.tiangolo.com/zh/)

## 取得協助

如果遇到問題，請：

1. 檢查終端機的錯誤訊息
2. 確認虛擬環境已正確啟動
3. 確認 `.env` 檔案設定正確
4. 向團隊成員尋求協助
