# 官網基本資訊

## 資訊總覽

| 資訊 | 內容 |
|------|------|
| Google Sheet 副本 | 光復救災平台用的副本 |
| 官網連結 | https://sites.google.com/view/guangfu250923/%E7%81%BD%E6%B0%91%E5%8D%94%E5%8A%A9/slennh?authuser=0 |
| 前端 UI Spec | https://www.figma.com/design/3HmmJtwok42obsXH93s21b/%E8%8A%B1%E8%93%AE%E5%85%89%E5%BE%A9%E5%BE%A9%E5%8E%9F%E4%B9%8B%E8%B7%AF%EF%BC%81?node-id=162-553&t=Fw2L65c6BsMguQRh-0 |
| 前端技術 | Google Site |
| 資料庫類型 | PostgreSQL |
| 資料庫 endpoint | |
| 資料庫帳號密碼 | |
| 後端 API 框架 | Golang |

## API 格式

### 批量撈取資料

**端點：** `GET /resources/{resource_type}`

**Request Body：** N/A

**Response Body：**
```json
{
  "code": 200,
  "data": [
    {resource_entity_1},
    {resource_entity_2},
    ...
  ]
}
```

### 寫入單一資料

**端點：** `POST /resources/{resource_type}`

**Request Body：**
```json
{
  <same_schema_as_table_schema>
}
```

**Response Body：**
```json
{
  "code": 201
}
```

### 更新單一資料

**端點：** `POST /resources/{resource_type}/{id}`

**Request Body：**
```json
{
  <same_schema_as_table_schema>
}
```

**Response Body：**
```json
{
  "code": 200
}
```


## 資料表格式

### volunteer_organizations (救災團體)

| 欄位 | 類型 | 必填 | 說明 | 範例 |
|------|------|------|------|------|
| id | string | 是 | 團體唯一識別碼 | |
| created_at | string | 是 | 資料建立時間 (UTC) | |
| updated_at | string | 是 | 資料最後時間 (UTC) | |
| name | string | 是 | 單位名稱 | |
| registration_status | string | 是 | 持續超收, 停止招收 | |
| organization_nature | string | 是 | 大型分派組織, 小型志工團, 特殊專業志工團 | |
| coordinator | string | 是 | 統籌窗口 | |
| contact_info | string | 是 | 聯絡方式（電話、email 等） | |
| phone | string | 是 | 電話號碼 | 038-123456 |
| registration_method | string | 是 | 報名方式 | |
| service_content | string | 是 | 志工服務內容 | |
| meeting_info | string | 是 | 報到集合時間地點、交通事宜 | |
| notes | string | | 備註事項 | |

### supplies (物資)

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
|---------|---------|------|------|------|
| id | string | 是 | 需求唯一識別碼 | 26f95ee9-e920-4f44-95a2-d40ded631893 |
| created_at | string | 是 | 資料建立時間 (UTC) | |
| updated_at | string | 是 | 資料最後時間 (UTC) | |
| organization | string | 是 | 單位名稱 | 吉安鄉志工服務隊 |
| address | string | 是 | 地址 | 花蓮縣吉安鄉中山路三段100號 |
| phone | string | 是 | 電話號碼 | 038-123456 |
| status | string | 是 | 需求狀態 | active, completed, cancelled |
| is_completed | boolean | 是 | 是否已完成 | true, false |
| has_medical | boolean | 是 | 是否包含醫療用品 | true, false |
| supplies | string | 是 | 物資清單JSON | [{"name":"瓶裝水","type":"食物/水","need":30,"got":18,"unit":"箱"},{"name":"口罩","type":"醫療用品","need":100,"got":50,"unit":"盒"}] |

### counseling_resources (心理諮商資源)

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
|---------|---------|------|------|------|
| id | string | 是 | 服務唯一識別碼 | 550e8400-e29b-41d4-a716-446655440000 |
| created_at | string | 是 | 資料建立時間 (UTC) | |
| updated_at | string | 是 | 資料最後時間 (UTC) | |
| name | string | 是 | 服務名稱 | 安心關懷站 |
| service_duration | string | 是 | 服務類型 | 臨時, 長期 |
| service_form | string | 是 | 服務形式 | 實體, 電話, 線上, 多種 |
| operating_hours | string | 是 | 服務時間 | 每天早上九點到晚上九點 |
| phone | string | 是 | 電話號碼 | 03-8701114 |
| address | string | 是 | 服務地點 | 花蓮縣光復鄉大進國小 |
| contact_person | string | 是 | 聯絡人姓名 | 張小姐 |
| phone | string | 是 | 聯絡電話 | 03-8701129 |
| email | string | 是 | 聯絡Email | info@example.org |
| website | string |  | 官方網址 | https://www.1980.org.tw/ |
| notes | string |  | 備註 | 提供24小時服務 |

### locations (地點)

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
|---------|---------|------|------|------|
| id | string | 是 | 唯一識別碼 | 550e8400-e29b-41d4-a716-446655440000 |
| created_at | string | 是 | 資料建立時間 (UTC) | |
| updated_at | string | 是 | 資料最後時間 (UTC) | |
| type | string | 是 | 地點類型 | 住宿點, 庇護所, 醫療站, 洗澡點, 如廁點 |
| name | string | 是 | 名稱 | 行動沐浴車(光復國小) |
| status | string | 是 | 狀態 | 開放, 暫停, 關閉 |
| address | string | 是 | 地址 | 花蓮縣光復鄉中山路三段75號 |
| open_date | string | 是 |  |  |
| close_date | string | 是 |  |  |
| operating_hours | string | 是 |  |  |
| contact_person | string | 是 | 聯絡人姓名 | 張小姐 |
| phone | string | 是 | 聯絡電話 | 03-8701129 |
| email | string | 是 | 聯絡Email | info@example.org |
| lat | string | 是 | 緯度 | 23.663900 |
| lng | string | 是 | 經度 | 121.420800 |
| additional_info | string |  | 其他彈性欄位JSON | |
| data_source | string | | 資料來源 | |

#### 庇護所 additional_info

```json
{}
```

#### 醫療站 additional_info

```json
{}
```

#### 住宿點 additional_info

```json
{
  "room_info": "四人雅房４間、六人雅房1間、八人雅房1間"
}
```

#### 洗澡點 additional_info

```json
{}
```

#### 如廁點 additional_info

```json
{}
```