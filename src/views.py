from PySide import QtCore, QtGui

class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(660, 800)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 660, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))

class ChessBoard(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(660, 800)
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 10, 641, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.player_one_label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.player_one_label.setObjectName("player_one_label")
        self.horizontalLayout.addWidget(self.player_one_label)
        self.player_one_edit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.player_one_edit.setObjectName("player_one_edit")
        self.horizontalLayout.addWidget(self.player_one_edit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.player_two_label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.player_two_label.setObjectName("player_two_label")
        self.horizontalLayout.addWidget(self.player_two_label)
        self.player_two_edit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.player_two_edit.setObjectName("player_two_edit")
        self.horizontalLayout.addWidget(self.player_two_edit)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 700, 641, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.submit_btn = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.submit_btn.setObjectName("submit_btn")
        self.horizontalLayout_2.addWidget(self.submit_btn)
        self.chess_board = QtGui.QTableWidget(Form)
        self.chess_board.setGeometry(QtCore.QRect(10, 50, 640, 640))
        self.chess_board.setObjectName("chess_board")
        self.chess_board.setColumnCount(0)
        self.chess_board.setRowCount(0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.player_one_label.setText(QtGui.QApplication.translate("Form", "Player 1:", None, QtGui.QApplication.UnicodeUTF8))
        self.player_two_label.setText(QtGui.QApplication.translate("Form", "Player 2:", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_btn.setText(QtGui.QApplication.translate("Form", "Submit Move", None, QtGui.QApplication.UnicodeUTF8))

