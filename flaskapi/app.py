from flask import Flask, json, request, jsonify, make_response
from werkzeug.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid #  universal unique identifiers to generate random id numbers for users.
import jwt
import datetime
from functools import wraps
import os


app  = Flask(__name__) 

languages =  [{'name' : 'JavaScript'}, {'name' : 'Python'}, {'name' : 'Ruby'}]


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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





def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-image', methods=['POST'])
def upload_image():
    try:
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']

        # Check if a file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if the file has an allowed extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file extension'}), 400

        # Save the file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        
        return jsonify({'message': 'File uploaded successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8080)


