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

## CRUD-операции

Модуль для работы с данными внутри таблиц. Данные сохраняются в директорию `data/` в формате JSON.
[![asciicast](https://asciinema.org/connect/4d20ecc5-ee49-4ef5-9b43-de1bc6d13dc9)](https://asciinema.org/connect/4d20ecc5-ee49-4ef5-9b43-de1bc6d13dc9)
### Команды:
- `insert into <имя_таблицы> values (<значение1>, <значение2>, ...)` — создать запись.
- `select from <имя_таблицы> where <столбец> = <значение>` — прочитать записи по условию.
- `select from <имя_таблицы>` — прочитать все записи.
- `update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия>` — обновить запись.
- `delete from <имя_таблицы> where <столбец> = <значение>` — удалить запись.
- `info <имя_таблицы>` — вывести информацию о таблице.
- `exit` — выход из программы.
- `help` — справочная информация.

### Пример использования:
```bash
database
create_table users name:str age:int is_active:bool
insert into users values ("Sergei", 28, true)
select from users where age = 28
update users set age = 29 where name = "Sergei"
delete from users where ID = 1
info users
exit
```

### Декораторы и безопасность
### Демонстрация работы

[![asciicast](https://asciinema.org/connect/324177a2-65bb-4a78-96ef-ec5894240d53)](https://asciinema.org/connect/324177a2-65bb-4a78-96ef-ec5894240d53)

  - Централизованная обработка ошибок (`@handle_db_errors`).
  - Подтверждение опасных действий (`@confirm_action`).
  - Замер времени выполнения дисковых операций (`@log_time`).
  - Замыкание для кэширования одинаковых запросов на чтение (`create_cacher`).

  ## Команды

- `create_table <имя_таблицы> <столбец1:тип> ...` — создать таблицу.
- `list_tables` — показать список таблиц.
- `drop_table <имя_таблицы>` — удалить таблицу (с подтверждением).
- `insert into <имя_таблицы> values (<значение1>, ...)` — добавить запись.
- `select from <имя_таблицы> [where <столбец> = <значение>]` — прочитать данные.
- `update <имя_таблицы> set <столбец> = <новое_значение> where <условие>` — обновить данные.
- `delete from <имя_таблицы> where <условие>` — удалить запись (с подтверждением).
- `info <имя_таблицы>` — сводная информация о таблице.
- `help` — справочная информация.
- `exit` — выход из базы данных.

## Пример работы

```bash
database
create_table users name:str age:int is_active:bool
insert into users values ("Sergei", 28, true)
select from users where age = 28
delete from users where ID = 1
drop_table users
exit```