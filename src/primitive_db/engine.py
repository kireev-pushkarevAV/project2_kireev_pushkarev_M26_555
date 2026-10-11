import shlex

import prompt

from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import load_metadata, save_metadata


def print_help() -> None:
    """Выводит справочную информацию."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print(
        "<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("- <command> exit — выход из программы")
    print("- <command> help — справочная информация\n")


def run() -> None:
    """Главный интерактивный цикл управления таблицами."""
    print_help()

    while True:
        try:
            user_input = prompt.string(">>>Введите команду: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nВыход из программы.")
            break

        if not user_input:
            continue

        try:
            tokens = shlex.split(user_input)
        except ValueError as err:
            print(f"Ошибка парсинга команды: {err}")
            continue

        command = tokens[0]
        args = tokens[1:]

        metadata = load_metadata()

        match command:
            case "exit":
                break

            case "help":
                print_help()

            case "create_table":
                if len(args) < 1:
                    print(
                        "Некорректное значение: пропущено имя таблицы. "
                        "Попробуйте снова."
                    )
                    continue
                table_name = args[0]
                raw_columns = args[1:]
                old_tables_count = len(metadata)
                metadata = create_table(metadata, table_name, raw_columns)
                if len(metadata) > old_tables_count:
                    save_metadata(metadata)

            case "drop_table":
                if len(args) != 1:
                    print(
                        "Некорректное значение: укажите имя таблицы. "
                        "Попробуйте снова."
                    )
                    continue
                table_name = args[0]
                if table_name in metadata:
                    metadata = drop_table(metadata, table_name)
                    save_metadata(metadata)
                else:
                    drop_table(metadata, table_name)

            case "list_tables":
                list_tables(metadata)

            case _:
                print(f"Функции {command} нет. Попробуйте снова.")