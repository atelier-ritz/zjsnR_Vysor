import socket
import threading
import time

class Server(object):
    def __init__(self,host='192.168.0.172',port=9997):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.sock.bind((host, port))
        self.sock.listen(1) # backlog: specifies the maximum number of queued connections
        self.client = [] # [con, address]

    def start(self):
        print('Host: {}, Port: {}'.format(self.host, self.port))
        print('Waiting for client connection ...')
        con, address = self.sock.accept()
        print("[Connected] {}".format(address))
        self.client = [con, address]
        handle_thread = threading.Thread(target=self._handler, args=(con, address), daemon=True)
        handle_thread.start()

    def remove_conection(self,con,address):
        print('[Terminated] {}'.format(address))
        con.close()
        self.client.remove((con, address))

    def _handler(self,con,address):
        while True:
            try:
                data = con.recv(1024)
            except ConnectionResetError:
                self.remove_conection(con, address)
                break
            else:
                if not data:
                    self.remove_conection(con, address)
                    break
                else:
                    print("[Received] {} - {}".format(address, data.decode("utf-8")))
                    print('Processing ...')
                    time.sleep(3)
                    print('Done')
                    self.client[0].sendto(data, self.client[1])

# new = Server()
# new.start()
# while True:
#     time.sleep(3)
