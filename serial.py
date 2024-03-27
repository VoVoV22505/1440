import serial
from socket import *
import sys

host = "testhost"
port = 886
addr = (host, port)

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.connect(addr)

ser = serial.Serial(9600)


def parse():
    get = '"GET_A", "GET_B", "GET_C"'
    ser.write(get.encode("ascii"))

    if ser.inWaiting() > 0:
        response = ser.readline()
        decoded_response = response.decode("ascii")
        print(decoded_response)
    else:
        tcp_socket.send(get.encode("ascii"))
        response = tcp_socket.recv(1024)
        decoded_response = response.decode("ascii")
        print(decoded_response)


while True:
    parse()
