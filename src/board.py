from pieces import *
__author__ = "Alexander Saoutkin"

class Board(object):
    """Class which manages the pieces on the board."""

    def __init__(self, player_one="", player_two=""):
        """
        :param txt_board: loaded txt board
        :type txt_board: str
        """
        self.turn = "White"
        self.move_num = 1
        self.is_checkmate = False
        self.is_stalemate = False
        self.game_over = False
        self.player_one = player_one
        self.player_two = player_two
        self.move_logger = MoveLogger()
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
        chess_board[new_coords[0]][new_coords[1]] = self.board[old_coords[0]][old_coords[1]]
        chess_board[old_coords[0]][old_coords[1]] = 0
        if isinstance(chess_board[new_coords[0]][new_coords[1]], Piece):
            chess_board[new_coords[0]][new_coords[1]].position = [new_coords[0], new_coords[1]]
        return chess_board

    def permanently_move_piece(self, chess_board, old_coords, new_coords):
        """Moves a piece on the board"""
        if not self.game_over:
            chess_board[new_coords[0]][new_coords[1]] = self.board[old_coords[0]][old_coords[1]]
            chess_board[old_coords[0]][old_coords[1]] = 0
            self.move_num += 1
            if self.move_num % 2 == 0:
                self.turn = "Black"
            else:
                self.turn = "White"
            if isinstance(chess_board[new_coords[0]][new_coords[1]], Piece):
                chess_board[new_coords[0]][new_coords[1]].position = [new_coords[0], new_coords[1]]
                if self.calculate_is_checkmate(chess_board[new_coords[0]][new_coords[1]].colour, chess_board):
                    self.game_over = True
            return chess_board

    def get_king_coords(self, colour, board):
        """Finds the coords of the king depending on  its colour"""
        for x in range(8):
            for y in range(8):
                if isinstance(board[x][y], King) and board[x][y].colour == colour:
                    return [x, y]

    def calculate_legal_moves(self, piece):
        """Get all the legal moves of a piece and return them"""
        legal_moves = []
        print(str(self.__repr__()))
        if not isinstance(piece, Pawn):
            possible_legal_moves = self.get_attacking_moves(piece)
            for move in possible_legal_moves:
                if isinstance(self.board[move[0]][move[1]], Piece):
                    if not piece.colour == self.board[move[0]][move[1]].colour:
                        possible_board = self.preliminary_move_piece(self.board, piece.position, move)
                        print(str(self.__repr__()))
                        if not self.is_in_check(piece.colour, possible_board):
                            legal_moves.append(move)
                else:
                    possible_board = self.preliminary_move_piece(self.board, piece.position, move)
                    print(str(self.__repr__()))
                    if not self.is_in_check(piece.colour, possible_board):
                        legal_moves.append(move)
        else:
            if piece.colour == "White":
                legal_moves.append([piece.position[0]-1, piece.position[1]])
                if piece.position[0] == 6:
                    legal_moves.append([piece.position[0]-2, piece.position[1]])
            else:
                legal_moves.append([piece.position[0]+1, piece.position[1]])
                if piece.position[0] == 1:
                    legal_moves.append([piece.position[0]+2, piece.position[1]])
        print(legal_moves)
        return legal_moves


    def get_attacking_moves(self, piece):
        """
        Get all the attacking moves of a piece and return them.
        The difference between this function and get_legal_moves is that
        this shows you what the pieces can force a check while the other functions
        tells you whether the piece can move there.
        """
        legal_moves = []
        illegal_moves = []
        def get_legal_moves():
            for move in piece.possible_moves:
                if move not in illegal_moves:
                    legal_moves.append(move)
            return legal_moves
        if isinstance(piece, Rook):
            for move in piece.possible_moves:
                # If there is a piece in the way
                if self.board[move[0]][move[1]]:
                    # If piece in the way is above
                    if piece.position[0] > move[0]:
                        # Then it cannot influence anything above that piece
                        for i in range(move[0]+1):
                            if [i, move[1]] not in illegal_moves:
                                illegal_moves.append([i, move[1]])
                    # If piece in the way is below
                    elif piece.position[0] < move[0]:
                        # Then it cannot influence anything below that piece
                        for i in range(7, move[0]-1, -1):
                            if [i, move[1]] not in illegal_moves:
                                illegal_moves.append([i, move[1]])
                    # If piece in the way is to the left
                    elif piece.position[1] > move[1]:
                        # Then it cannot influence anything to the left
                        for i in range(move[1]+1):
                            if [move[1], i] not in illegal_moves:
                                illegal_moves.append([move[0], i])
                    # If piece in the way is to the right
                    elif piece.position[1] < move[1]:
                        # Then it cannot influence anything to the right
                        for i in range(7, move[1]-1, -1):
                            if [move[1], i] not in illegal_moves:
                                illegal_moves.append([move[0], i])
            return get_legal_moves()
        elif isinstance(piece, Bishop):
            for move in piece.possible_moves:
                if self.board[move[0]][move[1]]:
                    counter = 0
                    on_edge = False
                    # If piece in the way is north-west
                    if piece.position[0] > move[0] and piece.position[1] > move[1]:
                        # Then it cannot influence anything north-west
                        while not on_edge:
                            counter += 1
                            if [move[0]-counter, move[1]-counter] not in illegal_moves:
                                illegal_moves.append([move[0]-counter, move[1]-counter])
                            if move[0]-counter is 0 or move[1]-counter is 0:
                                on_edge = True
                    # If piece in the way is north-east
                    elif piece.position[0] > move[0] and piece.position[1] < move[1]:
                        # Then it cannot influence anything north-east
                        while not on_edge:
                            counter += 1
                            if [move[0]-counter, move[1]+counter] not in illegal_moves:
                                illegal_moves.append([move[0]-counter, move[1]+counter])
                            if move[0]-counter is 0 or move[1]+counter is 7:
                                on_edge = True
                    # If piece in the way is south-west
                    elif piece.position[0] < move[0] and piece.position[1] > move[1]:
                        # Then it cannot influence anything south-west
                        while not on_edge:
                            counter += 1
                            if [move[0]+counter, move[1]-counter] not in illegal_moves:
                                illegal_moves.append([move[0]+counter, move[1]-counter])
                            if move[0]+counter is 7 or move[1]-counter is 0:
                                on_edge = True
                    # If piece in the way is south-east
                    elif piece.position[0] < move[0] and piece.position[1] < move[1]:
                        # Then it cannot influence anything south-east
                        while not on_edge:
                            counter += 1
                            if [move[0]+counter, move[1]+counter] not in illegal_moves:
                                illegal_moves.append([move[0]+counter, move[1]+counter])
                            illegal_moves.append([move[0]+counter, move[1]+counter])
                            if move[0]+counter is 7 or move[1]+counter is 7:
                                on_edge = True
            return get_legal_moves()
        # This function is a combination of Rook and Bishop
        elif isinstance(piece, Queen):
            for move in piece.possible_moves:
                if self.board[move[0]][move[1]]:
                    counter = 0
                    on_edge = False
                    # If piece in the way is above
                    if piece.position[0] > move[0] and piece.position[1] == move[1]:
                        # Then it cannot influence anything above it
                        for i in range(move[0]+1):
                            if [i, move[1]] not in illegal_moves:
                                illegal_moves.append([i, move[1]])
                    # If piece in the way is below
                    elif piece.position[0] < move[0] and piece.position[1] == move[1]:
                        # Then it cannot influence below it...
                        for i in range(7, move[0]-1, -1):
                            if [i, move[1]] not in illegal_moves:
                                illegal_moves.append([i, move[1]])
                    # If piece in the way is to the left
                    elif piece.position[1] > move[1] and piece.position[0] == move[0]:
                        # Then it cannot influence anything to the left of it
                        for i in range(move[1]+1):
                            if [move[1], i] not in illegal_moves:
                                illegal_moves.append([move[0], i])
                    # If piece in the way is to the right
                    elif piece.position[1] < move[1] and piece.position[0] == move[0]:
                        # Then it cannot influence anything to the right of it
                        for i in range(7, move[1]-1, -1):
                            if [move[1], i] not in illegal_moves:
                                illegal_moves.append([move[0], i])
                   # If piece in the way is north-west
                    elif piece.position[0] > move[0] and piece.position[1] > move[1]:
                        # Then it cannot influence anything north-west
                        while not on_edge:
                            counter += 1
                            if [move[0]-counter, move[1]-counter] not in illegal_moves:
                                illegal_moves.append([move[0]-counter, move[1]-counter])
                            if move[0]-counter is 0 or move[1]-counter is 0:
                                on_edge = True
                    # If piece in the way is north-east
                    elif piece.position[0] > move[0] and piece.position[1] < move[1]:
                        # Then it cannot influence anything north-east
                        while not on_edge:
                            counter += 1
                            if [move[0]-counter, move[1]+counter] not in illegal_moves:
                                illegal_moves.append([move[0]-counter, move[1]+counter])
                            if move[0]-counter is 0 or move[1]+counter is 7:
                                on_edge = True
                    # If piece in the way is south-west
                    elif piece.position[0] < move[0] and piece.position[1] > move[1]:
                        # Then it cannot influence anything south-west
                        while not on_edge:
                            counter += 1
                            if [move[0]+counter, move[1]-counter] not in illegal_moves:
                                illegal_moves.append([move[0]+counter, move[1]-counter])
                            if move[0]+counter is 7 or move[1]-counter is 0:
                                on_edge = True
                    # If piece in the way is south-east
                    elif piece.position[0] < move[0] and piece.position[1] < move[1]:
                        # Then it cannot influence anything south-east
                        while not on_edge:
                            counter += 1
                            if [move[0]+counter, move[1]+counter] not in illegal_moves:
                                illegal_moves.append([move[0]+counter, move[1]+counter])
                            illegal_moves.append([move[0]+counter, move[1]+counter])
                            if move[0]+counter is 7 or move[1]+counter is 7:
                                on_edge = True
            return get_legal_moves()
        elif isinstance(piece, Pawn):
            if piece.colour == "White":
                legal_moves.append([piece.position[0]-1, piece.position[1]-1])
                legal_moves.append([piece.position[1]-1, piece.position[1]+1])
            elif piece.colour == "Black":
                legal_moves.append([piece.position[1]+1, piece.position[1]+1])
                legal_moves.append([piece.position[1]+1, piece.position[1]-1])
            return legal_moves
        elif isinstance(piece, Knight):
            return piece.possible_moves
        else:
            return legal_moves
        
    def calculate_is_checkmate(self, colour, board):
        """Finds out if the a player has been checkmated"""
        if self.is_in_check(colour, board):
            for row in board:
                for piece in row:
                    if self.calculate_legal_moves(piece):
                        return False
            return True
        else:
            return False

    def calculate_is_stalemate(self, colour, board):
        """Finds out if the game in """
        if not self.is_in_check("White", board) and not self.is_in_check("Black", board):
            for row in board:
                for piece in row:
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
                    if king_coords in self.get_attacking_moves(possible_board[x][y]):
                        return True
        return False
                    

    def __repr__(self):
        output = ""
        for row in self.board:
            for field in row:
                output += str(field)
            output += "\n"
        return output
class MoveLogger(object):

    def __init__(self, start=[], end=[]):
        """
        :param start: starting position before move
        :type start: 2d list
        :param end: ending position after move
        :type end: 2d list
        """
        self.start = start
        self.end = end

def test():
    board = Board()
    print(board)
    board.permanently_move_piece(board.board, [6, 4], [4, 4])
    print(board)
    print(board.get_king_coords("White", board.board))
    print(board.get_king_coords("Black", board.board))
    print('\n')
    bishop = Bishop([5, 5], "White")
    bishop.calculate_possible_moves()
    print(bishop.possible_moves)
    print('\n')
    queen = Queen([5, 5], "White")
    queen.calculate_possible_moves()
    print(queen.possible_moves)
    print('\n')
    knight = Knight([7, 7], "White")
    knight.calculate_possible_moves()
    print(knight.possible_moves)
    print('\n')
    king = King([5, 5], "White")
    king.calculate_possible_moves()
    print(king.possible_moves)
    

if __name__ == "__main__":
    test()
