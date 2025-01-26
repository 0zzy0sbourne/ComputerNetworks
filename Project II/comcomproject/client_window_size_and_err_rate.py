"""
    - UDP on top of unreliable channel. 
        - all packets are prone to be lost.  
        - packets include data packets and control packets such as handshake packets and ack packets. 
    - use SR.
    - errRate and N (window size) can take different values, compare the performance for each parameter combination. 
    - connection-oriented policy (connect before sending data)
"""

import socket
import random # for packet loss simulation 
import time 

# CONSTANTS FOR PACKET TYPES
HANDSHAKE = 0
ACK = 1
DATA = 2 
FIN = 3 

# CONFIG
HOST = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024 
TIMEOUT = 0.0001 # it's given in the project PDF 

# window size options for testing 
WINDOW_SIZES = [1, 10, 50, 100]
ERROR_RATES = [1, 5, 10, 20]

####### PACKET HANDLING FUNCTIONS  #######
def create_packet(type, sequence_number, payload=""):
    """
        - creates packets for different types - HANDSHAKE, ACK, DATA, FIN
        - handles byte encoding 
    """
    packet = bytearray()
    packet.append(type) # first byte in the packet is packet type

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
        payload = packet[2:2+payload_length].decode('utf-8')
        return (packet_type, None, payload)
    elif packet_type == ACK: 
        sequence_number = packet[1]
        return (packet_type, sequence_number, None)
    elif packet_type == DATA: 
        payload_length = packet[1]
        sequence_number = packet[2]
        payload = packet[3:3+payload_length].decode('utf-8')
        return (packet_type, sequence_number, payload)
    elif packet_type == FIN: 
        sequence_number = packet[1]
        return (packet_type, sequence_number, None)
    else: 
        raise ValueError(f"Unknown packet type: {packet_type}" )

def unreliableSend(packet, sock, addr, err_rate): 
    """
        sends packets with specified error rate
    """
    if err_rate < random.randint(0, 100): 
        sock.sendto(packet, addr)

####### CONNECTION MANAGEMENT #######
def establish_connection(sock, addr, filename, error_rate):
    for _ in range(3):  # 3 retries
        handshake_packet = create_packet(HANDSHAKE, 0, filename)
        unreliableSend(handshake_packet, sock, addr, error_rate)
        
        try:
            sock.settimeout(TIMEOUT)
            response, _ = sock.recvfrom(BUFFER_SIZE)
            packet_type, seq_num, _ = decode_packet(response)
            
            if packet_type == ACK:
                ack_packet = create_packet(ACK, 0)
                unreliableSend(ack_packet, sock, addr, error_rate)
                return True
                
        except socket.timeout:
            continue
            
    return False

def close_connection(filename): 
    """
        close connection based on the filename 
    """
    pass 

####### DATA RECEPTION  #######
def receive_data(sock, window_size, error_rate):
    base = 0  
    received_buffer = {}
    expected_seq = 0
    
    while True:
        try:
            packet, addr = sock.recvfrom(BUFFER_SIZE)
            packet_type, seq_num, payload = decode_packet(packet)
            
            if packet_type == FIN:
                ack_packet = create_packet(ACK, seq_num)
                unreliableSend(ack_packet, sock, addr, error_rate)
                return True
                
            elif packet_type == DATA:
                send_ack(sock, addr, seq_num, error_rate)
                
                if base <= seq_num < base + window_size:
                    received_buffer[seq_num] = payload
                    
                    while expected_seq in received_buffer:
                        print(f"Delivering packet {expected_seq}: {received_buffer[expected_seq]}")
                        del received_buffer[expected_seq]
                        expected_seq += 1
                        base = expected_seq
                        
        except socket.timeout:
            continue

def send_ack(sock, addr, sequence_number, err_rate):
    """
    Creates and sends ACK packets using unreliable_send
    """
    ack_packet = create_packet(ACK, sequence_number)
    unreliableSend(ack_packet, sock, addr, err_rate)

# Client main()
def main():
    results = []
    
    for error_rate in ERROR_RATES:
        for window_size in WINDOW_SIZES:
            print(f"\nTesting with error_rate: {error_rate}%, window size: {window_size}")
            time.sleep(0.01)

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_addr = (HOST, PORT)
            client_socket.settimeout(TIMEOUT)

            if establish_connection(client_socket, server_addr, "input.txt", error_rate):
                start_time = time.perf_counter()
                receive_data(client_socket, window_size, error_rate)
                end_time = time.perf_counter()
                
                results.append({
                    'error_rate': error_rate,
                    'window_size': window_size,
                    'transfer_time': end_time - start_time
                })
                
            client_socket.close()

    print("\nTest Results:")
    for result in results:
        print(f"Error Rate: {result['error_rate']}%, Window Size: {result['window_size']}, Time: {result['transfer_time']:.3f}s")

if __name__ == "__main__": 
    main()


