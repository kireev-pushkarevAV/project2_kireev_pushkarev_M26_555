# Primitive DB

## Управление таблицами

Модуль для управления структурой базы данных. Метаданные хранятся в `db_meta.json`.

### Команды:
- `create_table <имя_таблицы> <столбец1:тип> ...` — создать таблицу (типы: `int`, `str`, `bool`; первичный ключ `ID:int` добавляется автоматически).
- `list_tables` — показать список всех таблиц.
- `drop_table <имя_таблицы>` — удалить таблицу.
- `help` — справочная информация.
- `exit` — выход из программы.

### Пример использования:
```bash
database
create_table users name:str age:int is_active:bool
list_tables
drop_table users
exit
```
### Демонстрация работы

[![asciicast](https://asciinema.org/a/EEjnzgAIdLhoyOyG.svg)](https://asciinema.org/a/EEjnzgAIdLhoyOyG)