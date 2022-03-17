import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(5)
        self.connections = {}
        new_connections_thread = threading.Thread(target=self.new_connections)
        new_connections_thread.start()

    def new_connections(self):
        while True:
            sock, address = self.socket.accept()
            name = self.get_name(sock)
            self.connections[name] = sock
            print('New connection from ' + name)
            recv_thread = threading.Thread(target=self.recv_msg, args=(name,))
            recv_thread.start()

    def get_name(self, sock):
        msg = ''
        while True:
            try:
                msg += sock.recv(1024).decode('utf8')
                if '#' in msg:
                    return msg[0: len(msg) - 1]
            except:
                pass

    def recv_msg(self, sender):
        msg = ''
        sock = self.connections[sender]
        while True:
            try:
                msg += sock.recv(1024).decode('utf8')
                if '#' in msg:
                    msg, msg_remain = msg.split('#', 1)
                    send_to, msg = msg.split('%', 1)
                    self.send_msg(msg, sender, send_to)
                    msg = msg_remain
            except:
                print(sender + ' have been disconnected from the server')
                break

    def send_msg(self, msg, sender, send_to):
        sock = self.connections[send_to]
        sock.sendall((sender + '%' + msg + '#').encode('utf8'))


server = Server('localhost', 10000)
