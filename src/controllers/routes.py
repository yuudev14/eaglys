from fastapi import APIRouter
from src.controllers.parsers_controller import parser_route

api = APIRouter()


api.include_router(router=parser_route, prefix="/parse")
