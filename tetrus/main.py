from dataclasses import dataclass

PI = True

# Constant
mask = bytearray([1, 2, 4, 8, 16, 32, 64, 128])

# Game Constants
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Gameplay constants
PAUSE_AFTER_HARD_DROP_TIME = 0.1
PAUSE_BETWEEN_LINE_CLEAR_STEPS = 0.03

# Gamepad Constants
JKEY_X = 3
JKEY_Y = 4
JKEY_A = 0
JKEY_B = 1
JKEY_START = 7
JKEY_L = 6
JKEY_SEL = 10
JKEY_R = 11

if PI:
    JKEY_START = 11
    JKEY_R = 7

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


@dataclass
class Palette:
    piece_color: int = 0xff7c6b
    stack_color: int = 0x989898
    flash_color: int = 0xffffff
    drop_color: int = 0x0b1b2a
    death_fill: int = 0xff0000
    if PI:
        ghost_color: int = 0x040404
    else:
        ghost_color: int = 0x141414


default_palette = Palette()
beginner_palette = Palette(0x49a4f9,0x193b0a, 0x61ff1c, 0x091622)
moonlight_palette = Palette(0xf2ec3a, 0x2c2c6a, 0xff4e88, 0x1b1a07)
pollution_palette = Palette(0x82a78c, 0x3e3f3e, 0x9affb5, 0x11160f)
ice_palette = Palette(0xcbf9ff, 0x0090d3, 0xffffff, 0x001722)
meadow_palette = Palette(0x5096ff, 0x5da93c)
bubble_palette = Palette(0xfff840, 0xf33087, 0xfffcae)
spring_palette = Palette(0x76d90b, 0xe65987, 0xffdcb2)
autumn_palette = Palette(0x5f991c, 0x883e25)
grey_palette = Palette(0x6d7e74, 0x545e57)
night_palette = Palette(0x0c43e5, 0x092883, 0x056fff)
joker_palette = Palette(0x42ec0e, 0xb500cb, 0xfff955)
lava_palette = Palette(0xc5080c, 0x2a2727, 0xcf4b3d, 0x230202)
organic_palette = Palette(0x37946e, 0x524b24, 0xffd800)
witch_palette = Palette(0x4730f3, 0x5c0d3c, 0xf33087)
america_palette = Palette(0xea1f1f, 0x1f29ea, 0xffffff)
magic_palette = Palette(0xe65987, 0x0b3248, 0x91ea1f)
toy_palette = Palette(0x5cbb92, 0xa22e51, 0xfbea8b, 0x0f1c15)

palettes = [
    toy_palette,
    ice_palette,
    pollution_palette,
    lava_palette,
    beginner_palette,
    moonlight_palette,
    magic_palette,
    witch_palette,
    bubble_palette,
    night_palette,
    joker_palette,
    america_palette
]

# Color Constants
BLACK = (0, 0, 0)
NEOPIXEL_SIMULATOR_COLOR_OFF = (0, 0, 0)
SIMULATOR_BACKGROUND = (15, 15, 15)

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

pause_icon = [0x1f, 0x00, 0x00, 0x1f]

t_letter = [0x01, 0x1f, 0x01]
e_letter = [0x1f, 0x15, 0x11]
r_letter = [0x1f, 0x05, 0x1b]
u_letter = [0x1f, 0x10, 0x1f]
s_letter = [0x16, 0x15, 0x0d]

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


class SceneManager:
    def __init__(self):
        self.current_scene = None

    def change_scene(self, new_scene):
        if self.current_scene is not None:
            self.current_scene.exit()
        self.current_scene = new_scene
        new_scene.enter()

    def update(self):
        self.current_scene.update()


class InputManager:
    def __init__(self):
        self.pressing_left = False
        self.pressing_right = False
        self.pressing_down = False
        self.pressed_debug = False
        self.pressed_simulate_gamepad_connection = False
        self.pressed_simulate_gamepad_deconnection = False
        self.pressed_left = False
        self.pressed_right = False
        self.pressed_down = False
        self.pressed_rotate_left = False
        self.pressed_rotate_right = False
        self.pressed_hard_drop = False
        self.pressed_reset_board = False
        self.pressed_quit = False
        self.pressed_any = False
        self.pressed_pause = False
        self.released_down = False
        self.pressed_palette_left = False
        self.pressed_palette_right = False
        self.connected_joystick = False
        self.disconnected_joystick = False
        self.joystick_is_connected = False
        self.joystick = None
        self.update_controller_status()

    def update_controller_status(self):
        self.connected_joystick = False
        self.disconnected_joystick = False
        if not pygame.joystick.get_init():
            pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            if self.joystick is None:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                self.connected_joystick = True
                self.joystick_is_connected = True
        else:
            if self.joystick is not None:
                self.joystick.quit()
                self.disconnected_joystick = True
                self.joystick_is_connected = False
            self.joystick = None
        if self.pressed_simulate_gamepad_connection:
            self.connected_joystick = True
            self.joystick_is_connected = True
        elif self.pressed_simulate_gamepad_deconnection:
            self.disconnected_joystick = True
            self.joystick_is_connected = False

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
        self.pressed_simulate_gamepad_connection = False
        self.pressed_simulate_gamepad_deconnection = False
        self.pressed_pause = False
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
                elif event.key == K_q:
                    self.pressed_simulate_gamepad_connection = True
                elif event.key == K_w:
                    self.pressed_simulate_gamepad_deconnection = True
                elif event.key == K_c:
                    self.pressed_palette_left = True
                elif event.key == K_v:
                    self.pressed_palette_right = True
                elif event.key == K_p:
                    self.pressed_pause = True
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
                elif event.button == JKEY_START:
                    self.pressed_pause = True
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

    def set_cell(self, x, y, color):
        self.draw_cell(x, y, color)

    def clear_cell(self, x, y):
        self.draw_cell(x, y, BLACK)

    def set_line(self, y, color):
        for x in range(BOARD_WIDTH):
            self.set_cell(x, y, color)

    def fill(self, color):
        pixels.fill(color)
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
        application_surface.fill(SIMULATOR_BACKGROUND)

    def set_cell(self, x, y, color):
        self.draw_cell(x, y, color)

    def clear_cell(self, x, y):
        self.draw_cell(x, y, 0)

    def fill(self, color):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.draw_cell(x, y, color)

    def draw_cell(self, x, y, color):
        pygame.display.get_window_size()
        rect_x = pygame.display.get_window_size()[0] / 2 - NEOPIXEL_WIDTH / 2 + x * (NEOPIXEL_SIZE + NEOPIXEL_SPACING)
        rect_y = pygame.display.get_window_size()[1] / 2 - NEOPIXEL_HEIGHT / 2 + y * (NEOPIXEL_SIZE + NEOPIXEL_SPACING)
        pygame.draw.rect(application_surface, color, (rect_x, rect_y, NEOPIXEL_SIZE, NEOPIXEL_SIZE))
        self.need_refresh = True

    def refresh(self):
        if self.need_refresh:
            pygame.display.update()
            self.need_refresh = False


class LumaScreenPrototype:
    def __init__(self):
        self.child = None
        self.need_redraw = True

    def fill(self, color):
        pass

    def refresh(self):
        pass


class LumaScreen(LumaScreenPrototype):
    @staticmethod
    def draw_point(x, y, surface):
        surface.point((x, y), fill="white")

    def refresh(self):
        if self.need_redraw:
            with canvas(device) as draw_surface:
                self.child.draw(draw_surface)
                device.show()
            self.need_redraw = False


class LumaScreenSimulator(LumaScreenPrototype):
    @staticmethod
    def draw_point(x, y, color, surface):
        pygame.display.get_window_size()
        rect_x = pygame.display.get_window_size()[0] / 2 - LUMA_WIDTH / 2 + x * (LUMA_SIZE + LUMA_SPACING)
        rect_y = pygame.display.get_window_size()[1] / 2 + NEOPIXEL_HEIGHT / 2 + y * (LUMA_SIZE + LUMA_SPACING)
        pygame.draw.rect(surface, color, (rect_x, rect_y, LUMA_SIZE, LUMA_SIZE))

    def fill(self, color):
        for y in range(8):
            for x in range(32):
                self.draw_point(x, y, LUMA_COLOR_OFF, application_surface)

    def refresh(self):
        if self.need_redraw:
            self.fill(0)
            self.child.draw(application_surface)
            self.need_redraw = False


class LumaScreenChild:
    def __init__(self):
        self.parent_device = luma_screen

    def draw(self, surface):
        pass


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
        self.color = game_scene.current_palette.piece_color
        self.ghost_color = game_scene.current_palette.ghost_color
        self.fall_frequency = 0.8
        self.press_down_frequency = 0.035
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
        self.hard_drop_start = 0
        self.hard_drop_height = 0
        self.hard_drop_x = 0

    def reset(self, piece):
        shape_name = piece
        self.x = 3
        self.y = -2
        self.rotation = 0
        self.shape = shapes[shape_name]
        self.color = game_scene.current_palette.piece_color
        self.ghost_color = game_scene.current_palette.ghost_color
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
        self.draw_piece(self.x, self.y + self.get_drop_position(), self.ghost_color)
        self.draw_piece(self.x, self.y, self.color)
        if not self.is_valid_position(add_x=0, add_y=0):
            game_scene.begin_fill_state()
            #self.add_to_board()
            self.visible = True
        input_manager.pressing_down = False
        # input_manager.pressing_left = False
        # input_manager.pressing_right = False

    def update(self):
        if not self.active:
            return
        while self.movable:
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
                break
            # debug, reset the board
            if input_manager.pressed_reset_board:
                stack.reset()
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
            break
        if self.hard_dropped:
            if time.time() > self.last_hard_drop_time + PAUSE_AFTER_HARD_DROP_TIME:
                self.draw_hard_drop(0)
                self.add_to_board()

    def rotate(self, direction):
        self.clear_piece()
        self.clear_piece(add_y=self.get_drop_position())
        self.rotation = (self.rotation + direction) % len(self.shape)
        if not self.is_valid_position():
            self.rotation = (self.rotation - direction) % len(self.shape)
            self.draw_piece(self.x, self.y, self.color)
        self.draw_piece(self.x, self.y + self.get_drop_position(), self.ghost_color)
        self.draw_piece(self.x, self.y, self.color)

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
            self.draw_piece(self.x, self.y, self.color)

    def move_horizontal(self, x):
        if self.is_valid_position(add_x=x):
            self.clear_piece(add_y=self.get_drop_position())
            self.clear_piece()
            self.x += x
            self.last_run_time = time.time()
            self.draw_piece(self.x, self.y + self.get_drop_position(), self.ghost_color)
            self.draw_piece(self.x, self.y, self.color)
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

    def draw_piece(self, piece_x, piece_y, color):
        for x in range(self.template_width):
            for y in range(self.template_height):
                if self.shape[self.rotation][y][x] == blank:
                    continue
                if y + piece_y < 0:
                    continue
                neopixel_screen.set_cell(x + piece_x, y + piece_y, color)

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
        self.hard_drop_start = self.y
        self.hard_drop_height = self.get_drop_position()
        self.hard_drop_x = self.x
        self.draw_hard_drop(game_scene.current_palette.drop_color)
        self.y += self.hard_drop_height
        self.drop_row_count = self.hard_drop_height << 1
        self.movable = False
        self.hard_dropped = True
        self.last_hard_drop_time = time.time()
        self.draw_piece(self.x, self.y, self.color)

    def draw_hard_drop(self, color):
        for y in range(self.hard_drop_height):
            self.draw_piece(self.hard_drop_x, self.hard_drop_start + y, color)

    def clear_hard_drop(self):
        pass

    def get_drop_position(self):
        for i in range(1, stack.height - self.y):
            if not self.is_valid_position(add_y=i):
                break
        return i - 1

    def add_to_board(self):
        for x in range(self.template_width):
            for y in range(self.template_height):
                if self.shape[self.rotation][y][x] != blank:
                    stack.set_cell(x + self.x, y + self.y, stack.color)
                    neopixel_screen.set_cell(x + self.x, y + self.y, stack.color)
        self.visible = False
        self.active = False
        luma_screen.show_lines = False
        game_scene.score += self.drop_row_count
        luma_screen.need_redraw = True
        if game_scene.state == state_fall:
            game_scene.check_for_complete_line()

    def is_valid_position(self, add_x=0, add_y=0):
        for x in range(self.template_width):
            for y in range(self.template_height):
                if self.shape[self.rotation][y][x] == blank:
                    continue
                if not is_on_board(x + self.x + add_x, y + self.y + add_y):
                    return False
                if stack.get_cell(x + self.x + add_x, y + self.y + add_y) != blank:
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
        self.color = game_scene.current_palette.death_fill

    def reset(self):
        self.last_fill_time = time.time()
        self.line_to_fill = 20

    def update(self):
        if self.line_to_fill == 0 and time.time() - self.end_fill_time > self.pause_before_reset_duration:
            scene_manager.change_scene(menu_scene)
        elif self.line_to_fill > 0 and time.time() - self.last_fill_time > self.fill_frequency:
            self.line_to_fill -= 1
            neopixel_screen.set_line(self.line_to_fill, self.color)
            self.end_fill_time = time.time()
            self.last_fill_time = time.time()


class LineFlasher:
    def __init__(self):
        self.target_list = None
        self.progress = 0
        self.num_step = 4
        self.last_step_time = 0
        self.clean_frequency = 0.05
        self.flash_color = game_scene.current_palette.flash_color

    def enter(self, target_list):
        self.target_list = target_list
        self.progress = 0
        self.last_step_time = 0

    def update(self):
        if time.time() - self.last_step_time > self.clean_frequency:
            if self.progress == self.num_step:
                game_scene.begin_clear_state()
                game_scene.line_cleaner.enter(self.target_list)
            else:
                if self.progress % 2 == 0:
                    for y in self.target_list:
                        neopixel_screen.set_line(y, self.flash_color)
                else:
                    for y in self.target_list:
                        neopixel_screen.set_line(y, stack.color)
                self.last_step_time = time.time()
            self.progress += 1

    def change_color(self):
        self.flash_color = game_scene.current_palette.flash_color


class LineCleaner:
    def __init__(self):
        self.target_list = None
        self.progress = 0
        self.last_clean_time = 0
        self.clean_frequency = PAUSE_BETWEEN_LINE_CLEAR_STEPS
        self.points_to_give = 0
        self.burn_color = game_scene.current_palette.flash_color

    def enter(self, target_list):
        self.target_list = target_list
        self.progress = 0
        self.last_clean_time = 0
        self.points_to_give = 0
        if len(self.target_list) == 1:
            self.points_to_give = 40 * (game_scene.level + 1) // 5
        elif len(self.target_list) == 2:
            self.points_to_give = 100 * (game_scene.level + 1) // 5
        elif len(self.target_list) == 3:
            self.points_to_give = 300 * (game_scene.level + 1) // 5
        else:
            self.points_to_give = 1200 * (game_scene.level + 1) // 5

    def update(self):
        if time.time() - self.last_clean_time > self.clean_frequency:
            if self.progress == 7:
                self.collapse_gaps()
                if game_scene.total_line_cleared // 10 > game_scene.level:
                    game_scene.level += 1
                    game_scene.change_palette()
                    stack.change_color()
                    stack.draw_stack()
                    falling_piece.speed_up()
                game_scene.begin_fall_state()
            else:
                for y in self.target_list:
                    blank_pos = self.progress - 1
                    if 0 < self.progress < 6:
                        stack.set_cell(4 - blank_pos, y, blank)
                        stack.set_cell(5 + blank_pos, y, blank)
                        neopixel_screen.set_cell(4 - blank_pos, y, 0)
                        neopixel_screen.set_cell(5 + blank_pos, y, 0)
                    if self.progress < 5:
                        stack.set_cell(4 - self.progress, y, self.burn_color)
                        stack.set_cell(5 + self.progress, y, self.burn_color)
                        neopixel_screen.set_cell(4 - self.progress, y, self.burn_color)
                        neopixel_screen.set_cell(5 + self.progress, y, self.burn_color)
                self.last_clean_time = time.time()
                if self.progress < len(self.target_list):
                    game_scene.total_line_cleared += 1
                    luma_screen.need_redraw = True
                if self.progress < 5:
                    game_scene.score += self.points_to_give
                    luma_screen.need_redraw = True
            self.progress += 1

    def collapse_gaps(self):
        y = stack.height - 1  # start y at the bottom of the board
        for y in self.target_list:
            for shift_line in range(y, 0, -1):
                for x in range(stack.width):
                    top_color_index = stack.content[x][shift_line - 1]
                    stack.content[x][shift_line] = top_color_index
                    if top_color_index == blank:
                        neopixel_screen.set_cell(x, shift_line, 0)
                    else:
                        neopixel_screen.set_cell(x, shift_line, stack.color)
            for x in range(stack.width):
                stack.content[x][0] = blank
                neopixel_screen.set_cell(x, 0, 0x000000)

    def change_color(self):
        self.burn_color = game_scene.current_palette.flash_color


class Stack(GameObject):
    def __init__(self):
        super().__init__()
        self.width = 10
        self.height = 20
        self.color = game_scene.current_palette.stack_color
        self.content = []
        for i in range(self.width):
            self.content.append([blank] * self.height)

    def reset(self):
        for x in range(self.width):
            for y in range(self.height):
                self.set_cell(x, y, blank)

    def set_cell(self, x, y, value):
        self.content[x][y] = value

    def set_line(self, y, value):
        for x in range(stack.width):
            self.set_cell(x, y, value)

    def get_cell(self, x, y):
        if y < 0:
            return blank
        return self.content[x][y]

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

    def draw_stack(self):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                if self.content[x][y] == blank:
                    continue
                neopixel_screen.set_cell(x, y, self.color)

    def change_color(self):
        self.color = game_scene.current_palette.stack_color


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
        random.shuffle(self.bag)

    def deal_piece(self):
        dealt_piece = self.bag.pop()
        self.piece_history[dealt_piece] = self.piece_history[dealt_piece] + 1
        if len(self.bag) == 0:
            self.fill_bag()
        return dealt_piece

    def get_rare_piece(self):
        rare_piece_quantity = min(self.piece_history.values())
        rare_piece_candidates = []
        for i in self.piece_history:
            if self.piece_history.get(i) == rare_piece_quantity:
                rare_piece_candidates.append(i)
        choice = random.choice(rare_piece_candidates)
        return random.choice(rare_piece_candidates)


class Hud(LumaScreenChild):
    def draw_piece(self, piece, offset_x, offset_y, surface):
        for x in range(0, 8):
            for y in range(0, 4):
                index = x // 2 + y // 2 * 4
                if shape_previews[piece][index] == 1:
                    self.parent_device.draw_point(offset_x + x, offset_y + y, LUMA_COLOR_ON, surface)

    def draw_score(self, number, offset_x, offset_y, surface):
        for x in range(0, 3):
            for y in range(0, 5):
                if number_font[3 * number + x] & mask[y]:
                    self.parent_device.draw_point(offset_x + x, offset_y + y, LUMA_COLOR_ON, surface)

    def draw_lines(self, number, offset_x, offset_y, surface):
        for i in range(0, number % 10):
            self.parent_device.draw_point(31 - i, 6, LUMA_COLOR_ON, surface)

    def draw(self, surface):
        _score = game_scene.score
        _num_line = game_scene.total_line_cleared
        # draw score
        for i in range(0, 6):
            self.draw_score(_score % 10, 29 - i * 4, 0, surface)
            _score //= 10

        # draw next piece
        if game_scene.next_piece is not None:
            self.draw_piece(game_scene.next_piece, 0, 0, surface)

        self.draw_lines(game_scene.total_line_cleared, 0, 0, surface)


class MenuInfoPanel(LumaScreenChild):
    def draw_score(self, number, offset_x, offset_y, surface):
        for x in range(0, 3):
            for y in range(0, 5):
                if number_font[3 * number + x] & mask[y]:
                    self.parent_device.draw_point(offset_x + x, offset_y + y, LUMA_COLOR_ON, surface)

    def draw(self, surface):
        _score = menu_scene.last_score

        if _score == 0:
            return

        # draw score
        for i in range(0, 6):
            self.draw_score(_score % 10, 29 - i * 4, 0, surface)
            _score //= 10


class Scene:
    def __init__(self):
        self.active = True

    def enter(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass


class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.last_score = 0
        luma_screen.child = menu_info_panel
        luma_screen.need_redraw = True

    def enter(self):
        luma_screen.child = menu_info_panel
        luma_screen.need_redraw = True
        if input_manager.joystick_is_connected:
            self.draw_title(default_palette.piece_color)
        else:
            self.draw_title(default_palette.ghost_color)

    def update(self):
        if input_manager.connected_joystick:
            self.draw_title(default_palette.piece_color)
        elif input_manager.disconnected_joystick:
            self.draw_title(default_palette.ghost_color)
        if input_manager.pressed_pause:
            scene_manager.change_scene(game_scene)
        if input_manager.pressed_quit:
            terminate()

    @staticmethod
    def draw_title(color):
        draw_letter(1, 2, t_letter, color)
        draw_letter(6, 2, e_letter, color)
        draw_letter(1, 8, t_letter, color)
        draw_letter(6, 8, r_letter, color)
        draw_letter(1, 14, u_letter, color)
        draw_letter(6, 14, s_letter, color)


class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.current_palette = palettes[0]
        self.falling_piece = falling_piece
        self.line_cleaner = line_cleaner
        self.line_flasher: LineFlasher = None
        self.board_filler = board_filler
        self.next_piece = None
        self.state = state_wait
        self.score = 0
        self.total_line_cleared = 0
        self.level = 0
        self.hud_show_lines = False

    def enter(self):
        luma_screen.child = hud
        neopixel_screen.fill(0)
        falling_piece.__init__()
        falling_piece.active = True
        luma_screen.active = True
        luma_screen.visible = True
        self.score = 0
        self.total_line_cleared = 0
        self.level = 0
        self.change_palette()
        stack.change_color()
        self.next_piece = None
        self.pick_next_piece()
        self.begin_fall_state()

    def update(self):
        if self.active:
            if self.state == state_fall:
                if input_manager.pressed_pause or not input_manager.joystick_is_connected:
                    self.active = False
                    neopixel_screen.fill(0)
                    draw_pause_icon(3, 7)
                    return
                falling_piece.update()
            elif self.state == state_preclear:
                self.line_flasher.update()
            elif self.state == state_clear:
                self.line_cleaner.update()
            elif self.state == state_fill:
                self.board_filler.update()
        else:
            if input_manager.pressed_pause:
                self.active = True
                neopixel_screen.fill(0)
                stack.draw_stack()
                falling_piece.draw_piece(falling_piece.x, falling_piece.y + falling_piece.get_drop_position(), falling_piece.ghost_color)
        if input_manager.pressed_quit:
            terminate()

    def exit(self):
        stack.reset()
        neopixel_screen.fill(0)
        neopixel_screen.current_palette = 0

    def change_palette(self):
        self.current_palette = palettes[self.level % len(palettes)]
        self.line_flasher.change_color()
        self.line_cleaner.change_color()

    def pick_next_piece(self):
        self.next_piece = piece_dealer.deal_piece()
        luma_screen.need_redraw = True

    def begin_fall_state(self):
        self.state = state_fall
        falling_piece.reset(self.next_piece)
        self.pick_next_piece()

    def begin_wait_state(self):
        self.state = state_wait
        falling_piece.visible = False
        luma_screen.visible = False

    def begin_death_state(self):
        pass

    def begin_fill_state(self):
        self.board_filler.reset()
        self.state = state_fill
        menu_scene.last_score = self.score

    def begin_clear_state(self):
        self.state = state_clear

    def begin_preclear_state(self):
        self.state = state_preclear

    def check_for_complete_line(self):
        complete_lines = []
        for y in range(stack.height):
            if stack.is_line_complete(y):
                complete_lines.append(y)
        if len(complete_lines) > 0:
            self.begin_preclear_state()
            self.line_flasher.enter(complete_lines)
        else:
            falling_piece.reset(self.next_piece)
            self.pick_next_piece()


def is_on_board(x, y):
    return 0 <= x < stack.width and y < stack.height


def draw_pause_icon(offset_x, offset_y):
    for x in range(0, 4):
        for y in range(0, 5):
            if pause_icon[x] & mask[y]:
                neopixel_screen.set_cell(offset_x + x, offset_y + y, game_scene.current_palette.piece_color)


def draw_letter(offset_x, offset_y, letter, color):
    for x in range(0, 3):
        for y in range(0, 5):
            if letter[x] & mask[y]:
                neopixel_screen.set_cell(offset_x + x, offset_y + y, color)


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
state_preclear = 5

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

piece_dealer = PieceDealerBagAlex()
stack = None
falling_piece = None
board_filler = None
line_cleaner = None
line_flasher = None

scene_manager = SceneManager()
input_manager = InputManager()

clock = pygame.time.Clock()

if PI:
    neopixel_screen = NeoPixelScreen()
    luma_screen = LumaScreen()
else:
    neopixel_screen = NeoPixelScreenSimulator()
    luma_screen = LumaScreenSimulator()

menu_info_panel = MenuInfoPanel()
hud = Hud()

neopixel_screen.fill(0)
luma_screen.fill(0)

menu_scene = MenuScene()
game_scene = GameScene()
scene_manager.change_scene(menu_scene)

stack = Stack()
falling_piece = Piece()

game_scene.board_filler = BoardFiller()
game_scene.line_cleaner = LineCleaner()
game_scene.line_flasher = LineFlasher()

while True:
    # update
    input_manager.update()
    scene_manager.update()

    # draw
    luma_screen.refresh()
    neopixel_screen.refresh()

    clock.tick(30)
