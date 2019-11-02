import os
import base64
from pathlib import Path
import uuid
import pickle
import json

cache_path = 'cache/'


class ProxyManager(object):
    def __init__(self):
        self.init_settings()

    def init_settings(self):
        self.proxy_admins = []
        self.proxy_admins.append({'username': 'admin',
                                  'password': 'pass'})
        self.proxy_man = []
        self.proxy_man.append({'username': 'man',
                               'password': 'pass'})
        self.adminsites = []
        self.blocked = []
        self.cached = []
# admin

    def addadmin(self, user, passw):
        self.proxy_admins.append({'username': user,
                                  'password': passw})

    def isadmin(self, user, passw):
        for item in self.proxy_admins:
            if item['username'] == user:
                if item['password'] == passw:
                    return True
        return False

    def getadmins(self):
        return self.proxy_admins

# manager
    def addman(self, user, passw):
        self.proxy_man.append({'username': user,
                               'password': passw})

    def isman(self, user, passw):
        for item in self.proxy_man:
            if item['username'] == user:
                if item['password'] == passw:
                    return True
        return False

    def getmans(self):
        return self.proxy_man

# adminsites
    def addadminsite(self, url):
        self.adminsites.append('url')

    def isadminsite(self, url):
        if url in self.adminsites:
            return True
        return False

    def getadminsites(self):
        return self.adminsites

# blocked
    def addblocked(self, url):
        self.blocked.append(url)

    def isblocked(self, url):
        if url in self.blocked:
            return True
        return False

    def getblocked(self):
        return self.blocked

# cache
    def cache(self, request, data):
        try:
            url = request['url']
            file_name = str(uuid.uuid4())
            file = open(cache_path + file_name, "w+")
            file.write(data)
            file.close
            self.cached.append({'url': url,
                                'filename': file_name})
        except IOError:
            print('Error caching file')

    def iscached(self, url):
        for item in self.cached:
            if item['url'] == url:
                return True
        return False

    def getcached(self):
        return self.cached

    def getcacheddata(self, url):
        if self.iscached(url):
            file_name = self.getfilename(url)
            if file_name in os.listdir(cache_path):
                return self.getfile(file_name)
        return {'text': "NOT CACHED"}

    def getfile(self, file_name):
        filedata = ""
        file = open(cache_path+file_name, "r")
        line = file.readline()
        while line:
            filedata += line
            line = file.readline()
            return filedata

    def getfilename(self, url):
        for item in self.cached:
            if item['url'] == url:
                return item['filename']
        return False

    def clearcache(self):
        for item in self.cached:
            os.remove(item['filename'])
        self.cached = []
