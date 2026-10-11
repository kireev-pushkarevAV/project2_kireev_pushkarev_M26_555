# Primitive DB
Простая реляционная база данных с интерфейсом командной строки (CLI), поддержкой хранения
данных в формате JSON, CRUD-операциями, расширенной обработкой ошибок через декораторы и
замыканием для кэширования запросов.
## Возможности
- **Управление структурой данных**: создание таблиц с типизацией столбцов (int, str, bool),
автогенерация первичного ключа ID:int, просмотр списка таблиц и удаление.
- **CRUD-операции**: создание (insert), чтение с фильтрацией (select / where), обновление
(update) и удаление (delete) записей.
- **Табличный формат вывода**: структурированное отображение результатов запросов через
PrettyTable.
- **Декораторы и безопасность**:
- @handle_db_errors: централизованная обработка исключений (KeyError, ValueError,
FileNotFoundError).
- @confirm_action: интерактивный запрос подтверждения перед выполнением опасных операций
(drop_table, delete).
- @log_time: замер времени выполнения дисковых операций.
- **Замыкания (Closures)**:
- create_cacher: кэширование одинаковых запросов на чтение (select).
## Установка и запуск
### Установка зависимостей:
make install
# или: uv sync
### Запуск базы данных:
make run

# или: uv run database
### Проверка стиля (линтер):
make lint
# или: uv run ruff check .
## Доступные команды
### Управление структурой
- create_table &lt;имя_таблицы&gt; &lt;столбец1:тип&gt; ... — создать новую таблицу (типы: int, str,
bool). Поле ID:int создается автоматически.
- list_tables — показать список всех существующих таблиц.
- drop_table &lt;имя_таблицы&gt; — удалить таблицу и связанные данные (требует подтверждения).
### Операции с данными (CRUD)
- insert into &lt;имя_таблицы&gt; values (&lt;значение1&gt;, ...) — добавить новую запись.
- select from &lt;имя_таблицы&gt; — прочитать все записи таблицы.
- select from &lt;имя_таблицы&gt; where &lt;столбец&gt; = &lt;значение&gt; — прочитать записи по условию.
- update &lt;имя_таблицы&gt; set &lt;столбец&gt; = &lt;новое_значение&gt; where &lt;условие&gt; — обновить
существующую запись.
- delete from &lt;имя_таблицы&gt; where &lt;столбец&gt; = &lt;значение&gt; — удалить запись по условию
(требует подтверждения).
- info &lt;имя_таблицы&gt; — вывести информацию о таблице, схеме столбцов и количестве строк.
### Служебные команды
- help — вывод справочной информации.
- exit — выход из интерактивной сессии базы данных.
## Пример работы
database
create_table users name:str age:int is_active:bool
insert into users values (&quot;Sergei&quot;, 28, true)
select from users where age = 28
update users set age = 29 where name = &quot;Sergei&quot;
delete from users where ID = 1
info users
drop_table users
exit
## Демонстрация работы
[![asciicast](https://asciinema.org/a/CV4EpAFv4UYsnsOL.svg)](https://asciinema.org/a/CV4EpAFv4UYsnsOL)