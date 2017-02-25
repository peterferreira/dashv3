#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------
# Codemasters F1 Dash v2
# Author : Mark Rodman
# -------------------------------
import os, sys, pygame, random, time, datetime
from pygame.locals import *
from dash_support import *
from collections import deque


class DisplayText(object):
    def __init__(self, name, textval, forecolour, backcolour, loc_x, loc_y):
        self.name = name
        self.forecolour = forecolour
        self.backcolour = backcolour
        self.textval = textval
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.old_loc_x = loc_x
        self.old_loc_y = loc_y
        self.old_textval = textval

    def draw_text(self, textval, loc_x, loc_y):
        self.textval = textval
        self.loc_x = loc_x
        self.loc_y = loc_y

        oldtext = basicFont.render(self.old_textval, True, BLACK)
        oldtext_rect = oldtext.get_rect()
        windowSurface.blit(oldtext, (self.old_loc_x, self.old_loc_y))
        oldrect = (loc_x, loc_y, oldtext_rect[2], oldtext_rect[3])
        pygame.draw.rect(windowSurface, BLACK, oldrect, 0)
        pygame.display.update()

        text = basicFont.render(self.textval, True, self.forecolour)
        windowSurface.blit(text, (self.loc_x, self.loc_y))
        pygame.display.update()

        self.old_loc_x = self.loc_x
        self.old_loc_y = self.loc_y
        self.old_textval = self.textval

    def change_text(self, textval):
        self.textval = textval
        oldtext = basicFont.render(self.old_textval, True, BLACK)
        oldtext_rect = oldtext.get_rect()
        windowSurface.blit(oldtext, (self.old_loc_x, self.old_loc_y))
        oldrect = (self.loc_x, self.loc_y, oldtext_rect[2], oldtext_rect[3])
        pygame.draw.rect(windowSurface, BLACK, oldrect, 0)
        pygame.display.update()

        text = basicFont.render(self.textval, True, self.forecolour)
        windowSurface.blit(text, (self.loc_x, self.loc_y))
        pygame.display.update()

        self.old_loc_x = self.loc_x
        self.old_loc_y = self.loc_y
        self.old_textval = self.textval


class RpmLight(object):
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
            #print self.name + str(" : On :") + str(self.new_rpmValue)
            self.draw_update(0, 1)
        else:
            #print self.name + str(" : Off :") + str(self.new_rpmValue)
            self.draw_update(0, 0)


class DataSet(object):
    """ A data class used to hold incrementing race values.  Length of zero used to not set a fixed length array
        if length is greater than zero then fix length used.
        Data is reversed, so most recent value is first element with in the array.
        eg , deque([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
        """

    count = 0
    values = deque([])

    def __init__(self, name, length):
        DataSet.count += 1
        self.name = name
        self.length = length
        self.data_value = ''
        if self.length != 0:
            for x in range(self.length):
                self.values.append(0)
                self.values.rotate(1)
        else:
            self.values.append(0)

    def add_value(self, data_value):
        self.data_value = data_value
        self.values.append(self.data_value)
        self.values.rotate(1)
        if self.length > 0:
            if len(self.values) > self.length:
                self.values.pop()


def setup_rpm_markers(info):
    r_x = int(info.current_w) * 0.0225
    l_x = int(info.current_w) * 0.0227
    r_xf = r_x * 0.89
    l_xf = l_x * 0.85
    y = int(info.current_h) * bar_as_percentage_of_total_height
    l_y = y + 1
    rev_startx = int(info.current_w) - 1
    global right_lights
    global left_lights
    right_lights = []
    left_lights = []

    for i in range(len(light_trigger_val)):
        right_lights.append(RpmLight(light_name[i], light_colour[i], (i * r_x), 0, r_xf, y, light_trigger_val[i]))
        left_lights.append(RpmLight(light_name[i], light_colour[i], (rev_startx - (i * l_x)), l_y, -l_xf, -y,
                                     light_trigger_val[i]))

    for light in range(len(right_lights)):
        RpmLight.initialize(right_lights[light])
        RpmLight.initialize(left_lights[light])
    return


def setup_data_arrays():
    global sector1
    global sector2
    global sector3
    global lap_times
    sector1 = DataSet("S1", 0)
    sector2 = DataSet("S2", 0)
    sector3 = DataSet("S3", 0)
    lap_times = DataSet("Lap Times", 0)
    return


def setup_screen_text(info):
    global gear_indicator
    gear_indicator = DisplayText("gear", "-", GREEN, BLACK, (info.current_w*gear_text_width_multiplier),
                                 info.current_h*gear_text_height_multiplier)
    gear_indicator.draw_text("1", (info.current_w*gear_text_width_multiplier),
                             info.current_h*gear_text_height_multiplier)
    return

def initial_setup():
    info = pygame.display.Info()
    print type(info)
    setup_rpm_markers(info)
    setup_screen_text(info)
    setup_data_arrays()
    pygame.display.update()
    return


def update_rpm(rpm):
    for light in range(len(right_lights)):
        RpmLight.update(right_lights[light], rpm)
        RpmLight.update(left_lights[light], rpm)
    return


def update_gear(gear):
    gear_indicator.change_text(gear)
    return


def randomizer():
    x = 0
    while x < 100:
        random_val = random.randint(1000, 14000)
        update_rpm(random_val)
        x += 1
        pygame.display.update()
        time.sleep(0.08)
    return


def test_text():
    x = 0
    y = 300
    test1 = DisplayText("test", ".", GREEN, BLACK, 500, 300)

    while x < 500:
        test1.draw_text(str(x), 500, y)
        print x
        x += 1
        y += 1
    return


def test_data():
    points1 = DataSet("points1", 0)
    x = 0
    while x < 20:
        points1.add_value(x)
        x += 1


def game_loop():
    rpm = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                print sector1
                print sector2
                print sector3
                print lap_times
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    rpm += 500
                    update_rpm(rpm)
                if event.key == K_DOWN:
                    rpm -= 500
                    update_rpm(rpm)
                if event.key == K_r:
                    randomizer()
                if event.key == K_t:
                    test_text()
                if event.key == K_m:
                    test_data()
                if event.key == K_1:
                    update_gear("1")
                if event.key == K_2:
                    update_gear("2")
                if event.key == K_3:
                    update_gear("3")
                if event.key == K_4:
                    update_gear("4")
                if event.key == K_5:
                    update_gear("5")
                if event.key == K_6:
                    update_gear("6")
                if event.key == K_7:
                    update_gear("7")
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    return


def pix_array():
    # get a pixel array of the surface
    global pixArray
    pixArray = pygame.PixelArray(windowSurface)
    pixArray[480][800] = BLACK
    del pixArray
    return


def main():
    initial_setup()
    pix_array()
    game_loop()

    return

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    # find fonts  ----
    available_fonts = pygame.font.get_fonts()
    for font in range(len(available_fonts)):
        if available_fonts[font] == LCD_font:
            fontpath = pygame.font.match_font(available_fonts[font])
            # set up fonts
    basicFont = pygame.font.Font(fontpath, gear_fontsize)
    basicFont2 = pygame.font.Font(fontpath, 340)
    instruFont = pygame.font.SysFont(None, instru_fontsize)
    logoFont = pygame.font.SysFont(None, logo_fontsize)
    # rpmFont = pygame.font.SysFont(None, rpm_fontsize)
    bigFont = pygame.font.Font(fontpath, big_fontsize)
    midFont = pygame.font.Font(fontpath, mid_fontsize)
    mphFont = pygame.font.SysFont(None, rpm_fontsize)
    brakeFont = pygame.font.SysFont(None, rpm_fontsize)

    windowSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)  # Now automatically uses full screen
    pygame.display.set_caption(display_title)
    windowSurface.fill(BLACK)
    main()
