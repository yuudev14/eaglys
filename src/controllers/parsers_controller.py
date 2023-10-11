from fastapi import APIRouter
import sqlparse

from src.dto.request import SQL_Payload
from src import utils


parser_route = APIRouter()


@parser_route.post("/columns/hashed")
async def parse_query(sql_payload: SQL_Payload):
    parsed = sqlparse.parse(sql_payload.sql)
    columns = utils.helpers.find_columns(parsed)
    sql_hashed_columns = utils.helpers.hashed_columns(parsed[0], columns)

    return {"result": sql_hashed_columns}
