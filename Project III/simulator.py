import tkinter as tk
import time

class RdtSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("RDT Simulator")

        # Canvas to draw the RDT service model
        self.canvas = tk.Canvas(root, width=400, height=300)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        # Triggering function labels
        self.trigger_labels = {
            'rdt_send': self.create_label("rdt_send()", 50, 30, "blue"),
            'udt_send': self.create_label("udt_send()", 50, 130, "blue"),
            'make_pkt': self.create_label("make_pkt()", 200, 30, "green"),
            'send': self.create_label("send()", 200, 130, "green"),
            'deliver_data': self.create_label("deliver_data()", 350, 30, "red"),
            'recv': self.create_label("recv()", 350, 130, "red")
        }

        # Simulate Button
        self.simulate_button = tk.Button(root, text="Simulate", command=self.simulate)
        self.simulate_button.grid(row=1, column=0, pady=10)

    def create_label(self, text, x, y, color):
        label = tk.Label(self.root, text=text, fg=color)
        label_id = self.canvas.create_window(x, y, window=label, anchor=tk.W)
        return label_id

    def highlight_function_call(self, function_name):
        label_id = self.trigger_labels.get(function_name)
        if label_id:
            self.canvas.itemconfig(label_id)
            self.root.update()
            time.sleep(1)  # Simulate the function call duration
            self.canvas.itemconfig(label_id)
            self.root.update()

    def simulate(self):
        # Simulate the RDT service model
        self.highlight_function_call('rdt_send')
        self.highlight_function_call('make_pkt')
        self.highlight_function_call('udt_send')
        self.highlight_function_call('send')
        self.highlight_function_call('deliver_data')
        self.highlight_function_call('recv')

if __name__ == "__main__":
    root = tk.Tk()
    app = RdtSimulator(root)
    root.mainloop()
