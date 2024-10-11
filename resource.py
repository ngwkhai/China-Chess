""" Module UI của game """

import pygame

# [CONSTANTS]
ORIGIN_X, ORIGIN_Y = 45, 10 # Toạ độ gốc
START_X, START_Y = 47, 8
STEP_X, STEP_Y = 63, 65
PIECE_SIZE = 60 # Kích thước quân cờ
RESOURCES_PATH = 'resources/'
# [END CONSTANTS]

def piece_sprite(piece):
    """ Hình ảnh quân cờ và vị trí của nó. """

    position_x = START_X + piece.position[1] * STEP_Y
    position_y = START_Y + piece.position[0] * STEP_Y

    piece_img = pygame.image.load(RESOURCES_PATH + 'board/' + str(piece) + '.png')
    return piece_img, (position_x, position_y)

def chosen_ring_sprite(pos, inverse: bool = False):
    """ Vòng tròn xung quanh quân cờ khi chọn quân cờ. """
    chosen_ring_img = pygame.image.load(RESOURCES_PATH + 'chosen_ring.png')
    pos = (abs(pos[0] - 9 * int(inverse)), pos[1])

    position_x = START_X + pos[1]*STEP_X
    position_y = START_Y + pos[0]*STEP_Y
    
    return chosen_ring_img, (position_x, position_y)

def get_piece_position(pos, inverse: bool = False):
    """ Trả về vị trí logic của quân cờ. """
    position_x = (pos[1] - START_Y)//STEP_Y
    position_y = (pos[0] - START_X)//STEP_X
    
    if (
        position_x not in range(0, 10) 
        or position_y not in range(0, 9)
    ):
        return None
    return abs(position_x - 9 * int(inverse)), position_y

def board_sprite():
    """ Trả về sprite của bàn cờ."""

    chess_board_img = pygame.image.load(RESOURCES_PATH + 'board/' + 'chess_board.png')
    return chess_board_img, (ORIGIN_X, ORIGIN_Y)

def background():
    """ Trả về hình nền của bàn cờ. """
    background_img = pygame.image.load(RESOURCES_PATH + 'background.png')
    return background_img, (0, 0)
    

def icon():
    """ Trả về hình ảnh quân cờ."""
    icon_img = pygame.image.load(RESOURCES_PATH + 'chess_icon.png')
    return icon_img


def get_font(size, index):
    """Trả về phông chữ    """
    if index == 0:
        return pygame.font.Font(RESOURCES_PATH + "fonts/" + "HARMONI.otf", size)
    elif index == 1:
        return pygame.font.Font(RESOURCES_PATH + "fonts/" + "Tango.otf", size)
    elif index == 2:
        return pygame.font.Font(RESOURCES_PATH + "fonts/" + "font.ttf", size)