# 20251004 YJ's Note

Carol/糖糖 pass 過來的需求，希望將以下表單匯入人力頁面：
https://docs.google.com/spreadsheets/d/1UyZ5KoltCY8Dklqy5POWflEkdAu_4EdBiqwi3Nl4TZ8/edit?gid=744864469#gid=744864469

我預計把以下需求，以及相關資料餵給 AI，請他根據我的輸入產生我需要的輸出。

## 表單概述

這份表單是以「直欄」當作一筆一筆的資料，最左一欄是表單的 headers
- 橫向表格格式：每一列代表一筆記錄，第一列是欄位名稱
- 關鍵欄位：姓名、電話、需求、位置、補充、聯絡狀況等
- 約18筆記錄需要處理

## 資料處理需求

我需要把這份手動整理的表單，轉換成能夠匯入到我們資料庫的格式。
- 輸入 : data.csv
- 輸出1 : out.json (能夠拿去直接去呼叫 POST API 的格式)
- 輸出2 : out.csv
  - 包含 out.json 的所有欄位
  - 包含 data.csv 的原始欄位
  - 清楚區分原始資料來源欄位和資料庫欄位
  - 包含來源連結追蹤

## 資料轉換規則

### 1. 姓名轉換規則 (org)
- **規則**: 隱私保護格式，保留姓氏和末字，中間用 x 替代
- **範例**:
  - `王小明` → `王x明` (3字：保留首末字，中間用x)
  - `王陳小小明` → `王陳xx明` (5字：保留複姓和末字，中間用xx)
  - `王小` → `王x` (2字：保留首字，後面用x)

### 2. 地址標準化 (address)
- **規則**: 補全完整地址格式，移除註解到備註欄位
- **標準化處理**:
  - 補全縣市資訊：統一加上「花蓮縣光復鄉」前綴
  - 地址純化：移除地址中的說明文字和註解
  - 註解遷移：將地址中的註解移動到 assignment_notes
- **範例**:
  - `和平街26號` → `花蓮縣光復鄉和平街26號`
  - `中山路二段 351 號，林森路口第一間` →
    - address: `花蓮縣光復鄉中山路二段351號`
    - assignment_notes: 加入「林森路口第一間」
  - `大同村佛祖街21號，邦查農場斜對面的路進來，佛祖街 47 巷後面，因為路被封住了` →
    - address: `花蓮縣光復鄉大同村佛祖街21號`
    - assignment_notes: 加入位置說明

### 3. 電話號碼清理 (phone)
- **規則**: 移除所有非數字字符，保留純數字格式
- **範例**:
  - `0937-175360` → `0937175360`
  - `0916302770` → `0916302770`
  - `0933-823818` → `0933823818`

### 4. 需求解析 (role_name + headcount_need + headcount_unit)
- **role_name**: 保持原始需求文字
- **headcount_need**: 從需求文字中提取數量
  - 尋找 `*1`, `*2` 等數字標記
  - 預設為 1 （如果沒有明確數字）
- **headcount_unit**: 根據設備類型判斷單位
  - 卡車、怪手、山貓 → `台`
  - 志工 → `人`
  - 複合需求 → `項目`

### 5. 過濾條件
跳過以下記錄，不納入輸出：
- 包含「結案」的記錄
- 包含「不需要」的記錄
- 包含「已無需求」的記錄
- 姓名為空的記錄

### 6. out.csv 欄位結構
- **[原始資料-xxx]**: 來自 Google Sheets 的手動整理資料
  - 來源、更新時間、加入時間、姓名、電話、LINE、需求、位置、機具進出是否問題、補充、聯絡狀況、是否已調度機具、附圖、聯絡人員
- **[資料庫欄位-xxx]**: 轉換後準備匯入資料庫的欄位
  - org、address、phone、status、is_completed、has_medical、role_name、role_type、skills、certifications、language_requirements、headcount_need、headcount_got、headcount_unit、role_status、assignment_notes

## 人力頁面後端資料庫欄位

``` json
{
  "org": string, # 來自姓名，隱私保護格式：保留首末字，中間用x替代
  "address": string, # 來自位置，標準化為完整地址格式
  "phone": string, # 來自電話，清理後純數字格式 0987654321
  "status": "active", # 固定值，勿改
  "is_completed": False, # 固定值，勿改
  "role_name": string, # 來自需求，保持原文
  "role_type": "其他", # 固定值，勿改
  "headcount_need": 0, # 來自需求解析數量
  "headcount_got": 0, # 固定值，勿改
  "headcount_unit": string, # 來自需求解析單位 (台/人/項目)
  "role_status": "pending", # 固定值，勿改
  "assignment_notes": string # 來自補充
}
```

## 輸出結果

處理完成後生成：
- **out.json**: 9筆有效記錄（過濾後），可直接用於 POST API 調用
- **out.csv**: 包含原始資料和轉換後資料的完整追蹤表，便於驗證和審核
