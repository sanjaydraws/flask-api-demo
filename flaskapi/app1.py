from flask import Flask, jsonify, request, make_response 
import jwt 
import datetime 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this is secret key'

@app.route('/unprotected')
def unprotected():
    return ''

@app.route('/protected')
def protected():
    return ''

@app.route('/login')
def login():
    auth = request.authorization 
    if auth and  auth.password == 'password':
        print("jee")
        #if password correct
        token = jwt.encode({'user' : auth.username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return jsonify({'token' :token.decode('UTF-8')})
    return make_response("could not verify !", 401, {'WWW-Authenticate' : 'BAsic realm= "Login Required'})


if __name__ == '__main__':
    app.run(debug=True)

