import os
import socket
import subprocess

s = socket.socket()
#host = '10.2.3.70'
host = '172.17.29.20'
#host = '10.2.4.250'
port = 9001
s.connect((host, port))
s.send(str.encode("Client"))

while True:
	data = s.recv(1024)
	arr = data[:].decode("utf-8")
	var = arr[::-1]
	if arr != " ":
		print("Data received from Server : " + arr)
		print("Data sent to the Server: " + var + '\n')
	s.send(str.encode(var))

# Close Connection
print("Connection was broken")
s.close()