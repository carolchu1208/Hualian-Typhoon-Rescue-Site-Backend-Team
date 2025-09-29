# `map_spatial_info` Example

下面是 Zack 設計給所有地圖空間資訊於資料庫所需的通用欄位，Pichu 可以根據以下表格開設 SQL 欄位。在每個 `type` 後也有提供範例 JSON 供參閱，表格為原先 YJ 設計的欄位。

如有任何可以改進的地方歡迎提出～

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

## shelters

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
|---------|---------|------|------|------|
| id | string | 是 | 庇護所唯一識別碼 | shelter-uuid-001 |
| name | string | 是 | 庇護所/安置點名稱 | 光復國小臨時安置中心 |
| location | string | 是 | 地點/地址 | 花蓮縣光復鄉中正路一段1號 |
| phone | string | 是 | 連絡電話 | 03-8701129 |
| link | string | 否 | 相關連結（官網、地圖等） | https://maps.google.com/... |
| status | string | 是 | 營運狀態 | open, full, closed, temporary_closed |
| capacity | number | 否 | 容納人數上限 | 150 |
| current_occupancy | number | 否 | 目前收容人數 | 87 |
| available_spaces | number | 否 | 剩餘空位 | 63 |
| facilities | array | 否 | 提供設施 | ["盥洗設備", "用餐區", "醫療站"] |
| contact_person | string | 否 | 聯絡人姓名 | 王小明主任 |
| notes | string | 否 | 備註說明 | 僅限災民，需攜帶身分證件 |
| coordinates | object | 否 | GPS 座標 | {"lat": 23.6639, "lng": 121.4208} |
| opening_hours | string | 否 | 開放時間 | 24小時開放 |
| created_at | number | 是 | 建立時間（Unix timestamp） | 1727664000 |
| updated_at | number | 是 | 更新時間（Unix timestamp） | 1727750400 |

```json
{
  "id": "22222222-aaaa-bbbb-cccc-222222222222",
  "name": "光復國小臨時安置中心",
  "type_key": "shelters",
  "subtype_key": null,
  "status_key": "full",
  "address": "花蓮縣光復鄉中正路一段1號",
  "contact_person": "王小明主任",
  "phone": "03-8701129",
  "email": null,
  "org_id": null,
  "capacity_total": 150,
  "capacity_male": null,
  "capacity_female": null,
  "capacity_available": 63,
  "is_free": true,
  "price_amount": null,
  "price_currency": "TWD",
  "operating_hours": "24小時開放",
  "opening_hours": null,
  "source_name": "花蓮縣政府",
  "source_url": "https://maps.google.com/...",
  "source_ref": "shelter-uuid-001",
  "source_updated_at": "2024-10-01T00:00:00+08:00",
  "lat": 23.663900,
  "lng": 121.420800,
  "geom": null,
  "properties": {
    "facilities": ["盥洗設備", "用餐區", "醫療站"],
    "notes": "僅限災民，需攜帶身分證件"
  },
  "is_active": true,
  "valid_from": null,
  "valid_to": null,
  "created_at": "2024-10-01T00:00:00+08:00",
  "updated_at": "2024-10-01T00:00:00+08:00",
  "source_map": {
    "name": "庇護所/安置點名稱",
    "status_key": "營運狀態",
    "address": "地點/地址 (location)",
    "phone": "連絡電話",
    "contact_person": "聯絡人姓名",
    "source_url": "相關連結（官網、地圖等）",
    "capacity_total": "容納人數上限 (capacity)",
    "capacity_available": "剩餘空位 (available_spaces)",
    "properties.facilities": "提供設施 (facilities)",
    "operating_hours": "開放時間",
    "lat/lng": "GPS 座標 (coordinates)"
  }
}
```

---

## medical_stations

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
|---------|---------|------|------|------|
| id | string | 是 | 醫療站唯一識別碼 | station-uuid-001 |
| station_type | string | 是 | 醫療站類型 | self_organized, fixed_point, shelter_medical |
| name | string | 是 | 醫療站名稱 | 慈濟第三醫療站 |
| location | string | 是 | 地點/地址 | 全聯對面加油站帳篷下 |
| detailed_address | string | 否 | 詳細地址 | 花蓮縣光復鄉東富路30-2號 |
| phone | string | 否 | 聯絡電話 | 03-8701234 |
| contact_person | string | 否 | 負責人/聯絡人 | 李醫師 |
| status | string | 是 | 營運狀態 | active, temporarily_closed, closed |
| services | array | 否 | 提供服務項目 | ["急診處理", "傷口處理", "慢性病用藥"] |
| operating_hours | string | 否 | 營運時間 | 08:00-20:00 |
| equipment | array | 否 | 醫療設備 | ["血壓計", "體溫計", "急救箱"] |
| medical_staff | number | 否 | 醫護人員數 | 3 |
| daily_capacity | number | 否 | 每日服務量 | 50 |
| coordinates | object | 否 | GPS 座標 | {"lat": 23.6639, "lng": 121.4208} |
| affiliated_organization | string | 否 | 所屬組織 | 慈濟基金會 |
| notes | string | 否 | 備註說明 | 提供免費醫療諮詢 |
| link | string | 否 | 相關連結 | https://maps.google.com/... |
| created_at | number | 是 | 建立時間（Unix timestamp） | 1727664000 |
| updated_at | number | 是 | 更新時間（Unix timestamp） | 1727750400 |

```json
{
  "id": "33333333-aaaa-bbbb-cccc-333333333333",
  "name": "慈濟第三醫療站",
  "type_key": "medical_stations",
  "subtype_key": "fixed_point",
  "status_key": "active",
  "address": "全聯對面加油站帳篷下",
  "contact_person": "李醫師",
  "phone": "03-8701234",
  "email": null,
  "org_id": null,
  "capacity_total": null,
  "capacity_male": null,
  "capacity_female": null,
  "capacity_available": null,
  "is_free": true,
  "price_amount": null,
  "price_currency": "TWD",
  "operating_hours": "08:00-20:00",
  "opening_hours": null,
  "source_name": "慈濟基金會",
  "source_url": "https://maps.google.com/...",
  "source_ref": "station-uuid-001",
  "source_updated_at": "2024-10-01T00:00:00+08:00",
  "lat": 23.663900,
  "lng": 121.420800,
  "geom": null,
  "properties": {
    "services": ["急診處理", "傷口處理", "慢性病用藥"],
    "equipment": ["血壓計", "體溫計", "急救箱"],
    "medical_staff": 3,
    "daily_capacity": 50,
    "affiliated_organization": "慈濟基金會",
    "notes": "提供免費醫療諮詢",
    "link": "https://maps.google.com/..."
  },
  "is_active": true,
  "valid_from": null,
  "valid_to": null,
  "created_at": "2024-10-01T00:00:00+08:00",
  "updated_at": "2024-10-01T00:00:00+08:00",
  "source_map": {
    "subtype_key": "醫療站類型 (station_type)",
    "name": "醫療站名稱",
    "address": "地點/地址 (location) 或 詳細地址 (detailed_address)",
    "status_key": "營運狀態 (status)",
    "operating_hours": "營運時間",
    "properties.services": "提供服務項目 (services)",
    "properties.equipment": "醫療設備 (equipment)",
    "properties.medical_staff": "醫護人員數",
    "properties.daily_capacity": "每日服務量",
    "properties.affiliated_organization": "所屬組織",
    "properties.notes": "備註說明",
    "properties.link": "相關連結",
    "lat/lng": "GPS 座標 (coordinates)"
  }
}
```

---

## mental_health_resources

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
|---------|---------|------|------|------|
| id | string | 是 | 資源唯一識別碼 | mh-uuid-001 |
| duration_type | string | 是 | 服務期間類型 | temporary, long_term, both |
| name | string | 是 | 服務單位或計畫名稱 | 光復災後心理支持團隊 |
| service_format | string | 是 | 服務形式 | onsite, phone, online, hybrid |
| service_hours | string | 是 | 服務時間 | 週一至週五 09:00-17:00 |
| contact_info | string | 是 | 聯繫方式 | 0800-123-456 / support@example.org |
| website_url | string | 否 | 網址 | https://example.org |
| target_audience | array | 否 | 服務對象 | ["災民", "志工", "救災人員"] |
| specialties | array | 否 | 專業領域 | ["創傷輔導", "壓力管理", "哀傷輔導"] |
| languages | array | 否 | 提供語言服務 | ["中文", "台語", "英文"] |
| is_free | boolean | 是 | 是否免費 | true, false |
| location | string | 否 | 服務地點 | 光復鄉公所二樓會議室 |
| coordinates | object | 否 | GPS 座標 | {"lat": 23.6639, "lng": 121.4208} |
| status | string | 是 | 服務狀態 | active, paused, ended |
| capacity | number | 否 | 每日服務量 | 20 |
| waiting_time | string | 否 | 等候時間 | 即時服務, 需預約, 3-5天 |
| notes | string | 否 | 備註 | 提供個別諮商及團體輔導 |
| emergency_support | boolean | 是 | 是否提供緊急支援 | true, false |
| created_at | number | 是 | 建立時間（Unix timestamp） | 1727664000 |
| updated_at | number | 是 | 更新時間（Unix timestamp） | 1727750400 |

```json
{
  "id": "99999999-aaaa-bbbb-cccc-999999999999",
  "name": "光復災後心理支持團隊",
  "type_key": "mental_health_resources",
  "subtype_key": null,
  "status_key": "active",
  "address": "光復鄉公所二樓會議室",
  "contact_person": null,
  "phone": "0800-123-456",
  "email": "support@example.org",
  "org_id": null,
  "capacity_total": 20,
  "capacity_male": null,
  "capacity_female": null,
  "capacity_available": null,
  "is_free": true,
  "price_amount": null,
  "price_currency": "TWD",
  "operating_hours": "週一至週五 09:00-17:00",
  "opening_hours": null,
  "source_name": "衛生單位",
  "source_url": "https://example.org",
  "source_ref": "mh-uuid-001",
  "source_updated_at": "2024-10-01T00:00:00+08:00",
  "lat": 23.663900,
  "lng": 121.420800,
  "geom": null,
  "properties": {
    "duration_type": "temporary",
    "service_format": "onsite",
    "target_audience": ["災民", "志工", "救災人員"],
    "specialties": ["創傷輔導", "壓力管理", "哀傷輔導"],
    "languages": ["中文", "台語", "英文"],
    "waiting_time": "需預約",
    "emergency_support": true,
    "notes": "提供個別諮商及團體輔導"
  },
  "is_active": true,
  "valid_from": null,
  "valid_to": null,
  "created_at": "2024-10-01T00:00:00+08:00",
  "updated_at": "2024-10-01T00:00:00+08:00",
  "source_map": {
    "name": "服務單位或計畫名稱",
    "phone/email": "聯繫方式 (contact_info)",
    "operating_hours": "服務時間 (service_hours)",
    "status_key": "服務狀態 (status)",
    "address": "服務地點 (location)",
    "lat/lng": "GPS 座標 (coordinates)",
    "properties.duration_type": "服務期間類型 (duration_type)",
    "properties.service_format": "服務形式 (service_format)",
    "properties.target_audience": "服務對象",
    "properties.specialties": "專業領域",
    "properties.languages": "提供語言服務",
    "properties.waiting_time": "等候時間",
    "properties.emergency_support": "是否提供緊急支援",
    "properties.notes": "備註"
  }
}
```

---

## accommodations

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
|---------|---------|------|------|------|
| id | string | 是 | 住宿唯一識別碼 | acc-uuid-001 |
| township | string | 是 | 鄉鎮 | 吉安鄉, 花蓮市, 玉里鎮, 光復鄉 |
| name | string | 是 | 民宿/住宿點名稱 | 山緹民宿 |
| has_vacancy | string | 是 | 尚有空房狀態 | available, full, unknown, need_confirm |
| available_period | string | 是 | 開放期間 | 9/27-10/3, 9/24起 |
| restrictions | string | 否 | 入住限制 | 限救災志工, 每人限住兩晚, 需出示志工證 |
| contact_info | string | 是 | 聯繫方式 | 0932-520-949, Line: @treetree, FB私訊 |
| room_info | string | 否 | 時間、房型資訊 | 雙人房 2 間、四人房 1 間 |
| address | string | 是 | 地址 | 花蓮縣吉安鄉民治路242號 |
| coordinates | object | 否 | GPS 經緯度 | {"lat": 23.9608, "lng": 121.5798} |
| pricing | string | 是 | 費用 | 免費, 優惠價500元/晚, 待確認 |
| info_source | string | 否 | 資訊來源 | 花蓮國際民宿協會, threads, 經濟部FB |
| notes | string | 否 | 其他備註 | 通往光復的台鐵單程車程約30-50分鐘 |
| capacity | number | 否 | 總可容納人數 | 12 |
| status | string | 是 | 營運狀態 | active, paused, ended |
| registration_method | string | 否 | 報到方式 | 現場登記, 線上預約, 電話預約 |
| facilities | array | 否 | 提供設施 | ["盥洗", "Wi-Fi", "停車位", "早餐"] |
| distance_to_disaster_area | string | 否 | 至災區距離/車程 | 30-50分鐘車程, 15公里 |
| created_at | number | 是 | 建立時間（Unix timestamp） | 1727664000 |
| updated_at | number | 是 | 更新時間（Unix timestamp） | 1727750400 |

```json
{
  "id": "11111111-aaaa-bbbb-cccc-111111111111",
  "name": "山緹民宿",
  "type_key": "accommodations",
  "subtype_key": null,
  "status_key": "active",
  "address": "花蓮縣吉安鄉民治路242號",
  "contact_person": "黃先生",
  "phone": "0932-520-949",
  "email": null,
  "org_id": null,
  "capacity_total": 12,
  "capacity_male": null,
  "capacity_female": null,
  "capacity_available": 4,
  "is_free": false,
  "price_amount": 500.00,
  "price_currency": "TWD",
  "operating_hours": null,
  "opening_hours": null,
  "source_name": "花蓮國際民宿協會",
  "source_url": "https://example.org/accommodation/123",
  "source_ref": "acc-uuid-001",
  "source_updated_at": "2024-10-01T00:00:00+08:00",
  "lat": 23.960800,
  "lng": 121.579800,
  "geom": null,
  "properties": {
    "township": "吉安鄉",
    "has_vacancy": "available",
    "available_period": "9/27-10/3",
    "restrictions": "限救災志工",
    "room_info": "雙人房 2 間、四人房 1 間",
    "info_source": "threads",
    "notes": "台鐵到光復單程30-50分鐘",
    "registration_method": "電話預約",
    "facilities": ["盥洗", "Wi-Fi", "停車位", "早餐"],
    "distance_to_disaster_area": "30-50分鐘車程"
  },
  "is_active": true,
  "valid_from": null,
  "valid_to": null,
  "created_at": "2024-10-01T00:00:00+08:00",
  "updated_at": "2024-10-01T00:00:00+08:00",
  "source_map": {
    "name": "民宿/住宿點名稱",
    "address": "地址",
    "contact_person/phone": "聯繫方式 (contact_info)",
    "capacity_total": "總可容納人數 (capacity)",
    "price_amount/price_currency/is_free": "費用 (pricing)",
    "properties.has_vacancy": "尚有空房狀態 (has_vacancy)",
    "properties.available_period": "開放期間",
    "properties.restrictions": "入住限制",
    "properties.room_info": "時間、房型資訊",
    "properties.registration_method": "報到方式",
    "properties.facilities": "提供設施",
    "properties.distance_to_disaster_area": "距災區距離/車程",
    "lat/lng": "GPS 經緯度 (coordinates)"
  }
}
```

---

## shower_stations

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
|---------|---------|------|------|------|
| id | string | 是 | 洗澡點唯一識別碼 | shower-uuid-001 |
| name | string | 是 | 名稱 | 光復國小 |
| address | string | 是 | 地址 | 花蓮縣光復鄉中山路三段75號 |
| coordinates | object | 否 | GPS 經緯度 | {"lat": 23.6639, "lng": 121.4208} |
| phone | string | 否 | 聯絡電話 | 03-8702880 |
| facility_type | string | 是 | 設施類型 | mobile_shower, coin_operated, regular_bathroom |
| time_slots | string | 是 | 提供洗澡的時段 | 上午10:00-11:30, 下午15:30-17:30 |
| gender_schedule | object | 否 | 性別使用時段 | {"male": ["10:00-10:30"], "female": ["10:30-11:30"]} |
| available_period | string | 是 | 開放期間 | 9/26-9/28, 即日起至10/3 |
| capacity | number | 否 | 同時可容納人數 | 5 |
| is_free | boolean | 是 | 是否免費 | true, false |
| pricing | string | 否 | 費用說明 | 投幣式，每次10元 |
| notes | string | 否 | 備註 | 多座行動沐浴車, 僅開放廁所+浴室 |
| info_source | string | 否 | 資料來源 | https://www.threads.com/... |
| status | string | 是 | 營運狀態 | active, temporarily_closed, ended |
| facilities | array | 否 | 額外設施 | ["吹風機", "毛巾", "盥洗用品"] |
| distance_to_guangfu | string | 否 | 距光復車程 | 20分鐘, 40分鐘 |
| requires_appointment | boolean | 是 | 是否需預約 | true, false |
| contact_method | string | 否 | 預約方式 | LINE: @wowhostel, 電話預約 |
| created_at | number | 是 | 建立時間（Unix timestamp） | 1727664000 |
| updated_at | number | 是 | 更新時間（Unix timestamp） | 1727750400 |

```json
{
  "id": "44444444-aaaa-bbbb-cccc-444444444444",
  "name": "行動沐浴車（光復國小）",
  "type_key": "shower_stations",
  "subtype_key": "mobile_shower",
  "status_key": "active",
  "address": "花蓮縣光復鄉中山路三段75號",
  "contact_person": "張小姐",
  "phone": "03-8702880",
  "email": null,
  "org_id": null,
  "capacity_total": 5,
  "capacity_male": null,
  "capacity_female": null,
  "capacity_available": null,
  "is_free": true,
  "price_amount": null,
  "price_currency": "TWD",
  "operating_hours": "10:00–17:30",
  "opening_hours": null,
  "source_name": "Threads",
  "source_url": "https://threads.net/post/abc123",
  "source_ref": "shower-uuid-001",
  "source_updated_at": "2024-10-01T00:00:00+08:00",
  "lat": 23.663900,
  "lng": 121.420800,
  "geom": null,
  "properties": {
    "time_slots": "上午10:00-11:30, 下午15:30-17:30",
    "gender_schedule": {"male":["10:00-10:30"], "female":["10:30-11:30"]},
    "available_period": "即日起至10/3",
    "pricing": "免費",
    "notes": "多座行動沐浴車",
    "facilities": ["吹風機", "毛巾", "盥洗用品"],
    "requires_appointment": false,
    "contact_method": "電話預約"
  },
  "is_active": true,
  "valid_from": null,
  "valid_to": null,
  "created_at": "2024-10-01T00:00:00+08:00",
  "updated_at": "2024-10-01T00:00:00+08:00",
  "source_map": {
    "name": "名稱",
    "address": "地址",
    "phone": "聯絡電話",
    "subtype_key": "設施類型 (facility_type)",
    "operating_hours/properties.time_slots": "提供洗澡的時段 (time_slots)",
    "properties.gender_schedule": "性別使用時段",
    "properties.available_period": "開放期間",
    "capacity_total": "同時可容納人數 (capacity)",
    "is_free/properties.pricing": "是否免費 / 費用說明",
    "status_key": "營運狀態",
    "properties.facilities": "額外設施",
    "properties.requires_appointment": "是否需預約",
    "properties.contact_method": "預約方式",
    "lat/lng": "GPS 經緯度 (coordinates)"
  }
}
```

---

## water_refill_stations

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
|---------|---------|------|------|------|
| id | string | 是 | 裝水點唯一識別碼 | water-uuid-001 |
| name | string | 是 | 地點名稱 | 光復國小裝水站 |
| address | string | 是 | 地址 | 花蓮縣光復鄉中山路三段75號 |
| coordinates | object | 否 | GPS 經緯度 | {"lat": 23.6639, "lng": 121.4208} |
| phone | string | 否 | 聯絡電話 | 03-8701129 |
| water_type | string | 是 | 水源類型 | drinking_water, bottled_water, filtered_water |
| opening_hours | string | 是 | 開放時間 | 24小時, 08:00-20:00 |
| is_free | boolean | 是 | 是否免費 | true, false |
| container_required | string | 否 | 容器要求 | 自備容器, 現場提供瓶裝水 |
| daily_capacity | number | 否 | 每日供水量（公升） | 500 |
| status | string | 是 | 營運狀態 | active, temporarily_unavailable, ended |
| water_quality | string | 否 | 水質狀態 | tested, safe, needs_boiling |
| facilities | array | 否 | 額外設施 | ["飲水機", "水龍頭", "瓶裝水發放"] |
| accessibility | boolean | 是 | 無障礙設施 | true, false |
| distance_to_disaster_area | string | 否 | 距災區距離 | 在災區內, 5分鐘車程 |
| notes | string | 否 | 備註 | 提供冷熱水, 請自備容器 |
| info_source | string | 否 | 資料來源 | 鄉公所公告 |
| created_at | number | 是 | 建立時間（Unix timestamp） | 1727664000 |
| updated_at | number | 是 | 更新時間（Unix timestamp） | 1727750400 |

```json
{
  "id": "55555555-aaaa-bbbb-cccc-555555555555",
  "name": "光復國小裝水站",
  "type_key": "water_refill_stations",
  "subtype_key": "drinking_water",
  "status_key": "active",
  "address": "花蓮縣光復鄉中山路三段75號",
  "contact_person": null,
  "phone": "03-8701129",
  "email": null,
  "org_id": null,
  "capacity_total": null,
  "capacity_male": null,
  "capacity_female": null,
  "capacity_available": null,
  "is_free": true,
  "price_amount": null,
  "price_currency": "TWD",
  "operating_hours": "24小時",
  "opening_hours": null,
  "source_name": "鄉公所公告",
  "source_url": null,
  "source_ref": "water-uuid-001",
  "source_updated_at": "2024-10-01T00:00:00+08:00",
  "lat": 23.664500,
  "lng": 121.421000,
  "geom": null,
  "properties": {
    "container_required": "自備容器",
    "daily_capacity": 500,
    "water_quality": "safe",
    "facilities": ["飲水機", "水龍頭", "瓶裝水發放"],
    "accessibility": true,
    "distance_to_disaster_area": "在災區內",
    "notes": "提供冷熱水"
  },
  "is_active": true,
  "valid_from": null,
  "valid_to": null,
  "created_at": "2024-10-01T00:00:00+08:00",
  "updated_at": "2024-10-01T00:00:00+08:00",
  "source_map": {
    "name": "地點名稱",
    "address": "地址",
    "phone": "聯絡電話",
    "subtype_key": "水源類型 (water_type)",
    "operating_hours": "開放時間",
    "is_free": "是否免費",
    "status_key": "營運狀態 (status)",
    "properties.container_required": "容器要求",
    "properties.daily_capacity": "每日供水量（公升）",
    "properties.water_quality": "水質狀態",
    "properties.facilities": "額外設施",
    "properties.accessibility": "無障礙設施",
    "properties.distance_to_disaster_area": "距災區距離",
    "properties.notes": "備註",
    "lat/lng": "GPS 經緯度 (coordinates)"
  }
}
```

---

## restrooms

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
|---------|---------|------|------|------|
| id | string | 是 | 廁所點唯一識別碼 | restroom-uuid-001 |
| name | string | 是 | 地點名稱 | 光復國小臨時廁所 |
| address | string | 是 | 地址 | 花蓮縣光復鄉中山路三段75號 |
| coordinates | object | 否 | GPS 經緯度 | {"lat": 23.6639, "lng": 121.4208} |
| phone | string | 否 | 聯絡電話 | 03-8701129 |
| facility_type | string | 是 | 設施類型 | mobile_toilet, permanent_toilet, public_restroom |
| opening_hours | string | 是 | 開放時間 | 24小時, 06:00-22:00 |
| is_free | boolean | 是 | 是否免費 | true, false |
| male_units | number | 否 | 男廁數量 | 3 |
| female_units | number | 否 | 女廁數量 | 5 |
| unisex_units | number | 否 | 無性別廁所數量 | 2 |
| accessible_units | number | 否 | 無障礙廁所數量 | 1 |
| has_water | boolean | 是 | 是否有供水 | true, false |
| has_lighting | boolean | 是 | 是否有照明 | true, false |
| status | string | 是 | 營運狀態 | active, maintenance, out_of_service |
| cleanliness | string | 否 | 清潔狀態 | clean, needs_cleaning, under_cleaning |
| last_cleaned | number | 否 | 最後清潔時間（Unix timestamp） | 1727664000 |
| facilities | array | 否 | 額外設施 | ["洗手台", "衛生紙", "洗手乳", "烘手機"] |
| distance_to_disaster_area | string | 否 | 距災區距離 | 在災區內, 5分鐘步行 |
| notes | string | 否 | 備註 | 定時清潔，請保持整潔 |
| info_source | string | 否 | 資料來源 | 環保局 |
| created_at | number | 是 | 建立時間（Unix timestamp） | 1727664000 |
| updated_at | number | 是 | 更新時間（Unix timestamp） | 1727750400 |

```json
{
  "id": "66666666-aaaa-bbbb-cccc-666666666666",
  "name": "光復國小臨時廁所",
  "type_key": "restrooms",
  "subtype_key": "mobile_toilet",
  "status_key": "active",
  "address": "花蓮縣光復鄉中山路三段75號",
  "contact_person": null,
  "phone": "03-8701129",
  "email": null,
  "org_id": null,
  "capacity_total": null,
  "capacity_male": null,
  "capacity_female": null,
  "capacity_available": null,
  "is_free": true,
  "price_amount": null,
  "price_currency": "TWD",
  "operating_hours": "24小時",
  "opening_hours": null,
  "source_name": "環保局",
  "source_url": null,
  "source_ref": "restroom-uuid-001",
  "source_updated_at": "2024-10-01T00:00:00+08:00",
  "lat": 23.664000,
  "lng": 121.421500,
  "geom": null,
  "properties": {
    "male_units": 3,
    "female_units": 5,
    "unisex_units": 2,
    "accessible_units": 1,
    "has_water": true,
    "has_lighting": true,
    "cleanliness": "clean",
    "last_cleaned": 1727664000,
    "facilities": ["洗手台", "衛生紙", "洗手乳", "烘手機"],
    "distance_to_disaster_area": "在災區內",
    "notes": "定時清潔，請保持整潔"
  },
  "is_active": true,
  "valid_from": null,
  "valid_to": null,
  "created_at": "2024-10-01T00:00:00+08:00",
  "updated_at": "2024-10-01T00:00:00+08:00",
  "source_map": {
    "name": "地點名稱",
    "address": "地址",
    "phone": "聯絡電話",
    "subtype_key": "設施類型 (facility_type)",
    "operating_hours": "開放時間",
    "is_free": "是否免費",
    "status_key": "營運狀態",
    "properties.male_units": "男廁數量",
    "properties.female_units": "女廁數量",
    "properties.unisex_units": "無性別廁所數量",
    "properties.accessible_units": "無障礙廁所數量",
    "properties.has_water": "是否有供水",
    "properties.has_lighting": "是否有照明",
    "properties.cleanliness": "清潔狀態",
    "properties.last_cleaned": "最後清潔時間（Unix）",
    "properties.facilities": "額外設施",
    "properties.distance_to_disaster_area": "距災區距離",
    "properties.notes": "備註",
    "lat/lng": "GPS 經緯度 (coordinates)"
  }
}
```
