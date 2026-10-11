from typing import Any

from primitive_db.decorators import (
    confirm_action,
    handle_db_errors,
    log_time,
)
from primitive_db.utils import delete_table_data

VALID_TYPES = {"int", "str", "bool"}


@handle_db_errors
def create_table(
    metadata: dict[str, Any], table_name: str, columns: list[str]
) -> tuple[bool, str]:
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')

    schema: list[dict[str, str]] = [{"name": "ID", "type": "int"}]

    for col in columns:
        if ":" not in col:
            raise ValueError(f'Неверный формат столбца "{col}".')
        name, col_type = col.split(":", 1)
        if col_type not in VALID_TYPES:
            raise ValueError(f'Неподдерживаемый тип данных "{col_type}".')
        schema.append({"name": name, "type": col_type})

    metadata[table_name] = schema
    cols_desc = ", ".join(f"{c['name']}:{c['type']}" for c in schema)
    return True, (
        f'Таблица "{table_name}" успешно создана со столбцами: {cols_desc}'
    )


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata: dict[str, Any], table_name: str) -> tuple[bool, str]:
    if table_name not in metadata:
        raise KeyError(table_name)
    del metadata[table_name]
    delete_table_data(table_name)
    return True, f'Таблица "{table_name}" успешно удалена.'


@handle_db_errors
def list_tables(metadata: dict[str, Any]) -> str:
    if not metadata:
        return "Нет созданных таблиц."
    return "-\n" + "\n".join(metadata.keys())


@handle_db_errors
@log_time
def insert(
    metadata: dict[str, Any],
    table_name: str,
    values: list[Any],
    table_data: list[dict[str, Any]],
) -> tuple[bool, str, int | None]:
    if table_name not in metadata:
        raise KeyError(table_name)

    schema = metadata[table_name]
    user_columns = [col for col in schema if col["name"] != "ID"]

    if len(values) != len(user_columns):
        raise ValueError(
            f"Ожидалось {len(user_columns)} значений, получено {len(values)}."
        )

    new_row: dict[str, Any] = {}
    next_id = max([row["ID"] for row in table_data], default=0) + 1
    new_row["ID"] = next_id

    type_mapping = {"int": int, "str": str, "bool": bool}

    for col_info, val in zip(user_columns, values):
        expected_type = type_mapping[col_info["type"]]
        if col_info["type"] == "bool" and not isinstance(val, bool):
            raise ValueError(
                f"Поле '{col_info['name']}' должно иметь тип bool."
            )
        if col_info["type"] == "int" and (
            isinstance(val, bool) or not isinstance(val, int)
        ):
            raise ValueError(f"Поле '{col_info['name']}' должно иметь тип int.")
        if col_info["type"] == "str" and not isinstance(val, str):
            raise ValueError(f"Поле '{col_info['name']}' должно иметь тип str.")
        new_row[col_info["name"]] = expected_type(val)

    table_data.append(new_row)
    return (
        True,
        f'Запись с ID={next_id} успешно добавлена в таблицу "{table_name}".',
        next_id,
    )


@handle_db_errors
@log_time
def select(
    table_data: list[dict[str, Any]],
    where_clause: tuple[str, Any] | None = None,
) -> list[dict[str, Any]]:
    if not where_clause:
        return list(table_data)
    col, val = where_clause
    return [row for row in table_data if row.get(col) == val]


@handle_db_errors
@confirm_action("удаление записей")
def delete(
    table_data: list[dict[str, Any]],
    where_clause: tuple[str, Any],
) -> tuple[list[dict[str, Any]], list[int]]:
    w_col, w_val = where_clause
    deleted_ids = [row["ID"] for row in table_data if row.get(w_col) == w_val]
    remaining = [row for row in table_data if row.get(w_col) != w_val]
    return remaining, deleted_ids


@handle_db_errors
def update(
    table_data: list[dict[str, Any]],
    set_clause: tuple[str, Any],
    where_clause: tuple[str, Any],
) -> tuple[int, list[int]]:
    w_col, w_val = where_clause
    s_col, s_val = set_clause
    updated_ids: list[int] = []

    for row in table_data:
        if row.get(w_col) == w_val:
            row[s_col] = s_val
            updated_ids.append(row["ID"])

    return len(updated_ids), updated_ids