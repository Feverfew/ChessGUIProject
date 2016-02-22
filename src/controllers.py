from PySide import QtGui, QtCore
import views
from board import Board

class MainWindowController(QtGui.QMainWindow, views.MainWindow): 
    """Controller for the main window of the application"""
    def __init__(self):
        super(MainWindowController, self).__init__()
        self.setupUi(self)
        self.setCentralWidget(ChessBoardController())
        self.show()

class ChessBoardController(QtGui.QWidget, views.ChessBoard):
    """Controller for the chess board"""
    def __init__(self):
        super(ChessBoardController, self).__init__()
        self.setupUi(self)
        self.board = Board()
        self.from_cell = []
        self.to_cell = []
        self.initialise_board()
        self.output_board()

    def initialise_board(self):  
        self.chess_board.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.chess_board.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.chess_board.horizontalHeader().hide()
        self.chess_board.verticalHeader().hide()
        for y in range(8):
            for x in range(8):
                item = QtGui.QTableWidgetItem()
                if (x+y) % 2 == 0:
                    item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209)))
                else:
                    item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156)))
                self.chess_board.setItem(y, x, item)

    def output_board(self):
        """Output the board onto the GUI"""
        for y in range(8):
            for x in range(8):
                item = QtGui.QTableWidgetItem()
                item.setSizeHint(QtCore.QSize(80, 80))
                font = QtGui.QFont()
                font.setPixelSize(80)
                font.setFamily("Arial")
                item.setFont(font)
                if (x+y) % 2 == 0:
                    item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209))) # light
                else:
                    item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156))) # dark
                if self.board.board[y][x]:
                    item.setText(str(self.board.board[y][x]))
                self.chess_board.setItem(y, x, item)
