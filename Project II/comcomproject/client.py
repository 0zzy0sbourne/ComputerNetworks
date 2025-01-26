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
WINDOW_SIZE = 10 # CAN TAKE VALUES OF: [1, 10, 50, 100]
ERROR_RATE = 10 # CAN TAKE VALUES OF: [0, 1, 5, 10, 20]

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
def establish_connection(sock, addr, filename): 
    """
        - 3-way handshake
            - send handshake with filename
            - wait for ACK
            - send final confirmation 
    """

    handshake_packet = create_packet(HANDSHAKE, 0, filename)
    unreliableSend(handshake_packet, sock, addr, ERROR_RATE)

    # Set timeout for ACK reception
    sock.settimeout(TIMEOUT)
    
    try:
        # Wait for ACK
        response, _ = sock.recvfrom(BUFFER_SIZE)
        packet_type, seq_num, _ = decode_packet(response)
        
        if packet_type != ACK or seq_num != 0:
            return False
            
        # Send final confirmation
        ack_packet = create_packet(ACK, 0)
        unreliableSend(ack_packet, sock, addr, ERROR_RATE)
        return True
        
    except socket.timeout:
        return False
    
def close_connection(filename): 
    """
        close connection based on the filename 
    """
    pass 

####### DATA RECEPTION  #######

def receive_data(sock):
    base = 0  
    received_buffer = {}
    expected_seq = 0
    received_data = []  # Store received lines
    start_time = time.time()  # Track actual reception start

    
    while True:
        try:
            packet, addr = sock.recvfrom(BUFFER_SIZE)
            packet_type, seq_num, payload = decode_packet(packet)
            
            if packet_type == FIN:
                end_time = time.time()
                # Write to file before returning
                with open(f"received_file_err_rate{ERROR_RATE}_window_size{WINDOW_SIZE}.txt", 'w') as f:
                    f.write('\n'.join(received_data))
                ack_packet = create_packet(ACK, seq_num)
                unreliableSend(ack_packet, sock, addr, ERROR_RATE)
                # Calculate throughput (packets/sec)
                transfer_time = end_time - start_time
                throughput = len(received_data)/transfer_time
                print(f"\nThroughput: {throughput:.2f} packets/sec")
                return True
                
            elif packet_type == DATA:
                send_ack(sock, addr, seq_num)
                
                if base <= seq_num < base + WINDOW_SIZE:
                    received_buffer[seq_num] = payload
                    
                    while expected_seq in received_buffer:
                        line = received_buffer[expected_seq]
                        received_data.append(line)  # Add to received data
                        print(f"Delivering packet {expected_seq}: {line}")
                        del received_buffer[expected_seq]
                        expected_seq += 1
                        base = expected_seq
        except socket.timeout:
            continue
        
def send_ack(sock, addr, sequence_number):
    """
    Creates and sends ACK packets using unreliable_send
    """
    ack_packet = create_packet(ACK, sequence_number)
    unreliableSend(ack_packet, sock, addr, ERROR_RATE)

def main():
    results = []

    print(f"\nTesting with window size: {WINDOW_SIZE}")
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (HOST, PORT)
    client_socket.settimeout(TIMEOUT)

    filename = "input.txt"

    if establish_connection(client_socket, server_addr, filename):
        start_time = time.time()
        receive_data(client_socket)
        end_time = time.time()
        
        results.append({
            'window_size': WINDOW_SIZE,
            'transfer_time': end_time - start_time
        })
        
    client_socket.close()
    time.sleep(1)  # Wait before next test

    # Print results
    print("\nTest Results:")
    for result in results:
        print(f"Window Size: {result['window_size']}, Time: {result['transfer_time']:.2f}s")

if __name__ == "__main__": 
    main()