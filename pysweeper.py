import pygame, sys, board, resource, math
from tkinter import simpledialog

SIZE = WIDTH, HEIGHT = 1280, 720
TILE_SIZE = 25

class Game:

    def __init__(self, window_size):
        # Initialize Minesweeper states
        self.board = board.Board(board.generate_mine_map())
        self.revealed_board = self.board.generate_revealed_board()
        self.tile_selected = None
        self.failed_pos = None
        self.mouse_down = False


        # Calculate mine size
        self.tile_size = TILE_SIZE # self.calculate_tile_size()
        self.tiles = resource.load_tiles(self.tile_size)

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.tile_size*self.board.width, self.tile_size*self.board.height))
        pygame.display.set_caption("Minesweeper")

        # Start the game loop
        self.start()

    def update(self):
        pass

    def draw(self):
        # Clear screen
        self.screen.fill((182.5, 182.5, 182.5))

        # Draw board
        for y, row in enumerate(self.revealed_board):
            for x, val in enumerate(row):
                if self.tile_selected == (x, y) and val == board.UNREVEALED:
                    val = board.ZERO

                # Draw red square under bomb if failed
                if self.failed_pos == (x, y):
                    fail_pos_rect = pygame.Rect(self.tile_size*x, self.tile_size*y, self.tile_size, self.tile_size)
                    self.screen.fill((255, 0, 0), rect=fail_pos_rect)

                # Draw tile
                img = self.tiles[val]
                rect = img.get_rect()
                rect.x = self.tile_size * x
                rect.y = self.tile_size * y
                self.screen.blit(img, rect)

    def new_game(self, map=board.generate_mine_map()):
        self.revealed_board = self.board.generate_revealed_board(bombs=True)
        self.board = board.Board(board.generate_mine_map())

    def toggle_flag(self, pos):
        self.board.toggle_flag(pos)
        self.revealed_board = self.board.generate_revealed_board()

    def start(self):
        """Starts the game loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                    if self.mouse_down:
                        self.tile_selected = self.get_tile_at_position(self.mouse_pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                    self.tile_selected = self.get_tile_at_position(self.mouse_pos)
                
                if event.type == pygame.MOUSEBUTTONUP: # Discover
                    self.mouse_down = False
                    self.tile_selected = self.get_tile_at_position(self.mouse_pos)
                    if self.tile_selected:
                        safe = self.board.reveal(self.tile_selected)
                        if not safe:
                            # Lose
                            self.failed_pos = self.tile_selected
                            self.new_game()
                        else:
                            # Continue
                            self.failed_pos = None
                            self.revealed_board = self.board.generate_revealed_board()
                        self.tile_selected = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: # Mark flag
                        self.toggle_flag(self.get_tile_at_position(self.mouse_pos))
                    elif event.key == pygame.K_F2: # Restart
                        self.new_game()
                    elif event.key == pygame.K_ESCAPE: # Deselect
                        self.mouse_down = False
                        self.tile_selected = None

            self.update()
            self.draw()

            pygame.display.flip()

    def calculate_tile_size(self):
        """Calculates the size of a tile such that when the board is drawn, it will fit the window."""
        tiles_x, tiles_y = self.board.size
        screen_width, screen_height = self.screen.get_size()

        shorter_length = screen_width if screen_width < screen_height else screen_height

        return int(shorter_length/tiles_y if tiles_x > tiles_y else shorter_length/tiles_x)

    def get_tile_at_position(self, position):
        """Returns the tile position from a given pixel position"""
        # offset + size * i
        x = math.floor(position[0]/self.tile_size)
        y = math.floor(position[1]/self.tile_size)
        return x, y


if __name__ == "__main__":
    Game(SIZE)