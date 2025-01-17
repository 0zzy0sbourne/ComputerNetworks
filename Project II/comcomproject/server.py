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
TIMEOUT = 0.1  # it's given in the project PDF

# window size options for testing
WINDOW_SIZES = [1, 10, 50, 100]
ERROR_RATES = [0, 1, 5, 10, 20]

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
        unreliableSend(ack_packet, sock, client_addr, ERROR_RATES[0])
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
def send_file(sock, client_addr, filename, window_size):
    """
    Implements selective repeat sender logic
    """
    try:
        # Read actual file content
        try:
            with open(filename, 'r') as file:
                file_content = file.read().splitlines()
        except FileNotFoundError:
            print(f"File {filename} not found!")
            return False

        if not file_content:
            print("File is empty!")
            return False
            
        print(f"Loaded {len(file_content)} lines from {filename}")
        
        base = 0  # Base of sending window
        next_seq = 0  # Next sequence number to use
        window = {}  # Buffer for sent packets
        
        while base < len(file_content):
            # Send packets within window
            while next_seq < base + window_size and next_seq < len(file_content):
                data_packet = create_packet(DATA, next_seq, file_content[next_seq])
                unreliableSend(data_packet, sock, client_addr, ERROR_RATES[0])
                window[next_seq] = data_packet
                print(f"Sent packet {next_seq}")
                next_seq += 1
            
            # Try to receive ACKs
            try:
                sock.settimeout(TIMEOUT)
                ack_packet, _ = sock.recvfrom(BUFFER_SIZE)
                ack_type, ack_seq, _ = decode_packet(ack_packet)
                
                if ack_type == ACK:
                    print(f"Received ACK for packet {ack_seq}")
                    if ack_seq >= base:
                        # Remove acknowledged packet from window
                        if ack_seq in window:
                            del window[ack_seq]
                        if ack_seq == base:
                            # Move window forward
                            while base in window:
                                del window[base]
                                base += 1
                            base += 1
                
            except socket.timeout:
                # Resend unacknowledged packets
                print("Timeout, resending unacknowledged packets")
                for seq in window:
                    unreliableSend(window[seq], sock, client_addr, ERROR_RATES[0])
                    print(f"Resent packet {seq}")
                    
        # Send FIN packet
        print("File transfer complete, sending FIN")
        fin_packet = create_packet(FIN, len(file_content))
        unreliableSend(fin_packet, sock, client_addr, ERROR_RATES[0])
        
        # Wait for FIN acknowledgment
        try:
            sock.settimeout(TIMEOUT)
            fin_ack, _ = sock.recvfrom(BUFFER_SIZE)
            ack_type, ack_seq, _ = decode_packet(fin_ack)
            if ack_type == ACK:
                print("Received ACK for FIN")
        except socket.timeout:
            print("No ACK received for FIN")
        
        return True
        
    except Exception as e:
        print(f"Error sending file: {e}")
        return False

def main():
    # Create UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print(f"Server started on {HOST}:{PORT}")

    try:
        while True:
            print("\nWaiting for new connection...")
            success, client_addr, filename = handle_handshake(server_socket)

            if success:
                print(f"Starting file transfer for {filename}")
                if send_file(server_socket, client_addr, filename, WINDOW_SIZES[0]):
                    print("File transfer completed successfully")
                else:
                    print("File transfer failed")
            else:
                print("Handshake failed, waiting for new connection...")
                # Add a small delay to prevent CPU spinning
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
