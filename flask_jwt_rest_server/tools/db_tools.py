import jwt
from flask import  g
from tools.logging import logger
from db_con import get_db_instance, get_db
import bcrypt

global_db_con = get_db()

def insertIntoPurchases(username, bookTitle, clientDate):
    cur = global_db_con.cursor()
    submission = "insert into purchases(username, title, date) values( '"
    submission+= username
    submission+= "','"
    submission+= bookTitle
    submission+= "','"
    submission+= clientDate
    submission+= "');"
    print(submission)
    cur.execute(submission)
    global_db_con.commit()

def requestBookInfo(colName):
    cur = global_db_con.cursor()
    reqString = "select "
    reqString += colName
    reqString += " from books;"
    cur.execute(reqString)
    reqJson = cur.fetchall()
    return reqJson

def addNewUser(username, password):
    salted = bcrypt.hashpw( bytes(password,  'utf-8' ) , bcrypt.gensalt(10))
    submission = "insert into users(username, password) values( '"
    submission+= str(username)
    submission+= "','" 
    submission+= str(salted.decode('utf-8'))
    submission+= "');"
    cur = global_db_con.cursor()
    cur.execute(submission)
    global_db_con.commit()

def checkPassword(username, password):
    if checkUserExists(username) == False:
        return False;
    cur = global_db_con.cursor()
    userNameStr = "select password from users where username='"
    userNameStr+= username
    userNameStr+= "';"
    cur.execute(userNameStr)
    print(userNameStr)
    print(password)
    r = cur.fetchone()
    userPass = str(r[0])
    if bcrypt.checkpw(  bytes(password,  'utf-8' ) , userPass.encode('utf-8')):
            return True
    return False

def checkUserExists(username):
    cur = global_db_con.cursor()
    
    dbUser = "select exists (select username from users where username = '"
    dbUser+= username
    dbUser+= "' limit 1);"
    cur.execute(dbUser)
    r = cur.fetchone()
    print(r[0])
    if r[0] == True:
       return True
    return False
