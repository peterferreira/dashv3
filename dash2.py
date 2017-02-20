#!/usr/bin/env python
# --------------------------------
# Codemasters F1 Dash v2
# Author : Mark Rodman
# -------------------------------
import os, sys, pygame, time, datetime
from pygame.locals import *
from dash_support import *

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

    right_lights.append(rpm_light(light1[0], light1[1], 0, 0, r_xf, y, trig_val1))
    right_lights.append(rpm_light(light2[0], light2[1], r_x, 0, r_xf, y, trig_val2))
    right_lights.append(rpm_light(light3[0], light3[1], (2 * r_x), 0, r_xf, y, trig_val3))
    right_lights.append(rpm_light(light4[0], light4[1], (3 * r_x), 0, r_xf, y, trig_val4))
    right_lights.append(rpm_light(light5[0], light5[1], (4 * r_x), 0, r_xf, y, trig_val5))
    right_lights.append(rpm_light(light6[0], light6[1], (5 * r_x), 0, r_xf, y, trig_val6))
    right_lights.append(rpm_light(light7[0], light7[1], (6 * r_x), 0, r_xf, y, trig_val7))
    right_lights.append(rpm_light(light8[0], light8[1], (7 * r_x), 0, r_xf, y, trig_val8))
    right_lights.append(rpm_light(light9[0], light9[1], (8 * r_x), 0, r_xf, y, trig_val9))
    right_lights.append(rpm_light(light10[0], light10[1], (9 * r_x), 0, r_xf, y, trig_val10))
    right_lights.append(rpm_light(light11[0], light11[1], (10 * r_x), 0, r_xf, y, trig_val11))
    right_lights.append(rpm_light(light12[0], light12[1], (11 * r_x), 0, r_xf, y, trig_val12))
    right_lights.append(rpm_light(light13[0], light13[1], (12 * r_x), 0, r_xf, y, trig_val13))
    right_lights.append(rpm_light(light14[0], light14[1], (13 * r_x), 0, r_xf, y, trig_val14))
    right_lights.append(rpm_light(light15[0], light15[1], (14 * r_x), 0, r_xf, y, trig_val15))
    right_lights.append(rpm_light(light16[0], light16[1], (15 * r_x), 0, r_xf, y, trig_val16))
    right_lights.append(rpm_light(light17[0], light17[1], (16 * r_x), 0, r_xf, y, trig_val17))
    right_lights.append(rpm_light(light18[0], light18[1], (17 * r_x), 0, r_xf, y, trig_val18))
    right_lights.append(rpm_light(light19[0], light19[1], (18 * r_x), 0, r_xf, y, trig_val19))
    right_lights.append(rpm_light(light20[0], light20[1], (19 * r_x), 0, r_xf, y, trig_val20))
    right_lights.append(rpm_light(light21[0], light21[1], (20 * r_x), 0, r_xf, y, trig_val21))

    left_lights.append(rpm_light(light1[0], light1[1], rev_startx, l_y, -l_xf, -y, trig_val1))
    left_lights.append(rpm_light(light2[0], light2[1], (rev_startx - l_x), l_y, -l_xf, -y, trig_val2))
    left_lights.append(rpm_light(light3[0], light3[1], (rev_startx - (2 * l_x)), l_y, -l_xf, -y, trig_val3))
    left_lights.append(rpm_light(light4[0], light4[1], (rev_startx - (3 * l_x)), l_y, -l_xf, -y, trig_val4))
    left_lights.append(rpm_light(light5[0], light5[1], (rev_startx - (4 * l_x)), l_y, -l_xf, -y, trig_val5))
    left_lights.append(rpm_light(light6[0], light6[1], (rev_startx - (5 * l_x)), l_y, -l_xf, -y, trig_val6))
    left_lights.append(rpm_light(light7[0], light7[1], (rev_startx - (6 * l_x)), l_y, -l_xf, -y, trig_val7))
    left_lights.append(rpm_light(light8[0], light8[1], (rev_startx - (7 * l_x)), l_y, -l_xf, -y, trig_val8))
    left_lights.append(rpm_light(light9[0], light9[1], (rev_startx - (8 * l_x)), l_y, -l_xf, -y, trig_val9))
    left_lights.append(rpm_light(light10[0], light10[1], (rev_startx - (9 * l_x)), l_y, -l_xf, -y, trig_val10))
    left_lights.append(rpm_light(light11[0], light11[1], (rev_startx - (10 * l_x)), l_y, -l_xf, -y, trig_val11))
    left_lights.append(rpm_light(light12[0], light12[1], (rev_startx - (11 * l_x)), l_y, -l_xf, -y, trig_val12))
    left_lights.append(rpm_light(light13[0], light13[1], (rev_startx - (12 * l_x)), l_y, -l_xf, -y, trig_val13))
    left_lights.append(rpm_light(light14[0], light14[1], (rev_startx - (13 * l_x)), l_y, -l_xf, -y, trig_val14))
    left_lights.append(rpm_light(light15[0], light15[1], (rev_startx - (14 * l_x)), l_y, -l_xf, -y, trig_val15))
    left_lights.append(rpm_light(light16[0], light16[1], (rev_startx - (15 * l_x)), l_y, -l_xf, -y, trig_val16))
    left_lights.append(rpm_light(light17[0], light17[1], (rev_startx - (16 * l_x)), l_y, -l_xf, -y, trig_val17))
    left_lights.append(rpm_light(light18[0], light18[1], (rev_startx - (17 * l_x)), l_y, -l_xf, -y, trig_val18))
    left_lights.append(rpm_light(light19[0], light19[1], (rev_startx - (18 * l_x)), l_y, -l_xf, -y, trig_val19))
    left_lights.append(rpm_light(light20[0], light20[1], (rev_startx - (19 * l_x)), l_y, -l_xf, -y, trig_val20))
    left_lights.append(rpm_light(light21[0], light21[1], (rev_startx - (20 * l_x)), l_y, -l_xf, -y, trig_val21))

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
                    rpm += 750
                    update_rpm(rpm)
                if event.key == K_DOWN:
                    print "Down"
                    rpm -= 750
                    update_rpm(rpm)

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
