import socket
import sys
import pickle
import time
HOST = 'localhost'
PORT = 12000


class Client(object):
    def __init__(self, *args, **kwargs):
        self.HOST = HOST
        self.PORT = PORT
        self.init_socket()

    def init_socket(self):
        # try:
        self.newclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket Created")
        self.connect(self.HOST, self.PORT)
        # except socket.error as error:
        #     print(error)
        #     self.newclient.close

    def connect(self, HOST, PORT):
        # try:
        self.newclient.connect((HOST, PORT))
        print("Connected to " + HOST + ":" + str(PORT))
        # except socket.error as error:
        #     print(error)

    def handlerequest(self, data):
        self.send(data)
        return self._recieve()

    def send(self, data):
        serialize = pickle.dumps(data)
        print(serialize)
        self.newclient.send(serialize)

    def _recieve(self):
        buff = 1024
        data = b""
        while True:
            recieve_info = self.newclient.recv(buff)
            
            data += recieve_info
            if len(recieve_info) < buff:
                break

        return pickle.loads(data)

    def getadmindata(self):
        data = {'mode': 'admindata'}
        self.send(data)
        return self._recieve()

    def addadmin(self, name, passw):
        data = {'mode': 'addadmin',
                'username': name,
                'password': passw}
        self.send(data)

    def isadmin(self, name, passw):
        data = {'mode': 'isadmin',
                'username': name,
                'password': passw}
        self.send(data)
        recieve = self._recieve()
        return recieve['isadmin']

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

    def isman(self, username, password):
        data = {'mode': 'isman',
                'username': username,
                'password': password,
                }
        self.send(data)
        recieve = self._recieve()
        return recieve['isman']

    def clear_cache(self):
        data = {'mode': 'clear_cache'}
        self.send(data)
