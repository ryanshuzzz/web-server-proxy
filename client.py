import socket
import sys
import pickle
HOST = 'localhost'
PORT = 12000


class Client(object):
    def __init__(self, *args, **kwargs):
        self.HOST = HOST
        self.PORT = PORT
        # self.init_socket()

    def init_socket(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket Created")
            self.connect(self.HOST, self.PORT)
        except socket.error as error:
            print(error)

    def connect(self, HOST, PORT):
        try:
            self.client.connect(HOST, PORT)
            print("Connected to " + HOST + ":" + PORT)
        except socket.error as error:
            print(error)
    
    def handlerequest(self, data):
        send(data)

    def send(self, data):
        serialize = pickle.dumps(data)
        self.client.send(serialize)
    
    def recieve(self):
        BUFFER = 4096
        recieve = self.client.recv(BUFFER)
        deserialize = pickle.loads(recieve)
        return recieve

    def getadmindata(self):
        data = {'mode': 'admindata'}
        self.send(data)
        return self.recieve()

    def addadmin(self, name, passw):
        data = {'mode': 'addadmin',
                'username': name,
                'password': passw}
        self.send(data)

    def addblocked(self, url):
        data = {'mode': 'addblocked',
                'url': url}
        self.send(data)

    def addadminsite(self, url):
        data = {'mode': 'addadminsite',
                'url': url}
        self.send(data)

    def addmanager(self, username, password):
        data = {'mode': 'addmanager',
                'username': username,
                'password': password,
                }
        self.send(data)

    def clear_cache(self):
        data = {'mode': 'clear_cache'}
        self.send(data)
    
