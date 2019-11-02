import requests
from proxymanager import ProxyManager
import pickle
import threading

lock = threading.Lock()

class ProxyThread(object):

    def __init__(self, conn, client_addr):
        print("Thread successfully created")
        self.proxy_manager = ProxyManager()
        self.client = conn
        self.client_id = client_addr
        self.init_thread()

    def init_thread(self):
        print("waiting")
        while True:
            recieve_info = self.client.recv(4096)
            try:
                deserialize = pickle.loads(recieve_info)
                process = self.processrequest(deserialize)
                lock.release()
                if process is not None:
                    send_data = process
                    self._send(send_data)
            except EOFError:
                print('no data recieved')
                break

    def _send(self, data):
        serialize = pickle.dumps(data)
        self.client.send(serialize)

    def processrequest(self, request):
        lock.acquire()
        print(request['mode'])
        if request['mode'] == 'admindata':
            return self.getadmindata()
        elif request['mode'] == 'addadmin':
            user = request['username']
            passw = request['password']
            if user is not None and passw is not None:
                self.proxy_manager.addadmin(user, passw)
        elif request['mode'] == 'isadmin':
            user = request['username']
            passw = request['password']
            if user is not None and passw is not None:
                return {'isadmin': self.proxy_manager.isadmin(user, passw)}
        elif request['mode'] == 'addblocked':
            url = request['url']
            if url is not None:
                self.proxy_manager.addblocked(url)
        elif request['mode'] == 'addadminsite':
            self.proxy_manager.addadminsite(url)
        elif request['mode'] == 'addmanager':
            user = request['username']
            passw = request['password']
            if user is not None and passw is not None:
                self.proxy_manager.proxy_man.append({'username': user, 'password': passw})
                print(self.proxy_manager.proxy_man)
        elif request['mode'] == 'isman':
            user = request['username']
            passw = request['password']
            if user is not None and passw is not None:
                return {'isman': self.proxy_manager.isman(user, passw)}
        elif request['mode'] == 'clear_cache':
            self.proxy_manager.clearcache

    def getadmindata(self):
        print(self.proxy_manager.proxy_man)
        admindata = {'admins': self.proxy_manager.proxy_admins,
                     'managers': self.proxy_manager.proxy_man,
                     'cached': self.proxy_manager.cached,
                     'adminsites': self.proxy_manager.adminsites,
                     'blocked': self.proxy_manager.blocked}
        return admindata
