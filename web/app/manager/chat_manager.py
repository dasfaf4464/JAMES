'''
from flask_socketio import SocketIO, Namespace
from run import socketio

class ChatManager(Namespace):
    socket = None
    
    def __init__(self):
        self.socket = socketio
    
    def on_connect(self):
        return 
'''