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
        self.chess_board.cellClicked.connect(self.table_clicked)

    def enable_disable_buttons(self, legal_moves=[]):
        """Enable cells where there are pieces or if the move is legal"""
        for y in range(8):
            for x in range(8):
                if self.board.board[y][x]:
                    if self.board.move_num % 2 == 0 and self.board.board[y][x].colour == "Black":
                        item = self.chess_board.itemAt(y, x)
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.chess_board.setItem(y, x, item)
                    elif self.board.move_num % 2 != 0 and self.board.board[y][x].colour == "White":
                        item = self.chess_board.itemAt(y, x)
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.chess_board.setItem(y, x, item)
                    else:
                        item = self.chess_board.itemAt(y, x)
                        item.setFlags(QtCore.Qt.NoItemFlags)
                        self.chess_board.setItem(y, x, item)
        for move in legal_moves:
            item = self.chess_board.itemAt(move[0], move[1])
            item.setFlags(QtCore.Qt.NoItemFlags)
            self.chess_board.setItem(move[0], move[1], item)


    def table_clicked(self, row, column):
        if not self.from_cell and not self.to_cell:
            self.from_cell = [row, column]
            self.enable_disable_buttons(self.board.calculate_legal_moves(self.board.board[row][column]))
        elif self.from_cell and not self.to_cell:
            self.board.move_piece(self.board, from_cell, [row, column])
            self.output_board()
            self.from_cell = []

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
                """font = QtGui.QFont()
                font.setPixelSize(80)
                font.setFamily("Arial")
                item.setFont(font)"""
                if (x+y) % 2 == 0:
                    item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209))) # light
                else:
                    item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156))) # dark
                if self.board.board[y][x]:
                    item.setIcon(QtGui.QIcon(self.board.board[y][x].img_path))
                    item.setText(self.board.board[y][x].img_path)
                self.chess_board.setItem(y, x, item)
