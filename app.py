#!/env/python
#coding:utf-8

from flask import Flask, jsonify
from flask_socketio import SocketIO
import eventlet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

from MyCustomNamespace import MyNamespace
socketio.on_namespace(MyNamespace('/buyGrab', socketio))

@app.route("/")
def homepage():
    print('homepage')
    return jsonify({'code': 403, 'message': 'unauthorized', 'data': {}})

if __name__ == '__main__':
    socketio.run(app, debug=True)
    print('Server started on port 5000')


"""
https://flask-socketio.readthedocs.io/en/latest/
http://localhost/localhost/app.html
"""    