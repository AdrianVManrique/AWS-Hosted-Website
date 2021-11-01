from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import datetime
import bcrypt


from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = None

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    print(request.form)
    salted = bcrypt.hashpw( bytes(request.form['fname'],  'utf-8' ) , bcrypt.gensalt(10))
    print(salted)

    print(  bcrypt.checkpw(  bytes(request.form['fname'],  'utf-8' )  , salted ))

    return render_template('backatu.html',input_from_browser= str(request.form) )

@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)

#Assignment3
@app.route('/authUser',  methods=['POST']) #endpoint
def authUser():
    print(request.form)
    print("------------")
    jwt_str = jwt.encode({"username": request.form['userName']}, JWT_SECRET, algorithm='HS256')
    checkUser = checkToken(jwt_str)
    if checkUser == False:
        return json_response(status='401', msg='User does not exist')
    cur = global_db_con.cursor()
    userNameStr = "select password from users where username='"
    userNameStr+= request.form['userName']
    userNameStr+= "';"
    cur.execute(userNameStr)
    r = cur.fetchone()
    #print(r[0])
    userPass = str(r[0])
    if bcrypt.checkpw(  bytes(request.form['pWord'],  'utf-8' ) , userPass.encode('utf-8')):
            print("-------------------")
            print(jwt_str)
            return json_response(jwt=jwt_str)
    print("INVALID")
    return json_response(status='401', msg='Invalid Password')

        
@app.route('/addUser',  methods=['POST']) #endpoint
def addUser():
    print(request.form)
    tempUser = request.form['nName']
    tempPass = request.form['newWord']
    salted = bcrypt.hashpw( bytes(request.form['newWord'],  'utf-8' ) , bcrypt.gensalt(10))
    print(tempUser)
    #print(salted.decode('utf-8'))
    submission = "insert into users(username, password) values( '"
    submission+= str(tempUser)
    submission+= "','" 
    submission+= str(salted.decode('utf-8'))
    submission+= "');"
    print(submission) 
    #Hash the password then add to database
    cur = global_db_con.cursor()
    cur.execute(submission)
    #cur.execute("insert into users(username, password) values ('Rose', 'Megapassword');")
    global_db_con.commit()

    jwt_str = jwt.encode({"username": request.form['nName']}, JWT_SECRET, algorithm='HS256')


    return json_response(jwt=jwt_str)

@app.route('/getBooks',  methods=['GET']) #endpoint
def getBooks():
    print("Veryifying JWT")
    authHeader = request.headers.get('Authorization')
    #print(authHeader)
    tokenVal = checkToken(authHeader)
    #Check Token
    #print("++++++++")
    #print(decoded.get('username'))
    #print("++++++++")
    #tokenVal = checkToken('Tiffany')
    if tokenVal == False:
        return json_response(status='404', msg='Invalid JWT Token')

    print("VALID JWT +++++")
    cur = global_db_con.cursor()
    book_requestNames = "select name from books;"
    cur.execute(book_requestNames)
    book_responseNames = cur.fetchall()
    print(book_responseNames)

    book_requestPrice = "select price from books;"
    cur.execute(book_requestPrice)
    book_responsePrice = cur.fetchall()
    print(book_responsePrice)
    
    return json_response(jwt=authHeader, bookNames=book_responseNames, bookPrice=book_responsePrice)

@app.route('/buyBook',  methods=['POST']) #endpoint
def buyBook():
    print("IM BUYING A BOOK")
    print(request.form)
    purchaseInfo = request.form
    \
    authHeader = request.headers.get('Authorization')
    purchaseUser = decodeToken(authHeader)
    print(purchaseUser)

    submission = "insert into purchases(username, title, date) values( '"
    submission+= purchaseUser
    submission+= "','"
    submission+= request.form['bookTitle']
    submission+= "','"
    submission+= request.form['clientDate']
    submission+= "');"
    print(submission)
    cur = global_db_con.cursor()
    cur.execute(submission)
    global_db_con.commit()
    return json_response(status='good')

def decodeToken(authToken):
    decoded = jwt.decode(authToken, JWT_SECRET, algorithms=["HS256"])
    tokenString = decoded.get('username')
    return tokenString

def checkToken(authToken):
    print(authToken)
    tokenString = decodeToken(authToken)
    cur = global_db_con.cursor()
    
    dbUser = "select exists (select username from users where username = '"
    #dbUser+= 'Tiffany'
    dbUser+= tokenString
    dbUser+= "' limit 1);"
    cur.execute(dbUser)
    r = cur.fetchone()
    print(r[0])
    if r[0] == True:
       return True
    return False
    #Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )

@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] } 
                            , JWT_SECRET, algorithm="HS256")
    #print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    global_db_con.commit()
    return json_response(status="good")


app.run(host='0.0.0.0', port=80)







