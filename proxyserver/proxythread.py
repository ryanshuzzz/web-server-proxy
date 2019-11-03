import requests
from proxymanager import ProxyManager
import pickle
import threading
import urllib3
import contextlib

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

                if process is not None:
                    send_data = process
                    self._send(send_data)
                lock.release()
            except EOFError:
                print('no data recieved')
                break

    def _send(self, data):
        serialize = pickle.dumps(data)
        self.client.send(serialize)

    def processrequest(self, request):
        lock.acquire()
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
            url = request['url']
            self.proxy_manager.adminsites.append(url)

        elif request['mode'] == 'isadminsite':
            url = request['url']
            if url in self.proxy_manager.adminsites:
                return True
            else:
                return False

        elif request['mode'] == 'addmanager':
            user = request['username']
            passw = request['password']
            if user is not None and passw is not None:
                self.proxy_manager.proxy_man.append(
                    {'username': user, 'password': passw})

        elif request['mode'] == 'isman':
            user = request['username']
            passw = request['password']
            if user is not None and passw is not None:
                return {'isman': self.proxy_manager.isman(user, passw)}

        elif request['mode'] == 'clear_cache':
            self.proxy_manager.clearcache()

        elif request['mode'] == 'geturl':
            return self.handlerequests(request)

    def getadmindata(self):
        admindata = {'admins': self.proxy_manager.proxy_admins,
                     'managers': self.proxy_manager.proxy_man,
                     'cached': self.proxy_manager.cached,
                     'adminsites': self.proxy_manager.adminsites,
                     'blocked': self.proxy_manager.blocked}
        return admindata

    def handlerequests(self, request):
        print(request)
        url = request['url']
        private = request['private']
        if private:
            return self.handleprivaterequest(url)
        if self.proxy_manager.iscached(url):
            data = self.proxy_manager.getcacheddata(url)
            print(data)
            if self.checkhead(url, data.headers):
                returndata = {
                    'headers': data.headers,
                    'text': data.text
                }
                return returndata
        req = requests.get("http://" + url)
        data = {
            'headers': req.headers,
            'text': req.text
        }
        self.proxy_manager.cache(request, req)
        return data

    def handleprivaterequest(self, url):
        data = requests.get("http://" + url)
        return {
                'headers': data.headers,
                'text': data.text
            }

    def checkhead(self, url, head):
        with requests.get(
                "http://" + url,
                headers={"If-Modified-Since": head.get('date')}) as r:
            if r.status_code == 304:
                return True
            else:
                return False
        return False
