__author__ = "Alexander Saoutkin"

class Piece(object):
    """Base class for chess pieces"""

    def __init__(self, position, colour):
        """"
        :param coords: Coordinates on the board
        :type coords: list (with only two elements)
        """
        self.position = position
        self.colour = colour
        self.possible_moves = []
        self.calculate_possible_moves()

        @property
        def position(self):
            return self.position
        
        @position.setter
        def position(self, value):
            self.position = value
            self.calculate_possible_moves()

    def calculate_possible_moves(self):
        """Shows us the coords it can go to assuming that there are no other pieces on the board"""
        raise NotImplementedError


class Rook(Piece):
    """Class for a Rook"""

    def __init__(self, position, colour, has_moved=False):
        super().__init__(position, colour)
        self.img_path = "{}_rook.png".format(self.colour.lower())
        self.has_moved = has_moved

    def calculate_possible_moves(self):
        self.possible_moves = []
        for i in range(8):
            if self.position[1] != i:
                self.possible_moves.append([self.position[0], i])
            if self.position[0] != i:
                self.possible_moves.append([i, self.position[1]])
        

    def __str__(self):
        if self.colour == "White":
            return 'WR'
        else:
            return 'BR'


class Knight(Piece):
    """Class for a Knight"""
    def __init__(self, position, colour):
        super().__init__(position, colour)
        self.img_path = "{}_knight.png".format(self.colour.lower())

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
        if self.colour == "White":
            return 'WN'
        else:
            return 'BN'


class Bishop(Piece):
    """Class for a Bishop"""
    def __init__(self, position, colour):
        super().__init__(position, colour)
        self.img_path = "{}_bishop.png".format(self.colour.lower())

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
        if self.colour == "White":
            return 'WB'
        else:
            return 'BB'


class Queen(Piece):
    """Class for a Queen"""
    def __init__(self, position, colour):
        super().__init__(position, colour)
        self.img_path = "{}_queen.png".format(self.colour.lower())

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
        if self.colour == "White":
            return 'WQ'
        else:
            return 'BQ'


class King(Piece):
    """Class for a King"""
    def __init__(self, position, colour, has_moved=False, castling_moves=[]):
        super().__init__(position, colour)
        self.img_path = "{}_king.png".format(self.colour.lower())
        self.has_moved = has_moved
        self.castling_moves = castling_moves

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

    def can_castle(self):
        pass
        
    def __str__(self):
        if self.colour == "White":
            return 'WK'
        else:
            return 'BK'


class Pawn(Piece):
    """Class for a Pawn"""
    def __init__(self, position, colour, first_moved=0):
        super().__init__(position, colour)
        self.img_path = "{}_pawn.png".format(self.colour.lower())
        self.first_moved = first_moved

    def calculate_possible_moves(self):
        self.possible_moves.clear()
        if self.colour == "White":
            self.possible_moves.append([self.position[0]-1, self.position[1]])
        else:
            self.possible_moves.append([self.position[0]+1, self.position[1]])

        
    
    def __str__(self):
        if self.colour == "White":
            return 'WP'
        else:
            return 'BP'
