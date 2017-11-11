# Kormákur Atli Unnþórsson
# 31.10.2017
# Skilaverkefni 10

from bottle import *
import sanitize
import pymysql
import os

#static files route
@route("/static/<filename>")
def staticFile(filename):
    return static_file(filename, root="./static/")

@get("/")
def index():
    return template("index.tpl")

@get("/nyskraning")
def nyskraningarsida():
    return  template("nyskraning.tpl")

@post("/")
def nyskraning():
    connection = pymysql.connect(host='tsuts.tskoli.is',
                             port=3306,
                             user='1604002850',
                             passwd='mypassword',
                             db='1604002850_vef2verk10')

    username = sanitize(request.forms.get("username"))
    password = sanitize(request.forms.get("password"))
    passconf = sanitize(request.forms.get("passconf"))
    
    with connection.cursor() as cursor:
        sql = "SELECT user, pass FROM user WHERE user = '"+username+"'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            uttak = "Notandi er nú þegar til"
        else:
            sql = "INSERT INTO user (user, pass) VALUES ('"+username+"', '"+password+"')"
            cursor.execute(sql)
            connection.commit()
            uttak = "Notandi hefur verið stofnaður!"
    connection.close()
    return template("indexAfterSignup.tpl",uttak=uttak)

@post("/innskraning")
def nyskraning():
    connection = pymysql.connect(host='tsuts.tskoli.is',
                             port=3306,
                             user='1604002850',
                             passwd='mypassword',
                             db='1604002850_vef2verk10')
    username = sanitize(request.forms.get("username"))
    password = str(sanitize(request.forms.get("password")))
    with connection.cursor() as cursor:
        sql = "SELECT pass FROM user WHERE user = '"+username+"'"            
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            print(result[0])
            print(password)
            if str(result[0]) == str(password):
                response.set_cookie("account",username, secret=password)
                return template("leynisida.tpl",username=username)
            else:
                uttak = "Rangt lykilorð"
        else:
            uttak = "Notandinn er ekki til"
    connection.close()                
    if uttak == "Rangt lykilorð":
        return template("indexAfterSignup.tpl",uttak=uttak)
    elif uttak == "Notandinn er ekki til":
        return template("indexAfterSignup.tpl",uttak=uttak)

@route("/utskra")
def utskraning():
    response.set_cookie("account","", expires=0)
    return template("index.tpl")
    

run(host='0.0.0.0', port=os.environ.get('PORT'))
