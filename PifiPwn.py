# Imports

from PyQt5 import QtWidgets as widget
from PyQt5 import QtCore as core
import sys
import re
import iwlist
import time
from PyQt5 import QtGui as gui
import subprocess


# Global Configuration Options #

# === PifiAP === #
APInterface = "wlan0"
APName = "PifiAP"
APPassword = "12345678"

# == PifiPwn === #
PwnInterface = "wlan1"
PwnTimeout = 10
PwnWordlist = "wordlist.txt"

###############################


class BaseWindow(widget.QMainWindow):
    """ Main Window class"""
    def __init__(self):
        """ Initiates the Base Window UI"""

        super().__init__()
        self.startUI()

    def startUI(self):
        """ Starts the User Interface """

        # PifiPwn Button
        self.PifiPwnStart = widget.QPushButton("PifiPwn", self)
        self.PifiPwnStart.setGeometry(core.QRect(10, 25, 70, 25))
        self.PifiPwnStart.clicked.connect(self.pwnWindow)

        # PifiPwn Features Label
        self.PifiPwnLabel = widget.QLabel(self)
        self.PifiPwnLabel.setText("Features:\nCapture WPA Handshakes\nSend Deauth Packets\nCrack WPA Key")
        self.PifiPwnLabel.setGeometry(10, 40, 200, 70)
        self.PifiPwnLabel.setStyleSheet("font-size:10px")

        # Wireless AP Button
        self.WifiAPStart = widget.QPushButton("Wireless AP", self)
        self.WifiAPStart.setGeometry(10, 145, 90, 25)
        self.WifiAPStart.clicked.connect(self.openAP)
        self.WifiAPStart.setStyleSheet("font-size:10px")

        # Exit Button
        self.exitButton = widget.QPushButton("Exit", self)
        self.exitButton.setGeometry(core.QRect(10, 170, 60, 25))
        self.exitButton.clicked.connect(self.closeWindow)

        # Resize to fit Screen
        self.resize(300, 200)

        # Self.show() = Display at Resolution, Use showMaximized for Full-Screen

        #self.show()
        self.showMaximized()

    def closeWindow(self):
        """ Closes current Window"""

        self.close()

    def pwnWindow(self):
        """ Shows the PifiPwn Window"""

        self.PifipwnWindow = PwnWindow(self)
        self.PifipwnWindow.show()

    def openAP(self):
        """ Shows the Access Point Window"""
        self.apOpen = APWindow(self)
        self.apOpen.show()

class APWindow(widget.QMainWindow):
    """ Access Point Window Class"""
    def __init__(self, parent):
        super().__init__(parent)

        # Start Access Point Button
        self.startAPButton = widget.QPushButton("Start AP", self)
        self.startAPButton.setGeometry(core.QRect(10, 10, 60, 28))
        self.startAPButton.clicked.connect(self.startAP)
        self.startAPButton.setStyleSheet("font-size: 11px;")

        # Stop Access Point Button
        self.stopAPButton = widget.QPushButton("Stop AP", self)
        self.stopAPButton.setGeometry(core.QRect(80, 10, 60, 28))
        self.stopAPButton.setStyleSheet("font-size: 11px;")
        self.stopAPButton.clicked.connect(self.stopAP)


        checkMon = subprocess.getoutput("iwconfig")

        # Checks if AP is already started and sets buttons correctly
        if "Mode:Master" in checkMon:
            self.startAPButton.setStyleSheet("font-size:11px; border:1px solid green;")
            self.startAPButton.setDisabled(True)
            self.stopAPButton.setDisabled(False)
        else:
            self.stopAPButton.setStyleSheet("font-size:11px;border:1px solid red;")
            self.startAPButton.setDisabled(False)
            self.stopAPButton.setDisabled(True)

        # Refresh Connected Clients Button
        self.reClients = widget.QPushButton("Refresh", self)
        self.reClients.setGeometry(core.QRect(150, 10, 60, 28))
        self.reClients.setStyleSheet("font-size: 11px;")
        self.reClients.clicked.connect(self.refreshAP)

        # Exit Button
        self.exitButton = widget.QPushButton("Exit", self)
        self.exitButton.setGeometry(core.QRect(210, 10, 60, 28))
        self.exitButton.clicked.connect(self.closeWindow)
        self.exitButton.setStyleSheet("font-size: 11px;")


        # Connected Clients Table
        self.getClientsTable = widget.QTableWidget(self)
        self.getClientsTable.setGeometry(core.QRect(10, 50, 260, 100))
        self.getClientsTable.setColumnCount(3)
        self.rowCount = 1
        self.getClientsTable.setRowCount(self.rowCount)
        self.getClientsTable.setStyleSheet("font-size: 9px")
        self.getClientsTable.setHorizontalHeaderLabels(["MAC", "IP", "Hostname"])
        self.getClientsTable.resizeColumnsToContents()

        # AP Process (to call create_ap)
        self.apProcess = core.QProcess(self)

        # Resize Window
        self.resize(300, 200)

        self.showMaximized()

    def closeWindow(self):
        """ Close Current Window"""
        self.close()

    def startAP(self):
        """ Starts Access Point
        - Can easily set it to load a config file, instead of all details in the connection
        """

        # Start Create_AP Process & Set Button Colours
        # Uses QProcess().startDetached so we can still do other functions on the Qt Window
        self.apProcess.startDetached("create_ap {} eth0 {} {} --hostapd-debug 1 --daemon".format(APInterface, APName, APPassword))
        self.startAPButton.setDisabled(True)
        self.startAPButton.setStyleSheet("font-size: 11px; border:1px solid green;")
        self.stopAPButton.setDisabled(False)
        self.stopAPButton.setStyleSheet("font-size:11px;")

    def stopAP(self):
        # Stop AP Process & Set Buttons
        subprocess.getoutput("create_ap --stop {}".format(APInterface))
        self.stopAPButton.setDisabled(True)
        self.stopAPButton.setStyleSheet("font-size:11px; border:1px solid red;")
        self.startAPButton.setDisabled(False)
        self.startAPButton.setStyleSheet("font-size:11px;")

    def refreshAP(self):
        """ Refresh list of Connected Clients"""
        data = subprocess.getoutput("create_ap --list-clients {}".format(APInterface))
        dataS = data.splitlines()[1:]
        self.getClientsTable.setRowCount(len(dataS))
        curCol = 0
        curRow = 0
        for i in dataS:
            curCol = 0
            cData = i.split()
            for z in cData:
                self.getClientsTable.setItem(int(curRow), int(curCol), widget.QTableWidgetItem("{}".format(z)))
                curCol = curCol + 1
            curRow = curRow + 1
        self.getClientsTable.resizeColumnsToContents()



class PwnWindow(widget.QMainWindow):
    """PifiPwn Main Class"""
    def __init__(self, parent):
        super().__init__(parent)

        # Scan AP Button
        self.scanAPButton = widget.QPushButton("Scan APs", self)
        self.scanAPButton.setGeometry(core.QRect(10, 80, 70, 25))
        self.scanAPButton.clicked.connect(self.showAP)
        self.scanAPButton.setStyleSheet("font-size: 10px;")

        # Capture Handshakes Button
        self.captureHSButton = widget.QPushButton("Capture Handshakes", self)
        self.captureHSButton.setGeometry(core.QRect(160, 80,110, 25))
        self.captureHSButton.setStyleSheet("font-size: 10px;")
        self.captureHSButton.clicked.connect(self.capHS)

        checkMon = subprocess.getoutput("iwconfig")

        # Start Mon0 Button
        self.mon0start = widget.QPushButton("Start Monitor", self)
        self.mon0start.setGeometry(core.QRect(140, 8, 70, 25))
        self.mon0start.clicked.connect(self.startMon0)
        self.mon0start.setStyleSheet("font-size: 10px;")

        # Stop Mon0 Button
        self.mon0stop = widget.QPushButton("Stop Monitor", self)
        self.mon0stop.setGeometry(core.QRect(210, 8, 70, 25))
        self.mon0stop.clicked.connect(self.stopMon0)
        self.mon0stop.setStyleSheet("font-size: 10px;")

        # Checks if Monitor Mode is already enabled, and sets up Button Colours
        if "Mode:Monitor" in checkMon:
            self.mon0start.setStyleSheet("font-size:10px; border:1px solid green;")
            self.mon0start.setDisabled(True)
            self.mon0stop.setDisabled(False)
        else:
            self.mon0stop.setStyleSheet("font-size:10px;border:1px solid red;")
            self.mon0start.setDisabled(False)
            self.mon0stop.setDisabled(True)

        # Loaded AP Text QLine
        self.loadAPText = widget.QLineEdit(self)
        self.loadAPText.setEnabled(False)
        self.loadAPText.setGeometry(core.QRect(10, 45, 290, 30))
        self.loadAPText.setText("Scan APs then click on the Access Point to Load")
        self.loadAPText.setStyleSheet("background: gold; font-size:10px; color:black;")

        # AP Label
        self.loadedAPLabel = widget.QLabel("BSSID::SSID::Channel::Encryption", self)
        self.loadedAPLabel.setGeometry(core.QRect(15, 25, 200, 25))
        self.loadedAPLabel.setStyleSheet("font-size: 9px;")

        # DeAuth Button
        self.deAuthButton = widget.QPushButton("Send Deauth Packets", self)
        self.deAuthButton.setGeometry(core.QRect(10, 105, 110, 25))
        self.deAuthButton.clicked.connect(self.deAuth)
        self.deAuthButton.setStyleSheet("font-size: 10px;")

        # Crack WPA Handshakes Button
        self.crackWPAButton = widget.QPushButton("Crack WPA Password", self)
        self.crackWPAButton.setGeometry(core.QRect(160, 105, 110, 25))
        self.crackWPAButton.setStyleSheet("font-size: 10px;")
        self.crackWPAButton.clicked.connect(self.crackWPA)

        # Results QList Model
        self.resultModel = widget.QListView(self)
        self.resultModel.setGeometry(core.QRect(10, 135, 200, 90))
        self.resultModel.setStyleSheet("font-size: 12px;")

        # Results Item Model
        self.ff = gui.QStandardItemModel(self.resultModel)
        self.resultModel.setModel(self.ff)
        self.resultModel.clicked.connect(self.test)

        # QProcess
        self.daProcess = core.QProcess(self)

        self.hsProcess = core.QProcess(self)
        self.hsProcess.readyReadStandardOutput.connect(self.hstdoutReady)
        #self.hsProcess.readyReadStandardError.connect(self.hstderrReady)

        self.process = core.QProcess(self)
        self.process.readyReadStandardOutput.connect(self.stdoutReady)
        self.process.readyReadStandardError.connect(self.stderrReady)

        # Exit Button
        self.exitButton = widget.QPushButton("Exit", self)
        self.exitButton.setGeometry(core.QRect(220, 190, 60, 25))
        self.exitButton.clicked.connect(self.closeWindow)

        self.resize(310, 210)
        self.showMaximized()
        #self.show()

    def closeWindow(self):
        """ Closes current Window"""
        self.close()

    def crackWPA(self):
        """ Bruteforce WPA Handshake with Password List"""

        self.process.start('aircrack-ng', ['{}-01.ivs'.format(self.bssid),'-b','{}'.format(self.bssid),'-w','{}'.format(PwnWordlist)])


    def deAuth(self):
        """ Send Deauthentication Packets """
        self.daProcess.startDetached("timeout {} aireplay-ng -0 2 -a {} {}mon".format(PwnTimeout, self.bssid, PwnInterface))

    def test(self, index):
        """ Sets the Loaded AP -- Gotta rename this"""
        item = self.ff.item(index.row(),index.column())
        self.bssid = item.data(256)
        self.essid = item.data(257)
        self.channel = item.data(258)
        self.encryption = item.data(259)
        info = "{} :: {} :: {} :: {}".format(self.bssid, self.essid, self.channel, self.encryption)
        self.loadAPText.setText(info)
        self.loadAPText.setStyleSheet("background: LawnGreen; color:black; font-size:12px;")


    def capHS(self):
        """ Capture Handshakes with Airodump, save to output file BSSID.ivs"""
        print(self.bssid, self.channel, self.essid)
        # Delete all previous Captured ivs dumps
        subprocess.getoutput("rm *.ivs")
        self.process.start("timeout", ['{}'.format(PwnTimeout), 'airodump-ng', '--ivs', '-c', '{}'.format(self.channel),
                                       '--bssid', '{}'.format(self.bssid),  '-w', '{}'.format(self.bssid), '{}mon'.format(PwnInterface)])

    def hstdoutReady(self):
        text = str(self.hsProcess.readAll())
        #print(text)
        for line in text.split("\n"):
            print(line)
            if "handshake" in line:
                print(line)
                self.loadAPText.setText("Captured WPA Handshake")
                self.loadAPText.setStyleSheet("font-size:10px; color:black; background: LawnGreen;")


    def startMon0(self):
        """ Start Monitor mode on wlan0 Interface"""
        subprocess.getoutput("airmon-ng start {} {}".format(PwnInterface,self.channel))
        self.mon0start.setDisabled(True)
        self.mon0start.setStyleSheet("font-size:10px; border:1px solid green;")
        self.mon0stop.setDisabled(False)

    def stopMon0(self):
        """ Stop Monitor Mode on wlan0 Interface"""
        subprocess.getoutput("airmon-ng stop {}mon".format(PwnInterface))

        # Bugs out on Raspberry Pi so we gotta put the Interface back up after disabling Monitor Mode
        subprocess.getoutput("ifconfig {} up".format(PwnInterface))
        self.mon0stop.setDisabled(True)
        self.mon0stop.setStyleSheet("font-size:10px; border:1px solid red;")
        self.mon0start.setDisabled(False)

    def showAP(self):
        """ Displays Access Points in Range"""
        print("Scanning APs - May take several seconds\n")
        scan = iwlist.scan("{}".format(PwnInterface))
        # Set a timeout before Parsing, If there's multiple APs it may not find them all
        time.sleep(3)
        # Parse iwlist Output to a easily readable Dictionary
        parse = iwlist.parse(scan)

        # Clear AP List each time this function is called (ScanAP Button)
        self.ff.clear()
        try:
            for i in parse:
                item = gui.QStandardItem(str(i["essid"]))
                bssid = str(i["mac"])

                essid = str(i["essid"])
                channel = str(i["channel"])
                encryption = str(i["encryption"])
                item.setData(bssid, 256)
                item.setData(essid, 257)
                item.setData(channel, 258)
                item.setData(encryption, 259)

                self.ff.appendRow(item)
        except KeyError:
            print("KeyError")
            pass


    def append(self, text):
        self.loadAPText.setText(text)
        self.loadAPText.setStyleSheet("color:black; font-size:12px; background-color: LawnGreen;")

    def stdoutReady(self):
        #b'[00:00:01] 1248/5000 keys tested (1004.27 k/s) \x1b[6;7H'
        # KEY FOUND! [ 12345678 ]\n\x1b[11B'
        text = str(self.process.readAll())
        #print(text)
        for line in text.split("\n\n"):
            if 'tested' in line:
                #self.append(str(line[2:-10]))
                # Regex to strip unwanted ANSI Characters, unfortunately doesn't work as we'd like it to
                esc = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
                #esc = re.compile(r'\x1b\[[0-9;]*m//g')
                lnew = esc.sub('', line)
                self.append(str(lnew[2:-10]))

            elif "FOUND" in line:
                self.append(str(line[-34:-11]))
                self.loadAPText.setStyleSheet("background-color:gold; font-size:11px; color:black;")



    def stderrReady(self):
        text = str(self.process.readAllStandardError())
        #print(text)
        #print(text.strip())
        if "handshake" in text:
            self.loadAPText.setText("Captured WPA Handshake!")
            self.loadAPText.setStyleSheet("font-size:10px; background-color: LawnGreen; color:black;")


if __name__ == "__main__":  # Initiates Script
        app = widget.QApplication(sys.argv)
        baseWin = BaseWindow()
        app.exec_()
