from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.db_tools import insertIntoPurchases
from tools.logging import logger

def handle_request():
    logger.debug("Purchase Book Handle Request")
    insertIntoPurchases(request.form['curUserName'], request.form['bookTitle'], request.form['clientDate'])
    return json_response( token = create_token(  g.jwt_data ) , books = {})
