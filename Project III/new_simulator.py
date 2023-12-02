import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPainter, QColor
from protocol_fsms.rdt import RDTSimulationApp

app = QApplication(sys.argv)

# Run simulations for RDT1.0, RDT2.0, and RDT3.0
rdt_versions = ['rdt1.0', 'rdt2.0', 'rdt3.0']
for rdt_version in rdt_versions:
    ex = RDTSimulationApp(rdt_version)
    sys.exit(app.exec_())