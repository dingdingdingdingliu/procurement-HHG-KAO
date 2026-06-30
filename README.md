# MOMO 採購自動化系統

- Stage 1: momo補貨資料製作
- Stage 2: 採購單製作（Google Sheet → Excel）
- Stage 3: 採購單拆倉製作
- Stage 4: 待定

## 本機執行方式

### 1. 安裝套件

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

```bash
# macOS / Linux
export SHEET_A_URL="https://docs.google.com/spreadsheets/d/..."

# Windows PowerShell
$env:SHEET_A_URL = "https://docs.google.com/spreadsheets/d/..."
```

### 3. 放置 Google Service Account 金鑰

將 `.json` 金鑰檔放入 `credentials/` 資料夾（程式會自動搜尋）。

### 4. 放置公版 Excel

將 `_KAO_八達網花王採購單-可複製.xlsx` 放入 `stage2_purchase_order/`。

### 5. 啟動應用程式

```bash
streamlit run app.py
```

## 倉別資料維護

編輯 `stage2_purchase_order/warehouses.md`，依 Markdown 表格格式新增或修改倉別。

## 欄位對應設定（如公版 Excel 欄位異動）

編輯 `stage2_purchase_order/excel_writer.py` 頂部常數：

| 常數 | 說明 |
|------|------|
| `COL_ITEM_NO` | 品號欄位（用於 SKU 比對） |
| `COL_QTY_PCS` | 採購數量(pcs) 欄位 |
| `COL_ARRIVAL_DATE` | 到貨日欄位 |
| `DATA_START_ROW` | 主表格第一筆資料列號 |
