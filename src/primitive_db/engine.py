import re

from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.decorators import create_cacher
from primitive_db.parser import parse_condition, parse_values_clause
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help() -> None:
    print("\n***Операции с данными***\n")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values (<значение1>, "
        "<значение2>, ...) - создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение> "
        "- прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение> "
        "- удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> exit выход из программы")
    print("<command> help справочная информация\n")


def display_table(
    schema: list[dict[str, str]], rows: list[dict[str, str]]
) -> None:
    field_names = [col["name"] for col in schema]
    pt = PrettyTable()
    pt.field_names = field_names
    for row in rows:
        pt.add_row([row.get(f) for f in field_names])
    print(pt)


def run() -> None:
    metadata = load_metadata()
    cacher, clear_cache = create_cacher()
    print_help()

    while True:
        try:
            user_input = input(">>> Введите команду: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "exitвыход из программы"):
            break

        if user_input.lower() in ("help", "helpсправочная информация"):
            print_help()
            continue

        if user_input.startswith("create_table "):
            parts = user_input.split()
            if len(parts) < 3:
                print("Ошибка: укажите имя таблицы и хотя бы один столбец.")
                continue
            t_name = parts[1]
            cols = parts[2:]
            res = create_table(metadata, t_name, cols)
            if res:
                save_metadata(metadata)
                print(res[1])
            continue

        if user_input == "list_tables":
            res = list_tables(metadata)
            if res:
                print(res)
            continue

        if user_input.startswith("drop_table "):
            parts = user_input.split()
            if len(parts) < 2:
                print("Ошибка: укажите имя таблицы.")
                continue
            res = drop_table(metadata, parts[1])
            if res:
                save_metadata(metadata)
                clear_cache()
                print(res[1])
            continue

        if user_input.startswith("info "):
            t_name = user_input.split(maxsplit=1)[1].strip()
            if t_name not in metadata:
                print(f'Ошибка: Таблица "{t_name}" не существует.')
                continue
            data = load_table_data(t_name)
            schema = metadata[t_name]
            cols_str = ", ".join(f"{c['name']}:{c['type']}" for c in schema)
            print(f"Таблица: {t_name}")
            print(f"Столбцы: {cols_str}")
            print(f"Количество записей: {len(data)}")
            continue

        insert_match = re.match(
            r"^insert\s+into\s+(\w+)\s+values\s*(\(.*\))$",
            user_input,
            re.IGNORECASE,
        )
        if insert_match:
            t_name = insert_match.group(1)
            raw_vals = insert_match.group(2)
            vals = parse_values_clause(raw_vals)
            t_data = load_table_data(t_name)
            res = insert(metadata, t_name, vals, t_data)
            if res and res[0]:
                save_table_data(t_name, t_data)
                clear_cache()
                print(res[1])
            continue

        select_match = re.match(
            r"^select\s+from\s+(\w+)(?:\s+where\s+(.+))?$",
            user_input,
            re.IGNORECASE,
        )
        if select_match:
            t_name = select_match.group(1)
            where_raw = select_match.group(2)
            if t_name not in metadata:
                print(f'Ошибка: Таблица "{t_name}" не существует.')
                continue
            t_data = load_table_data(t_name)
            where_clause = None
            if where_raw:
                try:
                    where_clause = parse_condition(where_raw)
                except ValueError as err:
                    print(err)
                    continue

            cache_key = f"{t_name}:{where_raw}"
            filtered = cacher(
                cache_key,
                lambda: select(t_data, where_clause),
            )
            if filtered is not None:
                display_table(metadata[t_name], filtered)
            continue

        update_match = re.match(
            r"^update\s+(\w+)\s+set\s+(.+?)\s+where\s+(.+)$",
            user_input,
            re.IGNORECASE,
        )
        if update_match:
            t_name = update_match.group(1)
            set_raw = update_match.group(2)
            where_raw = update_match.group(3)
            if t_name not in metadata:
                print(f'Ошибка: Таблица "{t_name}" не существует.')
                continue
            try:
                set_clause = parse_condition(set_raw)
                where_clause = parse_condition(where_raw)
            except ValueError as err:
                print(err)
                continue
            t_data = load_table_data(t_name)
            res = update(t_data, set_clause, where_clause)
            if res:
                count, ids = res
                if count > 0:
                    save_table_data(t_name, t_data)
                    clear_cache()
                    ids_str = ", ".join(str(i) for i in ids)
                    print(
                        f'Запись с ID={ids_str} в таблице "{t_name}" '
                        "успешно обновлена."
                    )
                else:
                    print("Записи для обновления не найдены.")
            continue

        del_match = re.match(
            r"^delete\s+from\s+(\w+)\s+where\s+(.+)$",
            user_input,
            re.IGNORECASE,
        )
        if del_match:
            t_name = del_match.group(1)
            where_raw = del_match.group(2)
            if t_name not in metadata:
                print(f'Ошибка: Таблица "{t_name}" не существует.')
                continue
            try:
                where_clause = parse_condition(where_raw)
            except ValueError as err:
                print(err)
                continue
            t_data = load_table_data(t_name)
            res = delete(t_data, where_clause)
            if res:
                new_data, del_ids = res
                if del_ids:
                    save_table_data(t_name, new_data)
                    clear_cache()
                    ids_str = ", ".join(str(i) for i in del_ids)
                    print(
                        f'Запись с ID={ids_str} успешно удалена '
                        f'из таблицы "{t_name}".'
                    )
                else:
                    print("Записи для удаления не найдены.")
            continue

        print(f"Неизвестная команда: {user_input}")


if __name__ == "__main__":
    run()