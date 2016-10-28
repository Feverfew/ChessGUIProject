from pieces import *
import copy
__author__ = "Alexander Saoutkin"

class Board(object):
    """Class which manages the pieces on the board."""

    def __init__(self, player_one="", player_two=""):
        self.id = None
        self.last_played = None
        self.turn = "White"
        self.move_num = 1
        self.winner = ""
        self.colour_in_check = ""
        self.is_stalemate = False
        self.game_over = False
        self.must_promote = False
        self.has_been_in_check = {
            'Black': False,
            'White': False
        }
        self.enpassent_possible = {
            'Black': True,
            'White': True
            }
        self.can_castle = {
            'Black': True,
            'White': True
            }
        self.enpassent_move = {
            'from': [],
            'to': [],
            'taken': []
            }
        self.player_one = player_one
        self.player_two = player_two
        self.new_board()

    def new_board(self):
        """Creates a new fresh board"""
        self.board = []
        # Black side of the board
        row = [
            Rook([0,0], "Black"),
            Knight([0,1], "Black"),
            Bishop([0,2], "Black"),
            Queen([0,3], "Black"),
            King([0,4], "Black"),
            Bishop([0,5], "Black"),
            Knight([0,6], "Black"),
            Rook([0,7], "Black")
        ]
        self.board.append(row)
        row = [
            Pawn([1,0], "Black"),
            Pawn([1,1], "Black"),
            Pawn([1,2], "Black"),
            Pawn([1,3], "Black"),
            Pawn([1,4], "Black"),
            Pawn([1,5], "Black"),
            Pawn([1,6], "Black"),
            Pawn([1,7], "Black")
        ]
        self.board.append(row)
        # Add empty space
        for i in range(4):
            row = [0 for x in range(8)]
            self.board.append(row)
        # Add white pieces
        row = [
            Pawn([6,0], "White"),
            Pawn([6,1], "White"),
            Pawn([6,2], "White"),
            Pawn([6,3], "White"),
            Pawn([6,4], "White"),
            Pawn([6,5], "White"),
            Pawn([6,6], "White"),
            Pawn([6,7], "White")
        ]
        self.board.append(row)
        row = [
            Rook([7,0], "White"),
            Knight([7,1], "White"),
            Bishop([7,2], "White"),
            Queen([7,3], "White"),
            King([7,4], "White"),
            Bishop([7,5], "White"),
            Knight([7,6], "White"),
            Rook([7,7], "White")
        ]
        self.board.append(row)
     
    def preliminary_move_piece(self, chess_board, old_coords, new_coords):
        """"Will move a piece temporarily. e.g. used to see if piece puts itself in check."""
        chess_board[new_coords[0]][new_coords[1]] = copy.deepcopy(chess_board[old_coords[0]][old_coords[1]])
        chess_board[old_coords[0]][old_coords[1]] = 0
        if isinstance(chess_board[new_coords[0]][new_coords[1]], Piece):
            chess_board[new_coords[0]][new_coords[1]].position = [new_coords[0], new_coords[1]]
            chess_board[new_coords[0]][new_coords[1]].calculate_possible_moves()
        return chess_board

    def preliminary_enpassent(self, chess_board, old_coords, new_coords, removed_coords):
        """Will perform enpassent on a chess board and return that board."""
        chess_board[new_coords[0]][new_coords[1]] = copy.deepcopy(chess_board[old_coords[0]][old_coords[1]])
        chess_board[old_coords[0]][old_coords[1]] = 0
        chess_board[removed_coords[0]][removed_coords[1]] = 0
        if isinstance(chess_board[new_coords[0]][new_coords[1]], Piece):
            chess_board[new_coords[0]][new_coords[1]].position = [new_coords[0], new_coords[1]]
            chess_board[new_coords[0]][new_coords[1]].calculate_possible_moves()
        return chess_board

    def permanently_move_piece(self, chess_board, old_coords, new_coords):
        """Moves a piece on the board permanently. 
        It will also check for change in game state (checkmate, check, stalemate)."""
        if not self.game_over:
            # Performs enpassent if conditions are met.
            if old_coords == self.enpassent_move['from'] and new_coords == self.enpassent_move['to'] and self.enpassent_possible[self.turn]:
                chess_board[self.enpassent_move['to'][0]][self.enpassent_move['to'][1]] = copy.deepcopy(chess_board[old_coords[0]][old_coords[1]])
                chess_board[old_coords[0]][old_coords[1]] = 0
                chess_board[self.enpassent_move['taken'][0]][self.enpassent_move['taken'][1]] = 0
                if isinstance(chess_board[new_coords[0]][new_coords[1]], Piece):
                    chess_board[new_coords[0]][new_coords[1]].position = [new_coords[0], new_coords[1]]
                    chess_board[new_coords[0]][new_coords[1]].calculate_possible_moves()
                self.enpassent_possible[self.turn] = False
                self.enpassent_move['from'] = []
                self.enpassent_move['to'] = []
                self.enpassent_move['taken'] = []
            elif isinstance(chess_board[old_coords[0]][old_coords[1]], King):
                chess_board[new_coords[0]][new_coords[1]] = copy.deepcopy(self.board[old_coords[0]][old_coords[1]])
                chess_board[old_coords[0]][old_coords[1]] = 0
                # If legal move is castling move, perform castling...
                if new_coords in chess_board[new_coords[0]][new_coords[1]].castling_moves:
                    if old_coords[0] == 0:
                        if new_coords[1] == 2:
                            chess_board[0][3] = copy.deepcopy(self.board[0][0])
                            chess_board[0][3].position = [0, 3]
                            chess_board[0][3].calculate_possible_moves()
                            chess_board[0][0] = 0
                        else:
                            chess_board[0][5] = copy.deepcopy(self.board[0][7])
                            chess_board[0][5].position = [0, 5]
                            chess_board[0][5].calculate_possible_moves()
                            chess_board[0][7] = 0
                    else:
                        if new_coords[1] == 2:
                            chess_board[7][3] = copy.deepcopy(self.board[7][0])
                            chess_board[7][3].position = [7, 3]
                            chess_board[7][3].calculate_possible_moves()
                            chess_board[7][0] = 0
                        else:
                            chess_board[7][5] = copy.deepcopy(self.board[7][7])
                            chess_board[7][5].position = [7, 5]
                            chess_board[7][5].calculate_possible_moves()
                            chess_board[7][7] = 0
            else:
                # if enpassent possible but not done, then can never be done again.
                if self.enpassent_move['from'] and self.enpassent_move['to']:
                    self.enpassent_possible[self.turn] = False
                    self.enpassent_move['from'] = []
                    self.enpassent_move['to'] = []
                    self.enpassent_move['taken'] = []
                chess_board[new_coords[0]][new_coords[1]] = copy.deepcopy(self.board[old_coords[0]][old_coords[1]])
                chess_board[old_coords[0]][old_coords[1]] = 0
            if isinstance(chess_board[new_coords[0]][new_coords[1]], Pawn):
                chess_board[new_coords[0]][new_coords[1]].first_moved = self.move_num
                if chess_board[new_coords[0]][new_coords[1]].colour == "Black" and new_coords[0] == 7:
                    self.must_promote = True
                elif chess_board[new_coords[0]][new_coords[1]].colour == "White" and new_coords[0] == 0:
                    self.must_promote = True

            elif isinstance(chess_board[new_coords[0]][new_coords[1]], Rook) or isinstance(chess_board[new_coords[0]][new_coords[1]], King):
                # Won't work for rook when castling, but that doesn't matter as king has already moved, so can't castle anyway
                chess_board[new_coords[0]][new_coords[1]].has_moved = True
            self.move_num += 1
            if self.move_num % 2 == 0:
                self.turn = "Black"
            else:
                self.turn = "White"
            if isinstance(chess_board[new_coords[0]][new_coords[1]], Piece):
                chess_board[new_coords[0]][new_coords[1]].position = [new_coords[0], new_coords[1]]
                chess_board[new_coords[0]][new_coords[1]].calculate_possible_moves()
            return chess_board

    def permanently_promote_piece(self, type, coords):
        colour = self.board[coords[0]][coords[1]].colour
        if type == "Queen":
            self.board[coords[0]][coords[1]] = Queen(coords, colour)
            self.board[coords[0]][coords[1]].position = coords
            self.board[coords[0]][coords[1]].calculate_possible_moves()
        elif type == "Knight":
            self.board[coords[0]][coords[1]] = Knight(coords, colour)
            self.board[coords[0]][coords[1]].position = coords
            self.board[coords[0]][coords[1]].calculate_possible_moves()
        elif type == "Rook":
            self.board[coords[0]][coords[1]] = Rook(coords, colour)
            self.board[coords[0]][coords[1]].position = coords
            self.board[coords[0]][coords[1]].calculate_possible_moves()
        elif type == "Bishop":
            self.board[coords[0]][coords[1]] = Bishop(coords, colour)
            self.board[coords[0]][coords[1]].position = coords
            self.board[coords[0]][coords[1]].calculate_possible_moves()
        self.must_promote = False

    def check_game_state(self):
        if self.calculate_is_checkmate(self.turn, self.board):
            self.game_over = True
            if self.turn == "Black":
                self.winner = "White"
            else:
                self.winner = "Black"
            self.has_been_in_check[self.turn] = True
        elif self.is_in_check(self.turn, self.board):
            self.colour_in_check = self.turn
            self.has_been_in_check[self.turn] = True
        elif self.calculate_is_stalemate(self.turn, self.board):
            self.is_stalemate = True
            self.game_over = True
        else:
            self.colour_in_check = ""


    def get_king_coords(self, colour, board):
        """Finds the coords of the king depending on its colour"""
        for x in range(8):
            for y in range(8):
                if isinstance(board[x][y], King) and board[x][y].colour == colour:
                    return [x, y]

    def calculate_legal_moves(self, piece):
        """Get all the legal moves of a piece and returns them"""
        legal_moves = []
        original_board = copy.deepcopy(self.board) # fixed the moving bug.
        possible_legal_moves = self.get_attacking_moves(piece, original_board)
        if not isinstance(piece, Pawn):
            for move in possible_legal_moves:
                original_board = copy.deepcopy(self.board)
                if isinstance(original_board[move[0]][move[1]], Piece) and not isinstance(original_board[move[0]][move[1]], King):
                    if not piece.colour == original_board[move[0]][move[1]].colour:
                        possible_board = self.preliminary_move_piece(original_board, piece.position, move)
                        if not self.is_in_check(piece.colour, possible_board):
                            legal_moves.append(move)
                elif not isinstance(original_board[move[0]][move[1]], King):
                    possible_board = self.preliminary_move_piece(original_board, piece.position, move)
                    if not self.is_in_check(piece.colour, possible_board):
                        legal_moves.append(move)
            if isinstance(piece, King):
                original_board = copy.deepcopy(self.board)
                self.get_castling_moves(piece, original_board)
                if piece.castling_moves:
                    for move in piece.castling_moves:
                        legal_moves.append(move)
        else:
            # vertical legal moves for pawn
            if piece.colour == "White":
                if piece.position[0] > 0 and not isinstance(original_board[piece.position[0]-1][piece.position[1]], Piece):
                    possible_board = self.preliminary_move_piece(original_board, piece.position, [piece.position[0]-1, piece.position[1]])
                    if not self.is_in_check(piece.colour, possible_board):
                        legal_moves.append([piece.position[0]-1, piece.position[1]])
                original_board = copy.deepcopy(self.board)
                if piece.position[0] == 6 and not isinstance(original_board[piece.position[0]-2][piece.position[1]], Piece):
                    possible_board = self.preliminary_move_piece(original_board, piece.position, [piece.position[0]-2, piece.position[1]])
                    if not (self.is_in_check(piece.colour, possible_board) or isinstance(original_board[piece.position[0]-1][piece.position[1]], Piece)):
                        legal_moves.append([piece.position[0]-2, piece.position[1]])
            else:
                if piece.position[0] < 7 and not isinstance(original_board[piece.position[0]+1][piece.position[1]], Piece):
                    possible_board = self.preliminary_move_piece(original_board, piece.position, [piece.position[0]+1, piece.position[1]])
                    if not self.is_in_check(piece.colour, possible_board):
                        legal_moves.append([piece.position[0]+1, piece.position[1]])
                original_board = copy.deepcopy(self.board)
                if piece.position[0] == 1 and not isinstance(original_board[piece.position[0]+2][piece.position[1]], Piece):
                    possible_board = self.preliminary_move_piece(original_board, piece.position, [piece.position[0]+2, piece.position[1]])
                    if not(self.is_in_check(piece.colour, possible_board) or isinstance(original_board[piece.position[0]+1][piece.position[1]], Piece)):
                        legal_moves.append([piece.position[0]+2, piece.position[1]])
            # When pawn moves diagonally to take piece
            for move in possible_legal_moves:
                original_board = copy.deepcopy(self.board)
                if isinstance(original_board[move[0]][move[1]], Piece) and not isinstance(original_board[move[0]][move[1]], King):
                    possible_board = self.preliminary_move_piece(original_board, piece.position, move)
                    if not self.is_in_check(piece.colour, possible_board):
                        legal_moves.append(move)
            # If enpassent is possible, adds as a possible move.
            self.can_enpassent(piece, original_board)
            if self.enpassent_move['to']:
                    legal_moves.append(self.enpassent_move['to'])
        return legal_moves

    def get_attacking_moves(self, piece, board):
        """
        Get all the attacking moves of a piece and return them.
        The difference between this function and get_legal_moves is that
        this shows you what pieces can force a check while the other functions
        tells you whether the piece can move there.
        """
        legal_moves = []
        illegal_moves = []
        illegal_moves.append(piece.position)
        def get_legal_moves():
            for move in piece.possible_moves:
                if move not in illegal_moves:
                    legal_moves.append(move)
            return legal_moves
        if isinstance(piece, Rook):
            for move in piece.possible_moves:
                # If there is a piece in the way
                if board[move[0]][move[1]]:
                    # If piece in the way is above
                    if piece.position[0] > move[0]:
                        # Then it cannot influence anything above that piece
                        for i in range(move[0]):
                            if [i, move[1]] not in illegal_moves:
                                illegal_moves.append([i, move[1]])
                    # If piece in the way is below
                    elif piece.position[0] < move[0]:
                        # Then it cannot influence anything below that piece
                        for i in range(7, move[0], -1):
                            if [i, move[1]] not in illegal_moves:
                                illegal_moves.append([i, move[1]])
                    # If piece in the way is to the left
                    elif piece.position[1] > move[1]:
                        # Then it cannot influence anything to the left
                        for i in range(move[1]):
                            if [move[0], i] not in illegal_moves:
                                illegal_moves.append([move[0], i])
                    # If piece in the way is to the right
                    elif piece.position[1] < move[1]:
                        # Then it cannot influence anything to the right
                        for i in range(7, move[1], -1):
                            if [move[0], i] not in illegal_moves:
                                illegal_moves.append([move[0], i])
            return get_legal_moves()
        elif isinstance(piece, Bishop):
            for move in piece.possible_moves:
                if board[move[0]][move[1]]:
                    counter = 0
                    # If piece in the way is north-west
                    if piece.position[0] > move[0] and piece.position[1] > move[1]:
                        # Then it cannot influence anything north-west
                        while move[0]-counter != 0 and move[1]-counter != 0:
                            counter += 1
                            if [move[0]-counter, move[1]-counter] not in illegal_moves:
                                illegal_moves.append([move[0]-counter, move[1]-counter])
                    # If piece in the way is north-east
                    elif piece.position[0] > move[0] and piece.position[1] < move[1]:
                        # Then it cannot influence anything north-east
                        while move[0]-counter != 0 and move[1]+counter != 7:
                            counter += 1
                            if [move[0]-counter, move[1]+counter] not in illegal_moves:
                                illegal_moves.append([move[0]-counter, move[1]+counter])
                    # If piece in the way is south-west
                    elif piece.position[0] < move[0] and piece.position[1] > move[1]:
                        # Then it cannot influence anything south-west
                        while move[0]+counter != 7 and move[1]-counter != 0:
                            counter += 1
                            if [move[0]+counter, move[1]-counter] not in illegal_moves:
                                illegal_moves.append([move[0]+counter, move[1]-counter])
                    # If piece in the way is south-east
                    elif piece.position[0] < move[0] and piece.position[1] < move[1]:
                        # Then it cannot influence anything south-east
                        while move[0]+counter != 7 and move[1]+counter != 7:
                            counter += 1
                            if [move[0]+counter, move[1]+counter] not in illegal_moves:
                                illegal_moves.append([move[0]+counter, move[1]+counter])
            return get_legal_moves()
        # This function is a combination of Rook and Bishop
        elif isinstance(piece, Queen):
            for move in piece.possible_moves:
                if board[move[0]][move[1]]:
                    counter = 0
                    # If piece in the way is above
                    if piece.position[0] > move[0] and piece.position[1] == move[1]:
                        # Then it cannot influence anything above it
                        for i in range(move[0]):
                            if [i, move[1]] not in illegal_moves:
                                illegal_moves.append([i, move[1]])
                    # If piece in the way is below
                    elif piece.position[0] < move[0] and piece.position[1] == move[1]:
                        # Then it cannot influence below it...
                        for i in range(7, move[0], -1):
                            if [i, move[1]] not in illegal_moves:
                                illegal_moves.append([i, move[1]])
                    # If piece in the way is to the left
                    elif piece.position[1] > move[1] and piece.position[0] == move[0]:
                        # Then it cannot influence anything to the left of it
                        for i in range(move[1]):
                            if [move[0], i] not in illegal_moves:
                                illegal_moves.append([move[0], i])
                    # If piece in the way is to the right
                    elif piece.position[1] < move[1] and piece.position[0] == move[0]:
                        # Then it cannot influence anything to the right of it
                        for i in range(7, move[1], -1):
                            if [move[0], i] not in illegal_moves:
                                illegal_moves.append([move[0], i])
                   # If piece in the way is north-west
                    elif piece.position[0] > move[0] and piece.position[1] > move[1]:
                        # Then it cannot influence anything north-west
                        while move[0]-counter != 0 and move[1]-counter != 0:
                            counter += 1
                            if [move[0]-counter, move[1]-counter] not in illegal_moves:
                                illegal_moves.append([move[0]-counter, move[1]-counter])
                    # If piece in the way is north-east
                    elif piece.position[0] > move[0] and piece.position[1] < move[1]:
                        # Then it cannot influence anything north-east
                        while move[0]-counter != 0 and move[1]+counter != 7:
                            counter += 1
                            if [move[0]-counter, move[1]+counter] not in illegal_moves:
                                illegal_moves.append([move[0]-counter, move[1]+counter])
                    # If piece in the way is south-west
                    elif piece.position[0] < move[0] and piece.position[1] > move[1]:
                        # Then it cannot influence anything south-west
                        while move[0]+counter != 7 and move[1]-counter != 0:
                            counter += 1
                            if [move[0]+counter, move[1]-counter] not in illegal_moves:
                                illegal_moves.append([move[0]+counter, move[1]-counter])
                    # If piece in the way is south-east
                    elif piece.position[0] < move[0] and piece.position[1] < move[1]:
                        # Then it cannot influence anything south-east
                        while move[0]+counter != 7 and move[1]+counter != 7:
                            counter += 1
                            if [move[0]+counter, move[1]+counter] not in illegal_moves:
                                illegal_moves.append([move[0]+counter, move[1]+counter])
            return get_legal_moves()
        elif isinstance(piece, Pawn):
            if piece.colour == "White":
                if piece.position[0] > 0 and piece.position[1] > 0:
                    if isinstance(board[piece.position[0]-1][piece.position[1]-1], Piece):
                        if board[piece.position[0]-1][piece.position[1]-1].colour == "Black":
                            legal_moves.append([piece.position[0]-1, piece.position[1]-1])
                if piece.position[0] > 0 and piece.position[1] < 7:
                    if isinstance(board[piece.position[0]-1][piece.position[1]+1], Piece):
                        if board[piece.position[0]-1][piece.position[1]+1].colour == "Black":
                            legal_moves.append([piece.position[0]-1, piece.position[1]+1])
            elif piece.colour == "Black":
                if piece.position[0] < 7 and piece.position[1] < 7:
                    if isinstance(board[piece.position[0]+1][piece.position[1]+1], Piece):
                        if board[piece.position[0]+1][piece.position[1]+1].colour == "White":
                            legal_moves.append([piece.position[0]+1, piece.position[1]+1])
                if piece.position[0] < 7 and piece.position[1] > 0:
                    if isinstance(board[piece.position[0]+1][piece.position[1]-1], Piece):
                        if board[piece.position[0]+1][piece.position[1]-1].colour == "White":
                            legal_moves.append([piece.position[0]+1, piece.position[1]-1])
            return legal_moves
        elif isinstance(piece, Knight):
            return piece.possible_moves
        elif isinstance(piece, King):
            return piece.possible_moves
        else:
            return legal_moves
        
    def calculate_is_checkmate(self, colour, board):
        """Finds out if the a player has been checkmated"""
        if self.is_in_check(colour, board):
            for row in board:
                for piece in row:
                    if isinstance(piece, Piece) and piece.colour == colour:
                        if self.calculate_legal_moves(piece):
                            return False
            return True
        else:
            return False

    def calculate_is_stalemate(self, colour, board):
        """Finds out if the game is in stalemate"""
        if not self.is_in_check("White", board) and not self.is_in_check("Black", board):
            for row in board:
                for piece in row:
                    if isinstance(piece, Piece) and piece.colour == self.turn:
                        if self.calculate_legal_moves(piece):
                            return False
            return True
        else:
            return False

    def is_in_check(self, colour, possible_board):
        """Checks if the king of the corresponding colour is in check."""
        king_coords = self.get_king_coords(colour, possible_board)
        for x in range(8):
            for y in range(8):
                if isinstance(possible_board[x][y], Piece) and possible_board[x][y].colour != colour:
                    if king_coords in self.get_attacking_moves(possible_board[x][y], possible_board):
                        return True
        return False
    
    def get_castling_moves(self, king, original_board):
        king.castling_moves = []
        if not king.has_moved and not self.has_been_in_check[king.colour] and not self.is_in_check(king.colour, self.board):
            if king.colour == "Black":
                if isinstance(original_board[0][0], Rook):
                    if original_board[0][0].colour == "Black" and not original_board[0][0].has_moved and not(original_board[0][2] or original_board[0][3]):
                        original_board = copy.deepcopy(self.board)
                        possible_board = self.preliminary_move_piece(original_board, king.position, [king.position[0], king.position[1]-1])
                        if not self.is_in_check(king.colour, possible_board):
                            original_board = copy.deepcopy(self.board)
                            possible_board = self.preliminary_move_piece(original_board, king.position, [king.position[0], king.position[1]-2])
                            if not self.is_in_check(king.colour, possible_board):
                                king.castling_moves.append([king.position[0], king.position[1]-2])
                if isinstance(original_board[0][7], Rook):
                    if original_board[0][7].colour == "Black" and not original_board[0][7].has_moved and not(original_board[0][5] or original_board[0][6]):
                        original_board = copy.deepcopy(self.board)
                        possible_board = self.preliminary_move_piece(original_board, king.position, [king.position[0], king.position[1]+1])
                        if not self.is_in_check(king.colour, possible_board):
                            original_board = copy.deepcopy(self.board)
                            possible_board = self.preliminary_move_piece(original_board, king.position, [king.position[0], king.position[1]+2])
                            if not self.is_in_check(king.colour, possible_board):
                                king.castling_moves.append([king.position[0], king.position[1]+2])                
            else:
                if isinstance(original_board[7][0], Rook):
                    if original_board[7][0].colour == "White" and not original_board[7][0].has_moved and not(original_board[7][2] or original_board[7][3]):
                        original_board = copy.deepcopy(self.board)
                        possible_board = self.preliminary_move_piece(original_board, king.position, [king.position[0], king.position[1]-1])
                        if not self.is_in_check(king.colour, possible_board):
                            original_board = copy.deepcopy(self.board)
                            possible_board = self.preliminary_move_piece(original_board, king.position, [king.position[0], king.position[1]-2])
                            if not self.is_in_check(king.colour, possible_board):
                                king.castling_moves.append([king.position[0], king.position[1]-2])
                if isinstance(original_board[7][7], Rook):
                    if original_board[7][7].colour == "White" and not original_board[7][7].has_moved and not(original_board[7][5] or original_board[7][6]):
                        original_board = copy.deepcopy(self.board)
                        possible_board = self.preliminary_move_piece(original_board, king.position, [king.position[0], king.position[1]+1])
                        if not self.is_in_check(king.colour, possible_board):
                            original_board = copy.deepcopy(self.board)
                            possible_board = self.preliminary_move_piece(original_board, king.position, [king.position[0], king.position[1]+2])
                            if not self.is_in_check(king.colour, possible_board):
                                king.castling_moves.append([king.position[0], king.position[1]+2])

    def can_enpassent(self, piece, possible_board):
        """Checks if enpassent is possible, and assigns the enpassent move."""
        if self.enpassent_possible[piece.colour] and ((piece.position[0] == 4 and piece.colour == "Black") or (piece.position[0] == 3 and piece.colour == "White")):
            try:
                if isinstance(possible_board[piece.position[0]][piece.position[1]-1], Pawn):
                    if possible_board[piece.position[0]][piece.position[1]-1].first_moved == self.move_num - 1:
                        if piece.colour == "Black":
                            temp_board = self.preliminary_enpassent(possible_board, piece.position, [piece.position[0]+1, piece.position[1]-1], [piece.position[0], piece.position[1]-1])
                            if self.is_in_check("Black", temp_board):
                                return False
                            else:
                                self.enpassent_move['from'] = piece.position
                                self.enpassent_move['to'] = [piece.position[0]+1, piece.position[1]-1]
                                self.enpassent_move['taken'] = [piece.position[0], piece.position[1]-1]
                                return True
                        else:
                            temp_board = self.preliminary_enpassent(possible_board, piece.position, [piece.position[0]-1, piece.position[1]-1], [piece.position[0], piece.position[1]-1])
                            if self.is_in_check("White", temp_board):
                                return False
                            else:
                                self.enpassent_move['from'] = piece.position
                                self.enpassent_move['to'] = [piece.position[0]-1, piece.position[1]-1]
                                self.enpassent_move['taken'] = [piece.position[0], piece.position[1]-1]
                                return True
                    else:
                        return False
            except IndexError:
                pass
            try:
                if isinstance(possible_board[piece.position[0]][piece.position[1]+1], Pawn):
                    if possible_board[piece.position[0]][piece.position[1]+1].first_moved == self.move_num - 1:
                        if piece.colour == "Black":
                            temp_board = self.preliminary_enpassent(possible_board, piece.position, [piece.position[0]+1, piece.position[1]+1], [piece.position[0], piece.position[1]+1])
                            if self.is_in_check("Black", temp_board):
                                return False
                            else:
                                self.enpassent_move['from'] = piece.position
                                self.enpassent_move['to'] = [piece.position[0]+1, piece.position[1]+1]
                                self.enpassent_move['taken'] = [piece.position[0], piece.position[1]+1]
                                return True
                        else:
                            temp_board = self.preliminary_enpassent(possible_board, piece.position, [piece.position[0]-1, piece.position[1]+1], [piece.position[0], piece.position[1]+1])
                            if self.is_in_check("White", temp_board):
                                return False
                            else:
                                self.enpassent_move['from'] = piece.position
                                self.enpassent_move['to'] = [piece.position[0]-1, piece.position[1]+1]
                                self.enpassent_move['taken'] = [piece.position[0], piece.position[1]+1]
                                return True
                    else:
                        return False
            except IndexError:
                pass
            return False
        else:
            return False