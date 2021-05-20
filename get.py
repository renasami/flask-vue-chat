from random import *

from flask import Flask, jsonify, render_template

from backend.venv import db
from backend.venv.models import Talk, User

import json

user = db.session.query(User).all() 
talks = db.session.query(Talk).all()
db.session.close()
dic = dict()
s = ""
for n in range(len(talks)):
    s += json.dumps(str(talks[n])) + "\n"

print(s)
    
