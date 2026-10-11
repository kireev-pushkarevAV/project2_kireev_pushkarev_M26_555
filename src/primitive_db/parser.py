import re
import shlex
from typing import Any


def parse_value(val_str: str) -> Any:
    val_str = val_str.strip()
    if val_str.lower() == "true":
        return True
    if val_str.lower() == "false":
        return False
    if (val_str.startswith('"') and val_str.endswith('"')) or (
        val_str.startswith("'") and val_str.endswith("'")
    ):
        return val_str[1:-1]
    try:
        return int(val_str)
    except ValueError:
        return val_str


def parse_values_clause(raw_values: str) -> list[Any]:
    raw = raw_values.strip()
    if raw.startswith("(") and raw.endswith(")"):
        raw = raw[1:-1]
    lexer = shlex.shlex(raw, posix=True)
    lexer.whitespace = ","
    lexer.whitespace_split = True
    lexer.quotes = "\"'`"
    tokens = list(lexer)
    return [parse_value(token) for token in tokens]


def parse_condition(cond_str: str) -> tuple[str, Any]:
    match = re.match(r"^(\w+)\s*=\s*(.+)$", cond_str.strip())
    if not match:
        raise ValueError(
            "Некорректный формат условия. Ожидается: <столбец> = <значение>"
        )
    col = match.group(1).strip()
    val = parse_value(match.group(2).strip())
    return col, val