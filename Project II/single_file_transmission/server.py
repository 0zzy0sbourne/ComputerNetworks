import socket

# Server configuration
host = '127.0.0.1'
port = 12345

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print(f"Server listening on {host}:{port}")

# Accept a client connection
client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

# Receive and save the uploaded text file
with open('server_data.txt', 'wb') as file:
    data = client_socket.recv(1024)
    while data:
        file.write(data)
        data = client_socket.recv(1024)

print("File received and saved successfully.")

# Close the client connection
client_socket.close()

# Server waits for the second connection to serve the downloaded file

# Accept a client connection
client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

# Send the saved file to the client
with open('server_data.txt', 'rb') as file:
    data = file.read(1024)
    while data:
        client_socket.send(data)
        data = file.read(1024)

print("File sent to the client.")

# Close the client connection
client_socket.close()

# Close the server socket
server_socket.close()
