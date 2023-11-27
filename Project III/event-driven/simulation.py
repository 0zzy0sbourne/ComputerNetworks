import simpy
import random

class Channel:
    def __init__(self, env, loss_probability=0.1):
        self.env = env
        self.loss_probability = loss_probability
        self.queue = simpy.Store(env)

    def send(self, packet):
        if random.uniform(0, 1) > self.loss_probability:
            return self.queue.put(packet)
        else:
            print("Packet lost!")

    def receive(self):
        return self.queue.get()

class Sender:
    def __init__(self, env, channel, timeout=2):
        self.env = env
        self.channel = channel
        self.timeout = timeout

    def send_data(self, data):
        print("Triggering function call: rdt_send()")
        packet = {'data': data}
        self.channel.send(packet)

class Receiver:
    def __init__(self, env, channel):
        self.env = env
        self.channel = channel

    def receive_data(self):
        print("Triggering function call: rdt_rcv()")
        packet = yield self.channel.receive()
        return packet['data']

def simulate_rdt(env, sender, receiver, data, scenario):
    yield env.timeout(1)  # Initial delay

    if scenario == "normal":
        print(f"Sending data: {data}")
        sender.send_data(data)
        yield env.timeout(1)  # Simulate network delay
    elif scenario == "premature_ack":
        print(f"Sending data: {data}")
        sender.send_data(data)
        yield env.timeout(0.5)  # Simulate premature ACK
        print("Premature ACK received.")
    elif scenario == "lost_packet":
        print(f"Sending data: {data}")
        sender.send_data(data)
        yield env.timeout(1.5)  # Simulate lost packet
        print("Lost packet scenario.")
    elif scenario == "timeout":
        print(f"Sending data: {data}")
        sender.send_data(data)
        yield env.timeout(2.5)  # Simulate timeout
        print("Timeout scenario.")

    received_data = yield env.process(receiver.receive_data())
    print(f"Received data: {received_data}")

    # Print state diagram action/events
    print("\nState Diagram Action/Events:")
    if scenario == "normal":
        print("Sender: Data sent, Receiver: ACK received")
    elif scenario == "premature_ack":
        print("Sender: Data sent, Receiver: Premature ACK received")
    elif scenario == "lost_packet":
        print("Sender: Data sent, Receiver: Packet lost")
    elif scenario == "timeout":
        print("Sender: Data sent, Receiver: Timeout")

    # Print operation sequence diagram
    print("\nOperation Sequence Diagram:")
    print("1. Sender sends data")
    print("2. Receiver receives data")

    # Print command prompt
    print("\nCommand Prompt:")
    print("Commands:")
    print("1. sender.send_data(data)")
    print("2. receiver.receive_data()")
    print("Outputs:")
    print(f"1. Sending data: {data}")
    print(f"2. Received data: {received_data}")

# Simulation environment
env = simpy.Environment()

# Create channel, sender, and receiver
channel = Channel(env)
sender = Sender(env, channel)
receiver = Receiver(env, channel)

# Run the simulation for different scenarios
scenarios = ["normal", "premature_ack", "lost_packet", "timeout"]
for scenario in scenarios:
    print(f"\nRunning simulation for {scenario} scenario:")
    env.process(simulate_rdt(env, sender, receiver, "Hello, SimPy!", scenario))
    env.run()
