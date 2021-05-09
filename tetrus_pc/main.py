# Tetrus (a Tetris clone)
# By Alexandre Szybiak @aszybiak
# https://alexandreszybiak.itch.io/
# Creative Commons BY-NC-SA 3.0 US

import pygame
import random
import sys
import time

from pygame.locals import *

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

# shape templates
s_shape_template = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

z_shape_template = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

i_shape_template = [['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....'],
                    ['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....']]

o_shape_template = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

j_shape_template = [['.....',
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

l_shape_template = [['.....',
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

t_shape_template = [['.....',
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

shapes = {'s': s_shape_template,
          'z': z_shape_template,
          'j': j_shape_template,
          'l': l_shape_template,
          'i': i_shape_template,
          'o': o_shape_template,
          't': t_shape_template}


class StateMachine:
    def __init__(self):
        self.state = None

    def set_state(self, new_state):
        self.state = new_state

class Display:
    def __init__(self, x, y, width, height, pixel_size):
        self.x = x
        self.y = y
        self.pixels = []
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        for i in range(self.width):
            self.pixels.append([0] * self.height)

    def set_pixel_size(self, value):
        self.pixel_size = value

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.set_cell(x, y, blank)

    def set_cell(self, x, y, value):
        self.pixels[x][y] = value

    def draw(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.pixels[x][y] != blank:
                    self.draw_pixel(x, y, self.pixels[x][y])

    def draw_pixel(self, x, y, color_index):
        pygame.draw.rect(application_surface, (255, 255, 255),
                         (x * self.pixel_size, y * self.pixel_size, self.pixel_size, self.pixel_size))


class MatrixDisplay(Display):
    pass


class LedDisplay(Display):
    def __init__(self, x, y, width, height, pixel_size):
        super().__init__(x, y, width, height, pixel_size)
        self.palette = 0

    def update(self):
        if input_manager.pressed_palette_right:
            self.palette = (self.palette + 1) % len(color_palettes)
        elif input_manager.pressed_palette_left:
            self.palette = (self.palette - 1) % len(color_palettes)

    def draw_pixel(self, x, y, color_index):
        pygame.draw.rect(application_surface, color_palettes[self.palette][color_index],
                         (x * self.pixel_size, y * self.pixel_size, self.pixel_size, self.pixel_size))


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
                if event.button == 3:
                    self.pressed_hard_drop = True
                elif event.button == 2:
                    self.pressed_rotate_left = True
                elif event.button == 0:
                    self.pressed_rotate_right = True
                elif event.button == 5:
                    self.pressed_palette_left = True
                elif event.button == 4:
                    self.pressed_palette_right = True
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
                led_display.set_cell(x + self.x + add_x, y + self.y + add_y, color)

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
                    led_display.set_cell(x, y, self.content[x][y])
        self.falling_piece.update_pixels(color_indexes["piece_shadow"], add_y=self.falling_piece.get_drop_position())
        self.falling_piece.update_pixels(self.falling_piece.color_index)


def is_on_board(x, y):
    return 0 <= x < board.width and y < board.height


def terminate():
    pygame.quit()
    sys.exit()


def run():
    while True:
        # pre update
        input_manager.update()

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

        led_display.update()

        # pre-draw
        led_display.clear()
        matrix_display.clear()
        application_surface.fill((0, 0, 0))

        # draw
        board.update_pixels()
        led_display.draw()
        matrix_display.draw()

        # post-draw
        pygame.display.update()
        fps_clock.tick(fps)


# constant for empty cell
blank = '.'

# state machine
state_fall = 0
state_clear = 1
state_fill = 2
state_wait = 3
state_pause = 4
state_wait_for_controller = 5
state = StateMachine()
state.set_state(state_wait)

pygame.init()

fps = 60
fps_clock = pygame.time.Clock()

board = Board()
board.falling_piece = Piece()
board.board_filler = BoardFiller()

input_manager = InputManager()

led_display = LedDisplay(0, 0, 10, 20, 20)
matrix_display = MatrixDisplay(0, led_display.width * led_display.pixel_size, 32, 8, 8)

window_size = (board.width * led_display.pixel_size,
               board.height * led_display.pixel_size + matrix_display.height * matrix_display.pixel_size)
application_surface = pygame.display.set_mode(window_size)
pygame.display.set_caption('Tetrus')

run()
