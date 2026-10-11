VALID_TYPES = {"int", "str", "bool"}


def create_table(metadata: dict, table_name: str, raw_columns: list[str]) -> dict:
    """Создает новую таблицу с валидацией типов и автоматическим ID."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    columns: dict[str, str] = {}

    for item in raw_columns:
        if ":" not in item:
            print(f"Некорректное значение: {item}. Попробуйте снова.")
            return metadata

        col_name, col_type = item.split(":", 1)
        col_name = col_name.strip()
        col_type = col_type.strip()

        if col_type not in VALID_TYPES:
            print(f"Некорректное значение: {item}. Попробуйте снова.")
            return metadata

        columns[col_name] = col_type

    # Гарантируем столбец ID:int первым
    ordered_columns: dict[str, str] = {}
    if "ID" not in columns:
        ordered_columns["ID"] = "int"
    ordered_columns.update(columns)

    metadata[table_name] = ordered_columns

    cols_str = ", ".join(f"{name}:{ctype}" for name, ctype in ordered_columns.items())
    print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')
    return metadata


def drop_table(metadata: dict, table_name: str) -> dict:
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def list_tables(metadata: dict) -> None:
    """Выводит список всех таблиц."""
    if not metadata:
        print("База данных не содержит таблиц.")
        return

    for table_name in metadata:
        print(f"-\n{table_name}")