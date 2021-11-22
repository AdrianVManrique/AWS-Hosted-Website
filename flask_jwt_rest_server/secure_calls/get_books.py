from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.db_tools import requestBookInfo
from tools.logging import logger

def handle_request():
    logger.debug("Get Books Handle Request")

    #request a column from the books table
    book_responseNames = requestBookInfo("name")
    book_responsePrice = requestBookInfo("price")

    return json_response( token = create_token(  g.jwt_data ) , bookNames = book_responseNames, bookPrice = book_responsePrice)

