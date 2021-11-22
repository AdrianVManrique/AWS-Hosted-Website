from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.db_tools import addNewUser
from tools.logging import logger

def handle_request():
    logger.debug("Signup Handle Request")
    password_from_user_form = request.form['newWord']
    user_from_user_form = request.form['nName']
    addNewUser(user_from_user_form, password_from_user_form)
    user = {
            "sub" : user_from_user_form #sub is used by pyJwt as the owner of the token
            }

    return json_response( token = create_token(user) , authenticated = True, username = user_from_user_form)
