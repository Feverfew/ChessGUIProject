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
        self.player_one = player_one
        self.player_two = player_two
        self.move_logger = MoveLogger()
        self.new_board()


    def new_board(self):
        """Creates a new fresh board"""
        self.field = []
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
        self.field.append(row)
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
        self.field.append(row)
        # Add empty space
        for i in range(4):
            row = [0 for x in range(8)]
            self.field.append(row)
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
        self.field.append(row)
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
        self.field.append(row)

    def move_piece(self, old_x, old_y, new_x, new_y):
        """Moves a piece on the board"""
        self.field[new_x][new_y] = self.field[old_x][old_y]
        self.field[old_x][old_y] = 0
        self.move_logger.start.append([old_x, old_y])
        self.move_logger.end.append([new_x, new_y])

    def get_king_coords(self, colour):
        """Finds the coords of the king depending on  its colour"""
        for x in range(8):
            for y in range(8):
                if isinstance(self.field[x][y], King) and self.field[x][y].colour == colour:
                    return [x, y]

    def get_legal_moves(self, piece):
        """Get all the legal moves of a piece and return them"""
        legal_moves = []
        if isinstance(piece, King):
            for move in piece.possible_moves:
                # If there is no piece on that part of the board...
                if not self.field[move[0]][move[1]]:
                    legal_moves.append(move)
            return legal_moves
        elif isinstance(piece, Rook):
            for move in piece.possible_moves:
                if self.field[move[0]][move[1]]:
                    pass
                else:
                    pass
   
    def get_attacking_moves(self, piece):
        """
        Get all the attacking moves of a piece and return them.
        The difference between this function and get_legal_moves is that
        this shows you what the pieces can force a check while the other functions
        tells you whether the piece can move there.
        """
        legal_moves = []
        ilegal_moves = []
        if isinstance(piece, Rook):
            for move in piece.possible_moves:
                if self.field[move[0]][move[1]]:
                    # If piece in the way is on the left side
                    if piece.position[0] < move[0]:
                        # Then it cannot influence anything left of it...
                        for i in range(move[0]+1):
                            if [i, move[1]] not in illegal_moves:
                                illegal_moves.append([i, move[1]])
                    # If piece in the way is on the right side
                    elif piece.position[0] > move[0]:
                        # Then it cannot influence anything right of it...
                        for i in range(7, move[0]-1, -1):
                            if [i, move[1]] not in illegal_moves:
                                illegal_moves.append([i, move[1]])
                    # If piece in the way is above
                    if piece.position[1] < move[1]:
                        # Then it cannot influence anything above that piece
                        for i in range(move[1]+1):
                            if [move[1], i] not in illegal_moves:
                                illegal_moves.append([move[0], i])
                    # If piece in the way is bellow
                    elif piece.position[1] > move[1]:
                        # Then it cannot influence anything below that piece
                        for i in range(7, move[1]-1, -1):
                            if [move[1], i] not in illegal_moves:
                                illegal_moves.append([move[0], i])
        elif isinstance(piece, Bishop):
            for move in piece.possible_moves:
                if self.field[move[0]][move[1]]:
                    counter = 0
                    on_edge = False
                    # If piece in the way is north-west
                    if piece.position[0] < move[0] and piece.position[1] < move[1]:
                        # Then it cannot influence anything north-west
                        while not on_edge:
                            counter += 1
                            illegal_moves.append([move[0]-counter, move[1]-counter])
                            if move[0]-counter is 0 or move[1]-counter is 0:
                                on_edge = True
                    # If piece in the way is north-east
                    elif piece.position[0] < move[0] and piece.position[1] > move[1]:
                        # Then it cannot influence anything north-west
                        while not on_edge:
                            counter += 1
                            illegal_moves.append([move[0]-counter, move[1]+counter])
                            if move[0]-counter is 0 or move[1]+counter is 7:
                                on_edge = True
                    # If piece in the way is south-west
                    elif piece.position[0] < move[0] and piece.position[1] > move[1]:
                        # Then it cannot influence anything north-west
                        while not on_edge:
                            counter += 1
                            illegal_moves.append([move[0]-counter, move[1]+counter])
                            if move[0]-counter is 0 or move[1]+counter is 7:
                                on_edge = True
            
                        

    def is_in_check(self, colour, possible_board):
        """Checks if the king of the corresponding colour is in check."""
        king_coords = get_king_coords(colour)
        for x in range(8):
            for y in range(8):
                if isinstance(possible_board[x][y], Piece) and possible_board[x][y].colour != colour:
                    pass
        
        

    def __repr__(self):
        output = ""
        for row in self.field:
            for field in row:
                output += str(field)
            output += "\n"
        return output

class MoveValidator(object):
    """Contains functions that validates moves"""
    pass

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
        


class Piece(object):
    """Base class for chess pieces"""

    def __init__(self, position, colour, has_moved=False):
        """"
        :param coords: Coordinates on the board
        :type coords: list (with only two elements)
        """
        self.position = position
        self.colour = colour
        self.has_moved = has_moved
        self.possible_moves = []
        

    def calculate_possible_moves(self):
        """
        Shows us the coords it can go to assuming
        that there are no other pieces on the board
        :param x: x coordinate of the piece
        :type x: int
        :param y: y coordinate of the piece
        :type y: int
        """
        raise NotImplementedError


class Rook(Piece):
    """Class for a Rook"""

    def calculate_possible_moves(self):
        self.possible_moves = []
        for i in range(8):
            if self.position[1] != i:
                self.possible_moves.append([self.position[0], i])
            if self.position[0] != i:
                self.possible_moves.append([i, self.position[1]])
        

    def __str__(self):
        return 'R'


class Knight(Piece):
    """Class for a Knight"""

    def calculate_possible_moves(self):
        self.possible_moves = []
        potential_moves = []
        potential_moves.append([self.position[0]+2, self.position[1]+1])
        potential_moves.append([self.position[0]+2, self.position[1]-1])
        potential_moves.append([self.position[0]-2, self.position[1]+1])
        potential_moves.append([self.position[0]-2, self.position[1]-1])
        potential_moves.append([self.position[0]+1, self.position[1]+2])
        potential_moves.append([self.position[0]+1, self.position[1]-2])
        potential_moves.append([self.position[0]-1, self.position[1]+2])
        potential_moves.append([self.position[0]-1, self.position[1]-2])
        for move in potential_moves:
            if move[0] <= 7 and move [0] >= 0 and move[1] <= 7 and move[1] >= 0:
                self.possible_moves.append(move)
            
                
            

    def __str__(self):
        return 'N'


class Bishop(Piece):
    """Class for a Bishop"""

    def calculate_possible_moves(self):
        self.possible_moves = []
        on_edge = False
        counter = 0
        # Dont' bother iterating to the right if already on the edge
        if self.position[0] is 7 or self.position[1] is 7:
            on_edge = True
        # Find all positions diagonally  to south-east.
        while not on_edge:
            counter += 1
            self.possible_moves.append([self.position[0]+counter, self.position[1]+counter])
            if self.position[0]+counter is 7 or self.position[1]+counter is 7:
                on_edge = True
        counter = 0
        on_edge = False
        # Dont' bother iterating to the right if already on the edge
        if self.position[0] is 0 or self.position[1] is 0:
            on_edge = True
        # Find all positions diagonally to north-west
        while not on_edge:
            counter += 1
            self.possible_moves.append([self.position[0]-counter, self.position[1]-counter])
            if self.position[0]-counter is 0 or self.position[1]-counter is 0:
                on_edge = True
        counter = 0
        on_edge = False
        # Find all positions diagonally to north-east
        if self.position[0] is 0 or self.position[1] is 7:
            on_edge = True
        while not on_edge:
            counter +=1
            self.possible_moves.append([self.position[0]-counter, self.position[1]+counter])
            if self.position[0]-counter is 0 or self.position[1]+counter is 7:
                on_edge = True
        counter = 0
        on_edge = False
        # Find all positions diagonally to south-west
        if self.position[0] is 7 or self.position[1] is 0:
            on_edge = True
        while not on_edge:
            counter +=1
            self.possible_moves.append([self.position[0]+counter, self.position[1]-counter])
            if self.position[0]+counter is 7 or self.position[1]-counter is 0:
                on_edge = True                
    
    def __str__(self):
        return 'B'


class Queen(Piece):
    """Class for a Queen"""

    def calculate_possible_moves(self):
        self.possible_moves = []
        on_edge = False
        counter = 0
        # Do not bother iterating if already on the edge
        if self.position[0] is 7 or self.position[1] is 7:
            on_edge = True
        # Find all positions diagonally  to south-east.
        while not on_edge:
            counter += 1
            self.possible_moves.append([self.position[0]+counter, self.position[1]+counter])
            if self.position[0]+counter is 7 or self.position[1]+counter is 7:
                on_edge = True
        counter = 0
        on_edge = False
        if self.position[0] is 0 or self.position[1] is 0:
            on_edge = True
        # Find all positions diagonally to north-west
        while not on_edge:
            counter += 1
            self.possible_moves.append([self.position[0]-counter, self.position[1]-counter])
            if self.position[0]-counter is 0 or self.position[1]-counter is 0:
                on_edge = True
        counter = 0
        on_edge = False
        # Find all positions diagonally to north-east
        if self.position[0] is 0 or self.position[1] is 7:
            on_edge = True
        while not on_edge:
            counter +=1
            self.possible_moves.append([self.position[0]-counter, self.position[1]+counter])
            if self.position[0]-counter is 0 or self.position[1]+counter is 7:
                on_edge = True
        counter = 0
        on_edge = False
        # Find all positions diagonally to south-west
        if self.position[0] is 7 or self.position[1] is 0:
            on_edge = True
        while not on_edge:
            counter +=1
            self.possible_moves.append([self.position[0]+counter, self.position[1]-counter])
            if self.position[0]+counter is 7 or self.position[1]-counter is 0:
                on_edge = True
        # Find all positions horizontally and vertically
        for i in range(8):
            if self.position[1] != i:
                self.possible_moves.append([self.position[0], i])
            if self.position[0] != i:
                self.possible_moves.append([i, self.position[1]])
    
    def __str__(self):
        return 'Q'


class King(Piece):
    """Class for a King"""

    def calculate_possible_moves(self):
        self.possible_moves.clear()
        potential_moves = []
        potential_moves.append([self.position[0]+1, self.position[1]+1])
        potential_moves.append([self.position[0]+1, self.position[1]-1])
        potential_moves.append([self.position[0]+1, self.position[1]])
        potential_moves.append([self.position[0]-1, self.position[1]+1])
        potential_moves.append([self.position[0]-1, self.position[1]-1])
        potential_moves.append([self.position[0]-1, self.position[1]])
        potential_moves.append([self.position[0], self.position[1]+1])
        potential_moves.append([self.position[0], self.position[1]-1])
        for move in potential_moves:
            if move[0] <= 7 and move [0] >= 0 and move[1] <= 7 and move[1] >= 0:
                self.possible_moves.append(move)    
        if not self.has_moved:
            pass

    def can_castle(self):
        pass
        
    def __str__(self):
        return 'K'


class Pawn(Piece):
    """Class for a Pawn"""

    def calculate_possible_moves(self):
        self.possible_moves.clear()
        if self.colour == "White":
            self.possible_moves.append([self.position[0]-1, self.position[1]])
        else:
            self.possible_moves.append([self.position[0]+1, self.position[1]])

        
    
    def __str__(self):
        return 'P'

def test():
    board = Board()
    print(board)
    board.move_piece(6, 4, 4, 4)
    print(board)
    print(board.get_king_coords("White"))
    print(board.get_king_coords("Black"))
    print(board.move_logger.start)
    print(board.move_logger.end)
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
