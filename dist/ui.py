# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from files import Config
from PyQt5.QtCore import QProcess
import os
import time
import threading
import webbrowser

class Ui_Konfigurator(object):
    def setupUi(self, Konfigurator):
        Konfigurator.setObjectName("Konfigurator Sokoła")
        Konfigurator.resize(1200, 600)
        Konfigurator.setFixedSize(1200, 650)

        Konfigurator.setWindowIcon(QtGui.QIcon('./restore1.png')) 

        self.centralwidget = QtWidgets.QWidget(Konfigurator)
        self.centralwidget.setObjectName("centralwidget")


        self.loadConfigButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadConfigButton.setGeometry(QtCore.QRect(50, 530, 190, 27))
        self.loadConfigButton.setObjectName("loadConfigButton")

        self.adminerOpenButton = QtWidgets.QPushButton(self.centralwidget)
        self.adminerOpenButton.setGeometry(QtCore.QRect(50, 570, 190, 27))
        self.adminerOpenButton.setObjectName("adminerOpenButton")

        self.saveConfigButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveConfigButton.setGeometry(QtCore.QRect(250, 530, 190, 27))
        self.saveConfigButton.setObjectName("saveConfigButton")

        self.restoreConfigButton = QtWidgets.QPushButton(self.centralwidget)
        self.restoreConfigButton.setGeometry(QtCore.QRect(450, 530, 240, 27))
        self.restoreConfigButton.setObjectName("restoreConfigButton")

        self.downButton = QtWidgets.QPushButton(self.centralwidget)
        self.downButton.setGeometry(QtCore.QRect(760, 530, 190, 27))
        self.downButton.setObjectName("downButton")

        self.executeConfigButton = QtWidgets.QPushButton(self.centralwidget)
        self.executeConfigButton.setGeometry(QtCore.QRect(960, 530, 190, 27))
        self.executeConfigButton.setObjectName("executeConfigButton")

        self.closeConfigButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeConfigButton.setGeometry(QtCore.QRect(960, 570, 190, 27))
        self.closeConfigButton.setObjectName("closeConfigButton")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 67, 19))
        self.label.setObjectName("label")
        self.ipTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ipTextEdit.setGeometry(QtCore.QRect(50, 40, 250, 25))
        self.ipTextEdit.setObjectName("ipTextEdit")

        self.authLabel = QtWidgets.QLabel(self.centralwidget)
        self.authLabel.setGeometry(QtCore.QRect(50, 90, 250, 19))
        self.authLabel.setObjectName("label")
        self.authTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.authTextEdit.setGeometry(QtCore.QRect(50, 110, 250, 50))
        self.authTextEdit.setObjectName("authTextEdit")



        self.statusTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.statusTextEdit.setGeometry(QtCore.QRect(350, 40, 800, 450))
        self.statusTextEdit.setObjectName("statusTextEdit")
        self.statusTextEdit.setFont(QtGui.QFont('Arial', 10))

        
        self.apistatusLabel = QtWidgets.QLabel(self.centralwidget)
        self.apistatusLabel.setGeometry(QtCore.QRect(50, 400, 250, 19))
        self.apistatusLabel.setObjectName("label")

        self.adminerstatusLabel = QtWidgets.QLabel(self.centralwidget)
        self.adminerstatusLabel.setGeometry(QtCore.QRect(50, 430, 250, 19))
        self.adminerstatusLabel.setObjectName("label")

        self.sokolstatusLabel = QtWidgets.QLabel(self.centralwidget)
        self.sokolstatusLabel.setGeometry(QtCore.QRect(50, 460, 250, 19))
        self.sokolstatusLabel.setObjectName("label")




        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 67, 19))
        self.label_2.setObjectName("label_2")

        Konfigurator.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Konfigurator)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 556, 24))
        self.menubar.setObjectName("menubar")
        Konfigurator.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(Konfigurator)
        self.statusbar.setObjectName("statusbar")

        Konfigurator.setStatusBar(self.statusbar)
        self.retranslateUi(Konfigurator)

        # Actions
        self.loadConfigButton.clicked.connect(self.load_config)
        self.saveConfigButton.clicked.connect(self.save_config)
        self.executeConfigButton.clicked.connect(self.execute)
        self.restoreConfigButton.clicked.connect(self.restore)
        self.downButton.clicked.connect(self.down)

        self.adminerOpenButton.clicked.connect(lambda: webbrowser.open('http://127.0.0.1:8080'))
        
        # InitLoad
        self.load_config()
        self.closeConfigButton.clicked.connect(Konfigurator.close)
        
        # Ping
        t = threading.Thread(target=self.check_statuses,args=[])
        t.daemon = True
        t.start()

        
        

    def retranslateUi(self, Konfigurator):
        _translate = QtCore.QCoreApplication.translate
        Konfigurator.setWindowTitle(_translate("Konfigurator", "Konfigurator Sokoła"))
        self.loadConfigButton.setText(_translate("Konfigurator", "Załaduj konfiguracje"))
        self.saveConfigButton.setText(_translate("Konfigurator", "Zapisz konfiguracje"))
        self.executeConfigButton.setText(_translate("Konfigurator", "Uruchom Sokoła"))
        self.adminerOpenButton.setText(_translate("Konfigurator", "Konfiguracja adminera"))
        self.restoreConfigButton.setText(_translate("Konfigurator", "Załaduj konfiguracje startową"))
        self.closeConfigButton.setText(_translate("Konfigurator", "Zamknij"))
        self.downButton.setText(_translate("Konfigurator", "Wyłącz Sokoła"))
        self.label.setText(_translate("Konfigurator", "API:"))
        self.apistatusLabel.setText(_translate("Konfigurator", "..."))
        self.adminerstatusLabel.setText(_translate("Konfigurator", "..."))
        self.sokolstatusLabel.setText(_translate("Konfigurator", "..."))
        self.authLabel.setText(_translate("Konfigurator", "Autoryzacja:"))
        self.executeConfigButton.setIcon(QtGui.QIcon('execute.png')) 
        self.downButton.setIcon(QtGui.QIcon('terminate.png')) 
        self.restoreConfigButton.setIcon(QtGui.QIcon('initialize.png')) 
        self.saveConfigButton.setIcon(QtGui.QIcon('save.png')) 
        self.loadConfigButton.setIcon(QtGui.QIcon('load.png')) 


    def check_host(self,name,ip,port,label):
        cmd = f"nmap -p {port} {ip} | grep 'open'" 
        response = os.system(cmd)
        if response == 0:
            pingstatus = True
            print(f"port: {port} hosta: {ip} jest otwarty")
            label.setText(f"{name}: Online")
            label.setStyleSheet("color: green") 
        else:
            pingstatus = False
            print(f"port: {port} hosta: {ip} jest zamkniety")
            label.setText(f"{name}: Offline")
            label.setStyleSheet("color: red") 


    def check_statuses(self):
        while True:
            ip = self.config.address.split(":")[0]
            port = self.config.address.split(":")[1]
            self.check_host("API",ip,port,self.apistatusLabel)
            self.check_host("Adminer","127.0.0.1","8080",self.adminerstatusLabel)
            self.check_host("Sokoł","127.0.0.1","88",self.sokolstatusLabel)
            time.sleep(5)
    


    def load_config(self):
        print("Ładuje config")
        self.statusTextEdit.appendPlainText("Ładuje config...")  
        self.config = Config()
        self.config.path = "../app/subiektapi.json"
        self.ipTextEdit.setPlainText(str(self.config.address))
        self.authTextEdit.setPlainText(str(self.config.authorization))
        self.statusTextEdit.appendPlainText("Załadowano") 
    
    def save_config(self):
        self.statusTextEdit.appendPlainText("Zapisuje config...") 
        self.config = Config()
        self.config.path = "../app/subiektapi.json"
        self.config.address = self.ipTextEdit.toPlainText()
        self.statusTextEdit.appendPlainText("Zapisano") 

    def execute(self):
        print("executing")
        self.statusTextEdit.appendPlainText("Uruchamiam...") 
        process = QProcess()
        process.readyReadStandardOutput.connect(lambda:self.handle_stdout_a(process))
        process.readyReadStandardError.connect(lambda:self.handle_stderr_a(process))
        process.finished.connect(lambda:self.finish(process))
        process.start("python3", ['execute.py'])


        # self.p.stateChanged.connect(self.handle_state)


    def restore(self):
        process = QProcess()
        process.readyReadStandardOutput.connect(lambda:self.handle_stdout_a(process))
        process.readyReadStandardError.connect(lambda:self.handle_stderr_a(process))
        process.start("python3", ['restore.py'])


    def down(self):
        print("killing...")
        self.statusTextEdit.appendPlainText("Zabijam kontenery...")
        process = QProcess()
        process.readyReadStandardOutput.connect(lambda:self.handle_stdout_a(process))
        process.readyReadStandardError.connect(lambda:self.handle_stderr_a(process))
        process.finished.connect(lambda:self.finish(process))
        process.start("python3", ['kill.py'])

    def finish(self,process):
        self.statusTextEdit.appendPlainText("Zakończono") 
        process = None   


    def handle_stderr_a(self,process):
        data = process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.statusTextEdit.appendPlainText(stderr)

    def handle_stdout_a(self,process):
        data = process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.statusTextEdit.appendPlainText(stdout)


    def execute_finished(self):
        self.statusTextEdit.appendPlainText("Zakończono") 
        self.p = None   

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.statusTextEdit.appendPlainText(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.statusTextEdit.appendPlainText(stdout)

    def handle_state(self, state):
        states = {   
            QProcess.NotRunning: 'Wyłączono',
            QProcess.Starting: 'Startuje...',
            QProcess.Running: 'Uruchomiony',
        }
        state_name = states[state]
        self.statusTextEdit.appendPlainText(f"Zmieniono status: {state_name}")




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Konfigurator = QtWidgets.QMainWindow()
    ui = Ui_Konfigurator()
    ui.setupUi(Konfigurator)
    Konfigurator.show()
    sys.exit(app.exec_())

