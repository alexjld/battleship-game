"""
    File: battleship.py
    Author: Alex Dunn
    Purpose: Plays a game of Battleship by initializing a game board and
        responds accordingly based on the effects of each player's guess.
"""
import  sys

#  Limits:
#
MAXBOARD = 10
NUMFIELDS = 5

#  Valid ship types and sizes:
#
SHIPTYPES = {"A":5, "B":4, "D":3, "P":2, "S":3}

#  Orientation:
#
OTHER = "?"
HORIZONTAL = "H"
VERTICAL = "V"

class Ship:
    """Manages information related to a ship of the py game, ie, 
        type and placement."""
    def __init__(self, line):
        """Initializes an instance with fields from the parameter line.
            line is in the form:
                Abbreviation x1 y1 x2 y2
            where,
                Abbreviation is one of {"A", "B", "D", "P", "S"}
                coordinates, x1, y1, x2, y2, are between 0 and 9
            
            Parameters: line which contains type and placement information.
            
            Pre-condition: file that contains data must exist.
        """
        #  Validate correct number of fields:
        #
        fields = line.split()
        if (len(fields) != NUMFIELDS):
            #  Invalid number of fields in input line
            #
            print("ERROR: fleet composition incorrect")
            sys.exit(1)
            
        #  Validate ship type:
        #
        if (fields[0].upper() not in SHIPTYPES):
            #  Invalid type of ship
            #
            print("ERROR: fleet composition incorrect")
            sys.exit(1)
            
        self._ship_type = fields[0]

        #    Validate positional values:  x0, y0, x1, y1
        #
        self._position = [0, 0, 0, 0]
        for i in range(1, len(fields)):
            try:
                value = int(fields[i])
            except:
                print("ERROR: fleet composition incorrect")
                sys.exit(1)

            if ((value < 0) or (9 < value)):
                print("ERROR: ship out-of-bounds: " + line)
                sys.exit(1)

            self._position[i - 1] = value

        #  Validate orientation of ship:  horizontal or vertical
        #
        if (self._position[0] == self._position[2]):
            #  Vertical placement
            #
            self._orientation = VERTICAL

            if (self._position[1] > self._position[3]):
                temp = self._position[1]
                self._position[1] = self._position[3]
                self._position[3] = temp

            self._size = (self._position[3] - self._position[1]) + 1
        elif (self._position[1] == self._position[3]):
            #  Horizontal placement
            #
            self._orientation = HORIZONTAL

            if (self._position[0] > self._position[2]):
                temp = self._position[0]
                self._position[0] = self._position[2]
                self._position[2] = temp

            self._size = (self._position[2] - self._position[0]) + 1
        else:
            print("ERROR: ship not horizontal or vertical: " + line)
            sys.exit(1)

        #  Validate ship's size
        #
        if (self._size != SHIPTYPES[self.get_ship_type()]):
            print("ERROR: incorrect ship size: " + line)
            sys.exit(1)
    
        #  Initialize hits
        #
        self._hits = [False] * self._size
        self._floating = self._size

    def get_ship_type(self):
        return self._ship_type

    def get_orientation(self):
        return self._orientation

    def get_size(self):
        return self._size

    def placement(self):
        return (self._position[0], self._position[1], self._size)

    def sunk(self, x, y):
        """Displays proper response based on accuracy of player's guesses.
        
        Parameters: x and y coordinate 
        
        Returns: Prints response based on effect of guess."""
        if (self._floating > 0):
            if (self._orientation == HORIZONTAL):
                i = x - self._position[0]
            else:
                i = y - self._position[1]
    
            if (self._hits[i] == True):
                print ("hit (again)")

                return  False

            self._hits[i] = True
            self._floating -= 1

            if (self._floating > 0):
                print ("hit")
                
                return  False

        print("{} sunk".format(self._ship_type))

        return  True

    def __str__(self):
        """Returns ship's relevant attributes"""
        return "{} @ ({}, {}) - ({}, {}) {}:{}".format(self._ship_type,
                                                       self._position[0], 
                                                       self._position[1],
                                                       self._position[2], 
                                                       self._position[3],
                                                       self._orientation, 
                                                       self._hits)
               
class GridPos:
    """Describes item at grid position."""
    def __init__(self, x, y, ship):
        """Initializes x, y coordinate and ship.
        
        Parameters: x, y coordinates and ship"""
        self._x = x
        self._y = y
        self._ship = ship
        self._guessed = False

    def get_ship(self):
        return self._ship

    def get_guessed(self):
        return self._guessed

    def set_ship(self, ship):
        self._ship = ship

    def set_guessed(self):
        self._guessed = True

    def get_ship_type(self):
        """Returns ship type.
        
        Returns: ship type?"""
        if (self._ship == None):
            return "."

        return self._ship.get_ship_type()

    def __str__(self):
        """Returns coordinates of ship and whether or not that position has 
            been guessed yet.
            
        Returns: attributes of ship position."""
            
        return  "({}, {}):  {} {}".format(self._x, self._y,
                                          self._guessed, self.get_ship_type())

class Board:
    """Describes board with placement of ships"""
    def __init__(self):
        """Initializes game grid"""
        self._ships = {}

        #  Initialize game grid with GridPos
        #
        self._grid = []
        for y in range(0, MAXBOARD):
            row = []
            for x in range(0, MAXBOARD):
                row.append(GridPos(x, y, None))
            
            self._grid.append(row)

    def fleet_complete(self):
        """Determines if all ships have been placed.
        
        Returns: True if all ships have been placed."""
        if (len(self._ships) != len(SHIPTYPES)):
            print("ERROR: fleet composition incorrect")
            sys.exit(1)
            
        return True

    def add(self, line):
        """Places all ships on boards and determines if there are overlaps.
        
        Parameters: line"""
        new_ship = Ship(line)

        ship_type = new_ship.get_ship_type()
        if (ship_type in self._ships):
            print("ERROR: fleet composition incorrect")
            sys.exit(1)

        (x1, y1, size) = new_ship.placement()
        if (new_ship.get_orientation() == HORIZONTAL):
            for x in range(x1, x1 + size):
                if (self._grid[y1][x].get_ship() != None):
                    print("ERROR: overlapping ship: " + line)
                    sys.exit(1)
                    
                self._grid[y1][x].set_ship(new_ship)
        else:  #  VERTICAL orientation
            for y in range(y1, y1 + size):
                if (self._grid[y][x1].get_ship() != None):
                    print("ERROR: overlapping ship: " + line)
                    sys.exit(1)
                    
                self._grid[y][x1].set_ship(new_ship)

        self._ships[ship_type] = new_ship

    def shot_fired(self, x, y):
        """Determines if a shot missed, hit, or sunk ship.
        
        Parameters: x and y
        
        Returns: Response based on effect of guess (shot)."""
        position = self._grid[y][x]
        ship = position.get_ship()

        if (ship == None):
            #    No ship at this position
            #
            if (position.get_guessed() == False):
                position.set_guessed()

                print("miss")
                return False

            print("miss (again)")
            return False

        #    There's a ship at this position, how badly was it damaged?
        #
        if (ship.sunk(x, y) == True):
            self._ships.pop(ship.get_ship_type())
            
            if (len(self._ships) <= 0):
                return  True

        return False

    def __str__(self):
        """The game board"""
        lines = "\n"

        y = len(self._grid) - 1
        while (y >= 0):
            lines += "{:d}: ".format(y)
            
            for x in range(0, len(self._grid[y])):
                lines += self._grid[y][x].get_ship_type()

            lines += "\n"
            y -= 1
        
        lines += " : "
        for x in range(0, MAXBOARD):
            lines += str(x)
        
        lines += "\n"

        return lines

def process_data_file(placement_file):
    """Reads in placement file and places ships onto board.
    
    Parameters: file that contains ship placement data.
    
    Returns: Game board
    
    Pre-conditions: file must exist with valid data."""
    new_board = Board()

    #    Process ship placement file
    #
    try:
        file = open(placement_file)
    except:
        print("ERROR: Could not open file: " + placement_file)
        sys.exit(1)

    for line in file.readlines():
        if (len(line) > 0):
            new_board.add(line)

    file.close()
        
    #    Validate that all ships have been placed
    #
    new_board.fleet_complete()

    return  new_board

def process_guesses(board):
    """Reads in guess file and responds based on effect of guess on board.
    
    Parameters: board"""
    guess_file = input()
    
    try:
        file = open(guess_file)
    except:
        print("ERROR: Could not open file: " + guess_file)
        sys.exit(1)

    for line in file.readlines():
        line = line.strip()
        if (len(line) > 0):
            guess = line.split()

            #    Validate guesses
            #
            try:
                x = int(guess[0])
                y = int(guess[1])
            except:
                print("illegal guess")
                continue

            if ((0 <= x and x <= 9) and (0 <= y and y <= 9)):
                if (board.shot_fired(x, y) == True):
                    print("all ships sunk: game over")

                    break
            else:
                print("illegal guess")

    file.close()

#  Main:
#
def main():
    """Main function"""
    placement_file = input()
    placements = process_data_file(placement_file)
    process_guesses(placements)

main()