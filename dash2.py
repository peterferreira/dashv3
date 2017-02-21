#!/usr/bin/env python
# --------------------------------
# Codemasters F1 Dash v2
# Author : Mark Rodman
# -------------------------------
import os, sys, pygame, random, time, datetime
from pygame.locals import *
from dash_support import *


class display_text(object):
    def __init__(self, name, forecolour, backcolour):
        self.name = name
        self.forecolour = forecolour
        self.backcolour = backcolour


class rpm_light(object):
    def __init__(self, name, colour, startx, starty, width, height, trigger_val):
        self.name = name
        self.colour = colour
        self.startx = startx
        self.starty = starty
        self.width = width
        self.height = height
        self.trigger_val = trigger_val
        self.new_rpmValue = 0
        self.current_rpmValue = 0
        self.draw_mode = 0
        self.status = 0

    def draw_on(self):
        rect_par = (self.startx, self.starty, self.width, self.height)
        pygame.draw.rect(windowSurface, self.colour, rect_par, 0)

    def draw_update(self, draw_mode, status):
        self.draw_mode = draw_mode
        self.status = status
        rect_par = (self.startx, self.starty, self.width, self.height)
        if self.status == 1:
            pygame.draw.rect(windowSurface, self.colour, rect_par, self.draw_mode)
        elif self.status == 0:
            pygame.draw.rect(windowSurface, BLACK, rect_par, 0)
            pygame.draw.rect(windowSurface, self.colour, rect_par, 1)

    def initialize(self):
        rect_par = (self.startx, self.starty, self.width, self.height)
        pygame.draw.rect(windowSurface, self.colour, rect_par, 1)

    def update(self, new_rpmValue):
        self.new_rpmValue = new_rpmValue
        if self.new_rpmValue > self.trigger_val:
            print self.name + str(" : On :") + str(self.new_rpmValue)
            self.draw_update(0, 1)
        else:
            print self.name + str(" : Off :") + str(self.new_rpmValue)
            self.draw_update(0, 0)


def setup_rpm_markers(info):
    #Instantiate RPM ball objects
    # Parameters used to incrementally layout rpm rectangles from left to right
    r_x = int(info.current_w) * 0.0225
    l_x = int(info.current_w) * 0.0227
    r_xf = r_x * 0.89
    l_xf = l_x * 0.85
    y = int(info.current_h) * bar_as_percentage_of_total_height
    l_y = y + 1
    # Parameters used to incrementally layout rpm rectangles from right to left.
    # These are draw backwards.
    rev_startx = int(info.current_w) - 1
    global right_lights
    right_lights = []
    global left_lights
    left_lights = []

    for i in range(len(light_trigger_val)):
        print str(i) + "   "
        right_lights.append(rpm_light(light_name[i], light_colour[i], (i * r_x), 0, r_xf, y, light_trigger_val[i]))
        left_lights.append(rpm_light(light_name[i], light_colour[i], (rev_startx - (i * l_x)), l_y, -l_xf, -y, light_trigger_val[i]))

    for light in range(len(right_lights)):
        rpm_light.initialize(right_lights[light])
        rpm_light.initialize(left_lights[light])
    return


def initial_setup():
    info = pygame.display.Info()
    print type(info)
    setup_rpm_markers(info)
    pygame.display.update()
    return


def update_rpm(rpm):
    for light in range(len(right_lights)):
        rpm_light.update(right_lights[light], rpm)
        rpm_light.update(left_lights[light], rpm)
    return


def randomizer():
    x = 0
    while x < 100:
        random_val = random.randint(1000, 14000)
        update_rpm(random_val)
        x += 1
        pygame.display.update()
        time.sleep(0.07)
    return




def game_loop():
    print "game loop"
    rpm = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    print "UP"
                    rpm += 500
                    update_rpm(rpm)
                if event.key == K_DOWN:
                    print "Down"
                    rpm -= 500
                    update_rpm(rpm)
                if event.key == K_r:
                    randomizer()
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    return


def pix_Array():
    # get a pixel array of the surface
    global pixArray
    pixArray = pygame.PixelArray(windowSurface)
    pixArray[480][800] = BLACK
    del pixArray
    return


def main():
    initial_setup()
    pix_Array()
    game_loop()

    return

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    windowSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)  # Now automatically uses full screen
    pygame.display.set_caption(display_title)
    windowSurface.fill(BLACK)
    main()
