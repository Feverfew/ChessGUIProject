from PySide import QtGui, QtCore
import views
from board import Board
from pieces import *
import json
import datetime
from builtins import IOError

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
        self.settings = QtCore.QSettings("ComputingProjectAlex", "Chess")
        self.json_location = self.settings.value("json_location")
        self.from_cell = []
        self.chess_board.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.chess_board.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.chess_board.horizontalHeader().hide()
        self.chess_board.verticalHeader().hide()
        self.output_board()
        self.chess_board.itemClicked.connect(self.table_clicked)
        self.save_btn.clicked.connect(self.save_game)

    def table_clicked(self):
        """Handler for when table is clicked"""
        row = self.chess_board.currentRow()
        column = self.chess_board.currentColumn()
        if not self.from_cell and column != -1 and row != -1: # Piece is selected
            self.from_cell = [row, column]
            self.output_board(self.board.calculate_legal_moves(self.board.board[row][column]))
        elif self.from_cell and column != -1 and row != -1: # Piece is moved
            if self.board.board[row][column]:
                if self.board.board[self.from_cell[0]][self.from_cell[1]].colour == self.board.board[row][column].colour:
                    self.from_cell = [row, column]
                    self.output_board(self.board.calculate_legal_moves(self.board.board[row][column]))
                else:
                    self.board.board = self.board.permanently_move_piece(self.board.board, self.from_cell, [row, column])
                    if self.board.must_promote:
                        self.board.permanently_promote_piece(self.get_promotion_piece(), [row, column])
                    self.board.check_game_state()
                    self.output_board()
                    self.from_cell = []
                    if  self.board.game_over and self.board.is_stalemate:
                        self.show_message("Game is a draw. No one wins")
                    elif self.board.game_over:
                        self.show_message("{} is the winner".format(self.board.winner))
                    elif self.board.colour_in_check:
                        self.show_message("{} is in check".format(self.board.colour_in_check))
            else:
                self.board.board = self.board.permanently_move_piece(self.board.board, self.from_cell, [row, column])
                if self.board.must_promote:
                    self.board.permanently_promote_piece(self.get_promotion_piece(), [row, column])
                self.board.check_game_state()
                self.output_board()
                self.from_cell = []
                if self.board.game_over and self.board.is_stalemate:
                    self.show_message("Game is a draw. No one wins")
                elif self.board.game_over:
                    self.show_message("{} is the winner".format(self.board.winner))
                elif self.board.colour_in_check:
                    self.show_message("{} is in check".format(self.board.colour_in_check))

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
                        item.setIcon(QtGui.QIcon(":/pieces/{}".format(self.board.board[y][x].img_path)))
                        if (x+y) % 2 == 0:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209))) # light
                        else:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156))) # dark
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.chess_board.setItem(y, x, item)
                    elif self.board.turn == "White" and self.board.board[y][x].colour == "White":
                        item = QtGui.QTableWidgetItem()
                        item.setSizeHint(QtCore.QSize(80, 80))
                        item.setIcon(QtGui.QIcon(":/pieces/{}".format(self.board.board[y][x].img_path)))
                        if (x+y) % 2 == 0:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209))) # light
                        else:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156))) # dark
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.chess_board.setItem(y, x, item)
                    else:
                        item = QtGui.QTableWidgetItem()
                        item.setSizeHint(QtCore.QSize(80, 80))
                        item.setIcon(QtGui.QIcon(":/pieces/{}".format(self.board.board[y][x].img_path)))
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
                    if (x+y) % 2 == 0:
                        item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209))) # light
                    else:
                        item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156))) # dark
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.chess_board.setItem(y, x, item)
                else:
                    item = QtGui.QTableWidgetItem()
                    item.setSizeHint(QtCore.QSize(80, 80))
                    if (x+y) % 2 == 0:
                        item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209))) # light
                    else:
                        item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156))) # dark
                    item.setFlags(QtCore.Qt.NoItemFlags)
                    self.chess_board.setItem(y, x, item)

    def save_game(self):
        if self.player_one_edit.text() != "" and self.player_two_edit.text() != "":
            self.board.player_one = self.player_one_edit.text()
            self.board.player_two = self.player_two_edit.text()
            game = {
                'id': None,
                'last_played': str(datetime.datetime.now()),
                'turn': self.board.turn,
                'move_num': self.board.move_num,
                'winner': self.board.winner,
                'colour_in_check': self.board.colour_in_check,
                'is_stalemate': self.board.is_stalemate,
                'game_over': self.board.game_over,
                'must_promote': self.board.must_promote,
                'has_been_in_check': {
                    'Black': self.board.has_been_in_check['Black'],
                    'White': self.board.has_been_in_check['White']
                    },
                'enpassent_possible': {
                    'Black': self.board.enpassent_possible['Black'],
                    'White': self.board.enpassent_possible['White']
                    },
                'enpassent_move': {
                    'from': self.board.enpassent_move['from'],
                    'to': self.board.enpassent_move['to'],
                    'taken': self.board.enpassent_move['taken']
                    },
                'can_castle': {
                    'Black': self.board.can_castle['Black'],
                    'White': self.board.can_castle['White']
                },
                'player_one': self.board.player_one,
                'player_two': self.board.player_two,
                'pieces': {
                    'kings': [],
                    'queens': [],
                    'knights': [],
                    'bishops': [],
                    'rooks': [],
                    'pawns': []
                }
            }
            for row in self.board.board:
                for field in row:
                    if field:
                        if isinstance(field, Queen):
                            piece = {
                                'position': field.position,
                                'colour': field.colour
                            }
                            game['pieces']['queens'].append(piece)
                        elif isinstance(field, Bishop):
                            piece = {
                                'position': field.position,
                                'colour': field.colour
                            }
                            game['pieces']['bishops'].append(piece)
                        elif isinstance(field, Knight):
                            piece = {
                                'position': field.position,
                                'colour': field.colour
                            }
                            game['pieces']['knights'].append(piece)
                        elif isinstance(field, Rook):
                            piece = {
                                'position': field.position,
                                'colour': field.colour,
                                'has_moved': field.has_moved
                            }
                            game['pieces']['rooks'].append(piece)
                        elif isinstance(field, King):
                            piece = {
                                'position': field.position,
                                'colour': field.colour,
                                'has_moved': field.has_moved,
                                'castling_moves': field.castling_moves
                            }
                            game['pieces']['kings'].append(piece)
                        elif isinstance(field, Pawn):
                            piece = {
                                'position': field.position,
                                'colour': field.colour,
                                'first_moved': field.first_moved
                            }
                            game['pieces']['pawns'].append(piece)
            if self.json_location:
                try:
                    data = None
                    with open(self.json_location) as json_file:    
                        data = json.load(json_file)
                    id_list = [x['id'] for x in data['games']]

                    self.quick_sort(id_list)
                    if game['id']:
                        if self.binary_search(game['id'], id_list):
                            for x in range(len(data['games'])):
                                if game['id'] == data['games'][x]['id']:
                                    data['games'][x] = game
                    else:
                        game['id'] = id_list[-1] + 1
                        data['games'].append(game)
                    with open(self.json_location, 'w') as jsonfile:
                        json.dump(data, jsonfile, indent=4, separators=(',', ':'))
                #TODO Finish this whole section
                except IOError as e:
                    self.show_message("Error: File not found")
                    self.json_location = ""
            else:
                invalid = True
                while invalid:
                        json_dir = QtGui.QFileDialog().getExistingDirectory()
                        json_name = QtGui.QInputDialog.getText(self, "JSON File Name Input", "JSON File Name:")
                        if json_dir and json_name[1]:
                            invalid = False
                        else:
                            self.show_message("Please fill in save directory and name")

                self.json_location = "{}\{}.json".format(json_dir, json_name[0])
                self.settings.setValue("json_location", self.json_location)
                data = {'games': []}
                game['id'] = 1
                data['games'].append(game)
                with open(self.json_location, 'w') as jsonfile:
                    json.dump(data, jsonfile, indent=4, separators=(',', ':'))
        else:
            self.show_message("Please fill in the player names")

    def binary_search(self, search_term, array):
        """Searches for an item in an already sorted list."""
        found = False
        while len(array) > 1 and found == False:
            half_array = int(len(array)/2)
            if search_term == array[half_array]:
                found = True
            elif search_term > array[half_array]:
                array = array[half_array:]
            else:
                array = array[:half_array]
        return found

    def quick_sort(self, array, low=0, high=None):
        """Sorts a list using the quicksort algorithm"""
        def split(array, low, high):
            pivot = array[low]
            i = low + 1
            j = high
            while True:
                while i <= j  and array[i] <= pivot:
                    i +=1
                while j >= i and array[j] >= pivot:
                    j -=1
                if j <= i:
                    break
                array[i], array[j] = array[j], array[i]
            array[low], array[j] = array[j], array[low]
            return j
        if not high:
            high = len(array) - 1
        if high <= low:
            return
        else:
            s = split(array, low, high)
            self.quick_sort(array, low, s - 1)
            self.quick_sort(array, s + 1, high)

    def get_promotion_piece(self):
        """Gets the piece that needs to be promoted"""
        choice = ["", False]
        while not choice[1]:
            choice = QtGui.QInputDialog.getItem(self, "Piece to promote", "Choose piece:", ["Queen", "Knight", "Rook", "Bishop"], 0, False)
        return choice[0]
        
    def show_message(self, msg):
        """If there are errors show them in a message box."""
        msg_box = QtGui.QMessageBox()
        msg_box.setWindowTitle("Game State")
        msg_box.setText(msg)
        msg_box.exec_()

