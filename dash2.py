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
from dash_network import receiver


class IncomingData(object):
    def __init__(self, name):
        self.name = name
        self.data_gear = "1"
        self.data_rpm = 0
        self.data_mph_fix = 0
        self.data_brake = 0
        self.data_psi = 0
        self.data_sector = 0
        self.data_sector1 = 0
        self.data_sector2 = 0
        self.data_lastlap = 0
        self.data_fuel_in_tank = 0
        self.data_fuel_capacity = 0
        self.data_team_id = 0
        self.data_laptime = 0
        self.data_throttle_ped = 0
        self.data_brake_ped = 0
        self.data_drs = 0
        self.data_lap = 0
        self.data_position = 0
        self.new_data_gear = "1"
        self.new_data_rpm = 0
        self.new_data_mph_fix = 0
        self.new_data_brake = 0
        self.new_data_psi = 0
        self.new_data_sector = 0
        self.new_data_sector1 = 0
        self.new_data_sector2 = 0
        self.new_data_lastlap = 0
        self.new_data_fuel_in_tank = 0
        self.new_data_fuel_capacity = 0
        self.new_data_team_id = 0
        self.new_data_laptime = 0
        self.new_data_throttle_ped = 0
        self.new_data_brake_ped = 0
        self.new_data_drs = 0
        self.new_data_lap = 0
        self.new_data_position = 0

    def update_all(self, data_gear, data_mph_fix, data_brake, data_rpm, data_psi, data_sector, data_sector1,
                   data_sector2, data_lastlap, data_fuel_in_tank, data_fuel_capacity, data_team_id, data_laptime,
                   data_throttle_ped, data_brake_ped, data_drs, data_lap, data_position):
        self.new_data_gear = data_gear
        self.new_data_rpm = data_rpm
        self.new_data_mph_fix = data_mph_fix
        self.new_data_brake = data_brake
        self.new_data_psi = data_psi
        self.new_data_sector = data_sector
        self.new_data_sector1 = data_sector1
        self.new_data_sector2 = data_sector2
        self.new_data_lastlap = data_lastlap
        self.new_data_fuel_in_tank = data_fuel_in_tank
        self.new_data_fuel_capacity = data_fuel_capacity
        self.new_data_team_id = data_team_id
        self.new_data_laptime = data_laptime
        self.new_data_throttle_ped = data_throttle_ped
        self.new_data_brake_ped = data_brake_ped
        self.new_data_drs = data_drs
        self.new_data_lap = data_lap
        self.new_data_position = data_position

        # ____RPM____
        # Assume RPM has changed and updated, no need to check if the rpm has changed.
        # Only old women drive at a constant RPM, and those that crash Saxos on roundabouts.
        for light in range(len(right_lights)):
            RpmLight.update(right_lights[light], self.new_data_rpm)
            RpmLight.update(left_lights[light], self.new_data_rpm)
        rpm_indicator.change_text(str(int(self.new_data_rpm)))
        self.data_rpm = self.new_data_rpm

        # ____MPH____
        if self.new_data_mph_fix != self.data_mph_fix:
            mph_indicator.change_text(str(int(self.new_data_mph_fix)).ljust(3))
        self.data_mph_fix = self.new_data_mph_fix

        # ____GEAR____
        # Next check to see if the gear value has changed, working still as a float. compare new against stored.
        # Process helps reduce excessive screen updates, which can be a problem on hi-res displays.
        if self.new_data_gear != self.data_gear:
            update_gear(int(self.new_data_gear), int(self.new_data_rpm))    # It's changed, call update routine setting, casting Int first
        self.data_gear = self.new_data_gear              # Now update the stored values new --> stored.

        # ____LAPTIME____
        laptime_indicator.change_text(str(round(self.new_data_laptime, 3)).ljust(3))
        self.data_laptime = self.new_data_laptime

        if (self.new_data_sector1 != self.data_sector1) and self.new_data_sector1 > 0:
            print "new sector : " + str(self.new_data_sector1)
            sector1.add_value(round(self.new_data_sector1, 3))
            update_sectors()
            self.data_sector1 = self.new_data_sector1


class DisplayText(object):
    def __init__(self, name, textval, forecolour, backcolour, loc_x, loc_y, myfont):
        self.name = name
        self.forecolour = forecolour
        self.backcolour = backcolour
        self.textval = textval
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.old_loc_x = loc_x
        self.old_loc_y = loc_y
        self.old_textval = textval
        self.myfont = myfont
        self.colour = GREEN

    def draw_text(self, textval, loc_x, loc_y):
        self.textval = textval
        self.loc_x = loc_x
        self.loc_y = loc_y
        oldtext = self.myfont.render(self.old_textval, False, BLACK)
        self.myfont.set_bold(True)
        windowSurface.blit(oldtext, (self.old_loc_x, self.old_loc_y))
        pygame.display.update()
        self.myfont.set_bold(False)
        text = self.myfont.render(self.textval, False, self.forecolour)
        windowSurface.blit(text, (self.loc_x, self.loc_y))
        self.old_loc_x = self.loc_x
        self.old_loc_y = self.loc_y
        self.old_textval = self.textval

    def change_text(self, textval):
        self.textval = textval
        oldtext = self.myfont.render(self.old_textval, False, BLACK)
        self.myfont.set_bold(True)
        windowSurface.blit(oldtext, (self.old_loc_x, self.old_loc_y))
        self.myfont.set_bold(False)
        text = self.myfont.render(self.textval, False, self.forecolour)
        windowSurface.blit(text, (self.loc_x, self.loc_y))
        pygame.display.update()
        self.old_loc_x = self.loc_x
        self.old_loc_y = self.loc_y
        self.old_textval = self.textval

    def change_text_colour(self, textval, colour):
        self.textval = textval
        self.colour = colour
        oldtext = self.myfont.render(self.old_textval, False, BLACK)
        self.myfont.set_bold(True)
        windowSurface.blit(oldtext, (self.old_loc_x, self.old_loc_y))
        self.myfont.set_bold(False)
        text = self.myfont.render(self.textval, False, self.colour)
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

    def __init__(self, name, length):
        DataSet.count += 1
        self.name = name
        self.length = length
        self.data_value = ''
        self.values = deque([])
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
    # Function used to define data arrays specifically used in the application.
    global sector1                          # Sector 1 times,
    global sector2                          # Sector 2 times,
    global sector3                          # Sector 3 times,
    global lap_times                        # Sector 4 times,
    sector1 = DataSet("S1", 10)
    sector2 = DataSet("S2", 10)
    sector3 = DataSet("S3", 10)
    lap_times = DataSet("Lap Times", 0)
    return


def setup_screen_text(info):
    global laptime_indicator
    global gear_indicator
    global mph_indicator
    global rpm_indicator
    global s1a_indicator
    global s2a_indicator
    global s3a_indicator

    global s1b_indicator
    global s2b_indicator
    global s3b_indicator

    global s1c_indicator
    global s2c_indicator
    global s3c_indicator

    # MPH Indicator
    laptime_indicator = DisplayText("mph", "000", GREEN, BLACK, (info.current_w*laptime_text_width_multiplier),
                                (info.current_h*laptime_text_height_multiplier), laptimeFont)
    laptime_indicator.draw_text("000", (info.current_w*laptime_text_width_multiplier),
                            (info.current_h*laptime_text_height_multiplier))

    # Gear Indicator
    gear_indicator = DisplayText("gear", "-", GREEN, BLACK, (info.current_w*gear_text_width_multiplier), info.current_h*gear_text_height_multiplier, basicFont)
    gear_indicator.draw_text("1", (info.current_w*gear_text_width_multiplier), info.current_h*gear_text_height_multiplier)

    # MPH Indicator
    mph_indicator = DisplayText("mph", "000", GREEN, BLACK, (info.current_w*mph_text_width_multiplier),
                                (info.current_h*mph_text_height_multiplier), mphFont)
    mph_indicator.draw_text("000", (info.current_w*mph_text_width_multiplier),
                            (info.current_h*mph_text_height_multiplier))

    # MPH Indicator
    rpm_indicator = DisplayText("mph", "000", GREEN, BLACK, (info.current_w*rpm_text_width_multiplier),
                                (info.current_h*rpm_text_height_multiplier), mphFont)
    rpm_indicator.draw_text("000", (info.current_w*rpm_text_width_multiplier),
                            (info.current_h*rpm_text_height_multiplier))

    # Scaling factors for sector times
    height = info.current_h                                                             # Height of the screen
    height_ratio = 0.16                                                                 # Ratio multiplier

    # Latest Lap
    s1a_indicator = DisplayText("s1a", "0.00", GREEN, BLACK, (((info.current_w/sector_space_div)*0)+(info.current_w/60)), (height-((height*height_ratio)*2)), sectorFont)
    s1a_indicator.draw_text("0.00", (((info.current_w/sector_space_div)*0)+(info.current_w/60)), (height-((height*height_ratio)*2)))
    s2a_indicator = DisplayText("s2a", "0.00", GREEN, BLACK, (((info.current_w/sector_space_div)*1)+(info.current_w/60)), (height-((height*height_ratio)*2)), sectorFont)
    s2a_indicator.draw_text("0.00", (((info.current_w/sector_space_div)*1)+(info.current_w/60)), (height-((height*height_ratio)*2)))
    s3a_indicator = DisplayText("s3a", "0.00", GREEN, BLACK, (((info.current_w/sector_space_div)*2)+(info.current_w/60)), (height-((height*height_ratio)*2)), sectorFont)
    s3a_indicator.draw_text("0.00", (((info.current_w/sector_space_div)*2)+(info.current_w/60)), (height-((height*height_ratio)*2)))

    # Latest Lap + 1
    s1b_indicator = DisplayText("s1b", "0.00", GREEN, BLACK, (((info.current_w/sector_space_div)*0)+(info.current_w/60)),(height-((height*height_ratio)*1.5)), sectorFont)
    s1b_indicator.draw_text("0.00", (((info.current_w/sector_space_div)*0)+(info.current_w/60)), (height-((height*height_ratio)*1.5)))
    s2b_indicator = DisplayText("s2b", "0.00", GREEN, BLACK, (((info.current_w/sector_space_div)*1)+(info.current_w/60)), (height-((height*height_ratio)*1.5)), sectorFont)
    s2b_indicator.draw_text("0.00", (((info.current_w/sector_space_div)*1)+(info.current_w/60)), (height-((height*height_ratio)*1.5)))
    s3b_indicator = DisplayText("s3b", "0.00", GREEN, BLACK, (((info.current_w/sector_space_div)*2)+(info.current_w/60)), (height-((height*height_ratio)*1.5)), sectorFont)
    s3b_indicator.draw_text("0.00", (((info.current_w/sector_space_div)*2)+(info.current_w/60)), (height-((height*height_ratio)*1.5)))

    # Latest Lap +2
    s1c_indicator = DisplayText("s1c", "0.00", GREEN, BLACK, (((info.current_w/sector_space_div)*0)+(info.current_w/60)),(height-((height*height_ratio)*1)), sectorFont)
    s1c_indicator.draw_text("1.00", (((info.current_w/sector_space_div)*0)+(info.current_w/60)), (height-((height*height_ratio)*1)))

    s2c_indicator = DisplayText("s2c", "0.00", GREEN, BLACK, (((info.current_w/sector_space_div)*1)+(info.current_w/60)), (height-((height*height_ratio)*1)), sectorFont)
    s2c_indicator.draw_text("0.00", (((info.current_w/sector_space_div)*1)+(info.current_w/60)), (height-((height*height_ratio)*1)))

    s3c_indicator = DisplayText("s3c", "0.00", GREEN, BLACK, (((info.current_w/sector_space_div)*2)+(info.current_w/60)), (height-((height*height_ratio)*1)), sectorFont)
    s3c_indicator.draw_text("0.00", (((info.current_w/sector_space_div)*2)+(info.current_w/60)), (height-((height*height_ratio)*1)))

    return


def initial_setup():
    info = pygame.display.Info()
    print (info)
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


def update_gear(gear, rpm):
    gear_indicator.change_text_colour(gear_lookup[gear], GREEN)
    return


def update_sectors():
    s1a_indicator.change_text(str(sector1.values[0]))
    s2a_indicator.change_text(str(sector2.values[0]))
    s3a_indicator.change_text(str(sector3.values[0]))
    s1b_indicator.change_text(str(sector1.values[1]))
    s2b_indicator.change_text(str(sector2.values[1]))
    s3b_indicator.change_text(str(sector3.values[1]))
    s1c_indicator.change_text(str(sector1.values[2]))
    s2c_indicator.change_text(str(sector2.values[2]))
    s3c_indicator.change_text(str(sector3.values[2]))
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


def test_sectors():
    sector1.add_value(random.randint(10,90)*1.345)
    sector2.add_value(random.randint(10,90)*1.345)
    sector3.add_value(random.randint(10,90)*1.234)
    update_sectors()
    return


def game_loop():
    my_received_data = IncomingData("telemetry")
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
                if event.key == K_s:
                    test_sectors()
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

        data_gear, data_mph_fix, data_brake, data_rpm, data_psi, data_sector, data_sector1, data_sector2, \
        data_lastlap, data_fuel_in_tank, data_fuel_capacity, data_team_id, data_laptime, data_throttle_ped, \
        data_brake_ped, data_drs, data_lap, data_position = receiver()

        my_received_data.update_all(data_gear, data_mph_fix, data_brake, data_rpm, data_psi, data_sector,
                                    data_sector1, data_sector2, data_lastlap, data_fuel_in_tank,
                                    data_fuel_capacity, data_team_id, data_laptime, data_throttle_ped,
                                    data_brake_ped, data_drs, data_lap, data_position)

        #update_gear(str(data_gear))
        #update_rpm(data_rpm)

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
    info = pygame.display.Info()
    # find fonts  ----
    available_fonts = pygame.font.get_fonts()
    for font in range(len(available_fonts)):
        if available_fonts[font] == LCD_font:
            fontpath = pygame.font.match_font(available_fonts[font])
            # set up fonts
    basicFont = pygame.font.Font(fontpath, int((info.current_w) * gear_fontsize_ratio))
    sectorFont = pygame.font.Font(fontpath, int(info.current_w * sector_fontsize_ratio))
    mphFont = pygame.font.Font(fontpath, int(info.current_w * mph_fontsize_ratio))
    laptimeFont = pygame.font.Font(fontpath, int(info.current_w * laptime_fontsize_ratio))
    instruFont = pygame.font.SysFont(None, instru_fontsize)
    logoFont = pygame.font.SysFont(None, logo_fontsize)

    windowSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)  # Now automatically uses full screen
    pygame.display.set_caption(display_title)
    windowSurface.fill(BLACK)
    main()
