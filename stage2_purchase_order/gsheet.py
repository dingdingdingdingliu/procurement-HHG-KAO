"""Google Sheets helpers using gspread + service account."""

import glob
import os
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

_CREDS_GLOB = str(Path(__file__).parent.parent / "credentials" / "*.json")


def _get_client() -> gspread.Client:
    matches = glob.glob(_CREDS_GLOB)
    if not matches:
        raise FileNotFoundError(f"找不到 Service Account 金鑰，請放置於 credentials/*.json")
    creds = Credentials.from_service_account_file(matches[0], scopes=_SCOPES)
    return gspread.authorize(creds)


def read_master_sheet() -> list[dict]:
    """
    Read 採購單母體 from PROCUREMENT_MASTER_SHEET_URL env var.
    Returns list of row dicts keyed by header.
    """
    url = os.environ.get("PROCUREMENT_MASTER_SHEET_URL", "")
    if not url:
        raise ValueError("環境變數 PROCUREMENT_MASTER_SHEET_URL 未設定")
    client = _get_client()
    sh = client.open_by_url(url)
    ws = sh.get_worksheet(0)
    return ws.get_all_records()


def read_review_sheet(url: str) -> list[dict]:
    """
    Read 自動化採單審核版 from user-supplied URL.
    Returns (data, headers).
    """
    client = _get_client()
    sh = client.open_by_url(url)
    ws = sh.get_worksheet(0)
    rows = ws.get_all_values()

    # Find header row (first row containing 'ItemSKU')
    header_row_idx = None
    for i, row in enumerate(rows):
        if any("ItemSKU" in str(cell) for cell in row):
            header_row_idx = i
            break

    if header_row_idx is None:
        raise ValueError("審核版 Google Sheet 中找不到含有 'ItemSKU' 的標題列")

    headers = rows[header_row_idx]
    data = []
    for row in rows[header_row_idx + 1:]:
        if not any(row):
            continue
        data.append(dict(zip(headers, row)))
    return data, headers


def build_sku_qty_map(review_sheet_data: list[dict], headers: list[str]) -> dict[str, str]:
    """
    Build {ItemSKU: qty} map from 審核版.
    D column = ItemSKU (index 3), AM column = index 38.
    """
    sku_col = "ItemSKU"

    # AM = column index 38 (0-based)
    am_idx = 38
    am_header = headers[am_idx] if am_idx < len(headers) else None

    result = {}
    for row in review_sheet_data:
        sku = str(row.get(sku_col, "")).strip()
        qty = str(row.get(am_header, "")).strip() if am_header else ""
        if sku:
            result[sku] = qty
    return result
