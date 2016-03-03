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
        self.chess_board.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.chess_board.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.chess_board.horizontalHeader().hide()
        self.chess_board.verticalHeader().hide()
        self.output_board()
        self.chess_board.itemClicked.connect(self.table_clicked)

    def table_clicked(self):
        row = self.chess_board.currentRow()
        column = self.chess_board.currentColumn()
        if not self.from_cell and column != -1 and row != -1:
            print("from: ({},{})".format(row, column))
            self.from_cell = [row, column]
            self.output_board(self.board.calculate_legal_moves(self.board.board[row][column]))
        elif self.from_cell and column != -1 and row != -1:
            if self.board.board[row][column]:
                if self.board.board[self.from_cell[0]][self.from_cell[1]].colour == self.board.board[row][column].colour:
                    self.from_cell = [row, column]
                    self.output_board(self.board.calculate_legal_moves(self.board.board[row][column]))
                else:
                    self.board.board = self.board.permanently_move_piece(self.board.board, self.from_cell, [row, column])
                    print("from: {} to: {},{}".format(self.from_cell, row, column))
                    self.output_board()
                    self.from_cell = []
            else:
                self.board.board = self.board.permanently_move_piece(self.board.board, self.from_cell, [row, column])
                print("from: {} to: {},{}".format(self.from_cell, row, column))
                self.output_board()
                self.from_cell = []


    def output_board(self, legal_moves=[]):
        """Output the board onto the GUI"""
        self.chess_board.clear()
        self.chess_board.setRowCount(8)
        self.chess_board.setColumnCount(8)
        for y in range(8):
            for x in range(8):
                if self.board.board[y][x]:
                    if self.board.turn == "Black" and self.board.board[y][x].colour == "Black":
                        item = QtGui.QTableWidgetItem()
                        item.setSizeHint(QtCore.QSize(80, 80))
                        font = QtGui.QFont()
                        font.setPixelSize(40)
                        font.setFamily("Arial Unicode MS")
                        item.setFont(font)
                        item.setText(str(self.board.board[y][x]))
                        if (x+y) % 2 == 0:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209))) # light
                        else:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156))) # dark
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.chess_board.setItem(y, x, item)
                    elif self.board.turn == "White" and self.board.board[y][x].colour == "White":
                        item = QtGui.QTableWidgetItem()
                        item.setSizeHint(QtCore.QSize(80, 80))
                        font = QtGui.QFont()
                        font.setPixelSize(40)
                        font.setFamily("Arial Unicode MS")
                        item.setFont(font)
                        item.setText(str(self.board.board[y][x]))
                        if (x+y) % 2 == 0:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209))) # light
                        else:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156))) # dark
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.chess_board.setItem(y, x, item)
                    else:
                        item = QtGui.QTableWidgetItem()
                        item.setSizeHint(QtCore.QSize(80, 80))
                        font = QtGui.QFont()
                        font.setPixelSize(40)
                        font.setFamily("Arial Unicode MS")
                        item.setFont(font)
                        item.setText(str(self.board.board[y][x]))
                        if (x+y) % 2 == 0:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209))) # light
                        else:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156))) # dark
                        if [y, x] in legal_moves:
                            item.setFlags(QtCore.Qt.ItemIsEnabled)
                        else:
                            item.setFlags(QtCore.Qt.NoItemFlags)
                        self.chess_board.setItem(y, x, item)
                elif [y, x] in legal_moves:
                    item = QtGui.QTableWidgetItem()
                    item.setSizeHint(QtCore.QSize(80, 80))
                    font = QtGui.QFont()
                    font.setPixelSize(40)
                    font.setFamily("Arial Unicode MS")
                    item.setFont(font)
                    if (x+y) % 2 == 0:
                        item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209))) # light
                    else:
                        item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156))) # dark
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.chess_board.setItem(y, x, item)
                else:
                    item = QtGui.QTableWidgetItem()
                    item.setSizeHint(QtCore.QSize(80, 80))
                    font = QtGui.QFont()
                    font.setPixelSize(40)
                    font.setFamily("Arial Unicode MS")
                    item.setFont(font)
                    if (x+y) % 2 == 0:
                        item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209))) # light
                    else:
                        item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156))) # dark
                    item.setFlags(QtCore.Qt.NoItemFlags)
                    self.chess_board.setItem(y, x, item)
        
    def show_message(self, msg):
        """If there are errors show them in a message box."""
        msg_box = QtGui.QMessageBox()
        msg_box.setWindowTitle("Game State")
        msg_box.setText(msg)
        msg_box.exec_()
