from flask import Flask, json, request, jsonify, make_response
from werkzeug.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid #  universal unique identifiers to generate random id numbers for users.
import jwt
import datetime
from functools import wraps

app  = Flask(__name__) 

languages =  [{'name' : 'JavaScript'}, {'name' : 'Python'}, {'name' : 'Ruby'}]

@app.route('/', methods=['GET'])
def test():
    return jsonify({'message' : 'It Works'})

@app.route('/getalllang', methods=['GET'])
def returnAll():
    return jsonify({'languages' : languages}) 


@app.route('/langbyname/<string:name>', methods=['GET'])
def returnOne(name):
    langs = [language for language in languages if language['name'] == name]
    return jsonify({'language' : langs})

@app.route('/addlang', methods=['POST'])
def addOne():
    language = {'name' : request.json['name']}
    languages.append(language)
    return jsonify({'languages' : languages})

# to edit languages
@app.route('/editlang/<string:name>', methods=['PUT'])
def editOne(name):
    langs = [language for language in languages if language['name'] == name]
    langs[0]['name'] = request.json['name']
    return jsonify({'language' : langs[0]}) 

@app.route('/deletelang/<string:name>',methods=['DELETE'])
def removeOne(name):
    lang = [language for language in languages if language['name'] == name]
    languages.remove(lang[0])
    return jsonify({'language' : languages}) 



if __name__ == '__main__':
    app.run(debug=True, port=8080)


