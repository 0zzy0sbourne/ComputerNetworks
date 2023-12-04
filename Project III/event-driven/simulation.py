import simpy
import enum

class SenderState(enum.Enum):
    CLOSED = 0
    SYN_SENT = 1
    ESTABLISHED = 2

class ReceiverState(enum.Enum):
    CLOSED = 0
    SYN_RCVD = 1
    ESTABLISHED = 2

# Create an environment
env = simpy.Environment()

# Function to simulate the state diagrams
def print_state_diagram(entity, state, event):
    print(f"{entity} State: {state.name} | Event: {event}")

# Function to simulate the operation sequence diagram
def print_operation_sequence(sender_action, receiver_action):
    print(f"Sender: {sender_action} -> Receiver: {receiver_action}")

# Define a process that simulates the sender behavior
def sender(env, message_buffer):
    sender_state = SenderState.CLOSED
    while True:
        if sender_state == SenderState.CLOSED:
            # Send a SYN message and set a timeout
            print_state_diagram("Sender", sender_state, "Send SYN")
            message_buffer.put(('SYN', 'Sender'))
            sender_state = SenderState.SYN_SENT
            yield env.timeout(1)
        elif sender_state == SenderState.SYN_SENT:
            try:
                syn_ack, entity = yield message_buffer.get()
                if syn_ack == 'SYN-ACK':
                    print_state_diagram("Sender", sender_state, "Receive SYN-ACK")
                    sender_state = SenderState.ESTABLISHED
            except simpy.Interrupt as interrupt:
                # If the timeout occurs, print a message and resend the SYN message
                print_state_diagram("Sender", sender_state, "Timeout")
                print_state_diagram("Sender", sender_state, "Resend SYN")
                message_buffer.put(('SYN', 'Sender'))
                yield env.timeout(1)
        elif sender_state == SenderState.ESTABLISHED:
            # Send and receive data messages
            print_state_diagram("Sender", sender_state, "Send DATA")
            message_buffer.put(('DATA', 'Sender'))
            yield env.timeout(1)

# Define a process that simulates the receiver behavior
def receiver(env, message_buffer):
    receiver_state = ReceiverState.CLOSED
    while True:
        if receiver_state == ReceiverState.CLOSED:
            # Wait for a SYN message
            syn, entity = yield message_buffer.get()
            if syn == 'SYN':
                print_state_diagram("Receiver", receiver_state, "Receive SYN")
                receiver_state = ReceiverState.SYN_RCVD
                print_state_diagram("Receiver", receiver_state, "Send SYN-ACK")
                message_buffer.put(('SYN-ACK', 'Receiver'))
                yield env.timeout(1)
        elif receiver_state == ReceiverState.SYN_RCVD:
            # Wait for data messages
            data, entity = yield message_buffer.get()
            if data == 'DATA':
                print_state_diagram("Receiver", receiver_state, "Receive DATA")
                receiver_state = ReceiverState.ESTABLISHED
                print_state_diagram("Receiver", receiver_state, "Send ACK")
                message_buffer.put(('ACK', 'Receiver'))
                yield env.timeout(1)

# Create a message buffer
message_buffer = simpy.Store(env, capacity=10)

# Add the sender and receiver processes to the environment
env.process(sender(env, message_buffer))
env.process(receiver(env, message_buffer))

# Run the simulation scenarios
print_operation_sequence("SYN", "SYN Received")
env.run(until=1)
print_operation_sequence("DATA", "ACK Received Prematurely")
env.run(until=3)
print_operation_sequence("DATA", "Data Lost")
env.run(until=6)
print_operation_sequence("Timeout", "Resend Data")
env.run(until=9)
