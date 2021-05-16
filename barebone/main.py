import random, time, sys, os, pickle

import pygame
from pygame.locals import *

import board
import neopixel
import subprocess
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

JKEY_X = 3
JKEY_Y = 4
JKEY_A = 0
JKEY_B = 1
JKEY_R = 7
JKEY_L = 6
JKEY_SEL = 10
JKEY_START = 11

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, blocks_arranged_in_reverse_order=True, block_orientation=90)
pixel_pin = board.D21
num_pixels = 10 * 20

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.30, auto_write=False, pixel_order=neopixel.GRB)

joystick_detected = False
pygame.init()
pygame.joystick.init()

pixels.fill((32, 0, 0))

while True:
    pixels[0] = (0, 0, 0)

    if not joystick_detected:
        pygame.joystick.quit()
        pygame.joystick.init()
        try:
            joystick = pygame.joystick.Joystick(0)  # create a joystick instance
            joystick.init()  # init instance
            # print("Initialized joystick: {}".format(joystick.get_name()))
            joystick_detected = True
            pixels.fill((0, 0, 128))
        except pygame.error:
            print("no joystick found.")
            joystick_detected = False

    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            myevent = event.button
            if myevent == JKEY_A:
                pixels.fill((128, 0, 0))
            elif myevent == JKEY_B:
                pixels.fill((0, 128, 0))
            elif myevent == JKEY_X:
                pixels[0] = (255, 255, 0)

    pixels.show()
    time.sleep(0.03)

# show_message(device, "Ca marche la non ?", fill="white", font=proportional(LCD_FONT))
