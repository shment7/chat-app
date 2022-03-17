import socket
import threading
import sys

class Client:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.socket = self.connect()
        self.socket.sendall((self.name + '#').encode('utf8'))
        receiveThread = threading.Thread(target=self.recv_msg)
        receiveThread.start()
        send_thread = threading.Thread(target=self.send_msg)
        send_thread.start()

    def recv_msg(self):
        msg = ''
        while True:
            try:
                msg += self.socket.recv(1024).decode('utf-8')
                if '#' in msg:
                    msg, msg_remain = msg.split('#', 1)
                    sender, msg = msg.split('%', 1)
                    print()
                    print(sender + ': ' + msg)
                    msg = msg_remain
            except:
                print('You have been disconnected from the server')
                break

    def send_msg(self):
        while True:
            try:
                send_to, msg = input('').split('%', 1)
                self.socket.sendall((send_to + '%' + msg + '#').encode('utf8'))
            except:
                print('send message fail')
                break

    def connect(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            print('Successful connection')
        except:
            print('Could not make a connection to the server')
            input('Press enter to quit')
            sys.exit(0)

        return sock

client = Client('localhost', 10000, 'shment1')
