import os
import sys
import threading
import socket
from proxythread import ProxyThread

HOST = 'localhost'
PORT = 12000
MAX_DATA_RECV = 4096
MAX_NUM_CONNECTIONS = 5


class ProxyServer(object):

    def __init__(self):
        self.clients = []

    def run(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((HOST, PORT))
            self.server.listen(MAX_NUM_CONNECTIONS)
            while True:
                client_sock, client_id = self.accept_clients()
                print("Client " + str(client_id) + " has made a request")
                new_thread = threading.Thread(target=ProxyThread,
                                              args=(client_sock, client_id))
                new_thread.start()
        except socket.error as message:
            print(message)
        except KeyboardInterrupt:
            print("\nExiting...")
            self.server.close()
            sys.exit(0)

    def accept_clients(self):
        client_sock, client_addr = self.server.accept()
        client_id = client_addr[1]
        return client_sock, client_id

    def proxy_thread(self, conn, client_addr):
        proxy_thread = ProxyThread(conn, client_addr)
        proxy_thread.init_thread()


server = ProxyServer()
server.run()
