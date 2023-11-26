
class TcpSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("TCP Protocol Simulator")

        # Section 1: Reliable Data Transfer Service Model
        self.rdt_label = tk.Label(root, text="Reliable Data Transfer Service Model")
        self.rdt_label.grid(row=0, column=0, padx=10, pady=10)

        # Section 2: State Diagram
        self.state_label = tk.Label(root, text="State Diagram")
        self.state_label.grid(row=0, column=1, padx=10, pady=10)

        # Section 3: Operation Sequence Diagram
        self.operation_label = tk.Label(root, text="Operation Sequence Diagram")
        self.operation_label.grid(row=1, column=0, padx=10, pady=10)

        # Section 4: Command Prompt
        self.cmd_label = tk.Label(root, text="Command Prompt")
        self.cmd_label.grid(row=1, column=1, padx=10, pady=10)

        # Command Prompt Text Area
        self.cmd_output = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
        self.cmd_output.grid(row=2, column=1, padx=10, pady=10)

        # Simulate Button
        self.simulate_button = tk.Button(root, text="Simulate", command=self.simulate)
        self.simulate_button.grid(row=3, column=0, columnspan=2, pady=10)

    def simulate(self):
        self.cmd_output.delete(1.0, tk.END)
        self.log_command("Simulation Started")

        # Simulate a Normal Transaction
        self.simulate_normal_transaction()

        # Simulate a Premature ACK
        self.simulate_premature_ack()

        # Simulate a Lost Packet
        self.simulate_lost_packet()

        # Simulate a Timeout Event
        self.simulate_timeout()

        self.log_command("Simulation Completed")

    def simulate_normal_transaction(self):
        self.log_command("Normal Transaction Simulation Started")

        # Simulate sending data from sender to receiver
        self.log_command("Sender: Sending data...")
        time.sleep(1)  # Simulating the time taken for data transfer
        self.log_command("Receiver: Data received.")

        # Simulate sending acknowledgment from receiver to sender
        self.log_command("Receiver: Sending ACK...")
        time.sleep(1)  # Simulating the time taken for ACK transmission
        self.log_command("Sender: ACK received.")

        self.log_command("Normal Transaction Simulation Completed")

    def simulate_premature_ack(self):
        self.log_command("Premature ACK Simulation Started")

        # Simulate sending data from sender to receiver
        self.log_command("Sender: Sending data...")
        time.sleep(1)  # Simulating the time taken for data transfer

        # Simulate a premature acknowledgment from the receiver
        self.log_command("Receiver: Premature ACK sent.")
        self.log_command("Sender: ACK received.")

        self.log_command("Premature ACK Simulation Completed")

    def simulate_lost_packet(self):
        self.log_command("Lost Packet Simulation Started")

        # Simulate sending data from sender to receiver
        self.log_command("Sender: Sending data...")
        time.sleep(1)  # Simulating the time taken for data transfer

        # Simulate a lost packet (no acknowledgment received)
        self.log_command("Sender: Packet lost. Resending data...")
        time.sleep(1)
        self.log_command("Receiver: Data received.")
        self.log_command("Sender: ACK received.")

        self.log_command("Lost Packet Simulation Completed")

    def simulate_timeout(self):
        self.log_command("Timeout Simulation Started")

        # Simulate sending data from sender to receiver
        self.log_command("Sender: Sending data...")
        time.sleep(2)  # Simulating a longer time for data transfer

        # Simulate a timeout event
        self.log_command("Sender: Timeout. Resending data...")
        time.sleep(1)
        self.log_command("Receiver: Data received.")
        self.log_command("Sender: ACK received.")

        self.log_command("Timeout Simulation Completed")

    def log_command(self, message):
        self.cmd_output.insert(tk.END, f"{message}\n")
        self.cmd_output.see(tk.END)  # Scroll to the end

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = TcpSimulator(root)
#     root.mainloop()