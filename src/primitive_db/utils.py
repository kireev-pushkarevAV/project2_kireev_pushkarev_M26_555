import json
from pathlib import Path

META_FILE = Path("db_meta.json")


def load_metadata(filepath: Path | str = META_FILE) -> dict:
    """Загружает метаданные из JSON-файла.

    Возвращает пустой словарь, если файл отсутствует.
    """
    path = Path(filepath)
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(data: dict, filepath: Path | str = META_FILE) -> None:
    """Сохраняет метаданные в JSON-файл."""
    path = Path(filepath)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)