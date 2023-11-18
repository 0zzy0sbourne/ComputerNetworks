import socket
import os

port = 1337

ss = socket.socket()
print('[+] Server socket is created.')

ss.bind(('', port))
print('[+] Socket is binded to {}'.format(port))

ss.listen(5)
print('[+] Waiting for connection...')

con, addr = ss.accept()
print('[+] Got connection from {}'.format(addr[0]))

# Receive the number of files from the client
num_files = int(con.recv(1024).decode())

for _ in range(num_files):
    filename = con.recv(1024).decode()

    f = open(filename, 'wb')
    l = con.recv(1024)
    while l:
        f.write(l)
        l = con.recv(1024)
    f.close()
    print('[+] Received file ' + filename)

con.close()
ss.close()
