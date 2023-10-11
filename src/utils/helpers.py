from typing import Any, Optional
import hashlib
import sqlparse


def find_columns(
    tokens: tuple[sqlparse.sql.Statement | Any, ...],
    is_possible_column: Optional[bool] = False,
    columns: Optional[list[str]] = [],
) -> list[str]:
    """
    Find all the columns in the sql query
    Args:
        tokens (tuple[sqlparse.sql.Statement | Any, ...]) -> parsed sql query
        is_possible_column (Optional[bool]) -> passed if column or identifier is possibly a column
        columns (Optional[list[str]]) -> where we store the list of columns
    Returns:
        list of columns available in the sql query
    """
    for token in tokens:
        if isinstance(token, sqlparse.sql.Statement):
            find_columns(token.tokens, is_possible_column, columns)
        elif isinstance(token, sqlparse.sql.Identifier):
            name = token.get_real_name()
            if is_possible_column:
                columns.append(name)
        elif isinstance(token, sqlparse.sql.Where):
            find_columns(token.tokens, is_possible_column, columns)
        elif isinstance(token, sqlparse.sql.Comparison):
            find_columns(token.tokens, is_possible_column, columns)
        elif isinstance(token, sqlparse.sql.Function):
            find_columns(token.tokens, is_possible_column, columns)
        elif isinstance(token, sqlparse.sql.Parenthesis):
            find_columns(token.tokens, True, columns)
        elif isinstance(token, sqlparse.sql.Having):
            find_columns(token.tokens, is_possible_column, columns)
        elif isinstance(token, sqlparse.sql.IdentifierList):
            find_columns(token.tokens, is_possible_column, columns)
        elif isinstance(token, sqlparse.sql.Token) and token.is_keyword:
            if token.normalized in [
                "INNER JOIN",
                "JOIN",
                "FROM",
                "CREATE",
                "TABLE",
                "INSERT",
                "INTO",
            ]:
                is_possible_column = False
            else:
                is_possible_column = True
        elif isinstance(token, sqlparse.sql.Token) and token.is_whitespace:
            continue
    return columns


def hashed_columns(
    tokens: tuple[sqlparse.sql.Statement | Any, ...], columns: list[str]
) -> str:
    """
    Convert all columns in sql query in hash sha256 value
    Args:
        tokens (tuple[sqlparse.sql.Statement | Any, ...]) -> parsed sql query
        columns [list[str] -> columns to check
    Returns:
        return sql query where all the columns are hashed in sha256
    """
    result = ""
    for token in tokens:
        if isinstance(token, sqlparse.sql.Token):
            if token.value in columns:
                sha256 = hashlib.sha256()
                sha256.update(token.value.encode("utf-8"))
                hashed_string = sha256.hexdigest()
                result += hashed_string
            else:
                result += token.value
    return result
