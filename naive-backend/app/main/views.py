#codeing:utf-8
from flask import Flask, request, jsonify
from app.modles import User, db_session
import hashlib
import time

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello_world'

@app.route('/login', methods=['POST'])
def login():
    phone_number = request.get_json().get('phone_number')
    password = request.get_json().get('password')
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({'code': 0, 'message': 'this user doesnt exist'})
    if user.password != password:
        return jsonify({'code': 0, 'message': 'password error'})

    m = hashlib.md5()
