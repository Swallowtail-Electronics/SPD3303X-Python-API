import socket
import time

class SCPI:
    '''
    Standard Commands for Programmable Interface server for sending commands to compatible devices
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip, port):
        '''
        Open the socket and set the default timeout
        '''
        try:
            self.s.connect((ip,port))
            self.s.settimeout(10)
        except:
            print(f"Unable to connect to {ip}:{port}. Is the IP/Port correct? ")

    def send(self, cmd):
        '''
        Send a command
        '''
        cmd = cmd.encode('utf-8')
        self.s.sendall(cmd)
        self.s.sendall(b"\n")

    def recv(self):
        '''
        Listen on the socket for a reply
        '''
        response = self.s.recv(2048).decode()
        return response


    def close(self):
        '''
        Close the socket
        '''
        self.s.close()
        time.sleep(1)