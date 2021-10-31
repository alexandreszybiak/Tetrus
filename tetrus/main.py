PI = True

# Constant
mask = bytearray([1, 2, 4, 8, 16, 32, 64, 128])

# Game Constants
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Gameplay constants
PAUSE_AFTER_HARD_DROP_TIME = 0.1

# Gamepad Constants
JKEY_X = 3
JKEY_Y = 4
JKEY_A = 0
JKEY_B = 1
JKEY_R = 7
JKEY_L = 6
JKEY_SEL = 10
JKEY_START = 11

# Display simulation Constants
NEOPIXEL_SIZE = 26
NEOPIXEL_SPACING = 4
NEOPIXEL_WIDTH = BOARD_WIDTH * (NEOPIXEL_SIZE + NEOPIXEL_SPACING)
NEOPIXEL_HEIGHT = BOARD_HEIGHT * (NEOPIXEL_SIZE + NEOPIXEL_SPACING)
LUMA_SIZE = 3
LUMA_SPACING = 1
LUMA_COLOR_ON = (255, 0, 0)
LUMA_COLOR_OFF = (0, 0, 0)
LUMA_WIDTH = 32 * (LUMA_SIZE + LUMA_SPACING)
LUMA_HEIGHT = 8 * (LUMA_SIZE + LUMA_SPACING)
BOTH_DEVICE_HEIGHT = NEOPIXEL_HEIGHT + LUMA_HEIGHT

# Color Palettes
colors_default = [0x000000,  # background
                  0xffc96b,  # s
                  0xffc16b,  # z
                  0xff966b,  # j
                  0xffaf6b,  # l
                  0xe82a4d,  # i
                  0xf54e5d,  # o
                  0xff7c6b,  # t
                  0x555555,  # piece shadow
                  0x989898,  # placed_piece
                  0xff0000,  # death_fill
                  0xffffff  # cleared piece
                  ]

colors_meadow = [0x000000,  # background
                 0x5096ff,  # s
                 0x5096ff,  # z
                 0x5096ff,  # j
                 0x5096ff,  # l
                 0x5096ff,  # i
                 0x5096ff,  # o
                 0x5096ff,  # t
                 0x272b29,  # piece shadow
                 0x5da93c,  # placed_piece
                 0xff0000,  # death_fill
                 0xffffff  # cleared piece
                 ]

colors_bubble = [0x000000,  # background
                 0xfff840,  # s
                 0xfff840,  # z
                 0xfff840,  # j
                 0xfff840,  # l
                 0xfff840,  # i
                 0xfff840,  # o
                 0xfff840,  # t
                 0x53071c,  # piece shadow
                 0xf33087,  # placed_piece
                 0xff0000,  # death_fill
                 0xffffff  # cleared piece
                 ]

colors_spring = [0x000000,  # background
                 0x91ea1f,  # s
                 0x91ea1f,  # z
                 0x91ea1f,  # j
                 0x91ea1f,  # l
                 0x91ea1f,  # i
                 0x91ea1f,  # o
                 0x91ea1f,  # t
                 0x0b3248,  # piece shadow
                 0xe65987,  # placed_piece
                 0xff0000,  # death_fill
                 0xffffff  # cleared piece
                 ]

colors_autumn = [0x000000,  # background
                 0x5f991c,  # s
                 0x5f991c,  # z
                 0x5f991c,  # j
                 0x5f991c,  # l
                 0x5f991c,  # i
                 0x5f991c,  # o
                 0x5f991c,  # t
                 0x322610,  # piece shadow
                 0x883e25,  # placed_piece
                 0xff0000,  # death_fill
                 0xffffff  # cleared piece
                 ]

colors_grey = [0x000000,  # background
               0x6d7e74,  # s
               0x6d7e74,  # z
               0x6d7e74,  # j
               0x6d7e74,  # l
               0x6d7e74,  # i
               0x6d7e74,  # o
               0x6d7e74,  # t
               0x2b2d2c,  # piece shadow
               0x545e57,  # placed_piece
               0xff0000,  # death_fill
               0xffffff  # cleared piece
               ]

colors_night = [0x000000,  # background
                0x3131d4,  # s
                0x3131d4,  # z
                0x3131d4,  # j
                0x3131d4,  # l
                0x3131d4,  # i
                0x3131d4,  # o
                0x3131d4,  # t
                0x1b1730,  # piece shadow
                0x1f1f72,  # placed_piece
                0xff0000,  # death_fill
                0xffffff  # cleared piece
                ]

colors_joker = [0x000000,  # background
                0x42ec0e,  # s
                0x42ec0e,  # z
                0x42ec0e,  # j
                0x42ec0e,  # l
                0x42ec0e,  # i
                0x42ec0e,  # o
                0x42ec0e,  # t
                0x50008d,  # piece shadow
                0xb500cb,  # placed_piece
                0xff0000,  # death_fill
                0xffffff  # cleared piece
                ]

colors_lava = [0x000000,  # background
               0xed5e2d,  # s
               0xed5e2d,  # z
               0xed5e2d,  # j
               0xed5e2d,  # l
               0xed5e2d,  # i
               0xed5e2d,  # o
               0xed5e2d,  # t
               0x8e0014,  # piece shadow
               0xd8341e,  # placed_piece
               0xff0000,  # death_fill
               0xffffff  # cleared piece
               ]

color_indexes = {"background": 0,
                 "s": 1,
                 "z": 2,
                 "j": 3,
                 "l": 4,
                 "i": 5,
                 "o": 6,
                 "t": 7,
                 "piece_shadow": 8,
                 "placed_piece": 9,
                 "death_fill": 10,
                 "cleared line": 11
                 }

color_palettes = [colors_meadow, colors_spring, colors_autumn, colors_grey, colors_night, colors_bubble, colors_lava,
                  colors_joker]

# Color Constants
BLACK = (0, 0, 0)
NEOPIXEL_SIMULATOR_COLOR_OFF = (0, 0, 0)
SIMULATOR_BACKGROUND = (24, 24, 24)

# Constant for empty cell
blank = '.'

import random, time, sys, os, pickle
from enum import Enum
import pygame
from pygame.locals import *

if PI:
    import board
    import neopixel
    import subprocess
    from luma.led_matrix.device import max7219
    from luma.core.interface.serial import spi, noop
    from luma.core.render import canvas
    from luma.core.virtual import viewport
    from luma.core.legacy import text, show_message
    from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


class ShapeTemplates(Enum):
    S = [['.....',
          '.....',
          '..OO.',
          '.OO..',
          '.....'],
         ['.....',
          '..O..',
          '..OO.',
          '...O.',
          '.....']]

    Z = [['.....',
          '.....',
          '.OO..',
          '..OO.',
          '.....'],
         ['.....',
          '..O..',
          '.OO..',
          '.O...',
          '.....']]

    I = [['.....',
          '.....',
          'OOOO.',
          '.....',
          '.....'],
         ['..O..',
          '..O..',
          '..O..',
          '..O..',
          '.....']]

    O = [['.....',
          '.....',
          '.OO..',
          '.OO..',
          '.....']]

    J = [['.....',
          '.....',
          '.OOO.',
          '...O.',
          '.....'],
         ['.....',
          '..O..',
          '..O..',
          '.OO..',
          '.....'],
         ['.....',
          '.O...',
          '.OOO.',
          '.....',
          '.....'],
         ['.....',
          '..OO.',
          '..O..',
          '..O..',
          '.....']]

    L = [['.....',
          '.....',
          '.OOO.',
          '.O...',
          '.....'],
         ['.....',
          '.OO..',
          '..O..',
          '..O..',
          '.....'],
         ['.....',
          '...O.',
          '.OOO.',
          '.....',
          '.....'],
         ['.....',
          '..O..',
          '..O..',
          '..OO.',
          '.....']]

    T = [['.....',
          '.....',
          '.OOO.',
          '..O..',
          '.....'],
         ['.....',
          '..O..',
          '.OO..',
          '..O..',
          '.....'],
         ['.....',
          '..O..',
          '.OOO.',
          '.....',
          '.....'],
         ['.....',
          '..O..',
          '..OO.',
          '..O..',
          '.....']]


shapes = {'s': ShapeTemplates.S.value,
          'z': ShapeTemplates.Z.value,
          'j': ShapeTemplates.J.value,
          'l': ShapeTemplates.L.value,
          'i': ShapeTemplates.I.value,
          'o': ShapeTemplates.O.value,
          't': ShapeTemplates.T.value}


class ShapePreviews(Enum):
    S = [0, 1, 1, 0,
         1, 1, 0, 0]
    Z = [1, 1, 0, 0,
         0, 1, 1, 0]
    I = [1, 1, 1, 1,
         0, 0, 0, 0]
    O = [1, 1, 0, 0,
         1, 1, 0, 0]
    J = [1, 1, 1, 0,
         0, 0, 1, 0]
    L = [1, 1, 1, 0,
         1, 0, 0, 0]
    T = [1, 1, 1, 0,
         0, 1, 0, 0]


number_font = [
    0x1F, 0x11, 0x1F,
    0x00, 0x00, 0x1F,
    0x1D, 0x15, 0x17,
    0x15, 0x15, 0x1F,
    0x07, 0x04, 0x1F,
    0x17, 0x15, 0x1D,
    0x1F, 0x15, 0x1D,
    0x01, 0x01, 0x1F,
    0x1F, 0x15, 0x1F,
    0x17, 0x15, 0x1F]

shape_previews = {'s': ShapePreviews.S.value,
                  'z': ShapePreviews.Z.value,
                  'j': ShapePreviews.J.value,
                  'l': ShapePreviews.L.value,
                  'i': ShapePreviews.I.value,
                  'o': ShapePreviews.O.value,
                  't': ShapePreviews.T.value}

PIECES_ORDER = {'s': 0, 'z': 1, 'i': 2, 'j': 3, 'l': 4, 'o': 5, 't': 6}

theTetrisFont = [
    0x78, 0x78, 0x1E, 0x1E,  # S
    0x1E, 0x1E, 0x78, 0x78,  # Z
    0x00, 0xFF, 0xFF, 0x00,  # I
    0x06, 0x06, 0x7E, 0x7E,  # J
    0x7E, 0x7E, 0x06, 0x06,  # L
    0x3C, 0x3C, 0x3C, 0x3C,  # O
    0x7E, 0x7E, 0x18, 0x18,  # T
]


class GameObject:
    def __init__(self):
        self.active = False
        self.visible = False

    def update(self):
        pass

    def draw(self):
        pass


class StateMachine:
    def __init__(self):
        self.state = None

    def set_state(self, new_state):
        self.state = new_state


class InputManager:
    def __init__(self):
        self.pressing_left = False
        self.pressing_right = False
        self.pressing_down = False
        self.pressed_debug = False
        self.pressed_left = False
        self.pressed_right = False
        self.pressed_down = False
        self.pressed_rotate_left = False
        self.pressed_rotate_right = False
        self.pressed_hard_drop = False
        self.pressed_reset_board = False
        self.pressed_quit = False
        self.pressed_any = False
        self.released_down = False
        self.pressed_palette_left = False
        self.pressed_palette_right = False
        self.joystick = None
        self.update_controller_status()

    def update_controller_status(self):
        if not pygame.joystick.get_init():
            pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            if self.joystick is None:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
        else:
            if self.joystick is not None:
                self.joystick.quit()
            self.joystick = None

    def update(self):
        self.update_controller_status()
        self.pressed_left = False
        self.pressed_right = False
        self.pressed_down = False
        self.pressed_rotate_left = False
        self.pressed_rotate_right = False
        self.pressed_hard_drop = False
        self.pressed_reset_board = False
        self.pressed_palette_left = False
        self.pressed_palette_right = False
        self.pressed_quit = False
        self.pressed_debug = False
        self.pressed_any = False
        self.released_down = False
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                self.pressed_any = True
                if event.key == K_LEFT:
                    self.pressing_left = True
                    self.pressed_left = True
                elif event.key == K_RIGHT:
                    self.pressing_right = True
                    self.pressed_right = True
                elif event.key == K_UP:
                    self.pressed_rotate_left = True
                elif event.key == K_DOWN:
                    self.pressing_down = True
                    self.pressed_down = True
                elif event.key == K_SPACE:
                    self.pressed_hard_drop = True
                elif event.key == K_d:
                    self.pressed_reset_board = True
                elif event.key == K_c:
                    self.pressed_palette_left = True
                elif event.key == K_v:
                    self.pressed_palette_right = True
                elif event.key == K_ESCAPE:
                    self.pressed_quit = True
                elif event.key == K_TAB:
                    self.pressed_debug = True
            elif event.type == KEYUP:
                if event.key == K_DOWN:
                    self.pressing_down = False
                    self.released_down = True
                elif event.key == K_LEFT:
                    self.pressing_left = False
                elif event.key == K_RIGHT:
                    self.pressing_right = False
            elif event.type == JOYBUTTONDOWN:
                self.pressed_any = True
                if event.button == JKEY_X:
                    self.pressed_hard_drop = True
                elif event.button == JKEY_SEL:
                    self.pressed_quit = True
                elif event.button == 2:
                    self.pressed_rotate_left = True
                elif event.button == 0:
                    self.pressed_rotate_right = True
                elif event.button == 5:
                    self.pressed_palette_left = True
                elif event.button == 4:
                    self.pressed_palette_right = True
                elif event.button == JKEY_R:
                    self.pressed_debug = True
            elif event.type == pygame.JOYAXISMOTION:
                axis = event.axis
                val = round(event.value)
                if axis == 0:
                    if val == 0:
                        self.pressing_left = False
                        self.pressing_right = False
                    elif val == -1:
                        self.pressing_left = True
                        self.pressed_left = True
                    elif val == 1:
                        self.pressing_right = True
                        self.pressed_right = True
                elif axis == 1:
                    if val == 0:
                        if self.pressing_down:
                            self.released_down = True
                        self.pressing_down = False
                    elif val == 1:
                        self.pressed_down = True
                        self.pressing_down = True
            elif event.type == JOYHATMOTION:
                if event.value[0] == -1:
                    self.pressing_left = True
                    self.pressed_left = True
                elif event.value[0] == 1:
                    self.pressing_right = True
                    self.pressed_right = True
                elif event.value[0] == 0:
                    self.pressing_left = False
                    self.pressing_right = False
                if event.value[1] == -1:
                    self.pressing_down = True
                    self.pressed_down = True
                elif event.value[1] == 1:
                    self.pressed_hard_drop = True
                elif event.value[1] == 0:
                    if self.pressing_down:
                        self.released_down = True
                    self.pressing_down = False


class NeoPixelScreen:
    def __init__(self):
        self.current_palette = 0
        self.need_refresh = True

    def set_cell(self, x, y, color_index):
        self.draw_cell(x, y, color_palettes[self.current_palette][color_index])

    def clear_cell(self, x, y):
        self.draw_cell(x, y, BLACK)

    def set_line(self, y, color_index):
        for x in range(BOARD_WIDTH):
            self.set_cell(x, y, color_index)

    def fill(self, color_index):
        pixels.fill(color_palettes[self.current_palette][color_index])
        self.need_refresh = True

    def draw_cell(self, x, y, color):
        try:
            if x >= 0 and y >= 0:
                if x % 2 == 1:
                    pixels[x * BOARD_HEIGHT + y] = color
                else:
                    pixels[x * BOARD_HEIGHT + (BOARD_HEIGHT - 1 - y)] = color
        except:
            print(str(x) + ' --- ' + str(y))
        self.need_refresh = True

    def refresh(self):
        if self.need_refresh:
            pixels.show()
        self.need_refresh = False


class NeoPixelScreenSimulator(NeoPixelScreen):
    def __init__(self):
        super().__init__()
        self.content = []
        for i in range(BOARD_WIDTH):
            self.content.append([0] * BOARD_HEIGHT)

    def set_cell(self, x, y, color_index):
        self.content[x][y] = color_palettes[self.current_palette][color_index]

    def clear_cell(self, x, y):
        self.content[x][y] = 0

    def fill(self, color_index):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.content[x][y] = color_palettes[self.current_palette][color_index]

    @staticmethod
    def draw_cell(x, y, color):
        pygame.display.get_window_size()
        rect_x = pygame.display.get_window_size()[0] / 2 - NEOPIXEL_WIDTH / 2 + x * (NEOPIXEL_SIZE + NEOPIXEL_SPACING)
        rect_y = pygame.display.get_window_size()[1] / 2 - NEOPIXEL_HEIGHT / 2 + y * (NEOPIXEL_SIZE + NEOPIXEL_SPACING)
        pygame.draw.rect(application_surface, color, (rect_x, rect_y, NEOPIXEL_SIZE, NEOPIXEL_SIZE))

    def refresh(self):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.draw_cell(x, y, self.content[x][y])
        pygame.display.update()


class Piece(GameObject):
    def __init__(self):
        super().__init__()
        shape_name = piece_dealer.deal_piece()
        self.x = 3
        self.y = -2
        self.rotation = 0
        self.shape = shapes[shape_name]
        self.template_width = 5
        self.template_height = 5
        self.color_index = color_indexes[shape_name]
        self.fall_frequency = 0.8
        self.press_down_frequency = 0.025
        self.run_charge_time = 0.15
        self.run_frequency = 0.04
        self.last_fall_time = time.time()
        self.last_soft_drop_time = time.time()
        self.last_run_time = time.time()
        self.last_hard_drop_time = time.time()
        self.run_init_time = time.time()
        self.drop_row_count = 0
        self.movable = True
        self.hard_dropped = False

    def reset(self, piece):
        shape_name = piece
        self.x = 3
        self.y = -2
        self.rotation = 0
        self.shape = shapes[shape_name]
        self.color_index = color_indexes[shape_name]
        self.last_fall_time = time.time()
        self.last_soft_drop_time = time.time()
        self.last_run_time = time.time()
        self.run_init_time = time.time()
        self.last_hard_drop_time = time.time()
        self.visible = True
        self.active = True
        self.drop_row_count = 0
        self.movable = True
        self.hard_dropped = False
        self.draw_piece(color_indexes["piece_shadow"], add_y=self.get_drop_position())
        self.draw_piece(self.color_index)
        if not self.is_valid_position(add_x=0, add_y=0):
            board.begin_fill_state()
            self.add_to_board(self.color_index)
            self.visible = True
        input_manager.pressing_down = False
        # input_manager.pressing_left = False
        # input_manager.pressing_right = False

    def update(self):
        if self.movable:
            if input_manager.released_down:
                self.last_fall_time = time.time()
                self.drop_row_count = 0
                if not self.is_valid_position(add_y=1):
                    self.add_to_board()
            # move horizontally
            if input_manager.pressed_left:
                self.run_init_time = time.time()
                self.move_horizontal(-1)
            elif input_manager.pressed_right:
                self.move_horizontal(1)
                self.run_init_time = time.time()
            # rotation
            if input_manager.pressed_rotate_left:
                self.rotate(-1)
            elif input_manager.pressed_rotate_right:
                self.rotate(1)
            # soft and hard drops
            if input_manager.pressed_down:
                self.move_vertical()
                self.last_soft_drop_time = time.time()
            if input_manager.pressed_hard_drop:
                self.hard_drop()
            # debug, reset the board
            if input_manager.pressed_reset_board:
                board.reset()
            # fast movements
            if input_manager.pressing_left:
                self.run(-1)
            elif input_manager.pressing_right:
                self.run(1)
            if input_manager.pressing_down:
                self.soft_drop()
            elif time.time() - self.last_fall_time > self.fall_frequency:
                self.last_fall_time = time.time()
                self.move_vertical()
        elif self.hard_dropped:
            if time.time() > self.last_hard_drop_time + PAUSE_AFTER_HARD_DROP_TIME:
                self.add_to_board()

    def rotate(self, direction):
        self.clear_piece()
        self.clear_piece(add_y=self.get_drop_position())
        self.rotation = (self.rotation + direction) % len(self.shape)
        if not self.is_valid_position():
            self.rotation = (self.rotation - direction) % len(self.shape)
            self.draw_piece(self.color_index)
        self.draw_piece(color_indexes["piece_shadow"], add_y=self.get_drop_position())
        self.draw_piece(self.color_index)

    def speed_up(self):
        if self.fall_frequency > 0.216:
            self.fall_frequency -= 0.083
        elif self.fall_frequency > 0:
            self.fall_frequency -= 0.0166

    def move_vertical(self):
        if not self.is_valid_position(add_x=0, add_y=1):
            self.add_to_board()
        else:
            self.clear_piece()
            self.y += 1
            self.draw_piece(self.color_index)

    def move_horizontal(self, x):
        if self.is_valid_position(add_x=x):
            self.clear_piece(add_y=self.get_drop_position())
            self.clear_piece()
            self.x += x
            self.last_run_time = time.time()
            self.draw_piece(color_indexes["piece_shadow"], add_y=self.get_drop_position())
            self.draw_piece(self.color_index)
        else:
            self.run_init_time = 0
            self.last_run_time = 0

    def run(self, x):
        if time.time() - self.last_run_time > self.run_frequency and time.time() - self.run_init_time > self.run_charge_time:
            self.move_horizontal(x)

    def soft_drop(self):
        if time.time() - self.last_soft_drop_time > self.press_down_frequency:
            self.move_vertical()
            self.drop_row_count += 1
            self.last_soft_drop_time = time.time()
            if not self.is_valid_position(add_y=1):
                self.last_soft_drop_time = time.time() + (self.press_down_frequency * 5)

    def draw_piece(self, color, add_x=0, add_y=0):
        for x in range(self.template_width):
            for y in range(self.template_height):
                if self.shape[self.rotation][y][x] == blank:
                    continue
                if y + self.y + add_y < 0:
                    continue
                neopixel_screen.set_cell(x + self.x + add_x, y + self.y + add_y, color)

    def clear_piece(self, add_x=0, add_y=0):
        for x in range(self.template_width):
            for y in range(self.template_height):
                if self.shape[self.rotation][y][x] == blank:
                    continue
                if y + self.y + add_y < 0:
                    continue
                neopixel_screen.clear_cell(x + self.x + add_x, y + self.y + add_y)

    def hard_drop(self):
        if not self.is_valid_position(add_y=1):
            return
        self.clear_piece()
        row_count = self.get_drop_position()
        self.y += row_count
        self.drop_row_count = row_count << 1
        self.movable = False
        self.hard_dropped = True
        self.last_hard_drop_time = time.time()
        self.draw_piece(self.color_index)

    def get_drop_position(self):
        for i in range(1, board.height - self.y):
            if not self.is_valid_position(add_y=i):
                break
        return i - 1

    def add_to_board(self, color_index=color_indexes["placed_piece"]):
        for x in range(self.template_width):
            for y in range(self.template_height):
                if self.shape[self.rotation][y][x] != blank:
                    board.set_cell(x + self.x, y + self.y, color_index)
                    neopixel_screen.set_cell(x + self.x, y + self.y, color_index)
        self.visible = False
        self.active = False
        hud.show_lines = False
        board.score += self.drop_row_count
        hud.need_redraw = True
        if board.state == state_fall:
            board.check_for_complete_line()

    def is_valid_position(self, add_x=0, add_y=0):
        for x in range(self.template_width):
            for y in range(self.template_height):
                if self.shape[self.rotation][y][x] == blank:
                    continue
                if not is_on_board(x + self.x + add_x, y + self.y + add_y):
                    return False
                if board.get_cell(x + self.x + add_x, y + self.y + add_y) != blank:
                    return False
        return True

    def __del__(self):
        pass


class BoardFiller:
    def __init__(self):
        self.line_to_fill = 20
        self.pause_before_reset_duration = 0.75
        self.end_fill_time = 0
        self.last_fill_time = 0
        self.fill_frequency = 0.05

    def reset(self):
        self.last_fill_time = time.time()
        self.line_to_fill = 20

    def update(self):
        if self.line_to_fill == 0 and time.time() - self.end_fill_time > self.pause_before_reset_duration:
            board.reset()
            board.begin_wait_state()
            neopixel_screen.fill(0)
            neopixel_screen.current_palette = 0
        elif self.line_to_fill > 0 and time.time() - self.last_fill_time > self.fill_frequency:
            self.line_to_fill -= 1
            neopixel_screen.set_line(self.line_to_fill, color_indexes["death_fill"])
            self.end_fill_time = time.time()
            self.last_fill_time = time.time()


class LineCleaner:
    def __init__(self, target_list):
        self.target_list = target_list
        self.progress = 0
        self.last_clean_time = 0
        self.clean_frequency = 0.05
        self.points_to_give = 0
        if len(self.target_list) == 1:
            self.points_to_give = 40 * (board.level + 1) // 5
        elif len(self.target_list) == 2:
            self.points_to_give = 100 * (board.level + 1) // 5
        elif len(self.target_list) == 3:
            self.points_to_give = 300 * (board.level + 1) // 5
        else:
            self.points_to_give = 1200 * (board.level + 1) // 5

    def update(self):
        if time.time() - self.last_clean_time > self.clean_frequency:
            if self.progress == 7:
                self.collapse_gaps()
                if board.total_line_cleared // 10 > board.level:
                    board.level += 1
                    neopixel_screen.current_palette = board.level % len(color_palettes)
                    board.draw_stack()
                    falling_piece.speed_up()
                board.begin_fall_state()
            else:
                for y in self.target_list:
                    blank_pos = self.progress - 1
                    if 0 < self.progress < 6:
                        board.set_cell(4 - blank_pos, y, blank)
                        board.set_cell(5 + blank_pos, y, blank)
                        neopixel_screen.set_cell(4 - blank_pos, y, 0)
                        neopixel_screen.set_cell(5 + blank_pos, y, 0)
                    if self.progress < 5:
                        board.set_cell(4 - self.progress, y, color_indexes["cleared line"])
                        board.set_cell(5 + self.progress, y, color_indexes["cleared line"])
                        neopixel_screen.set_cell(4 - self.progress, y, color_indexes["cleared line"])
                        neopixel_screen.set_cell(5 + self.progress, y, color_indexes["cleared line"])
                self.last_clean_time = time.time()
                if self.progress < len(self.target_list):
                    board.total_line_cleared += 1
                    hud.need_redraw = True
                if self.progress < 5:
                    board.score += self.points_to_give
                    hud.need_redraw = True
            self.progress += 1

    def collapse_gaps(self):
        y = board.height - 1  # start y at the bottom of the board
        for y in self.target_list:
            for shift_line in range(y, 0, -1):
                for x in range(board.width):
                    top_color_index = board.content[x][shift_line - 1]
                    board.content[x][shift_line] = top_color_index
                    if top_color_index == blank:
                        neopixel_screen.set_cell(x, shift_line, 0)
                    else:
                        neopixel_screen.set_cell(x, shift_line, top_color_index)
            for x in range(board.width):
                board.content[x][0] = blank
                neopixel_screen.set_cell(x, 0, 0)


class Board(GameObject):
    def __init__(self):
        super().__init__()
        self.width = 10
        self.height = 20
        self.content = []
        self.next_piece = None
        self.line_cleaner = None
        self.board_filler = None
        self.state = state_wait
        self.score = 0
        self.total_line_cleared = 0
        self.level = 0
        self.hud_show_lines = False
        for i in range(self.width):
            self.content.append([blank] * self.height)

    def reset(self):
        self.score = 0
        self.total_line_cleared = 0
        self.level = 0
        self.next_piece = None
        for x in range(self.width):
            for y in range(self.height):
                self.set_cell(x, y, blank)

    def set_cell(self, x, y, value):
        self.content[x][y] = value

    def set_line(self, y, value):
        for x in range(board.width):
            self.set_cell(x, y, value)

    def get_cell(self, x, y):
        if y < 0:
            return blank
        return self.content[x][y]

    def pick_next_piece(self):
        self.next_piece = piece_dealer.deal_piece()
        hud.need_redraw = True

    def begin_fall_state(self):
        del self.line_cleaner
        self.line_cleaner = None
        self.state = state_fall
        falling_piece.reset(self.next_piece)
        self.pick_next_piece()

    def begin_wait_state(self):
        self.state = state_wait
        falling_piece.visible = False
        hud.visible = False

    def begin_fill_state(self):
        self.board_filler.reset()
        self.state = state_fill

    def check_for_complete_line(self):
        complete_lines = []
        for y in range(self.height):
            if self.is_line_complete(y):
                complete_lines.append(y)
        if len(complete_lines) > 0:
            self.state = state_clear
            self.line_cleaner = LineCleaner(complete_lines)
        else:
            falling_piece.reset(self.next_piece)
            self.pick_next_piece()

    def is_line_complete(self, y):
        for x in range(self.width):
            if self.content[x][y] == blank:
                return False
        return True

    def is_line_empty(self, y):
        for x in range(self.width):
            if self.content[x][y] != blank:
                return False
        return True

    def transition_to_clear_state(self):
        self.state = state_clear
        LineCleaner()

    def update(self):
        if self.state == state_fall:
            pass
        elif self.state == state_clear:
            self.line_cleaner.update()
        elif self.state == state_fill:
            self.board_filler.update()
        elif self.state == state_wait:
            if input_manager.pressed_any:
                falling_piece.__init__()
                falling_piece.active = True
                hud.active = True
                hud.visible = True
                self.pick_next_piece()
                self.begin_fall_state()

    def draw_stack(self):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                if self.content[x][y] == blank:
                    continue
                neopixel_screen.set_cell(x, y, self.content[x][y])


class HUD(GameObject):
    def __init__(self):
        super().__init__()
        self.show_lines = False
        self.show_fps = False
        self.need_redraw = True

    @staticmethod
    def draw_piece(piece, offset_x, offset_y, draw_surface):
        for x in range(0, 8):
            for y in range(0, 4):
                index = x // 2 + y // 2 * 4
                if shape_previews[piece][index] == 1:
                    luma_draw(offset_x + x, offset_y + y, (255, 0, 0), draw_surface)

    @staticmethod
    def draw_score(number, offset_x, offset_y, draw_surface):
        for x in range(0, 3):
            for y in range(0, 5):
                if number_font[3 * number + x] & mask[y]:
                    luma_draw(offset_x + x, offset_y + y, (255, 0, 0), draw_surface)

    @staticmethod
    def draw_lines(number, offset_x, offset_y, draw_surface):

        for i in range(0, number % 10):
            luma_draw(31 - i, 6, (255, 0, 0), draw_surface)

    def update(self):
        if input_manager.pressed_debug:
            self.show_fps = not self.show_fps
            self.need_redraw = True

    def draw(self):
        if input_manager.pressed_debug:
            self.draw_fps()
        else:
            self.draw_hud()

    def draw_fps(self):
        _fps = int(clock.get_fps())
        if PI:
            if not self.need_redraw:
                return
            self.need_redraw = False
            with canvas(device) as draw_surface:
                for i in range(0, 2):
                    self.draw_score(_fps % 10, 29 - i * 4, 0, draw_surface)
                    _fps //= 10

                device.show()
        else:
            for i in range(0, 2):
                self.draw_score(_fps % 10, 29 - i * 4, 0, application_surface)
                _fps //= 10

    def draw_hud(self):
        _score = board.score
        _num_line = board.total_line_cleared
        if PI:
            if not self.need_redraw:
                return
            self.need_redraw = False
            with canvas(device) as draw_surface:
                # draw score
                if not self.show_lines:
                    for i in range(0, 6):
                        self.draw_score(_score % 10, 29 - i * 4, 0, draw_surface)
                        _score //= 10
                else:
                    for i in range(0, 3):
                        self.draw_score(_num_line % 10, 29 - i * 4, 0, draw_surface)
                        _num_line //= 10

                # draw next piece
                if board.next_piece is not None:
                    self.draw_piece(board.next_piece, 0, 0, draw_surface)

                device.show()
        else:
            # draw score
            if not self.show_lines:
                for i in range(0, 6):
                    self.draw_score(_score % 10, 29 - i * 4, 0, application_surface)
                    _score //= 10
            else:
                for i in range(0, 3):
                    self.draw_score(_num_line % 10, 29 - i * 4, 0, application_surface)
                    _num_line //= 10

            # draw next piece
            if board.next_piece is not None:
                self.draw_piece(board.next_piece, 0, 0, application_surface)

            self.draw_lines(board.total_line_cleared, 0, 0, application_surface)


class PieceDealer:
    def __init__(self):
        pass

    def deal_piece(self):
        return random.choice(list(shapes))


class PieceDealerBag(PieceDealer):
    def __init__(self):
        self.bag = []
        self.fill_bag()

    def fill_bag(self):
        self.bag = list(shapes.keys())
        random.shuffle(self.bag)
        print(self.bag)

    def deal_piece(self):
        dealt_piece = self.bag.pop()
        if len(self.bag) == 0:
            self.fill_bag()
        return dealt_piece


class PieceDealerBagAlex(PieceDealer):
    def __init__(self):
        self.bag = []
        self.piece_history = {'s': 0,
                              'z': 0,
                              'j': 0,
                              'l': 0,
                              'i': 0,
                              'o': 0,
                              't': 0}
        self.fill_bag()

    def fill_bag(self):
        self.bag = list(shapes.keys())
        self.bag.append(random.choice(list(shapes)))
        self.bag.append(random.choice(list(shapes)))
        self.bag.append(random.choice(list(shapes)))
        self.bag.append(random.choice(list(shapes)))
        self.bag.append(self.get_rare_piece())
        print(self.bag)
        random.shuffle(self.bag)

    def deal_piece(self):
        dealt_piece = self.bag.pop()
        self.piece_history[dealt_piece] = self.piece_history[dealt_piece] + 1
        #print(self.piece_history)
        if len(self.bag) == 0:
            self.fill_bag()
        return dealt_piece

    def get_rare_piece(self):
        rare_piece_quantity = min(self.piece_history.values())
        rare_piece_candidates = []
        for i in self.piece_history:
            if self.piece_history.get(i) == rare_piece_quantity:
                rare_piece_candidates.append(i)
        print(rare_piece_candidates)
        print(self.piece_history)
        choice = random.choice(rare_piece_candidates)
        return random.choice(rare_piece_candidates)


def is_on_board(x, y):
    return 0 <= x < board.width and y < board.height


def luma_fill(color):
    if PI:
        pass
    else:
        for y in range(8):
            for x in range(32):
                luma_draw(x, y, color, application_surface)


def luma_draw(x, y, color, draw_surface):
    if PI:
        draw_surface.point((x, y), fill="white")
    else:
        pygame.display.get_window_size()
        rect_x = pygame.display.get_window_size()[0] / 2 - LUMA_WIDTH / 2 + x * (LUMA_SIZE + LUMA_SPACING)
        rect_y = pygame.display.get_window_size()[1] / 2 + NEOPIXEL_HEIGHT / 2 + y * (LUMA_SIZE + LUMA_SPACING)
        pygame.draw.rect(draw_surface, color, (rect_x, rect_y, LUMA_SIZE, LUMA_SIZE))


def terminate():
    neopixel_screen.fill(0)
    neopixel_screen.refresh()
    pygame.quit()
    exit()


# state machine
state_fall = 0
state_clear = 1
state_fill = 2
state_wait = 3
state_pause = 4
state_wait_for_controller = 5
state = StateMachine()
state.set_state(state_wait)

# Init
if PI:
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, blocks_arranged_in_reverse_order=True, block_orientation=90)
    device.contrast(20)
    pixel_pin = board.D21
    num_pixels = BOARD_WIDTH * BOARD_HEIGHT
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.30, auto_write=False, pixel_order=neopixel.GRB)
else:
    pygame.display.set_caption("Tetrus Desktop")
    application_surface = pygame.display.set_mode((0, 0))

joystick_detected = False
pygame.init()
pygame.joystick.init()

board = Board()
piece_dealer = PieceDealerBagAlex()
falling_piece = Piece()
board.board_filler = BoardFiller()
hud = HUD()
input_manager = InputManager()

draw_list = [hud]
update_list = [board, falling_piece, hud]
board.active = True
board.visible = True



clock = pygame.time.Clock()

if PI:
    neopixel_screen = NeoPixelScreen()
else:
    neopixel_screen = NeoPixelScreenSimulator()

neopixel_screen.fill(0)

if not PI:
    application_surface.fill(SIMULATOR_BACKGROUND)
    luma_fill(LUMA_COLOR_OFF)

while True:
    # Pre-draw
    if not PI:
        luma_fill(LUMA_COLOR_OFF)
    # neopixel_fill(NEOPIXEL_SIMULATOR_COLOR_OFF)

    # Pre-update
    input_manager.update()

    # update
    for game_object in update_list:
        if game_object.active:
            game_object.update()

    if input_manager.pressed_quit:
        terminate()

    # Draw
    for sprite in draw_list:
        if sprite.visible:
            sprite.draw()

    # Post-draw
    neopixel_screen.refresh()

    clock.tick(30)
