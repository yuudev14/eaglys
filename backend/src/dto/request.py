from pydantic import BaseModel


class SQL_Payload(BaseModel):
    sql: str
