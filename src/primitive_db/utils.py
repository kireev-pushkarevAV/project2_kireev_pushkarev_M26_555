
import json
from pathlib import Path
from typing import Any

DATA_DIR = Path("data")
META_FILE = Path("db_meta.json")


def load_metadata() -> dict[str, Any]:
    if not META_FILE.exists():
        return {}
    with open(META_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metadata(metadata: dict[str, Any]) -> None:
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def load_table_data(table_name: str) -> list[dict[str, Any]]:
    file_path = DATA_DIR / f"{table_name}.json"
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_table_data(table_name: str, data: list[dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / f"{table_name}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def delete_table_data(table_name: str) -> None:
    file_path = DATA_DIR / f"{table_name}.json"
    if file_path.exists():
        file_path.unlink()