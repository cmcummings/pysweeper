import pygame, board, os

IMG_PATH = 'res/img'
IMG = {
    board.ZERO: "0.png",
    board.ONE: "1.png",
    board.TWO: "2.png",
    board.THREE: "3.png",
    board.FOUR: "4.png",
    board.FIVE: "5.png",
    board.SIX: "6.png",
    board.SEVEN: "7.png",
    board.EIGHT: "8.png",

    board.FLAG: "flagged.png",
    board.UNREVEALED: "unrevealed.png",
    board.BOMB: "bomb.png"
}

def load_tiles(tile_size):
    tiles = {}

    for val, filename in IMG.items():
        img = load_image(filename)
        tiles[val] = pygame.transform.scale(img, (tile_size, tile_size))

    return tiles

def load_image(filename):
    return pygame.image.load(os.path.join(IMG_PATH, filename))