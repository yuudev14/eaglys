from fastapi import APIRouter
import sqlparse

from src.dto.request import SQL_Payload
from src import utils


parser_route = APIRouter()


@parser_route.post("/columns/hashed")
async def parse_query(sql_payload: SQL_Payload):
    """
    api that returns the modified sql where all columns are hashed in sha256
    Args:
        sql_payload (SQL_Payload) -> payload of the request.
    Returns:
        sql query where all the columns are hashed in sha256
    """
    parsed = sqlparse.parse(sql_payload.sql)
    columns = utils.helpers.find_columns(parsed)
    sql_hashed_columns = utils.helpers.hashed_columns(parsed[0], columns)

    return {"result": sql_hashed_columns}


@parser_route.post("/columns/mapped")
async def parse_query(sql_payload: SQL_Payload):
    """
    api that returns the key value pair of the original column and the hashed column
    Args:
        sql_payload (SQL_Payload) -> payload of the request.
    Returns:
        sql query where all the columns are hashed in sha256
    """
    parsed = sqlparse.parse(sql_payload.sql)
    columns = utils.helpers.find_columns(parsed)
    mapped_columns = utils.helpers.mapped_hashed_columns(columns)

    return {"result": mapped_columns}
