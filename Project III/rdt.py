import tkinter as tk
import time


class RdtSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("RDT Simulator")

        # Subsections
        self.canvas_rdt_model = self.create_canvas(0, 0, 400, 300)
        self.canvas_state_diagram = self.create_canvas(400, 0, 400, 300)
        self.canvas_sequence_diagram = self.create_canvas(0, 300, 400, 200)
        self.text_command_prompt = self.create_text_widget(400, 300, 400, 200)

        # Triggering function labels
        self.trigger_labels = {
            'rdt_send': self.create_label(self.canvas_rdt_model, "rdt_send()", 50, 30, "blue"),
            'udt_send': self.create_label(self.canvas_rdt_model, "udt_send()", 50, 130, "blue"),
            'make_pkt': self.create_label(self.canvas_rdt_model, "make_pkt()", 200, 30, "green"),
            'send': self.create_label(self.canvas_rdt_model, "send()", 200, 130, "green"),
            'deliver_data': self.create_label(self.canvas_rdt_model, "deliver_data()", 350, 30, "red"),
            'recv': self.create_label(self.canvas_rdt_model, "recv()", 350, 130, "red")
        }

        # Simulate Button
        self.simulate_button = tk.Button(root, text="Simulate", command=self.simulate)
        self.simulate_button.grid(row=1, column=0, pady=10)

    def create_canvas(self, x, y, width, height):
        canvas = tk.Canvas(self.root, width=width, height=height, bg="white")
        canvas.grid(row=0, column=0, padx=10, pady=10)
        return canvas

    def create_text_widget(self, x, y, width, height):
        text_widget = tk.Text(self.root, wrap=tk.WORD, width=40, height=10)
        text_widget.grid(row=0, column=1, padx=10, pady=10)
        return text_widget

    def create_label(self, canvas, text, x, y, color):
        label = tk.Label(self.root, text=text, bg="white", fg=color)
        label_id = canvas.create_window(x, y, window=label, anchor=tk.W)
        return label_id

    def highlight_function_call(self, function_name, canvas):
        label_id = self.trigger_labels.get(function_name)
        if label_id:
            canvas.itemconfig(label_id, bg="yellow")
            self.root.update()
            time.sleep(1)  # Simulate the function call duration
            canvas.itemconfig(label_id, bg="white")
            self.root.update()

    def simulate(self):
        # Simulate the RDT service model
        self.highlight_function_call('rdt_send', self.canvas_rdt_model)
        self.highlight_function_call('make_pkt', self.canvas_rdt_model)
        self.highlight_function_call('udt_send', self.canvas_rdt_model)
        self.highlight_function_call('send', self.canvas_rdt_model)
        self.highlight_function_call('deliver_data', self.canvas_rdt_model)
        self.highlight_function_call('recv', self.canvas_rdt_model)

        # You can add more simulation steps and update other sections accordingly


if __name__ == "__main__":
    root = tk.Tk()
    app = RdtSimulator(root)
    root.mainloop()
