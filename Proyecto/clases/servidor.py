import socket
import threading
import socketserver
from pathlib import Path
import os, sys, binascii
from datetime import datetime

global PORT

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("hola 1")
        data = self.request[0].strip()
        socket = self.request[1]

        value2 = 0xA0
        packed_data_2 = bytearray()
        packed_data_2 += value2.to_bytes(1, "big")
        socket.sendto(packed_data_2, self.client_address)
        print("--2--")


if name == "main":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()