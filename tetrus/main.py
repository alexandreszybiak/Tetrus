PI = True

# Game Constants
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

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
                  0x111111,  # piece shadow
                  0x989898,  # placed_piece
                  0xff0000  # death_fill
                  ]

colors_blue = [0x000000,  # background
               0xffffff,  # s
               0xff412e,  # z
               0xffffff,  # j
               0xff412e,  # l
               0x49ebf5,  # i
               0x4982f5,  # o
               0x4982f5,  # t
               0x111111,  # piece shadow
               0x5f5f5f,  # placed_piece
               0xff0000  # death_fill
               ]

colors_bubble = [0x000000,  # background
                 0xffffff,  # s
                 0xf6ff00,  # z
                 0xf6ff00,  # j
                 0xffffff,  # l
                 0xf6ff00,  # i
                 0xf6ff00,  # o
                 0xf6ff00,  # t
                 0x111111,  # piece shadow
                 0xff00a8,  # placed_piece
                 0xff0000  # death_fill
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
                 "death_fill": 10
                 }

color_palettes = [colors_blue, colors_default, colors_bubble]

# Color Constants
BLACK = (0, 0, 16)

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
        self.pressed_any = False
        self.released_down = False
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
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
            if event.type == KEYUP:
                if event.key == K_DOWN:
                    self.pressing_down = False
                    self.released_down = True
                elif event.key == K_LEFT:
                    self.pressing_left = False
                elif event.key == K_RIGHT:
                    self.pressing_right = False
            if event.type == JOYBUTTONDOWN:
                self.pressed_any = True
                if event.button == JKEY_X:
                    self.pressed_hard_drop = True
                elif event.button == JKEY_R:
                    self.pressed_quit = True
                elif event.button == 2:
                    self.pressed_rotate_left = True
                elif event.button == 0:
                    self.pressed_rotate_right = True
                elif event.button == 5:
                    self.pressed_palette_left = True
                elif event.button == 4:
                    self.pressed_palette_right = True
            if event.type == JOYHATMOTION:
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
            if event.type == pygame.JOYAXISMOTION:
                axis = event.axis
                val = round(event.value)
                if axis == 0 and val == 0:
                    self.pressing_left = False
                    self.pressing_right = False
                if axis == 0 and val == -1:
                    self.pressing_left = True
                    self.pressed_left = True
                if axis == 0 and val == 1:
                    self.pressing_right = True
                    self.pressed_right = True


class Piece:
    def __init__(self):
        shape_name = random.choice(list(shapes))
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
        self.run_init_time = time.time()
        self.visible = False

    def reset(self):
        shape_name = random.choice(list(shapes))
        self.x = 3
        self.y = -2
        self.rotation = 0
        self.shape = shapes[shape_name]
        self.color_index = color_indexes[shape_name]
        self.last_fall_time = time.time()
        self.last_soft_drop_time = time.time()
        self.last_run_time = time.time()
        self.run_init_time = time.time()
        self.visible = True
        if not self.is_valid_position(add_x=0, add_y=0):
            board.begin_fill_state()
            self.add_to_board(self.color_index)
            self.visible = False
        input_manager.pressing_down = False
        input_manager.pressing_left = False
        input_manager.pressing_right = False

    def update(self):
        if input_manager.released_down:
            self.last_fall_time = time.time()
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

    def rotate(self, direction):
        self.rotation = (self.rotation + direction) % len(self.shape)
        if not self.is_valid_position():
            self.rotation = (self.rotation - direction) % len(self.shape)

    def speed_up(self):
        if self.fall_frequency > 0.216:
            self.fall_frequency -= 0.083
        elif self.fall_frequency > 0:
            self.fall_frequency -= 0.0166

    def move_vertical(self):
        if not self.is_valid_position(add_x=0, add_y=1):
            self.add_to_board()
        else:
            self.y += 1

    def move_horizontal(self, x):
        if self.is_valid_position(add_x=x):
            self.x += x
            self.last_run_time = time.time()
        else:
            self.run_init_time = 0
            self.last_run_time = 0

    def run(self, x):
        if time.time() - self.last_run_time > self.run_frequency and time.time() - self.run_init_time > self.run_charge_time:
            self.move_horizontal(x)

    def soft_drop(self):
        if time.time() - self.last_soft_drop_time > self.press_down_frequency:
            self.move_vertical()
            self.last_soft_drop_time = time.time()
            if not self.is_valid_position(add_y=1):
                self.last_soft_drop_time = time.time() + (self.press_down_frequency * 5)

    def update_pixels(self, color, add_x=0, add_y=0):
        if not self.visible:
            return
        for x in range(self.template_width):
            for y in range(self.template_height):
                if self.shape[self.rotation][y][x] == blank:
                    continue
                if y + self.y + add_y < 0:
                    continue
                neopixel_draw(x + self.x + add_x, y + self.y + add_y, color_palettes[0][color])

    def hard_drop(self):
        if not self.is_valid_position(add_y=1):
            return
        self.y += self.get_drop_position()
        self.last_fall_time = time.time() - (self.fall_frequency * 0.7)

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
        self.visible = False
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
        elif self.line_to_fill > 0 and time.time() - self.last_fill_time > self.fill_frequency:
            self.line_to_fill -= 1
            board.set_line(self.line_to_fill, color_indexes["death_fill"])
            self.end_fill_time = time.time()
            self.last_fill_time = time.time()


class LineCleaner:
    def __init__(self, target_list):
        self.target_list = target_list
        self.progress = 0
        self.last_clean_time = 0
        self.clean_frequency = 0.05

    def update(self):
        if time.time() - self.last_clean_time > self.clean_frequency:
            if self.progress == 10:
                self.collapse_gaps()
                board.begin_fall_state()
                board.falling_piece.speed_up()
            else:
                for y in self.target_list:
                    board.set_cell(self.progress, y, blank)
                self.last_clean_time = time.time()
            self.progress += 1

    def collapse_gaps(self):
        y = board.height - 1  # start y at the bottom of the board
        for y in self.target_list:
            for shift_line in range(y, 0, -1):
                for x in range(board.width):
                    board.content[x][shift_line] = board.content[x][shift_line - 1]
            for x in range(board.width):
                board.content[x][0] = blank


class Board:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.content = []
        self.falling_piece = None
        self.line_cleaner = None
        self.board_filler = None
        self.state = state_wait
        for i in range(self.width):
            self.content.append([blank] * self.height)

    def reset(self):
        for x in range(self.width):
            for y in range(self.height):
                self.set_cell(x, y, blank)

    def set_cell(self, x, y, value):
        self.content[x][y] = value

    def set_line(self, y, value):
        for x in range(board.width):
            self.content[x][y] = value

    def get_cell(self, x, y):
        if y < 0:
            return blank
        return self.content[x][y]

    def begin_fall_state(self):
        del self.line_cleaner
        self.line_cleaner = None
        self.state = state_fall
        self.falling_piece.reset()

    def begin_wait_state(self):
        self.state = state_wait

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
            self.falling_piece.reset()

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

    def update_pixels(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.content[x][y] != blank:
                    neopixel_draw(x, y, color_palettes[0][self.content[x][y]])
        self.falling_piece.update_pixels(color_indexes["piece_shadow"], add_y=self.falling_piece.get_drop_position())
        self.falling_piece.update_pixels(self.falling_piece.color_index)


def is_on_board(x, y):
    return 0 <= x < board.width and y < board.height


def neopixel_fill(color):
    if PI:
        pixels.fill(color)
    else:
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                neopixel_draw(x, y, color)


def neopixel_draw(x, y, color):
    if PI:
        try:
            if x >= 0 and y >= 0:
                if x % 2 == 1:
                    pixels[x * BOARD_HEIGHT + y] = color
                else:
                    pixels[x * BOARD_HEIGHT + (BOARD_HEIGHT - 1 - y)] = color
        except:
            print(str(x) + ' --- ' + str(y))
    else:
        pygame.display.get_window_size()
        rect_x = pygame.display.get_window_size()[0] / 2 - NEOPIXEL_WIDTH / 2 + x * (NEOPIXEL_SIZE + NEOPIXEL_SPACING)
        rect_y = pygame.display.get_window_size()[1] / 2 - NEOPIXEL_HEIGHT / 2 + y * (NEOPIXEL_SIZE + NEOPIXEL_SPACING)
        pygame.draw.rect(application_surface, color, (rect_x, rect_y, NEOPIXEL_SIZE, NEOPIXEL_SIZE))


def luma_fill(color):
    if PI:
        pass
    else:
        for y in range(8):
            for x in range(32):
                luma_draw(x, y, color)


def luma_draw(x, y, color):
    if PI:
        with canvas(device) as draw:
            draw.point((x, y), fill="white")
        device.show()
    else:
        pygame.display.get_window_size()
        rect_x = pygame.display.get_window_size()[0] / 2 - LUMA_WIDTH / 2 + x * (LUMA_SIZE + LUMA_SPACING)
        rect_y = pygame.display.get_window_size()[1] / 2 + NEOPIXEL_HEIGHT / 2 + y * (LUMA_SIZE + LUMA_SPACING)
        pygame.draw.rect(application_surface, color, (rect_x, rect_y, LUMA_SIZE, LUMA_SIZE))


def update_screen():
    if PI:
        pixels.show()
    else:
        pygame.display.update()


def terminate():
    neopixel_fill((0, 0, 0))
    update_screen()
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
board.falling_piece = Piece()
board.board_filler = BoardFiller()

input_manager = InputManager()

neopixel_fill((0, 0, 32))

if PI:
    with canvas(device) as draw:
        text(draw, (0, 0), "B00BA", fill="white")
        device.show()

while True:
    # Pre-update
    if not PI:
        application_surface.fill((54, 87, 219))
        luma_fill(LUMA_COLOR_OFF)
    input_manager.update()
    neopixel_fill((0, 0, 16))

    # update
    if board.state == state_fall:
        board.falling_piece.update()
    elif board.state == state_clear:
        board.line_cleaner.update()
    elif board.state == state_fill:
        board.board_filler.update()
    elif board.state == state_wait:
        if input_manager.pressed_any:
            board.falling_piece.__init__()
            board.begin_fall_state()

    if input_manager.pressed_quit:
        terminate()

    # Draw
    board.update_pixels()

    # Post-draw
    update_screen()

    time.sleep(0.03)