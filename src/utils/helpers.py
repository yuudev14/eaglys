from typing import Any, Optional
import hashlib
import sqlparse


def traverse_tokens(
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
            traverse_tokens(token.tokens, is_possible_column, columns)
        elif isinstance(token, sqlparse.sql.Identifier):
            name = token.get_real_name()
            if is_possible_column:
                columns.append(name)
        elif isinstance(token, sqlparse.sql.Where):
            traverse_tokens(token.tokens, is_possible_column, columns)
        elif isinstance(token, sqlparse.sql.Comparison):
            traverse_tokens(token.tokens, is_possible_column, columns)
        elif isinstance(token, sqlparse.sql.Function):
            traverse_tokens(token.tokens, is_possible_column, columns)
        elif isinstance(token, sqlparse.sql.Parenthesis):
            traverse_tokens(token.tokens, True, columns)
        elif isinstance(token, sqlparse.sql.Having):
            traverse_tokens(token.tokens, is_possible_column, columns)
        elif isinstance(token, sqlparse.sql.IdentifierList):
            traverse_tokens(token.tokens, is_possible_column, columns)
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


def unparse(
    tokens: tuple[sqlparse.sql.Statement | Any, ...], columns: list[str]
) -> str:
    """
    Convert all columns in sql query in hash value
    Args:
        tokens (tuple[sqlparse.sql.Statement | Any, ...]) -> parsed sql query
        columns [list[str] -> columns to check
    Returns:
        return sql query where all the columns are hashed
    """
    result = ""
    for token in tokens:
        if isinstance(token, sqlparse.sql.Token):
            if token.value in columns:
                input_string = "Hello, World!"
                sha256 = hashlib.sha256()
                sha256.update(input_string.encode("utf-8"))
                hashed_string = sha256.hexdigest()
                result += hashed_string
            else:
                result += token.value
    return result
