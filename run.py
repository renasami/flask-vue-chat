# -*- coding: utf-8 -*-
import ast
import hashlib
import json
import socket
import time
import ssl
import eventlet
from random import *
from threading import Lock

from gevent import *
from flask import Flask, Response, jsonify, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
# from flask_sockets import Sockets
from gevent.pywsgi import WSGIServer
#from geventwebsocket.handler import WebSocketHandler
from werkzeug.exceptions import abort

from backend.venv import db
from backend.venv.models import Talk, User

#FLASK_APP=run.py FLASK_DEBUG=1 flask run
async_mode = None

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist"
            )
sio = SocketIO(app)
print(sio)

@app.route('/api/random')
def random_number():
    print("rand")
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/chat_api/')
def get_chat():
    talks = db.session.query(Talk).all()
    db.session.close()
    res = dict()
    for i in range(len(talks)):
        res[i] = str(talks[i])
    return res

@app.route('/send_chat/',methods=['POST'])
def send_chat():
    n = request.data
    s = n.decode()
    talDic = ast.literal_eval(s)
    addTal = Talk(
        user_id = talDic["user_id"],
        content = talDic["message"],
    )
    db.session.add(addTal)
    db.session.commit()
    db.session.close() 
    return "succsess"

@app.route('/user_api/',methods=['POST'])
def get_user():
    user = db.session.query(User).all()
    db.session.close()
    res = dict()
    n = request.data
    s = n.decode()
    dic = ast.literal_eval(s)
    has = dic["pas"]
    pasHas = hashlib.md5(has.encode()).hexdigest()
    print(dic)
    for i in range(len(user)):
        res[i] = str(user[i])
        if str(dic["name"]) == user[i].username:
            # print(user[i])
            # print(dic["pas"])
            # print(pasHas)
            # print(user[i].password)
            print(user[i])
            if pasHas == user[i].password:
                return str(user[i])
            elif pasHas != user[i].password:
                return "username or password is wrong"
    return "username or password is not wrong"


@sio.on('message', namespace="/test")
def connect(message):
    print("message:"+message)
    emit('message', message,broadcast=True)


ipAddr = socket.gethostbyname(socket.gethostname())
@sio.on('ip', namespace="/ip")
def ip(ip):
    print(ip)
    emit('ip', ipAddr,broadcast=True)




if __name__ == '__main__':
    #app.run(debug=True, host='localhost', port=5000)
    sio.run(app,port=5000, debug=True)
    