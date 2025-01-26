"""
    - UDP on top of unreliable channel. 
        - all packets are prone to be lost.  
        - packets include data packets and control packets such as handshake packets and ack packets. 
    - use SR.
    - errRate and N (window size) can take different values, compare the performance for each parameter combination. 
    - connection-oriented policy (connect before sending data)
"""


"""
    - UDP on top of unreliable channel. 
        - all packets are prone to be lost.  
        - packets include data packets and control packets such as handshake packets and ack packets. 
    - use SR.
    - errRate and N (window size) can take different values, compare the performance for each parameter combination. 
    - connection-oriented policy (connect before sending data)
"""
import socket
import random
import time 

# CONSTANTS FOR PACKET TYPES
HANDSHAKE = 0
ACK = 1
DATA = 2
FIN = 3

# CONFIG
HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024
TIMEOUT = 0.01  # it's given in the project PDF

# window size options for testing
WINDOW_SIZE = 1 # CAN TAKE VALUES OF: [1, 10, 50, 100]
ERROR_RATE = 20 # CAN TAKE VALUES OF: [0, 1, 5, 10, 20]

# for window_size:1, error_rate: 10 --> time: 0.05s 
# for window_size:1, error_rate: 20 --> time: 0.06s 
# code starts to struggle in window_size:10, error_rate:10 config

####### PACKET HANDLING FUNCTIONS  #######
def create_packet(type, sequence_number, payload=""):
    """
        - creates packets for different types - HANDSHAKE, ACK, DATA, FIN
        - handles byte encoding 
    """
    packet = bytearray()
    packet.append(type)  # first byte in the packet is packet type

    if type == HANDSHAKE:
        """
            in this case packet includes: 
                - packet type 
                - payload length
                - payload 
        """
        payload_bytes = payload.encode('utf-8')
        packet.append(len(payload_bytes))
        packet.extend(payload_bytes)
    elif type == ACK:
        """
            in this case packet includes: 
                - packet type 
                - sequence number 
        """
        packet.append(sequence_number)
    elif type == DATA:
        """
            in this case packet includes: 
                - packet type
                - payload length
                - sequence number
                - payload
        """
        payload_bytes = payload.encode('utf-8')
        packet.append(len(payload_bytes))  # Payload length
        packet.append(sequence_number)
        packet.extend(payload_bytes)  # Data
    elif type == FIN:
        """
            in this case packet includes:
                - packet type
                - sequence number
        """
        packet.append(sequence_number)

    return packet

def decode_packet(packet):
    """
        - extracts packet type, sequence number, payload --> it returns tuple (type, sequence_number, payload)
        - handles byte decoding 
    """
    packet_type = packet[0]

    if packet_type == HANDSHAKE:
        payload_length = packet[1]
        payload = packet[2:2 + payload_length].decode('utf-8')
        return (packet_type, None, payload)
    elif packet_type == ACK:
        sequence_number = packet[1]
        return (packet_type, sequence_number, None)
    elif packet_type == DATA:
        payload_length = packet[1]
        sequence_number = packet[2]
        payload = packet[3:3 + payload_length].decode('utf-8')
        return (packet_type, sequence_number, payload)
    elif packet_type == FIN:
        sequence_number = packet[1]
        return (packet_type, sequence_number, None)
    else:
        raise ValueError(f"Unknown packet type: {packet_type}")

def unreliableSend(packet, sock, addr, err_rate):
    """
        sends packets with specified error rate
    """
    if err_rate < random.randint(0, 100):
        sock.sendto(packet, addr)

####### CONNECTION MANAGEMENT #######
def handle_handshake(sock):
    """
    Handles the server side of three-way handshake:
        1. Wait for handshake packet with filename
        2. Send ACK
        3. Wait for final confirmation
    Returns (success, client_addr, filename)
    """
    try:
        print("Waiting for handshake...")
        # Wait for initial handshake
        packet, client_addr = sock.recvfrom(BUFFER_SIZE)
        packet_type, _, filename = decode_packet(packet)

        if packet_type != HANDSHAKE:
            print("Expected handshake packet, received:", packet_type)
            return False, None, None

        print(f"Received handshake with filename: {filename}")

        # Send ACK
        ack_packet = create_packet(ACK, 0)
        unreliableSend(ack_packet, sock, client_addr, ERROR_RATE)
        print("Sent ACK for handshake")

        # Wait for final confirmation
        sock.settimeout(TIMEOUT)
        confirmation, _ = sock.recvfrom(BUFFER_SIZE)
        conf_type, conf_seq, _ = decode_packet(confirmation)

        if conf_type != ACK or conf_seq != 0:
            print("Invalid confirmation received")
            return False, None, None

        print("Handshake completed successfully")
        return True, client_addr, filename

    except socket.timeout:
        print("Timeout during handshake")
        return False, None, None
    except Exception as e:
        print(f"Error during handshake: {e}")
        return False, None, None

####### DATA TRANSMISSION #######
def send_file(sock, client_addr, filename):
    try:
        with open(filename, 'r') as file:
            file_content = file.read().splitlines()

        base = 0  
        next_seq = 0
        window = {}
        
        while base < len(file_content):
            while next_seq < base + WINDOW_SIZE and next_seq < len(file_content):
                seq_num = next_seq % 256
                if next_seq - base < WINDOW_SIZE:  # Only send if within window
                    data_packet = create_packet(DATA, seq_num, file_content[next_seq])
                    unreliableSend(data_packet, sock, client_addr, ERROR_RATE)
                    window[next_seq] = data_packet
                    print(f"Sent packet {next_seq}")
                next_seq += 1
            
            try:
                sock.settimeout(TIMEOUT)
                ack_packet, _ = sock.recvfrom(BUFFER_SIZE)
                ack_type, ack_seq, _ = decode_packet(ack_packet)
                
                if ack_type == ACK:
                    expected_seq = base % 256
                    if ack_seq == expected_seq:
                        if base in window:
                            del window[base]
                        base += 1
                        while base in window:
                            del window[base]
                            base += 1
            except socket.timeout:
                for seq in window:
                    unreliableSend(window[seq], sock, client_addr, ERROR_RATE)
                    
        fin_packet = create_packet(FIN, len(file_content) % 256)
        unreliableSend(fin_packet, sock, client_addr, ERROR_RATE)
        
        return True
        
    except Exception as e:
        print(f"Error sending file: {e}")
        return False

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    results = []

    print(f"\nTesting with window size: {WINDOW_SIZE}")
    
    # Reset socket for each test
    server_socket.close()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    
    success = False
    while not success:
        success, client_addr, filename = handle_handshake(server_socket)
        if success:
            start_time = time.time()
            transfer_success = send_file(server_socket, client_addr, filename)
            end_time = time.time()
            
            if transfer_success:
                results.append({
                    'window_size': WINDOW_SIZE,
                    'transfer_time': end_time - start_time
                })
                print(f"Transfer completed in {end_time - start_time:.2f} seconds")
        else:
            time.sleep(0.9)  # Longer delay between retries

    print("\nTest Results:")
    for result in results:
        print(f"Window Size: {result['window_size']}, Time: {result['transfer_time']:.2f}s")

if __name__ == "__main__":
    main()