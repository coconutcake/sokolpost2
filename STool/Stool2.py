# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GH.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import requests
import threading, os, time
import datetime
import json

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(390, 365)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(390, 365))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/ignat/Downloads/sokol_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("C:/Users/ignat/Downloads/sokol_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        Dialog.setWindowIcon(icon)
        Dialog.setAutoFillBackground(False)
        Dialog.setSizeGripEnabled(False)
        self.Sendbtn = QtWidgets.QPushButton(Dialog)
        self.Sendbtn.setGeometry(QtCore.QRect(20, 310, 161, 41))
        self.Sendbtn.setObjectName("Sendbtn")
        self.Exitbtn = QtWidgets.QPushButton(Dialog)
        self.Exitbtn.setGeometry(QtCore.QRect(200, 310, 171, 41))
        self.Exitbtn.setObjectName("Exitbtn")
        self.StatusLbl = QtWidgets.QLabel(Dialog)
        self.StatusLbl.setGeometry(QtCore.QRect(80, 40, 291, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.StatusLbl.setFont(font)
        self.StatusLbl.setAutoFillBackground(False)
        self.StatusLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.StatusLbl.setObjectName("StatusLbl")
        self.LoginLbl = QtWidgets.QLabel(Dialog)
        self.LoginLbl.setGeometry(QtCore.QRect(20, 120, 47, 13))
        self.LoginLbl.setObjectName("LoginLbl")
        self.PasswdLbl = QtWidgets.QLabel(Dialog)
        self.PasswdLbl.setGeometry(QtCore.QRect(200, 120, 47, 13))
        self.PasswdLbl.setObjectName("PasswdLbl")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(20, 170, 351, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setEnabled(True)
        self.line_2.setGeometry(QtCore.QRect(20, 80, 351, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.line_2.setFont(font)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(290, 190, 81, 81))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/Users/ignat/Downloads/72385251_1555436987929960_6835200397271891968_o.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.LoginInput = QtWidgets.QLineEdit(Dialog)
        self.LoginInput.setGeometry(QtCore.QRect(20, 140, 161, 20))
        self.LoginInput.setObjectName("LoginInput")
        self.PasswdLine = QtWidgets.QLineEdit(Dialog)
        self.PasswdLine.setGeometry(QtCore.QRect(200, 140, 171, 20))
        self.PasswdLine.setObjectName("PasswdLine")
        self.checkBoxAssign = QtWidgets.QCheckBox(Dialog)
        self.checkBoxAssign.setEnabled(True)
        self.checkBoxAssign.setGeometry(QtCore.QRect(20, 190, 131, 17))
        self.checkBoxAssign.setChecked(False)
        self.checkBoxAssign.setObjectName("checkBoxAssign")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setGeometry(QtCore.QRect(20, 240, 161, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 220, 111, 16))
        self.label_2.setObjectName("label_2")
        self.line_3 = QtWidgets.QFrame(Dialog)
        self.line_3.setGeometry(QtCore.QRect(20, 280, 351, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 71, 71))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("C:/Users/ignat/Downloads/sokol_logo.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Wpisz kompletne dane logowania!")
        self.msg.setWindowTitle("Brak danych logowania")



        self.retranslateUi(Dialog)
        self.checkBoxAssign.toggled['bool'].connect(self.lineEdit.setEnabled)
        self.Exitbtn.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "STool"))
        self.Sendbtn.setText(_translate("Dialog", "Wyślij moją konfiguracje"))
        self.Exitbtn.setText(_translate("Dialog", "Wyjdź"))
        self.StatusLbl.setText(_translate("Dialog", "Status: Oczekuje na wysłanie"))
        self.LoginLbl.setText(_translate("Dialog", "Login:"))
        self.PasswdLbl.setText(_translate("Dialog", "Hasło:"))
        self.checkBoxAssign.setText(_translate("Dialog", "Przypisz do zlecenia"))
        self.label_2.setText(_translate("Dialog", "Nr zlecenia:"))


if __name__ == "__main__":
    import sys
    import platform
    import psutil
    from datetime import datetime

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)


    class Request():
        def __init__(self, token, url="https://192.168.1.172/getharwareinfo/"):
            self.token = token
            self.url = url
            self._running = True
            self.status = False
        def run(self):
            print("uruchomiono")
            print("TOKEN: %s" % self.token)

            # boot
            boot_time_timestamp = psutil.boot_time()
            bt = datetime.fromtimestamp(boot_time_timestamp)
            
            print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
            print("Physical cores:", psutil.cpu_count(logical=False))
            print("Total cores:", psutil.cpu_count(logical=True))


            # CPU
            cpufreq = psutil.cpu_freq()
            # print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
            # print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
            # print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
            # CPU usage
            # print("CPU Usage Per Core:")
            # for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
            #     print(f"Core {i}: {percentage}%")
            # print(f"Total CPU Usage: {psutil.cpu_percent()}%")

            svmem = psutil.virtual_memory()
            def get_size(bytes, suffix="B"):
                """
                Scale bytes to its proper format
                e.g:
                    1253656 => '1.20MB'
                    1253656678 => '1.17GB'
                """
                factor = 1024
                for unit in ["", "K", "M", "G", "T", "P"]:
                    if bytes < factor:
                        return f"{bytes:.2f}{unit}{suffix}"
                    bytes /= factor

            # swap
            # print(f"Total: {get_size(svmem.total)}")
            # print(f"Available: {get_size(svmem.available)}")
            # print(f"Used: {get_size(svmem.used)}")
            # print(f"Percentage: {svmem.percent}%")
            # print("="*20, "SWAP", "="*20)
            # get the swap memory details (if exists)
            swap = psutil.swap_memory()
            # print(f"Total: {get_size(swap.total)}")
            # print(f"Free: {get_size(swap.free)}")
            # print(f"Used: {get_size(swap.used)}")
            # print(f"Percentage: {swap.percent}%")


            # Disk Information
            # print("="*40, "Disk Information", "="*40)
            # print("Partitions and Usage:")
            # get all disk partitions
            partitions = psutil.disk_partitions()
            partitions_list = []

            for partition in partitions:
                partition_ = {}
                # print(f"=== Device: {partition.device} ===")
                # print(f"  Mountpoint: {partition.mountpoint}")
                # print(f"  File system type: {partition.fstype}")

                partition_['device'] = partition.device
                partition_['mountpoint'] = partition.mountpoint
                partition_['file_system'] = partition.fstype

                

                try:

                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    partition_['disk_usage'] = psutil.disk_usage(partition.mountpoint)
                except PermissionError:
                    # this can be catched due to the disk that
                    # isn't ready
                    continue
                # print(f"  Total Size: {get_size(partition_usage.total)}")
                # print(f"  Used: {get_size(partition_usage.used)}")
                # print(f"  Free: {get_size(partition_usage.free)}")
                # print(f"  Percentage: {partition_usage.percent}%")

                partition_['total_size'] = get_size(partition_usage.total)
                partition_['used_size'] = get_size(partition_usage.used)
                partition_['free_size'] = get_size(partition_usage.free)
                partition_['percentage_size'] = partition_usage.percent

                partitions_list.append(partition_.copy())
                # print(partition_)

            # get IO statistics since boot
            disk_io = psutil.disk_io_counters()
            # print(f"Total read: {get_size(disk_io.read_bytes)}")
            # print(f"Total write: {get_size(disk_io.write_bytes)}")

            # print("-"%30)
            # print(partitions_list)
            # print("-"*30)


            # Network information

            print("="*40, "Network Information", "="*40)
            # get all network interfaces (virtual and physical)
            if_addrs = psutil.net_if_addrs()
            interfaces = []

            for interface_name, interface_addresses in if_addrs.items():
                interface = {}
                interface['interface'] = interface_name
                interface['adress'] = interface_addresses
                interfaces.append(interface)
                

                


            data = {
                'login': ui.LoginInput.text(),
                'passwd': ui.PasswdLine.text(),
                'platform': platform.machine(),
                'platform_version': platform.version(),
                'platform_os': platform.platform(),
                'platform_uname': platform.uname(),
                'platform_system': platform.system(),
                'cpu': platform.processor(),
                'cpu_physical_cores': psutil.cpu_count(logical=False),
                'cpu_total_cores': psutil.cpu_count(logical=True),
                'cpu_min': cpufreq.min,
                'cpu_max': cpufreq.max,
                'boot_time': "%s/%s/%s %s:%s:%s" % (bt.year, bt.month, bt.day, bt.hour, bt.minute, bt.second),
                'svem_total': get_size(svmem.total),
                'svem_free': get_size(svmem.available),
                'svem_used': get_size(svmem.used),
                'svem_percentage': svmem.percent,
                'swap_total': get_size(swap.total),
                'swap_free': get_size(swap.free),
                'swap_used': get_size(swap.used),
                'swap_percentage': swap.percent,
                'partitions': partitions_list,
                'net': interfaces,

                }

            ui.StatusLbl.setText('Status: Konwertuje JSON...')
            json_data = json.dumps(data, sort_keys=True, indent=4)
            print(json_data)

            responce = requests.post(url = self.url, data=json_data, verify=False)
            ui.StatusLbl.setText('Status: Wysłano JSON...')
            
            # Konwertuj na json
            get_json = json.loads(responce.text)
            if get_json['logged']:
                ui.StatusLbl.setText('Status: Poprawnie zalogowano')
            else:
                ui.StatusLbl.setText('Status: Nie udało sie zalogować!')
            
            try:
                if get_json['exists']:
                    ui.StatusLbl.setText('Status: Sprzęt znaleziony! aktualizuje...')
                else:    
                    ui.StatusLbl.setText('Status: Dodaje nowy sprzet...!')
            except:
                pass

            if responce.status_code == 200 and get_json['logged'] == True:
                print("%s" % responce.text)
                ui.Sendbtn.setText('Wysłano!')
                ui.Sendbtn.setEnabled(False)
                ui.StatusLbl.setText('Status: Poprawnie wysłano konfiguracje!')
                ui.StatusLbl.setStyleSheet("color: green;")
                ui.LoginInput.setEnabled(False)
                ui.PasswdLine.setEnabled(False)
                ui.checkBoxAssign.setEnabled(False)

                

            else: 
                print("Nie wysłano")
                if get_json['logged'] == False:
                    ui.StatusLbl.setText('Status: Błąd logowania - niepoprawne dane')
                    ui.StatusLbl.setStyleSheet("color: redn;")
                else:
                    ui.StatusLbl.setText('Status: Błąd połączenia z hostem')
                    ui.StatusLbl.setStyleSheet("color: redn;")



        def terminate(self): 
            self._running = False

        def start(self):
            self.thread = threading.Thread(target=self.run, args=())
            self.thread.daemon = True                            # Daemonize thread
            self._running = True
            self.thread.start()
    
    def send_click():
        print("to jest %s" % ui.lineEdit.text() )
        if ui.LoginInput.text() == '' or ui.PasswdLine.text() == '':
            print("brak danych logowania!")
            ui.msg.show()
            ui.StatusLbl.setText('Status: Brak danych logowania!')
            ui.StatusLbl.setStyleSheet("color: redn;")
        else:
            ui.StatusLbl.setText('Status: Wysyłam...')
            r = Request(ui.lineEdit.text())
            r.start()

    ui.Sendbtn.clicked.connect(send_click)

    Dialog.show()
    sys.exit(app.exec_())
