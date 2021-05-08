import mysql.connector  # todo: uncomment
from flask import jsonify, request

import os
import flask
import json

app = flask.Flask(__name__)

# todo: move config to config.py + core

assert True in [x in os.listdir() for x in ["administrators.json", "config.json"]], \
    "Please make sure the required config files are present in the same directory as the executable. "
# todo: back to false

config = json.loads(open("config.json", "r").read())

dbconfig = config["DATABASE"]  # todo: with
mydb = mysql.connector.connect(host=dbconfig["HOST"], user=dbconfig["USER"], password=dbconfig["PASSWORD"],
                               database=dbconfig["DATABASE"])

permissions = json.loads(open("administrators.json", "r").read())


def has_permissions(h_token, lvl):
    return True in [h_token == x["check"] for x in permissions.values() if x["level"] >= lvl]


@app.route('/', methods=['GET'])  # todo: better decorator (perm req, )
def home():
    auth = request.args.get("auth")

    if has_permissions(h_token=auth, lvl=1) is False:
        return forbidden(403)

    return "OK"  # todo: online socket check / whois / perms


@app.route('/accounts', methods=['GET'])
def get_accounts():
    query = request.args

    auth = query.get("auth")
    
    if has_permissions(h_token=auth, lvl=2) is False:
        return forbidden(403)

    mycursor = mydb.cursor()
    mycursor.execute("SELECT data FROM accounts")

    myresult = mycursor.fetchall()
    accountData = "{"

    for account in myresult:
        accountData += account[0]
        accountData += ","

    accountData = accountData[:-1]
    accountData += "}"

    return accountData


@app.route('/sendaccounts', methods=['POST', 'GET'])
def send_accounts():
    query = request.args
    auth = query.get("auth")
    if has_permissions(h_token=auth, lvl=3) is False:
        return forbidden(403)

    if 'data' in request.args:
    
        data = query.get("data")
        newAccount = jsonify(data)

        mycursor = mydb.cursor()
        mycursor.execute(f"INSERT INTO `accounts`(`data`) VALUES ('{newAccount}')")

        return "<h1>204 Complete no content</h1><p>There is no content to be shown</p>"
    
    else:
        return badrequest(401)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 Not Found</h1><p>The resource could not be found.</p>", 404
@app.errorhandler(403)
def forbidden(e):
    return "<h1>403 Forbidden</h1><p>Incorrect access token</p>", 403
@app.errorhandler(401)
def badrequest(e):
    return "<h1>401 Bad Request</h1><p>Check URL</p>", 401


app.run()