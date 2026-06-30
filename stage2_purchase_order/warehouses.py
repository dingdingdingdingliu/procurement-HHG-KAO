"""Parse warehouses.md and return warehouse data."""

import re
from pathlib import Path

_MD_PATH = Path(__file__).parent / "warehouses.md"


def load_warehouses() -> list[dict]:
    """Return list of {name, code, address} dicts parsed from warehouses.md."""
    warehouses = []
    text = _MD_PATH.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or "倉別名稱" in line or "---" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 3:
            warehouses.append({"name": parts[0], "code": parts[1], "address": parts[2]})
    return warehouses


def warehouse_names() -> list[str]:
    return [w["name"] for w in load_warehouses()]


def get_warehouse(name: str) -> dict:
    for w in load_warehouses():
        if w["name"] == name:
            return w
    raise ValueError(f"倉別 '{name}' 不存在於 warehouses.md")
