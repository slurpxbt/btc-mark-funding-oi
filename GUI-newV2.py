###########################

# Author: slurpxbt

##########################
# import any missing packages
#TODO: change file paths in rows 107 and 125


####################################################

# simple GUI for btc and eth perpetual futures data

###################################################

from PyQt5 import QtCore, QtGui, QtWidgets
import pause
from datetime import datetime
import time
import oi_mark_funding as exchange_data
from pathlib import Path

class Worker(QtCore.QRunnable):

    def run(self):
        i = 0
        min15 = 60 * 15
        # while true needs to run on separate thread in order for window to not crash
        while True:
            start_time = time.time()   # timestap

            i = i + 1
            print(f"getting data #{i}")

            exchange_data.get_and_store_btc_data() 
            exchange_data.get_and_store_eth_data()

            exe_time = time.time() - start_time             # calculates script execution time
            print(f"script execution time was: {exe_time}s")
            print(f"script will sleep {(min15 - exe_time)/60} minutes")
            time.sleep(min15 - exe_time)                    # subtracts script execution time from time interval so we don't get data request delays
            QtWidgets.QApplication.processEvents()
            print("----------------------------NEW OI DATA-------------------------------")

class Ui_MainWindow(object):

    def start_threadpool(self):
        # threadpool setup
        self.threadpool = QtCore.QThreadPool()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1159, 1490)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Start button
        self.StartBtn = QtWidgets.QPushButton(self.centralwidget)
        self.StartBtn.setGeometry(QtCore.QRect(20, 20, 351, 71))
        self.StartBtn.setObjectName("StartBtn")

        self.StartBtn.clicked.connect(self.clicked)
        self.StartBtn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # list view (data is shown in here)
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(20, 110, 1111, 1331))
        self.listView.setObjectName("listView")
        self.listView.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # btc data button
        self.btcBtn = QtWidgets.QPushButton(self.centralwidget)
        self.btcBtn.setGeometry(QtCore.QRect(400, 20, 351, 71))
        self.btcBtn.setObjectName("btcBtn")

        self.btcBtn.clicked.connect(self.load_btc_data)
        self.btcBtn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # eth data button
        self.ethBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ethBtn.setGeometry(QtCore.QRect(780, 20, 351, 71))
        self.ethBtn.setObjectName("ethBtn")

        self.ethBtn.clicked.connect(self.load_eth_data)
        self.ethBtn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1159, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Perpetual futures data"))
        self.StartBtn.setText(_translate("MainWindow", "START"))
        self.btcBtn.setText(_translate("MainWindow", "BTC"))
        self.ethBtn.setText(_translate("MainWindow", "ETH"))

    def clicked(self):
            worker = Worker()
            self.threadpool.start(worker)

    def load_btc_data(self):
        
        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)
        root = Path(".")
        data_file_path = "YOUR PATH"
        with open(f"{data_file_path}/data storage/avgMark_cumOI_oiWfunding_storage.txt") as btc:

            Lines_btc = btc.readlines()

            for i in range(len(Lines_btc)):
                        
                elements_btc = Lines_btc[i].split(";")
                data = [float(elements_btc[0]),float(elements_btc[1]),float(elements_btc[2]), elements_btc[3]]
                display_format = f"Contract=BTC\t mark price={round(data[0], 2)}\t OI={round(data[1], 3)} mil\t funding={data[2]} %\t date={data[3]}"
                item = QtGui.QStandardItem(display_format)
                model.appendRow(item)


    def load_eth_data(self):
        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)
        root = Path(".")
        data_file_path = "YOUR PATH"
        with open(f"{data_file_path}/data storage/avgMark_cumOI_oiWfunding_storage_eth.txt") as eth:
            
            Lines_eth = eth.readlines()

            for i in range(len(Lines_eth)):
                elements_eth = Lines_eth[i].split(";")
                data = [float(elements_eth[0]),float(elements_eth[1]),float(elements_eth[2]), elements_eth[3]]
                display_format = f"Contract=ETH\t mark price={round(data[0], 2)}\t\t OI={round(data[1], 3)} mil\t funding={data[2]} %\t date={data[3]}"
                item = QtGui.QStandardItem(display_format)
                model.appendRow(item)






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.start_threadpool()
    ui.setupUi(MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec_())
