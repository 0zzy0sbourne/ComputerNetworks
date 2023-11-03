import socket

# Client configuration
host = '127.0.0.1'
port = 12345

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))
print(f"Connected to {host}:{port}")

# Upload a text file to the server
with open('client_data.txt', 'rb') as file:
    data = file.read(1024)
    while data:
        client_socket.send(data)
        data = file.read(1024)

print("File uploaded to the server.")

# Close the connection
client_socket.close()

# Client initiates a second connection to download the file

# Create a new socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server again
client_socket.connect((host, port))
print(f"Connected to {host}:{port} for download")

# Receive and save the downloaded file
with open('client_downloaded.txt', 'wb') as file:
    data = client_socket.recv(1024)
    while data:
        file.write(data)
        data = client_socket.recv(1024)

print("File downloaded from the server.")

# Comparing part
# Compare the content of the uploaded and downloaded files
with open('client_data.txt', 'rb') as uploaded_file, open('client_downloaded.txt', 'rb') as downloaded_file:
    uploaded_data = uploaded_file.read()
    downloaded_data = downloaded_file.read()

if uploaded_data == downloaded_data:
    print("File transmission successful. Files match.")
else:
    print("Error: Files do not match. Transmission failed.")

# Close the connection
client_socket.close()
