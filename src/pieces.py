__author__ = "Alexander Saoutkin"


class Piece(object):
    """Base class for all chess pieces

    Attributes:
        position (list): coordinates on the board in the form [x, y]
        colour (str): Colour of the piece, either "White" or "Black"
    """

    def __init__(self, position, colour):
        """This constructor initialises the class variables and also calculates all possible moves for the piece."""
        self.position = position
        self.colour = colour
        self.possible_moves = []
        self.calculate_possible_moves()

        @property
        def position(self):
            return self.position

        @position.setter
        def position(self, value):
            """ This setter calculates the new possible moves once the position has changed.

            Args:
                value (list): coordinates on the board in the form [x, y]
            """
            self.position = value
            self.calculate_possible_moves()

    def calculate_possible_moves(self):
        """Shows us the coords it can go to assuming that there are no other pieces on the board

        Raises:
            NotImplementedError: Method not overridden in subclass.
        """
        raise NotImplementedError


class Rook(Piece):
    """Class for a Rook

    Attributes:
        position (list): coordinates on the board in the form [x, y]
        colour (str): colour of the piece, either "White" or "Black"
        img_path (str): path to the image of the piece
        has_moved (bool): Denotes whether the piece has moved before.
    """

    def __init__(self, position, colour, has_moved=False):
        """
        This constructor initialises the class variables and also calculates all possible moves for the piece.
        In addition the image path is added.
        """
        super().__init__(position, colour)
        self.img_path = "{}_rook.png".format(self.colour.lower())
        self.has_moved = has_moved

    def calculate_possible_moves(self):
        """Calculates all the possible moves for a rook in a certain position."""
        self.possible_moves = []
        for i in range(8):
            if self.position[1] != i:
                self.possible_moves.append([self.position[0], i])
            if self.position[0] != i:
                self.possible_moves.append([i, self.position[1]])


class Knight(Piece):
    """Class for a Knight

    Attributes:
        position (list): coordinates on the board in the form [x, y]
        colour (str): colour of the piece, either "White" or "Black"
        img_path (str): path to the image of the piece
    """

    def __init__(self, position, colour):
        """
        This constructor initialises the class variables and also calculates all possible moves for the piece.
        In addition the image path is added as an attribute self.img_path.
        """
        super().__init__(position, colour)
        self.img_path = "{}_knight.png".format(self.colour.lower())

    def calculate_possible_moves(self):
        """Calculates all the possible moves for a knight in a certain position."""
        self.possible_moves = []
        potential_moves = [[self.position[0] + 2, self.position[1] + 1],
                           [self.position[0] + 2, self.position[1] - 1],
                           [self.position[0] - 2, self.position[1] + 1],
                           [self.position[0] - 2, self.position[1] - 1],
                           [self.position[0] + 1, self.position[1] + 2],
                           [self.position[0] + 1, self.position[1] - 2],
                           [self.position[0] - 1, self.position[1] + 2],
                           [self.position[0] - 1, self.position[1] - 2]]
        for move in potential_moves:
            if 7 >= move[0] >= 0 and 7 >= move[1] >= 0:
                self.possible_moves.append(move)


class Bishop(Piece):
    """Class for a Bishop

    Attributes:
        position (list): coordinates on the board in the form [x, y]
        colour (str): colour of the piece, either "White" or "Black"
        img_path (str): path to the image of the piece
    """
    def __init__(self, position, colour):
        """
        This constructor initialises the class variables and also calculates all possible moves for the piece.
        In addition the image path is added as an attribute self.img_path.
        """
        super().__init__(position, colour)
        self.img_path = "{}_bishop.png".format(self.colour.lower())

    def calculate_possible_moves(self):
        """Calculates all the possible moves for a bishop in a certain position."""
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


class Queen(Piece):
    """Class for a Queen

    Attributes:
        position (list): coordinates on the board in the form [x, y]
        colour (str): colour of the piece, either "White" or "Black"
        img_path (str): path to the image of the piece
    """
    def __init__(self, position, colour):
        """
        This constructor initialises the class variables and also calculates all possible moves for the piece.
        In addition the image path is added as an attribute self.img_path.
        """
        super().__init__(position, colour)
        self.img_path = "{}_queen.png".format(self.colour.lower())

    def calculate_possible_moves(self):
        """Calculates all the possible moves for a queen in a certain position."""
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


class King(Piece):
    """Class for a King

    Attributes:
        position (list): coordinates on the board in the form [x, y].
        colour (str): colour of the piece, either "White" or "Black".
        img_path (str): path to the image of the piece.
        has_moved (bool): denotes whether piece has moved or not.
        castling_moves (list): list of all castling moves possible.
    """
    def __init__(self, position, colour, has_moved=False, castling_moves=[]):
        """
        This constructor initialises the class variables and also calculates all possible moves for the piece.
        In addition the image path is added as an attribute self.img_path.
        """
        super().__init__(position, colour)
        self.img_path = "{}_king.png".format(self.colour.lower())
        self.has_moved = has_moved
        self.castling_moves = castling_moves

    def calculate_possible_moves(self):
        """Calculates all the possible moves for a king in a certain position."""
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


class Pawn(Piece):
    """Class for a Pawn

    Attributes:
        position (list): coordinates on the board in the form [x, y]
        colour (str): colour of the piece, either "White" or "Black"
        img_path (str): path to the image of the piece
        first_moved (int): denotes at what stage (move) in the game the the piece was first moved.
    """
    def __init__(self, position, colour, first_moved=0):
        """
        This constructor initialises the class variables and also calculates all possible moves for the piece.
        In addition the image path is added as an attribute self.img_path.
        """
        super().__init__(position, colour)
        self.img_path = "{}_pawn.png".format(self.colour.lower())
        self.first_moved = first_moved

    def calculate_possible_moves(self):
        """Calculates all the possible moves for a pawn in a certain position."""
        self.possible_moves.clear()
        if self.colour == "White":
            self.possible_moves.append([self.position[0]-1, self.position[1]])
        else:
            self.possible_moves.append([self.position[0]+1, self.position[1]])
