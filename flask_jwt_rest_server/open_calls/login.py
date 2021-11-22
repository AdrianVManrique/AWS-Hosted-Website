from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.db_tools import checkPassword
from tools.logging import logger

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user
    print("AM IN LOGGGING IN WITH: ")
    print(request.form)
    password_from_user_form = request.form['pWord']
    user_from_user_form = request.form['userName']
    if checkPassword(user_from_user_form, password_from_user_form) == True: 
        user = {
                "sub" : user_from_user_form #sub is used by pyJwt as the owner of the token
               }
    else:
        user = False
    if not user:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )

    return json_response( token = create_token(user) , authenticated = True, username = user_from_user_form)

