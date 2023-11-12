import socket
import os

# Server configuration
host = '127.0.0.1'
port = 12345

# Function to handle file upload/download
def handle_file_transfer(client_socket, file_name, mode):
    if mode == 'upload':
        with open(file_name, 'wb') as file:
            data = client_socket.recv(1024)
            while data:
                file.write(data)
                data = client_socket.recv(1024)
        print(f"{file_name} received and saved successfully.")
    elif mode == 'download':
        with open(file_name, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)
        print(f"{file_name} sent to the client.")

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print(f"Server listening on {host}:{port}")

try:
    while True:
        # Accept a client connection
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Receive the mode (upload/download) from the client
        mode = client_socket.recv(1024).decode()

        # Receive the number of files
        num_files = int(client_socket.recv(1024).decode())

        for _ in range(num_files):
            # Receive the file name from the client
            file_name = client_socket.recv(1024).decode()

            # Handle file upload/download
            handle_file_transfer(client_socket, file_name, mode)

        # Close the client connection
        client_socket.close()

finally:
    # Close the server socket
    server_socket.close()
