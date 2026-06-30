"""MOMO 採購自動化系統 — Streamlit 主入口"""

import datetime
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(page_title="MOMO 採購自動化系統", layout="wide")
st.title("MOMO 採購自動化系統")

tab1, tab2, tab3 = st.tabs(["Stage 1：momo補貨資料製作", "Stage 2：採購單製作", "Stage 3：採購單拆倉製作"])

# ── Stage 1 ───────────────────────────────────────────────────────────────────
with tab1:
    st.info("敬請期待")

# ── Stage 2 ───────────────────────────────────────────────────────────────────
with tab2:
    st.header("採購單製作（Google Sheet → Excel）")

    from stage2_purchase_order.warehouses import warehouse_names, get_warehouse

    with st.form("stage2_form"):
        sheet_b_url = st.text_input(
            "本次下採自動化採單網址（送審版本）",
            placeholder="https://docs.google.com/spreadsheets/d/...",
        )

        warehouse_name = st.selectbox("到貨倉別", warehouse_names())

        purchase_date = st.date_input("採購日", value=datetime.date.today())

        arrival_date = st.date_input("到貨日", value=None)

        submitted = st.form_submit_button("產出採購單 Excel")

    if submitted:
        errors = []
        if not sheet_b_url.strip():
            errors.append("請輸入自動化採單網址")
        if arrival_date is None:
            errors.append("請選擇到貨日")

        if errors:
            for e in errors:
                st.error(e)
        else:
            try:
                from stage2_purchase_order.gsheet import read_sheet_b, build_sku_qty_map
                from stage2_purchase_order.excel_writer import generate_excel

                with st.spinner("讀取 Google Sheet 中..."):
                    sheet_b_data, headers = read_sheet_b(sheet_b_url.strip())
                    sku_qty_map = build_sku_qty_map(sheet_b_data, headers)

                warehouse = get_warehouse(warehouse_name)

                with st.spinner("產出 Excel 中..."):
                    file_bytes = generate_excel(
                        sku_qty_map=sku_qty_map,
                        warehouse_name=warehouse["name"],
                        warehouse_code=warehouse["code"],
                        warehouse_address=warehouse["address"],
                        purchase_date=purchase_date,
                        arrival_date=arrival_date,
                    )

                filename = f"採購單_{warehouse_name}_{purchase_date.strftime('%Y%m%d')}.xlsx"
                st.success(f"產出完成！共對應 {len(sku_qty_map)} 筆 SKU")
                st.download_button(
                    label="下載採購單 Excel",
                    data=file_bytes,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

            except FileNotFoundError as e:
                st.error(f"檔案錯誤：{e}")
            except ValueError as e:
                st.error(f"設定錯誤：{e}")
            except Exception as e:
                st.error(f"發生錯誤：{e}")
                st.exception(e)

# ── Stage 3 ───────────────────────────────────────────────────────────────────
with tab3:
    st.info("敬請期待")
