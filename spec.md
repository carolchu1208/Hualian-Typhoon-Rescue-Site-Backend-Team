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

---

## API Spec

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

### 更新資料 (updates)

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

---


## `map_info`

### volunteer_organizations

| 欄位 | 類型 | 必填 | 說明 | 範例 |
|------|------|------|------|------|
| id | string | 是 | 團體唯一識別碼 | |
| last_updated | datetime (ISO 8601) | | 最新更新時間 | |
| registration_status | string | | 接受報名情形（例：「接受中」、「額滿」、「已結束」） | |
| organization_nature | string | | 單位性質（例：「NGO」、「政府單位」、「民間團體」） | |
| organization_name | string | | 單位名稱 | |
| coordinator | string | | 統籌窗口 | |
| contact_info | string | | 聯絡方式（電話、email 等） | |
| registration_method | string | | 報名方式 | |
| service_content | string | | 志工服務內容 | |
| meeting_info | string | | 報到集合時間地點、交通事宜 | |
| notes | string | | 備註事項 | |
| image_url | string \| null | | 圖檔資訊 URL（如果有的話） | |

---

### supplies

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
|---------|---------|------|------|------|
| id | string | 是 | 需求唯一識別碼 | 26f95ee9-e920-4f44-95a2-d40ded631893 |
| org | string | 是 | 單位名稱 | 吉安鄉志工服務隊 |
| address | string | 是 | 地址 | 花蓮縣吉安鄉中山路三段100號 |
| phone | string | 是 | 電話號碼 | 038-123456 |
| status | string | 是 | 需求狀態 | active, completed, cancelled |
| is_completed | boolean | 是 | 是否已完成 | true, false |
| has_medical | boolean | 是 | 是否包含醫療用品 | true, false |
| created_at | number | 是 | 建立時間 | 1759164503 |
| updated_at | number | 是 | 更新時間 | 1759164503 |
| item_id | string | 是 | 物資項目ID | item-uuid-1 |
| item_name | string | 是 | 物資名稱 | 瓶裝水 |
| item_type | string | 是 | 物資類型 | 食物/水, 醫療用品, 生活用品, 大型機具, 其他 |
| item_need | number | 是 | 需求數量 | 30 |
| item_got | number | 是 | 已收到數量 | 18 |
| item_unit | string | 是 | 單位 | 箱, 包, 片, 台, 張, 卷, 套, 瓶, 項 |
| item_status | string | 是 | 物資狀態 | completed, pending, partial |
| delivery_id | string | 否 | 配送記錄ID | delivery-uuid |
| delivery_timestamp | number | 否 | 配送時間 | 1759164503 |
| delivery_quantity | number | 否 | 配送數量 | 10 |
| delivery_notes | string | 否 | 配送備註 | 已送達請簽收 |
| total_items_in_request | number | 否 | 此需求總物資項目數 | 3 |
| completed_items_in_request | number | 否 | 此需求已完成物資數 | 2 |
| pending_items_in_request | number | 否 | 此需求待完成物資數 | 1 |
| total_requests | number | 否 | 系統總需求數 | 150 |
| active_requests | number | 否 | 系統進行中需求數 | 45 |
| completed_requests | number | 否 | 系統已完成需求數 | 100 |
| cancelled_requests | number | 否 | 系統已取消需求數 | 5 |
| total_items | number | 否 | 系統總物資項目數 | 500 |
| completed_items | number | 否 | 系統已完成物資數 | 300 |
| pending_items | number | 否 | 系統待完成物資數 | 200 |
| urgent_requests | number | 否 | 系統緊急需求數 | 12 |
| medical_requests | number | 否 | 系統醫療需求數 | 25 |


---


### `map_spatial_info`

下面是 Zack 設計給所有地圖空間資訊於資料庫所需的通用欄位，Pichu 可以根據以下表格開設 SQL 欄位。

以下為核心設計邏輯：

1. 通用基礎層（Shared Core）： 盡可能列出所有地圖物件共同的核心欄位（如 id, name, address, lat/lng, status, contact 等），以確保資料的通用性和一致性。
2. 分類區隔層（Layering）： 使用 type_key (搭配 subtype_key) 作為主要的圖層分類依據，將異質性的物件進行高效率的區隔和篩選。
3. 彈性擴充層（Flexibility）： 依賴 properties (JSONB) 欄位作為彈性的擴充區域，專門處理每個 type_key 所特有的、非標準化的屬性，從而避免主表欄位爆炸。

如有任何可以改進的地方歡迎提出～

> 範例可以引用自 [`map_spatial_info_example.md`](../map_spatial_info_example.md)

| Column                 | Type                        | Required | Description            | Example                                                            |
|------------------------|-----------------------------|----------|------------------------|--------------------------------------------------------------------|
| **id**                 | `uuid`                      | ✔︎  | 唯一識別碼                     | `550e8400-e29b-41d4-a716-446655440000`                             |
| **name**               | `text`                      | ✔︎  | 名稱                          | `行動沐浴車（光復國小）`                                               |
| **type_key**           | `text` (FK → place_type)    | ✔︎  | 主要地點類型                   | `accommodations`, `shelters`, `medical_stations`, `shower_stations`|
| **subtype_key**        | `text` (FK → place_subtype) |    | 子地點類型，                   | `mobile_shower`, `coin_operated`, `station_type`                   |
| **status_key**         | `text` (FK → place_status)  |    | 狀態，例如                    | `active`, `full`, `paused`, `closed`, `temporarily_closed`         |
| **address**            | `text`                      |    | 地址                          | `花蓮縣光復鄉中山路三段75號`                                          |
| **contact_person**     | `text`                      |    | 聯絡人姓名                    | `張小姐`                                                            |
| **phone**              | `text`                      |    | 聯絡電話                      | `03-8701129`                                                       |
| **email**              | `text`                      |    | 聯絡 Email                    | `info@example.org`                                                |
| **org_id**             | `uuid` (FK → org)           |    | 屬組織 ID                     | `f2b6b7a2-7ef9-4c2a-90b7-b8a2e9123456`                             |
| **capacity_total**     | `integer`                   |    | 總可容納人數                   | `100`                                                              |
| **capacity_male**      | `integer`                   |    | 男性可容納人數                 | `50`                                                               |
| **capacity_female**    | `integer`                   |    | 女性可容納人數                 | `50`                                                               |
| **capacity_available** | `integer`                   |    | 目前剩餘空位                   | `20`                                                              |
| **is_free**            | `boolean`                   |    | 是否免費                      | `true`                                                             |
| **price_amount**       | `numeric(10,2)`             |    | 價格金額（若非免費）            | `50.00`                                                            |
| **price_currency**     | `text`                      |    | 價格幣別                      | `TWD`                                                              |
| **operating_hours**    | `text`                      |    | 營業時間（純文字）              | `10:00–17:30`                                                      |
| **opening_hours**      | `jsonb`                     |    | 結構化營業時間（選用）           | `{"mon":"09:00-18:00","tue":"09:00-18:00"}`                        |
| **source_name**        | `text`                      |    | 資料來源名稱                   | `Threads`                                                          |
| **source_url**         | `text`                      |    | 資料來源連結                   | `https://example.org/detail/123`                                   |
| **source_ref**         | `text`                      |    | 資料來源內部識別                | `sheet-row-45`                                                     |
| **source_updated_at**  | `timestamptz`               |    | 資料來源最後更新時間            | `2025-09-29 15:00:00+08`                                           |
| **lat**                | `numeric(9,6)`              |    | 緯度                         | `23.663900`                                                        |
| **lng**                | `numeric(9,6)`              |    | 經度                         | `121.420800`                                                       |
| **geom**               | `geometry(Point,4326)`      |    | 由 lat/lng 自動生成的地理位置點 | `POINT(121.4208 23.6639)`                                          |
| **properties**         | `jsonb`                     | ✔︎  | 其他彈性欄位 JSON              | `{"notes":"需排隊","has_wifi":true}`                                |
| **is_active**          | `boolean`                   |    | 是否啟用                      | `true`                                                             |
| **valid_from**         | `timestamptz`               |    | 資料有效起始時間                | `2025-09-01 00:00:00+08`                                           |
| **valid_to**           | `timestamptz`               |    | 資料有效結束時間                | `2025-12-31 23:59:59+08`                                           |
| **created_at**         | `timestamptz`               | ✔︎  | 建立時間                       | `2025-09-30 12:00:00+08`                                           |
| **updated_at**         | `timestamptz`               | ✔︎  | 最後更新時間                   | `2025-09-30 12:30:00+08`                                           |
