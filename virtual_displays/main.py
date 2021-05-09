PI = False

import random, time, sys, os, pickle
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

# Constants
JKEY_X = 3
JKEY_Y = 4
JKEY_A = 0
JKEY_B = 1
JKEY_R = 7
JKEY_L = 6
JKEY_SEL = 10
JKEY_START = 11


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


def fill_screen(color):
    if PI:
        pixels.fill(color)
    else:
        application_surface.fill(color)


def update_screen():
    if PI:
        pixels.show()
    else:
        pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()


# Init

if PI:
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, blocks_arranged_in_reverse_order=True, block_orientation=90)
    pixel_pin = board.D21
    num_pixels = 10 * 20
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.30, auto_write=False, pixel_order=neopixel.GRB)
else:
    pygame.display.set_caption("Tetrus Desktop")
    application_surface = pygame.display.set_mode((480,640))

joystick_detected = False
pygame.init()
pygame.joystick.init()

input_manager = InputManager()

fill_screen((0, 0, 32))

while True:
    # Pre-update
    input_manager.update()

    # Update
    if input_manager.joystick is not None:
        fill_screen((0,0,128))
    else:
        fill_screen((0,0,32))
    if input_manager.pressing_left:
        fill_screen((128,0,0))
    if input_manager.pressing_right:
        fill_screen((0,128,0))

    # Post-draw
    update_screen()

    time.sleep(0.03)

# show_message(device, "Ca marche la non ?", fill="white", font=proportional(LCD_FONT))
