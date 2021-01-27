
from files import Config
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_Konfigurator

class Actions():
    def load_config(self):
        print("Ładuje config")
        config = Config()
        config.path = "./config.json"
        self.ui.portTextEdit.setPlainText(str(config.port))
        self.ui.ipTextEdit.setPlainText(str(config.ip))
    
    def save_config(self):
        config = Config()
        config.path = "./config.json"
        config.ip = self.ui.ipTextEdit.toPlainText()
        config.port = self.ui.portTextEdit.toPlainText()