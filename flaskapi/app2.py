
from flask import Flask, request, jsonify,  make_response
from flask_sqlalchemy import SQLAlchemy 
import os 
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


app = Flask(__name__)


app.config['SECRET_KEY'] = "thisissecret"
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'socialapp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    token = db.Column(db.String(100))
    user_id = db.Column(db.String(50))

# class User1(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     password = db.Column(db.String(50))
#     token = db.Column(db.String(100))
#     user_id = db.Column(db.String(50))

@app.route('/signup', methods=['POST'])
def signUpuser():
    data = request.get_json()
    user_id = str(uuid.uuid4())
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token valid for 1 hour
    token = jwt.encode({'user_id': user_id}, app.config['SECRET_KEY'], algorithm='HS256')

    userData = User(name=data['name'],password=data['password'],token=token,user_id = user_id )
    user = {
        'user_id':user_id,
    'name': data['name'],
    'password': data['password'],
    'token': token.decode('utf-8')
    }
    db.session.add(userData)
    db.session.commit()

    return jsonify({"message" : "you've successfully created your account", "data" : {
        "user" : user  
    }})
if __name__ == '__main__':
    app.run(debug=True, port=8080)    


    