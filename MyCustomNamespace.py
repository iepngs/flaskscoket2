from flask import session, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect

class MyNamespace(Namespace):

    __sio = None

    def __init__(self, namespace = None, sio = None):
        Namespace.__init__(self, namespace)
        self.__sio = sio

    def __background_thread(self):
        """Example of how to send server generated events to clients."""
        self.__sio.sleep(10)
        self.__sio.emit('reply', {'data': 'Server generated event'}, namespace = self.namespace)

    # 处理系统消息请求
    def on_message(self, message):
        print(self.namespace, str(message))
        if message['data'] == 'backgroud':
                self.__sio.start_background_task(target=self.__background_thread)
                emit('reply', {'data': 'backgroud function will be trigger an event'})
                # 当前所在房间号
                # print(self.rooms(sid))
                # 当前namespace
                # print(self.namespace)
        else:
            if self.namespace == u'/buyGrab':
                try:
                    import json
                    requsetData = json.loads(message['data'])
                except:
                    pass
                else:
                    neededArgs = {
                        'uid': None,
                        'auid': None,
                        'grabid': None,
                        'num': None,
                        'sp': None,
                    }
                    for key, val in neededArgs.items():
                        val = requsetData.get(key)
                        if val is None:
                            emit('reply', {'code':400, 'message': 'Lack Of Param Or Invalid[%s]' % (key), 'data':{}})
                            return
                        neededArgs[key] = val
                    from model.UserModel import UserModel
                    import random
                    dbModel = UserModel()
                    data = dbModel.User(random.choice(range(1, 90000)))
                    message['data'] = data
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('reply',
                {'data': message['data'], 'count': session['receive_count']})

    
    # 处理广播消息请求
    def on_broadcastMsg(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('reply',
             {'data': message['data'], 'count': session['receive_count']},
             broadcast=True)

    # 处理加入房间请求
    def on_join(self, message):
        join_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('reply',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})

    # 处理离开房间请求
    def on_leave(self, message):
        leave_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('reply',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})

    # 处理解散房间请求
    def on_closeRoom(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('reply', {'data': 'Room ' + message['room'] + ' is closing.',
                             'count': session['receive_count']},
             room=message['room'])
        close_room(message['room'])

    # 处理房间消息请求
    def on_roomMsg(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('reply',
             {'data': message['data'], 'count': session['receive_count']},
             room=message['room'])

    # 监听客户端断连请求
    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('reply',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()
    
    # 处理给客户端ping请求
    def on_ping_from_client(self):
        emit('pong_from_server')

    # 监听客户端连接请求
    def on_connect(self):
        print('New client connected - {sid} '.format(sid = request.sid))
        emit('reply', {'data': 'Connected', 'count': 0})

    def on_disconnect(self):
        print('Client disconnected [ {sid} ]'.format(sid = request.sid))

