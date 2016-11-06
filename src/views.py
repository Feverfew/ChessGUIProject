from PySide import QtCore, QtGui
import resources_rc

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
        self.load_btn = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.load_btn.setObjectName("load_btn")
        self.horizontalLayout_2.addWidget(self.load_btn)
        self.save_btn = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.save_btn.setObjectName("save_btn")
        self.horizontalLayout_2.addWidget(self.save_btn)
        self.chess_board = QtGui.QTableWidget(Form)
        self.chess_board.setGeometry(QtCore.QRect(10, 50, 640, 640))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chess_board.sizePolicy().hasHeightForWidth())
        self.chess_board.setSizePolicy(sizePolicy)
        self.chess_board.setAutoFillBackground(False)
        self.chess_board.setLineWidth(1)
        self.chess_board.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.chess_board.setTabKeyNavigation(False)
        self.chess_board.setProperty("showDropIndicator", False)
        self.chess_board.setDragDropOverwriteMode(False)
        self.chess_board.setAlternatingRowColors(False)
        self.chess_board.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.chess_board.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.chess_board.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.chess_board.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.chess_board.setGridStyle(QtCore.Qt.NoPen)
        self.chess_board.setCornerButtonEnabled(True)
        self.chess_board.setObjectName("chess_board")
        self.chess_board.setColumnCount(8)
        self.chess_board.setRowCount(8)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.chess_board.setHorizontalHeaderItem(7, item)
        self.chess_board.horizontalHeader().setVisible(False)
        self.chess_board.horizontalHeader().setStretchLastSection(False)
        self.chess_board.verticalHeader().setVisible(True)
        self.chess_board.verticalHeader().setDefaultSectionSize(30)
        self.chess_board.verticalHeader().setHighlightSections(False)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.player_one_label.setText(QtGui.QApplication.translate("Form", "Player 1:", None, QtGui.QApplication.UnicodeUTF8))
        self.player_two_label.setText(QtGui.QApplication.translate("Form", "Player 2:", None, QtGui.QApplication.UnicodeUTF8))
        self.load_btn.setText(QtGui.QApplication.translate("Form", "Load Game", None, QtGui.QApplication.UnicodeUTF8))
        self.save_btn.setText(QtGui.QApplication.translate("Form", "Save Game", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.verticalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "New Row", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.verticalHeaderItem(1).setText(QtGui.QApplication.translate("Form", "New Row", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.verticalHeaderItem(2).setText(QtGui.QApplication.translate("Form", "New Row", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.verticalHeaderItem(3).setText(QtGui.QApplication.translate("Form", "New Row", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.verticalHeaderItem(4).setText(QtGui.QApplication.translate("Form", "New Row", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.verticalHeaderItem(5).setText(QtGui.QApplication.translate("Form", "New Row", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.verticalHeaderItem(6).setText(QtGui.QApplication.translate("Form", "New Row", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.verticalHeaderItem(7).setText(QtGui.QApplication.translate("Form", "New Row", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Form", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Form", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Form", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("Form", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("Form", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.horizontalHeaderItem(6).setText(QtGui.QApplication.translate("Form", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.chess_board.horizontalHeaderItem(7).setText(QtGui.QApplication.translate("Form", "New Column", None, QtGui.QApplication.UnicodeUTF8))

class LoadDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 9, 381, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.sortby_box = QtGui.QComboBox(self.verticalLayoutWidget)
        self.sortby_box.setObjectName("sortby_box")
        self.sortby_box.addItem("")
        self.sortby_box.addItem("")
        self.horizontalLayout.addWidget(self.sortby_box)
        self.sort_btn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.sort_btn.setObjectName("sort_btn")
        self.horizontalLayout.addWidget(self.sort_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.game_table = QtGui.QTableWidget(self.verticalLayoutWidget)
        self.game_table.setObjectName("game_table")
        self.game_table.setColumnCount(0)
        self.game_table.setRowCount(0)
        self.verticalLayout.addWidget(self.game_table)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Open)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Sort by:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "Player 1 Name", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "Player 2 Name", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "Last Played", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(3, QtGui.QApplication.translate("Dialog", "ID", None, QtGui.QApplication.UnicodeUTF8))
        self.sortby_box.setItemText(0, QtGui.QApplication.translate("Dialog", "Descending", None, QtGui.QApplication.UnicodeUTF8))
        self.sortby_box.setItemText(1, QtGui.QApplication.translate("Dialog", "Ascending", None, QtGui.QApplication.UnicodeUTF8))
        self.sort_btn.setText(QtGui.QApplication.translate("Dialog", "Sort", None, QtGui.QApplication.UnicodeUTF8))



