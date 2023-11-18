import socket
import os
import sys

host = '127.0.0.1'
port = 1337

s = socket.socket()
print('[+] Client socket is created.')

s.connect((host, port))
print('[+] Socket is connected to {}'.format(host))

# Get the list of txt files in the client directory
txt_files = [file for file in os.listdir() if file.endswith(".txt")]

# Send the number of files to the server
num_files = len(txt_files)
s.send(str(num_files).encode())

# Send each file to the server
for filename in txt_files:
    s.send(filename.encode())

    with open(filename, 'rb') as file:
        l = file.read(1024)
        while l:
            s.sendall(l)
            l = file.read(1024)
    print('[+] {} is sent'.format(filename))

s.close()
