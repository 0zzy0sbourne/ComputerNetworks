from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QGridLayout, QWidget 
from PyQt5.QtCore import pyqtSlot, Qt

class Rdt1_0:
    def __init__(self):
        self.state = "wait_for_call_from_above"
        self.packet = None
        self.data = "Some data"  # Add this line

    def fsm_rdt1_0(self):
        while True:
            if self.state == "wait_for_call_from_above":
                event = self.wait_for_event()
                if event == "call_from_above":
                    self.rdt_send()
                    self.state = "wait_for_ack"
            elif self.state == "wait_for_ack":
                event = self.wait_for_event()
                if event == "ack_received":
                    self.state = "wait_for_call_from_above"

    def rdt_send(self):
        # Assuming data is already set
        self.make_pkt(self.data)
        self.udt_send(self.packet)
        self.state = "wait_for_ack"

    def make_pkt(self, data):
        # Assuming packet is a simple string
        self.packet = str(data)

    def udt_send(self, packet):
        # Assuming udt_send simply prints the packet
        print("Sending packet: ", packet)

    @pyqtSlot(bool)
    def wait_for_event(self, checked):
        event, ok = QInputDialog.getText(None, "Input dialog", "Enter event:")
        if ok:
            # The user clicked OK and entered some text. Use the text as the event.
            return event
        else:
            # The user clicked Cancel or didn't enter any text. Return a default event.
            return "default_event"


class Rdt2_0:
    def __init__(self):
        self.state = "wait_for_call_from_above"
        self.packet = None

    def fsm_rdt2_0(self):
        while True:
            if self.state == "wait_for_call_from_above":
                event = self.wait_for_event()
                if event == "call_from_above":
                    self.rdt_send()
                    self.state = "wait_for_ack"
            elif self.state == "wait_for_ack":
                event = self.wait_for_event()
                if event == "ack_received":
                    self.state = "wait_for_call_from_above"
                elif event == "nack_received":
                    self.rdt_send()

    def rdt_send(self):
        # Assuming data is already set
        self.make_pkt(self.data)
        self.udt_send(self.packet)
        self.state = "wait_for_ack"

    def make_pkt(self, data):
        # Assuming packet is a simple string
        self.packet = str(data)

    def udt_send(self, packet):
        # Assuming udt_send simply prints the packet
        print("Sending packet: ", packet)

    def wait_for_event(self):
        # Assuming event is a string input from user
        event = input("Enter event: ")
        return event      
        


class Rdt3_0:
    def __init__(self):
        self.state = "wait_for_call_from_above"
        self.packet = None

    def fsm_rdt3_0(self):
        while True:
            if self.state == "wait_for_call_from_above":
                event = self.wait_for_event()
                if event == "call_from_above":
                    self.rdt_send()
                    self.state = "wait_for_ack"
            elif self.state == "wait_for_ack":
                event = self.wait_for_event()
                if event == "ack_received":
                    self.state = "wait_for_call_from_above"
                elif event == "nack_received":
                    self.rdt_send()
                elif event == "timeout":
                    self.rdt_send()

    def rdt_send(self):
        # Assuming data is already set
        self.make_pkt(self.data)
        self.udt_send(self.packet)
        self.state = "wait_for_ack"

    def make_pkt(self, data):
        # Assuming packet is a simple string
        self.packet = str(data)

    def udt_send(self, packet):
        # Assuming udt_send simply prints the packet
        print("Sending packet: ", packet)

    def wait_for_event(self):
        # Assuming event is a string input from user
        event = input("Enter event: ")
        return event

class OperationSequenceDiagram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.label.setText("Operation Sequence Diagram will be displayed here.")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.setLayout(self.vbox)

class CommandPromptLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Command Prompt")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("QLabel { background-color : black; color : white; }")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()

        self.serviceModelLabel = QLabel("Reliable Data Transfer Service Model")
        self.stateDiagramLabel = QLabel("State Diagram")
        
        # Create instances of OperationSequenceDiagram and CommandPromptLabel
        self.operationSequenceDiagram = OperationSequenceDiagram()
        self.commandPromptLabel = CommandPromptLabel()

        # Add labels and instances to the grid layout
        self.grid.addWidget(self.serviceModelLabel, 0, 0)
        self.grid.addWidget(self.stateDiagramLabel, 0, 1)
        self.grid.addWidget(self.operationSequenceDiagram, 1, 0)  # Add OperationSequenceDiagram
        self.grid.addWidget(self.commandPromptLabel, 1, 1)        # Add CommandPromptLabel

        # Set the central widget to the grid layout
        central_widget = QWidget()
        central_widget.setLayout(self.grid)
        self.setCentralWidget(central_widget)


app = QApplication([])
rdt = Rdt1_0()
window = MainWindow()
window.show()
app.exec_()