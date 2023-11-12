import socket
import os

# Client configuration
host = '127.0.0.1'
port = 12345

# Function to handle file upload/download
def handle_file_transfer(client_socket, file_name, mode):
    try:
        if mode == 'download':
            downloaded_file_name = modify_filename_for_download(file_name)  # Modify the filename for download
            with open(downloaded_file_name, 'wb') as file:
                data = client_socket.recv(1024)
                while data:
                    file.write(data)
                    data = client_socket.recv(1024)
            print(f"File {downloaded_file_name} is downloaded successfully.")

        elif mode == 'upload': 
            with open(file_name, 'rb') as file:
                data = file.read(1024)
                while data:
                    client_socket.send(data)
                    data = file.read(1024)
            print(f"File {file_name} is uploaded successfully.")
    
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")


# Function to modify the filename for download
def modify_filename_for_download(file_name):
    base_name, extension = os.path.splitext(file_name)
    return base_name + "_downloaded" + extension

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))
print(f"Connected to {host}:{port}")

try:
    # Upload files to the server
    client_socket.send('upload'.encode())

    # Get the list of txt files in the client directory
    txt_files = [file for file in os.listdir() if file.endswith(".txt")]

    # Send the number of files
    num_files = len(txt_files)
    client_socket.send(str(num_files).encode())

    # Send each file name to the server
    for file_name in txt_files:
        client_socket.send(file_name.encode())

    # Handle file upload
    for file_name in txt_files:
        handle_file_transfer(client_socket, file_name, 'upload')

    print("File upload completed.")

    # Download files from the server
    client_socket.send('download'.encode())

    # Send the number of files
    client_socket.send(str(num_files).encode())

    # Handle file download
    for file_name in txt_files:
        # Modify the filename for download
        # downloaded_file_name = modify_filename_for_download(file_name)
        handle_file_transfer(client_socket, file_name, 'download')

    print("File download completed.")

    # Close the connection
finally:
    client_socket.close()
