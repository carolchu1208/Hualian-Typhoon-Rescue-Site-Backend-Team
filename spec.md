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

## Table Schema

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

### shelters

目前上面資料是資訊總表的 【災民相關】避難所/安置點 分頁。

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

---

### medical_stations

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

---

### mental_health_resources

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

---

### accommodations

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

---

### shower_stations

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

---

### water_refill_stations

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

---

### restrooms

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

## human_resources
| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
| --- | --- | --- | --- | --- |
| id | string | 是 | 需求唯一識別碼 | hr-26f95ee9-e920-4f44-95a2-d40ded631893 |
| org | string | 是 | 單位名稱 | 吉安鄉志工服務隊 |
| address | string | 是 | 工作地點地址 | 花蓮縣吉安鄉中山路三段100號 |
| phone | string | 是 | 聯絡電話 | 038-123456 |
| status | string | 是 | 需求狀態 | active, completed, cancelled |
| is_completed | boolean | 是 | 是否已完成 | true, false |
| has_medical | boolean | 否 | 是否屬於醫療人力需求 | true, false |
| created_at | number | 是 | 建立時間 (Unix Timestamp) | 1759164503 |
| updated_at | number | 是 | 更新時間 (Unix Timestamp) | 1759164503 |
| role_name | string | 是 | 人力角色名稱 | 搬運志工 |
| role_type | string | 是 | 人力類型 | 一般志工, 醫療人員, 行政支援, 司機, 安全維護, 其他 |
| skills | array[string] | 否 | 所需技能或資格 | [“搬運”,“CPR”,“急救證照”] |
| certifications | array[string] | 否 | 必要證照 | [“急救員證照”] |
| experience_level | string | 否 | 經驗需求 | level_1, level_2, level_3 |
| language_requirements | array[string] | 否 | 語言需求 | [“中文”,“英文”] |
| headcount_need | number | 是 | 需求人數 | 30 |
| headcount_got | number | 是 | 已到位人數 | 18 |
| headcount_unit | string | 否 | 人數單位 | 人 |
| role_status | string | 是 | 人力填補狀態 | completed, pending, partial |
| shift_start_ts | number | 否 | 班次開始時間 (Unix Timestamp) | 1759164503 |
| shift_end_ts | number | 否 | 班次結束時間 (Unix Timestamp) | 1759168103 |
| shift_notes | string | 否 | 班次備註 | 需自備手套與安全鞋 |
| assignment_timestamp | number | 否 | 派工/報到時間 | 1759164503 |
| assignment_count | number | 否 | 本次派工人數 | 10 |
| assignment_notes | string | 否 | 派工備註 | 到現場與組長報到 |
| total_roles_in_request | number | 否 | 此需求總人力角色數 | 3 |
| completed_roles_in_request | number | 否 | 此需求已完成人力角色數 | 2 |
| pending_roles_in_request | number | 否 | 此需求待完成人力角色數 | 1 |
| total_requests | number | 否 | 系統總人力需求數 | 150 |
| active_requests | number | 否 | 系統進行中人力需求數 | 45 |
| completed_requests | number | 否 | 系統已完成人力需求數 | 100 |
| cancelled_requests | number | 否 | 系統已取消人力需求數 | 5 |
| total_roles | number | 否 | 系統總人力角色項目數 | 500 |
| completed_roles | number | 否 | 系統已完成人力角色數 | 300 |
| pending_roles | number | 否 | 系統待完成人力角色數 | 200 |
| urgent_requests | number | 否 | 系統緊急人力需求數 | 12 |
| medical_requests | number | 否 | 系統醫療人力需求數 | 25 |

## suppiles

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
| --- | --- | --- | --- | --- |
| id | string | 是 | 需求唯一識別碼 | 26f95ee9-e920-4f44-95a2-d40ded631893 |
| name | string | 否 | 需要救援的單位名字 | OOOO |
| address | string | 否 | 需要救援的單位地址 | OOOO |
| phone | string | 否 | 需要救援的單位電話 | OOOO |
| notes | string | 否 | 備註 | 無 |
| created_at | number | 是 | 建立時間（Unix timestamp） | 1727664000 |
| updated_at | number | 是 | 更新時間（Unix timestamp） | 1727750400 |

## suppily_items 

| 欄位名稱 | 資料類型 | 必填 | 說明 | 範例 |
| --- | --- | --- | --- | --- |
| id | string | 是 | 需求唯一識別碼 | 31f95ee9-e920-4f44-95a2-d40ded631893 |
| suppily_id | string | 是 | 對應的物資單ID | 26f95ee9-e920-4f44-95a2-d40ded631893 |
| tag | string | 否 | 物資總類 | 飲食 |
| name | string | 否 | 物資名稱 | OOOO |
| received_count | number | 否 | 已取得的物資數量 | 1 |
| total_number | number | 是 | 總共所需的物資數量 | 3 |
| unit | string | 否 | 物資的單位 | 箱 |
