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

### org (救災團體)
|欄位       |類型         |必填|說明/註解                                        |
|---------|-----------|--|---------------------------------------------|
|id       |UUID       |是 |                       |
|created_at |DateTime   |是 |UTC；建立時間                            |
|updated_at |DateTime   |是 |UTC；更新時間                            |
|name     |string(255)|是 |團體名稱                                         |
|status   |string(10) |是 |招募狀態；choices: over(持續超收)/stop(停止招收)          |
|type |string(20) |是 |組織性質；choices: dist_large/team_small/pro_special|
|contact_name |string(255)|是 |統籌窗口姓名                                       |
|contact_phone|string(50) |是 |聯絡電話                              |
|contact_email|email      |否 |聯絡 Email；格式驗證                                |
|contact_url |url        |否 |官方網址/聯絡頁面                                    |
|contact_other|string(255)|否 |其他聯絡方式（LINE/FB 等）                            | |
|services |text       |是 |服務內容                                    |
|meeting  |text       |是 |集合/交通資訊                                |
|note     |text       |否 |備註（非必填）                                      |

### supplies (物資)
|欄位        |類型         |必填|說明/註解                                                          |
|----------|-----------|--|---------------------------------------------------------------|
|id        |UUID       |是 |主鍵；UUID                                                        |
|created_at|DateTime   |是 |UTC；建立時間                                                       |
|updated_at|DateTime   |是 |UTC；更新時間                                                       |
|status    |string(10) |是 |需求狀態；choices: active/done/cancel                               | |
|has_med   |boolean    |是 |是否包含醫療用品；true/false                                            |
|org_id    |UUID(FK)   |否 |關聯組織；外鍵至 orgs，SET_NULL                                         |
|place_id  |UUID(FK)   |否 |關聯地點；外鍵至 places，SET_NULL                                       |
|address   |string(255)|否 |寄送地址（若非指向 Place，可填）                                            |
|phone     |string(50) |否 |聯絡電話                                                           |
|items     |JSON       |是 |物資清單；如 [{“name”:“瓶裝水”,“type”:“食物/水”,“need”:30,“got”:18,“unit”:“箱”}]|

### counseling (心理諮商資源)
| 欄位            |類型         |必填|說明/註解                         |
|---------------|-----------|--|------------------------------|
| id            |UUID       |是 |主鍵；UUID                       |
| created_at    |DateTime   |是 |UTC；建立時間                      |
| updated_at    |DateTime   |是 |UTC；更新時間                      |
| name          |string(255)|是 |服務名稱                          |
| duration      |string(10) |是 |服務期間；choices: temp(臨時)/long(長期) |
| form          |string(10) |是 |服務形式；choices: site/call/online/multi|
| org_id        |UUID(FK)   |否 |所屬組織；外鍵至 orgs，SET_NULL        |
| opening_hours |string(255)|是 |服務時間              |
| address       |string(255)|是 |服務地點                          |
| contact_name  |string(255)|是 |聯絡人姓名                         |
| contact_phone |string(50) |是 |聯絡電話                          |
| contact_email |email      |否 |聯絡 Email                      |
| contact_url   |url        |否 |官方網址                          |
| note          |text       |否 |備註                            |

### places (地點)
| 欄位            |類型          |必填|說明/註解                                  |
|---------------|------------|--|---------------------------------------|
| id            |UUID        |是 |主鍵；UUID                                |
| created_at    |DateTime    |是 |UTC；建立時間                               |
| updated_at    |DateTime    |是 |UTC；更新時間                               |
| type          |string(10)  |是 |地點類型；choices: stay/shelter/med/shower/toilet|
| name          |string(255) |是 |地點名稱                                   |
| status        |string(10)  |是 |狀態；choices: open/pause/close           |
| address       |string(255) |是 |地址                                     |
| org_id        |UUID(FK)    |否 |所屬組織；外鍵至 orgs，SET_NULL                 |
| open_date     |date        |否 |開始服務日期                                 |
| close_date    |date        |否 |結束服務日期                                 |
| opening_hours |string(255) |否 |營運時間（自由文字，例如「每天 09:00-21:00」）          |
| contact_name  |string(255) |是 |聯絡人姓名                                  |
| contact_phone |string(50)  |是 |聯絡電話                                   |
| contact_email |email       |否 |聯絡 Email                               |
| lat           |decimal(9,6)|是 |緯度                         |
| lng           |decimal(9,6)|是 |經度                           |
| extra         |JSON        |否 |彈性欄位                         |
| source        |string(255) |否 |資料來源（例如「社群貼文」或 API 名稱）                 |

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