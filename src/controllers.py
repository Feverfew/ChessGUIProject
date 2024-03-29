import copy
import datetime
import json
import re
from builtins import IOError, FileNotFoundError, TypeError

from PySide import QtGui, QtCore

import algorithms
import views
from board import Board
from pieces import *


class MainWindowController(QtGui.QMainWindow, views.MainWindow):
    """Controller for the main window of the application"""
    def __init__(self):
        super(MainWindowController, self).__init__()
        self.setupUi(self)
        self.setCentralWidget(ChessBoardController())
        self.show()


class ChessBoardController(QtGui.QWidget, views.ChessBoard):
    """Controller for the chess board.
    Attributes pertaining to the views.ChessBoard class are not listed here as there are too many
    and they merely refer to Qt GUI Objects.

    Attributes:
        board (Board): instance of the Board class which serves as the model for the controller.
        settings (QSettings): a class used to store settings (namely file path) on the host computer.
        from_cell (list): stores the coordinates of the cell that was chosen to move from.

    """
    def __init__(self):
        """Initialises necessary variables, connects click events to methods and presents a new game to the user."""
        super(ChessBoardController, self).__init__()
        self.setupUi(self)
        self.board = Board()
        self.settings = QtCore.QSettings("ComputingProjectAlex", "Chess")
        self.from_cell = []
        self.chess_board.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.chess_board.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.chess_board.horizontalHeader().hide()
        self.chess_board.verticalHeader().hide()
        self.output_board()
        self.chess_board.itemClicked.connect(self.table_clicked)
        self.new_btn.clicked.connect(self.new_game)
        self.save_btn.clicked.connect(self.save_game)
        self.load_btn.clicked.connect(self.load_game)

    def table_clicked(self):
        """Handler for when table is clicked.

        When a piece has been selected to move then its legal moves are calculated.
        These moves are then made clickable and highlighted yellow.
        If a user selects any of the highlighted colours then the piece is transferred to that position
        and a check of the game state occurs where any changes are shown in a msg box.
        Promotions, if necessary, are called in this method.
        """
        row = self.chess_board.currentRow()
        column = self.chess_board.currentColumn()
        if not self.from_cell and column != -1 and row != -1:  # Piece is selected
            self.from_cell = [row, column]
            self.output_board(self.board.calculate_legal_moves(self.board.board[row][column]))
        elif self.from_cell and column != -1 and row != -1:  # Piece is moved
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
                    if self.board.game_over and self.board.is_stalemate:
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
        """Output the board onto the GUI

        Uses the Board.board (2D list) to help populate the QTableWidget table.
        All pieces of the moving player are made clickable on the table.
        In addition, if there are legal moves specified they are all made clickable.

        Args:
            legal_moves (list): list of the legal moves a piece can make.
        """
        self.chess_board.clear()
        self.chess_board.setRowCount(8)
        self.chess_board.setColumnCount(8)
        for y in range(8):
            for x in range(8):
                if self.board.board[y][x]:
                    if self.board.turn == "Black" and self.board.board[y][x].colour == "Black":
                        item = QtGui.QTableWidgetItem()
                        item.setSizeHint(QtCore.QSize(80, 80))
                        item.setData(QtCore.Qt.DecorationRole,
                                     QtGui.QPixmap(":/pieces/{}".format(self.board.board[y][x].img_path)))
                        if (x+y) % 2 == 0:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209)))  # light
                        else:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156)))  # dark
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.chess_board.setItem(y, x, item)
                    elif self.board.turn == "White" and self.board.board[y][x].colour == "White":
                        item = QtGui.QTableWidgetItem()
                        item.setSizeHint(QtCore.QSize(80, 80))
                        item.setData(QtCore.Qt.DecorationRole,
                                     QtGui.QPixmap(":/pieces/{}".format(self.board.board[y][x].img_path)))
                        if (x+y) % 2 == 0:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209)))  # light
                        else:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156)))  # dark
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.chess_board.setItem(y, x, item)
                    else:
                        item = QtGui.QTableWidgetItem()
                        item.setSizeHint(QtCore.QSize(80, 80))
                        item.setData(QtCore.Qt.DecorationRole,
                                     QtGui.QPixmap(":/pieces/{}".format(self.board.board[y][x].img_path)))
                        if (x+y) % 2 == 0:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209)))  # light
                        else:
                            item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156)))  # dark
                        if [y, x] in legal_moves:
                            item.setFlags(QtCore.Qt.ItemIsEnabled)
                            item.setBackground(QtGui.QBrush(QtGui.QColor(227, 209, 16))) # highlight legal moves
                        else:
                            item.setFlags(QtCore.Qt.NoItemFlags)
                        self.chess_board.setItem(y, x, item)
                elif [y, x] in legal_moves:
                    item = QtGui.QTableWidgetItem()
                    item.setSizeHint(QtCore.QSize(80, 80))
                    item.setBackground(QtGui.QBrush(QtGui.QColor(227, 209, 16))) # highlight legal moves
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.chess_board.setItem(y, x, item)
                else:
                    item = QtGui.QTableWidgetItem()
                    item.setSizeHint(QtCore.QSize(80, 80))
                    if (x+y) % 2 == 0:
                        item.setBackground(QtGui.QBrush(QtGui.QColor(31, 177, 209)))  # light
                    else:
                        item.setBackground(QtGui.QBrush(QtGui.QColor(11, 129, 156)))  # dark
                    item.setFlags(QtCore.Qt.NoItemFlags)
                    self.chess_board.setItem(y, x, item)

    def new_game(self):
        """Creates a new game with initial board setup."""
        self.board = Board()
        self.from_cell = []
        self.output_board()
    
    def load_game(self):
        """Loads a game from a JSON file. If there is no JSON file the user is prompted for one.

        Raises:
            IOError: raised when there is an error loading a file.
            FileNotFoundError: raised when a file is not found.
            TypeError: raised when there is an error loading a file.
            KeyError: raised when there is corruption in the JSON file.
        """
        try:
            data = None
            with open(self.settings.value('json_location')) as json_file:
                data = json.load(json_file)
            game_loader = LoadDialogController(data)
            game_loader.exec()
            game = []
            if game_loader.chosen_game_id != 0:
                for temp_game in data['games']:
                    if game_loader.chosen_game_id == temp_game['id']:
                        game = temp_game
                        break
                self.board = Board(game)
                self.player_one_edit.setText(game['player_one'])
                self.player_two_edit.setText(game['player_two'])
                self.board.check_game_state()
                self.output_board()
                if self.board.game_over and self.board.is_stalemate:
                    self.show_message("Game is a draw. No one wins")
                elif self.board.game_over:
                    self.show_message("{} is the winner".format(self.board.winner))
                elif self.board.colour_in_check:
                    self.show_message("{} is in check".format(self.board.colour_in_check))
        except (IOError, FileNotFoundError, TypeError):
            self.show_message("Game file not found!")
            self.get_load_path()
            if self.settings.value:
                self.show_message("Press Load game again.")
        except (KeyError):
            self.show_message("Data file is corrupt. Please choose another file")
            self.get_load_path()
            if self.settings.value:
                self.load_game("Press Load game again.")

    def save_game(self):
        """Saves a currently played game, either in an existing JSON file or a new one.

        Raises:
            IOError: raised when there is an error loading a file.
            FileNotFoundError: raised when a file is not found.
        """
        if self.player_one_edit.text() != "" and self.player_two_edit.text() != "":
            self.board.player_one = self.player_one_edit.text()
            self.board.player_two = self.player_two_edit.text()
            self.board.check_game_state()
            if self.board.winner == "White":
                self.board.winner = self.player_one_edit.text()
            elif self.board.winner == "Black":
                self.board.winner = self.player_one_edit.text()
            now = datetime.datetime.now()
            year = str(now.year)
            month = int(now.month)
            day = int(now.day)
            if month < 10:
                month = "0" + str(month)
            else:
                month = str(month)
            if day < 10:
                day = "0" + str(day)
            else:
                day = str(day)
            game = {
                'id': self.board.id,
                'last_played': str(year + "/" + month + "/" + day),
                'turn': self.board.turn,
                'move_num': self.board.move_num,
                'winner': self.board.winner,
                'colour_in_check': self.board.colour_in_check,
                'is_stalemate': self.board.is_stalemate,
                'game_over': self.board.game_over,
                'must_promote': self.board.must_promote,
                'enpassant_possible': {
                    'Black': self.board.enpassant_possible['Black'],
                    'White': self.board.enpassant_possible['White']
                    },
                'enpassant_move': {
                    'from': self.board.enpassant_move['from'],
                    'to': self.board.enpassant_move['to'],
                    'taken': self.board.enpassant_move['taken']
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
            if self.settings.value('json_location'):
                try:
                    data = None
                    with open(self.settings.value('json_location')) as json_file:
                        data = json.load(json_file)
                    id_list = [x['id'] for x in data['games']]

                    algorithms.quick_sort(id_list, 0, len(id_list)-1)
                    if game['id']:
                        if algorithms.binary_search(game['id'], id_list):
                            for x in range(len(data['games'])):
                                if game['id'] == data['games'][x]['id']:
                                    data['games'][x] = game
                        else:
                            game['id'] = id_list[-1] + 1
                            self.board.id = id_list[-1] + 1
                            data['games'].append(game)
                    else:
                        game['id'] = id_list[-1] + 1
                        self.board.id = id_list[-1] + 1
                        data['games'].append(game)
                    with open(self.settings.value('json_location'), 'w') as jsonfile:
                        json.dump(data, jsonfile, indent=4, separators=(',', ':'))
                        self.show_message("Game saved at {}".format(self.settings.value('json_location')))
                except (IOError, FileNotFoundError):
                    self.show_message("Error: File not found")
                    self.settings.setValue("json_location", "")
                    self.save_game()
            else:
                self.get_save_path()
                if self.settings.value('json_location'):
                    data = {'games': []}
                    game['id'] = 1
                    self.board.id = 1
                    data['games'].append(game)
                    try:
                        with open(self.settings.value('json_location'), 'w') as jsonfile:
                            json.dump(data, jsonfile, indent=4, separators=(',', ':'))
                            self.show_message("Game saved at {}".format(self.settings.value('json_location')))
                    except (FileNotFoundError, OSError):
                        self.show_message("File not saved. Invalid file name.")
                        self.settings.setValue("json_location", "")
        else:
            self.show_message("Please fill in the player names")

    def get_load_path(self):
        """Gets the JSON file to load"""
        filepath = QtGui.QFileDialog().getOpenFileName(self, "Load Game", QtCore.QDir.homePath(),  "Game file (*.json)")
        if filepath[0]:
            self.settings.setValue("json_location", filepath[0])
        else:
            self.settings.setValue("json_location", "")
            self.show_message("File not chosen.")

    def get_save_path(self):
        """Gets the desired path and filename of the file to save."""
        filepath = QtGui.QFileDialog().getSaveFileName(self, "Save as", QtCore.QDir.homePath(), "Game file (*.json)")
        if filepath[0]:
            self.settings.setValue("json_location", filepath[0])
        else:
            self.settings.setValue("json_location", "")
            self.show_message("File not saved")

    def get_promotion_piece(self):
        """Gets the piece that needs to be promoted"""
        choice = ["", False]
        while not choice[1]:
            choice = QtGui.QInputDialog.getItem(self, "Piece to promote", "Choose piece:", ["Queen", "Knight", "Rook", "Bishop"], 0, False)
        return choice[0]
        
    def show_message(self, msg):
        """If there are errors, they are shown in a message box.

        Args:
            msg (str): message for the user to be shown.
            """
        msg_box = QtGui.QMessageBox()
        msg_box.setWindowTitle("Game State")
        msg_box.setText(msg)
        msg_box.exec_()


class LoadDialogController(QtGui.QDialog, views.LoadDialog):
    """Controller for the load dialog

    When 'Load Game' is pressed the user is shown this dialog if a JSON file is found and has been loaded.
    The user is shown a table where they can sort the games and can also choose which game to load.

    Attributes:
        chosen_game_id (int): id of the game that was chosen
        data (dict): List of games.
    """

    def __init__(self, data):
        """Necessary variables are initialised and table is shown to the user."""
        super(LoadDialogController, self).__init__()
        self.setupUi(self)
        self.chosen_game_id = 0
        self.data = data
        self.output_table()
        self.results_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.results_table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.sort_btn.clicked.connect(self.sort)

    def output_table(self):
        """List of games is shown to the user with this method."""
        self.results_table.setRowCount(0)
        self.buttonBox.accepted.connect(self.get_game)
        i = 0
        for game in self.data['games']:
            identifier = QtGui.QTableWidgetItem()
            identifier.setText(str(game['id']))
            player_one = QtGui.QTableWidgetItem()
            player_one.setText(game['player_one'])
            player_two = QtGui.QTableWidgetItem()
            player_two.setText(game['player_two'])
            winner = QtGui.QTableWidgetItem()
            winner.setText(game['winner'])
            moves_made = QtGui.QTableWidgetItem()
            moves_made.setText(str(game['move_num']-1))
            last_played = QtGui.QTableWidgetItem()
            last_played.setText(game['last_played'])
            self.results_table.insertRow(i)
            self.results_table.setItem(i, 0, identifier)
            self.results_table.setItem(i, 1, player_one)
            self.results_table.setItem(i, 2, player_two)
            self.results_table.setItem(i, 3, winner)
            self.results_table.setItem(i, 4, moves_made)
            self.results_table.setItem(i, 5, last_played)
            i += 1

    def sort(self):
        """Sorts the list of games"""
        sorted_games = []
        if self.sortby_box.currentText() == "Ascending":
            if self.sort_type.currentText() == "ID":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(int(self.results_table.item(x, 0).text()))
                algorithms.quick_sort(array, 0, len(array)-1)
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if array[i] == self.data['games'][j]['id']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['id'] = None
                            break
            elif self.sort_type.currentText() == "Player 1":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(self.results_table.item(x, 1).text())
                algorithms.quick_sort(array, 0, len(array)-1)
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if array[i] == self.data['games'][j]['player_one']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['player_one'] = None
                            break
            elif self.sort_type.currentText() == "Player 2":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(self.results_table.item(x, 2).text())
                algorithms.quick_sort(array, 0, len(array)-1)
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if array[i] == self.data['games'][j]['player_two']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['player_two'] = None
                            break
            elif self.sort_type.currentText() == "Winner":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(self.results_table.item(x, 3).text())
                algorithms.quick_sort(array, 0, len(array)-1)
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if array[i] == self.data['games'][j]['winner']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['winner'] = None
                            break
            elif self.sort_type.currentText() == "Moves Made":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(int(self.results_table.item(x, 4).text()))
                algorithms.quick_sort(array, 0, len(array)-1)
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if int(array[i])+1 == self.data['games'][j]['move_num']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['move_num'] = None
                            break
            elif self.sort_type.currentText() == "Last Played":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(self.results_table.item(x, 5).text())
                algorithms.quick_sort(array, 0, len(array)-1)
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if array[i] == self.data['games'][j]['last_played']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['last_played'] = None
                            break
        else:
            if self.sort_type.currentText() == "ID":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(int(self.results_table.item(x, 0).text()))
                algorithms.quick_sort(array, 0, len(array)-1)
                array = array[::-1]  # reverse list
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if array[i] == self.data['games'][j]['id']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['id'] = None
                            break
            elif self.sort_type.currentText() == "Player 1":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(self.results_table.item(x, 1).text())
                algorithms.quick_sort(array, 0, len(array)-1)
                array = array[::-1]  # reverse list
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if array[i] == self.data['games'][j]['player_one']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['player_one'] = None
                            break
            elif self.sort_type.currentText() == "Player 2":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(self.results_table.item(x, 2).text())
                algorithms.quick_sort(array, 0, len(array)-1)
                array = array[::-1]  # reverse list
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if array[i] == self.data['games'][j]['player_two']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['player_two'] = None
                            break
            elif self.sort_type.currentText() == "Winner":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(self.results_table.item(x, 3).text())
                algorithms.quick_sort(array, 0, len(array)-1)
                array = array[::-1]  # reverse list
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if array[i] == self.data['games'][j]['winner']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['winner'] = None
                            break
            elif self.sort_type.currentText() == "Moves Made":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(int(self.results_table.item(x, 4).text()))
                algorithms.quick_sort(array, 0, len(array)-1)
                array = array[::-1]  # reverse list
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if int(array[i])+1 == self.data['games'][j]['move_num']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['move_num'] = None
                            break
            elif self.sort_type.currentText() == "Last Played":
                array = []
                for x in range(self.results_table.rowCount()):
                    array.append(self.results_table.item(x, 5).text())
                algorithms.quick_sort(array, 0, len(array)-1)
                array = array[::-1]  # reverse list
                sorted_games = [None] * len(array)
                for i in range(len(array)):
                    for j in range(len(self.data['games'])):
                        if array[i] == self.data['games'][j]['last_played']:
                            sorted_games[i] = copy.deepcopy(self.data['games'][j])
                            self.data['games'][j]['last_played'] = None
                            break
        self.data['games'] = sorted_games
        self.output_table()

    def get_game(self):
        """When game is chosen the ID is then found."""
        if self.results_table.currentRow() != -1:
            self.chosen_game_id = int(self.results_table.item(self.results_table.currentRow(), 0).text())
        else: # if no game selected
            self.chosen_game_id = 0 # Will not attempt to load game if it is 0.
