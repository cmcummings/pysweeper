import random

def generate_mine_map(width=30, height=16, num_mines=99):
    """Generates a 2D array of boolean values, true representing a mine and false representing an empty space."""

    if num_mines > width * height:
        print("The number of mines exceeds the size of the board.")
        return
        
    mine_map = [[False for i in range(width)] for j in range(height)]
    mines = 0
    while mines < num_mines:
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        if not mine_map[y][x]:
            mine_map[y][x] = True
            mines += 1

    return mine_map

ZERO = 0
ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 7
EIGHT = 8
FLAG = 9
UNREVEALED = 10
BOMB = 12

class Board:
    """The Minesweeper board. Handles flags and revealing spaces."""

    def __init__(self, mine_map):
        self.mine_map = mine_map
        self.revealed = []
        self.flags = []

    @property
    def size(self):
        """The (width, height) of the board."""
        return self.width, self.height

    @property
    def width(self):
        """The width of the board."""
        return len(self.mine_map[0])

    @property
    def height(self):
        """The height of the board."""
        return len(self.mine_map)

    def generate_revealed_board(self, bombs=False):
        """Generates a board with numbers, empty spaces, and flags. Constants in the this module identify what a space is."""
        board = []

        for y, row in enumerate(self.mine_map):
            revealed_row = []
            for x, mine in enumerate(row):
                if (x, y) in self.revealed:
                    revealed_row.append(self.get_num_mines_around_position(x, y)) # Find how many mines are around this space
                elif (x, y) in self.flags:
                    revealed_row.append(FLAG)
                elif bombs and self.mine_map[y][x]:
                    revealed_row.append(BOMB)
                else:
                    revealed_row.append(UNREVEALED)
            board.append(revealed_row)
        
        return board

    def toggle_flag(self, position):
        if position in self.flags:
            self.flags.remove(position)
        elif position not in self.revealed:
            self.flags.append(position)

    def flag(self, position):
        """Flags a position."""
        if position not in self.revealed: # Cannot flag revealed spaces
            self.flags.append(position)

    def unflag(self, position):
        """Unflags a position."""
        if position in self.flags:
            self.flags.remove(position)

    def reveal(self, position):
        """Reveals a position if not flagged. Returns False if the position was a bomb, True otherwise."""
        if position not in self.flags:
            x, y = position
            
            if self.mine_map[y][x]:
                return False

            self.revealed.append(position)
            self.autoreveal_empty_spaces(position)
        return True

    def autoreveal_empty_spaces(self, position):
        """Reveals the empty spaces that are automatically discovered from a root zero space."""
        revealed = []
        zero_spaces = []
        check_stack = [position]
        checked = []

        while len(check_stack) > 0:
            pos = x, y = check_stack.pop()
            if self.get_num_mines_around_position(x, y) == 0:
                zero_spaces.append(pos)
                
                # Add spaces around
                for ay in range(y-1, y+2):
                    for ax in range(x-1, x+2):
                        if ay >= 0 and ax >= 0 and ay < len(self.mine_map) and ax < len(self.mine_map[ay]): # Don't check spaces that are outside of the array
                            apos = ax, ay
                            if apos not in checked:
                                check_stack.append(apos)
                                revealed.append(apos)
            checked.append(pos)
        
        self.revealed.extend(revealed)

    def get_num_mines_around_position(self, x, y):
        """Finds the number of mines around a position."""
        mines = 0
        for row in range(y-1, y+2):
            for col in range(x-1, x+2):
                if row >= 0 and col >= 0 and row < len(self.mine_map) and col < len(self.mine_map[row]): # Don't check spaces that are outside of the array
                    if self.mine_map[row][col]:
                        mines += 1
        return mines