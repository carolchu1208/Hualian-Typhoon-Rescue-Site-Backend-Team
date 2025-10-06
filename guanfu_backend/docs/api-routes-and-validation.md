# API 路由與資料驗證說明文件

> 本文件說明光復救災平台後端 API 的所有路由端點及其資料驗證規則

## 目錄

- [API 路由總覽](#api-路由總覽)
- [資料驗證機制](#資料驗證機制)
- [各資源端點詳細說明](#各資源端點詳細說明)
- [錯誤處理](#錯誤處理)

---

## API 路由總覽

### 基本資訊

- **API 版本**: v1.1.0
- **基礎 URL**: `http://localhost:8000` (開發環境)
- **文件位置**: `http://localhost:8000/docs` (Swagger UI)

### 資源列表

| 資源類型 | 路由前綴 | 說明 | 驗證欄位 |
|---------|---------|------|---------|
| 庇護所 | `/shelters` | 避難所/安置點管理 | `phone`, `link` |
| 醫療站 | `/medical_stations` | 醫療服務點管理 | `phone`, `link` |
| 心理健康資源 | `/mental_health_resources` | 心理支持服務 | `website_url` |
| 住宿資源 | `/accommodations` | 臨時住宿管理 | - |
| 洗澡點 | `/shower_stations` | 盥洗設施管理 | `phone` |
| 飲用水補給站 | `/water_refill_stations` | 飲水供應點 | `phone` |
| 廁所 | `/restrooms` | 公廁設施管理 | `phone` |
| 人力資源 | `/human_resources` | 志工人力調度 | `phone` |
| 物資單 | `/supplies` | 物資需求管理 | `phone` |
| 物資項目 | `/supply_items` | 物資細項管理 | - |
| 志工團體 | `/volunteer_organizations` | NGO 團體協調 | `image_url` |
| 回報事件 | `/reports` | 事件回報系統 | - |

---

## 資料驗證機制

### 驗證架構

本專案使用 **Pydantic** 進行資料驗證，所有驗證函數統一放在 `src/validators.py`，並在 `src/schemas.py` 的 `*Create` 類別中使用 `@field_validator` 裝飾器套用驗證規則。

```python
# 範例：庇護所建立時的驗證
from src.validators import validate_phone_number, validate_url

class ShelterCreate(ShelterBase):
    status: ShelterStatusEnum

    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v):
        return validate_phone_number(v)

    @field_validator('link')
    @classmethod
    def validate_link_format(cls, v):
        return validate_url(v)
```

### 電話號碼驗證 (`validate_phone_number`)

**函數位置**: `src/validators.py`

**支援格式**（自動接受有無 `-` 分隔符號）：

| 類型 | 格式範例 | 說明 |
|------|---------|------|
| 手機 | `09XX-XXXXXX`, `09XXXXXXXX` | 台灣手機號碼（10 位數） |
| 手機（容錯） | `9XXXXXXXX` | 允許省略前導 0（向後兼容） |
| 市話（含區碼） | `03-8701129`, `038701129` | 含區域碼的市話（9-10 位數） |
| 市話（僅本地） | `8701129`, `27001234` | 僅本地號碼（7-8 位數，災區常見） |
| 免付費專線 | `0800-XXX-XXX`, `0800XXXXXX` | 免付費電話（10 位數） |
| 國際格式 | `+886-9-XXXXXXXX` | 台灣國際碼格式 |

**驗證邏輯**:
1. 自動移除空白、`-`、`()` 等分隔符號
2. 保留 `+` 號（國際碼）
3. 依序檢查各種電話格式
4. 驗證失敗時拋出 `ValueError` 並顯示：`電話號碼格式不正確: {phone}`

**使用範例**:
```python
# ✅ 有效的電話號碼
validate_phone_number("03-8701129")     # 市話
validate_phone_number("0937-175360")    # 手機
validate_phone_number("8701129")        # 本地號碼
validate_phone_number("+886-3-8701129") # 國際格式

# ❌ 無效的電話號碼
validate_phone_number("123")            # 太短
validate_phone_number("abc")            # 非數字
```

### URL 驗證 (`validate_url`)

**函數位置**: `src/validators.py`

**支援格式**:

| 格式 | 範例 | 說明 |
|------|------|------|
| HTTPS | `https://maps.google.com` | 安全協定 |
| HTTP | `http://example.org` | 一般協定 |
| 省略協定 | `www.example.com` | 允許省略 `http(s)://` |

**驗證邏輯**:
1. 檢查是否以 `http://` 或 `https://` 開頭
2. 或檢查是否以 `www.` 開頭（允許省略協定）
3. 驗證失敗時拋出 `ValueError` 並顯示：`URL格式不正確: {url}`

**使用範例**:
```python
# ✅ 有效的 URL
validate_url("https://sites.google.com/view/guangfu250923/")
validate_url("http://example.org")
validate_url("www.hospital.com")

# ❌ 無效的 URL
validate_url("ftp://example.com")  # 不支援 FTP
validate_url("google.com")         # 缺少 www 或協定
validate_url("just-text")          # 不是 URL
```

---

## 各資源端點詳細說明

### 1. 庇護所（Shelters）

**路由前綴**: `/shelters`
**標籤**: `庇護所（Shelters）`

#### 端點列表

| 方法 | 路徑 | 功能 | 請求參數 | 驗證欄位 |
|------|------|------|---------|---------|
| GET | `/shelters/` | 取得庇護所清單（分頁） | `status`, `limit`, `offset` | - |
| POST | `/shelters/` | 建立新庇護所 | Request Body | `phone`, `link` |
| GET | `/shelters/{id}` | 取得特定庇護所 | `id` (路徑參數) | - |
| PATCH | `/shelters/{id}` | 更新特定庇護所 | `id`, Request Body | - |

#### 建立庇護所 (POST)

**請求範例**:
```json
{
  "name": "光復國小臨時安置中心",
  "location": "花蓮縣光復鄉中正路一段1號",
  "phone": "03-8701129",
  "status": "open",
  "link": "https://maps.google.com/...",
  "capacity": 150
}
```

**驗證規則**:
- `phone` (必填): 必須符合台灣電話號碼格式
- `link` (選填): 必須是有效的 URL 格式
- `status` (必填): 必須是 `ShelterStatusEnum` 的值 (`open`, `full`, `closed`, `temporary_closed`)

---

### 2. 醫療站（Medical Stations）

**路由前綴**: `/medical_stations`
**標籤**: `醫療站（Medical Stations）`

#### 端點列表

| 方法 | 路徑 | 功能 | 驗證欄位 |
|------|------|------|---------|
| GET | `/medical_stations/` | 取得醫療站清單 | - |
| POST | `/medical_stations/` | 建立新醫療站 | `phone`, `link` |
| GET | `/medical_stations/{id}` | 取得特定醫療站 | - |
| PATCH | `/medical_stations/{id}` | 更新特定醫療站 | - |

#### 建立醫療站 (POST)

**驗證規則**:
- `phone` (選填): 電話號碼格式驗證
- `link` (選填): URL 格式驗證
- `station_type` (必填): `MedicalStationTypeEnum` (`self_organized`, `fixed_point`, `shelter_medical`)
- `status` (必填): `MedicalStationStatusEnum` (`active`, `temporarily_closed`, `closed`)

---

### 3. 洗澡點（Shower Stations）

**路由前綴**: `/shower_stations`
**標籤**: `洗澡點（Shower Stations）`

#### 建立洗澡點 (POST)

**驗證規則**:
- `phone` (選填): 電話號碼格式驗證
- `facility_type` (必填): `ShowerFacilityTypeEnum` (`mobile_shower`, `coin_operated`, `regular_bathroom`)
- `status` (必填): `ShowerStationStatusEnum` (`active`, `temporarily_closed`, `ended`)

---

### 4. 飲用水補給站（Water Refill Stations）

**路由前綴**: `/water_refill_stations`
**標籤**: `飲用水補給站（Water Refill Stations）`

#### 建立補給站 (POST)

**驗證規則**:
- `phone` (選填): 電話號碼格式驗證
- `water_type` (必填): `WaterTypeEnum` (`drinking_water`, `bottled_water`, `filtered_water`)
- `status` (必填): `WaterRefillStationStatusEnum` (`active`, `temporarily_unavailable`, `ended`)

---

### 5. 廁所（Restrooms）

**路由前綴**: `/restrooms`
**標籤**: `廁所（Restrooms）`

#### 建立廁所 (POST)

**驗證規則**:
- `phone` (選填): 電話號碼格式驗證
- `facility_type` (必填): `RestroomFacilityTypeEnum` (`mobile_toilet`, `permanent_toilet`, `public_restroom`)
- `status` (必填): `RestroomStatusEnum` (`active`, `maintenance`, `out_of_service`)

---

### 6. 人力資源（Human Resources）

**路由前綴**: `/human_resources`
**標籤**: `人力資源（Human Resources）`

#### 建立人力需求 (POST)

**驗證規則**:
- `phone` (必填): 電話號碼格式驗證
- `status` (必填): `HumanResourceStatusEnum` (`active`, `completed`, `cancelled`)
- `role_type` (必填): `HumanResourceRoleTypeEnum` (如: `general_volunteer`, `medical_staff`, 等)
- `role_status` (必填): `HumanResourceRoleStatusEnum` (`completed`, `pending`, `partial`)

---

### 7. 志工團體（Volunteer Organizations）

**路由前綴**: `/volunteer_organizations`
**標籤**: `志工團體（Volunteer Organizations）`

#### 建立志工團體 (POST)

**驗證規則**:
- `image_url` (選填): URL 格式驗證（團體圖片連結）

---

### 8. 心理健康資源（Mental Health Resources）

**路由前綴**: `/mental_health_resources`
**標籤**: `心理健康資源（Mental Health Resources）`

#### 建立心理健康資源 (POST)

**驗證規則**:
- `website_url` (選填): URL 格式驗證
- `duration_type` (必填): `MentalHealthDurationEnum` (`temporary`, `long_term`, `both`)
- `service_format` (必填): `MentalHealthFormatEnum` (`onsite`, `phone`, `online`, `hybrid`)
- `status` (必填): `MentalHealthResourceStatusEnum` (`active`, `paused`, `ended`)

---

### 9. 物資單（Supplies）

**路由前綴**: `/supplies`
**標籤**: `物資單（Supplies）`

#### 建立物資單 (POST)

**驗證規則**:
- `phone` (選填): 電話號碼格式驗證

---

### 10. 其他資源

#### 住宿資源（Accommodations）
- **路由**: `/accommodations`
- **驗證**: 無特殊欄位驗證

#### 物資項目（Supply Items）
- **路由**: `/supply_items`
- **驗證**: 無特殊欄位驗證

#### 回報事件（Reports）
- **路由**: `/reports`
- **驗證**: 無特殊欄位驗證

---

## 錯誤處理

### 驗證錯誤 (422 Unprocessable Entity)

當資料驗證失敗時，API 會回傳格式化的錯誤訊息：

**回應格式**:
```json
{
  "phone": [
    "Value error, 電話號碼格式不正確: 123"
  ],
  "link": [
    "Value error, URL格式不正確: invalid-url"
  ]
}
```

### 資料庫完整性錯誤

系統會自動處理以下資料庫錯誤：

| 錯誤類型 | HTTP 狀態碼 | 說明 |
|---------|-----------|------|
| `CheckViolation` | 400 | 違反檢查約束 |
| `UniqueViolation` | 409 | 唯一性約束衝突 |
| `NotNullViolation` | 400 | 必填欄位為空 |
| `ForeignKeyViolation` | 400 | 外鍵約束失敗 |

**錯誤回應範例**:
```json
{
  "detail": "Required field 'phone' cannot be null."
}
```

---

## 驗證函數使用指南

### 如何新增驗證規則

1. **在 `src/validators.py` 新增驗證函數**:
```python
def validate_custom_field(value: Optional[str]) -> Optional[str]:
    """自訂驗證邏輯"""
    if not value:
        return value

    # 驗證邏輯
    if not is_valid(value):
        raise ValueError(f'欄位格式不正確: {value}')

    return value
```

2. **在 `src/schemas.py` 的 `*Create` 類別中套用**:
```python
from .validators import validate_custom_field

class MyResourceCreate(MyResourceBase):
    @field_validator('custom_field')
    @classmethod
    def validate_custom_format(cls, v):
        return validate_custom_field(v)
```

### 測試驗證函數

```python
from src.validators import validate_phone_number

# 測試有效輸入
assert validate_phone_number("03-8701129") == "03-8701129"

# 測試無效輸入
try:
    validate_phone_number("123")
except ValueError as e:
    print(e)  # 電話號碼格式不正確: 123
```

---

## 常見問題（FAQ）

### Q1: 為什麼允許省略區碼的本地電話號碼？
A: 在災害救援情境中，災民可能只記得本地號碼，為了降低資料輸入門檻，系統採用寬鬆驗證，接受 7-8 碼的本地號碼。

### Q2: 為什麼 URL 驗證允許 `www.` 開頭？
A: 許多使用者習慣省略 `http://` 或 `https://`，為提升使用者體驗，系統接受 `www.example.com` 格式。

### Q3: 如何查看所有可用的列舉值？
A: 所有列舉定義位於 `src/enum_serializer.py`，或造訪 Swagger UI (`/docs`) 查看互動式文件。

### Q4: 驗證錯誤訊息可以自訂嗎？
A: 可以，在 `src/validators.py` 中修改 `ValueError` 的訊息內容即可。建議使用繁體中文以提升使用者體驗。

---

## 相關文件

- [資料表規格](../../table_spec.md)
- [專案說明](../README.md)
- [開發指南](./getting-started.md)
- [Swagger API 文件](http://localhost:8000/docs)

---

**最後更新**: 2025-10-06
**維護者**: 光復救災平台開發團隊
