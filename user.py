import os
import socket
import subprocess
import time
import sys

# Creating Socket


def socket_create():
    try:
        global host
        global port
        global s
        host = '172.17.9.65'
        port = 9001
        s = socket.socket()
    except socket.error() as msg:
        print('Socket Creation Error: ' + str(msg))


# Connecting to a remote socket


def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
        msg = 'user'
        s.send(str.encode(msg))
    except socket.error() as msg:
        print('Error Connecting Socket: ' + str(msg))
        socket_connect()


# def send_string():
#     conn, address = s.accept()
#     received = str(conn.recv(1024),'utf-8')
#     if received == "Server Ready!!!":
#         while True:
#             print('Enter the string to be reversed: ')
#             cmd = input()
#             # print(cmd)
#             if cmd == 'quit':
#                 conn.send(str.encode(cmd))
#                 conn.close()
#                 s.close()
#                 sys.exit()
#                 break
#             if(len(str.encode(cmd))) > 0:
#                 conn.send(str.encode(cmd))
#                 client_response = str(conn.recv(1024),"utf-8")
#                 print(client_response, end="")
#     else:
#         print('Wait for server!!!')
#         conn.send(str.encode(received))
#         send_string()

def send_string():
    received = str(s.recv(1024),'utf-8')
    if received == "Server Ready!!!":
        while True:
            print('Enter the string to be reversed: ')
            cmd = input()
            # print(cmd)
            if cmd == 'quit':
                s.send(str.encode(cmd))
                s.close()
                sys.exit()
                break
            if(len(str.encode(cmd))) > 0:
                s.send(str.encode(cmd))
                client_response = str(s.recv(1024),"utf-8")
                print(client_response)
    else:
       #  print('Wait for server!!!')
        s.send(str.encode(received))
        send_string()

def main():
    socket_create()
    socket_connect()
    send_string()

main()