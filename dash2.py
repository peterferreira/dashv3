#!/usr/bin/env python
# --------------------------------
# Codemasters F1 Dash v2
#
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
    global r_rpm1
    global r_rpm2
    global r_rpm3
    global r_rpm4
    global r_rpm5
    global r_rpm6
    global r_rpm7
    global r_rpm8
    global r_rpm9
    global r_rpm10
    global r_rpm11
    global r_rpm12
    global r_rpm13
    global r_rpm14
    global r_rpm15
    global r_rpm16
    global r_rpm17
    global r_rpm18
    global r_rpm19
    global r_rpm20
    global r_rpm21

    global l_rpm1
    global l_rpm2
    global l_rpm3
    global l_rpm4
    global l_rpm5
    global l_rpm6
    global l_rpm7
    global l_rpm8
    global l_rpm9
    global l_rpm10
    global l_rpm11
    global l_rpm12
    global l_rpm13
    global l_rpm14
    global l_rpm15
    global l_rpm16
    global l_rpm17
    global l_rpm18
    global l_rpm19
    global l_rpm20
    global l_rpm21


    # Parameters used to incrementally layout rpm rectangles from left to right
    r_x = int(info.current_w) * 0.0225
    l_x = int(info.current_w) * 0.0227
    r_xf = r_x * 0.89
    l_xf = l_x * 0.85
    y = int(info.current_h) * 0.13
    l_y = y + 1
    # Parameters used to incrementally layout rpm rectangles from right to left.
    # These are draw backwards.
    rev_startx = int(info.current_w) - 1

    r_rpm1 = rpm_light(light1[0], light1[1], 0, 0, r_xf, y, trig_val1)
    r_rpm2 = rpm_light(light2[0], light2[1], r_x, 0, r_xf, y, trig_val2)
    r_rpm3 = rpm_light(light3[0], light3[1], (2 * r_x), 0, r_xf, y, trig_val3)
    r_rpm4 = rpm_light(light4[0], light4[1], (3 * r_x), 0, r_xf, y, trig_val4)
    r_rpm5 = rpm_light(light5[0], light5[1], (4 * r_x), 0, r_xf, y, trig_val5)
    r_rpm6 = rpm_light(light6[0], light6[1], (5 * r_x), 0, r_xf, y, trig_val6)
    r_rpm7 = rpm_light(light7[0], light7[1], (6 * r_x), 0, r_xf, y, trig_val7)
    r_rpm8 = rpm_light(light8[0], light8[1], (7 * r_x), 0, r_xf, y, trig_val8)
    r_rpm9 = rpm_light(light9[0], light9[1], (8 * r_x), 0, r_xf, y, trig_val9)
    r_rpm10 = rpm_light(light10[0], light10[1], (9 * r_x), 0, r_xf, y, trig_val10)
    r_rpm11 = rpm_light(light11[0], light11[1], (10 * r_x), 0, r_xf, y, trig_val11)
    r_rpm12 = rpm_light(light12[0], light12[1], (11 * r_x), 0, r_xf, y, trig_val12)
    r_rpm13 = rpm_light(light13[0], light13[1], (12 * r_x), 0, r_xf, y, trig_val13)
    r_rpm14 = rpm_light(light14[0], light14[1], (13 * r_x), 0, r_xf, y, trig_val14)
    r_rpm15 = rpm_light(light15[0], light15[1], (14 * r_x), 0, r_xf, y, trig_val15)
    r_rpm16 = rpm_light(light16[0], light16[1], (15 * r_x), 0, r_xf, y, trig_val16)
    r_rpm17 = rpm_light(light17[0], light17[1], (16 * r_x), 0, r_xf, y, trig_val17)
    r_rpm18 = rpm_light(light18[0], light18[1], (17 * r_x), 0, r_xf, y, trig_val18)
    r_rpm19 = rpm_light(light19[0], light19[1], (18 * r_x), 0, r_xf, y, trig_val19)
    r_rpm20 = rpm_light(light20[0], light20[1], (19 * r_x), 0, r_xf, y, trig_val20)
    r_rpm21 = rpm_light(light21[0], light21[1], (20 * r_x), 0, r_xf, y, trig_val21)

    l_rpm1 = rpm_light(light1[0], light1[1], rev_startx, l_y, -l_xf, -y, trig_val1)
    l_rpm2 = rpm_light(light2[0], light2[1], (rev_startx - l_x), l_y, -l_xf, -y, trig_val2)
    l_rpm3 = rpm_light(light3[0], light3[1], (rev_startx - (2 * l_x)), l_y, -l_xf, -y, trig_val3)
    l_rpm4 = rpm_light(light4[0], light4[1], (rev_startx - (3 * l_x)), l_y, -l_xf, -y, trig_val4)
    l_rpm5 = rpm_light(light5[0], light5[1], (rev_startx - (4 * l_x)), l_y, -l_xf, -y, trig_val5)
    l_rpm6 = rpm_light(light6[0], light6[1], (rev_startx - (5 * l_x)), l_y, -l_xf, -y, trig_val6)
    l_rpm7 = rpm_light(light7[0], light7[1], (rev_startx - (6 * l_x)), l_y, -l_xf, -y, trig_val7)
    l_rpm8 = rpm_light(light8[0], light8[1], (rev_startx - (7 * l_x)), l_y, -l_xf, -y, trig_val8)
    l_rpm9 = rpm_light(light9[0], light9[1], (rev_startx - (8 * l_x)), l_y, -l_xf, -y, trig_val9)
    l_rpm10 = rpm_light(light10[0], light10[1], (rev_startx - (9 * l_x)), l_y, -l_xf, -y, trig_val10)
    l_rpm11 = rpm_light(light11[0], light11[1], (rev_startx - (10 * l_x)), l_y, -l_xf, -y, trig_val11)
    l_rpm12 = rpm_light(light12[0], light12[1], (rev_startx - (11 * l_x)), l_y, -l_xf, -y, trig_val12)
    l_rpm13 = rpm_light(light13[0], light13[1], (rev_startx - (12 * l_x)), l_y, -l_xf, -y, trig_val13)
    l_rpm14 = rpm_light(light14[0], light14[1], (rev_startx - (13 * l_x)), l_y, -l_xf, -y, trig_val14)
    l_rpm15 = rpm_light(light15[0], light15[1], (rev_startx - (14 * l_x)), l_y, -l_xf, -y, trig_val15)
    l_rpm16 = rpm_light(light16[0], light16[1], (rev_startx - (15 * l_x)), l_y, -l_xf, -y, trig_val16)
    l_rpm17 = rpm_light(light17[0], light17[1], (rev_startx - (16 * l_x)), l_y, -l_xf, -y, trig_val17)
    l_rpm18 = rpm_light(light18[0], light18[1], (rev_startx - (17 * l_x)), l_y, -l_xf, -y, trig_val18)
    l_rpm19 = rpm_light(light19[0], light19[1], (rev_startx - (18 * l_x)), l_y, -l_xf, -y, trig_val19)
    l_rpm20 = rpm_light(light20[0], light20[1], (rev_startx - (19 * l_x)), l_y, -l_xf, -y, trig_val20)
    l_rpm21 = rpm_light(light21[0], light21[1], (rev_startx - (20 * l_x)), l_y, -l_xf, -y, trig_val21)

    r_rpm1.initialize()
    r_rpm2.initialize()
    r_rpm3.initialize()
    r_rpm4.initialize()
    r_rpm5.initialize()
    r_rpm6.initialize()
    r_rpm7.initialize()
    r_rpm8.initialize()
    r_rpm9.initialize()
    r_rpm10.initialize()
    r_rpm11.initialize()
    r_rpm12.initialize()
    r_rpm13.initialize()
    r_rpm14.initialize()
    r_rpm15.initialize()
    r_rpm16.initialize()
    r_rpm17.initialize()
    r_rpm18.initialize()
    r_rpm19.initialize()
    r_rpm20.initialize()
    r_rpm21.initialize()

    l_rpm1.initialize()
    l_rpm2.initialize()
    l_rpm3.initialize()
    l_rpm4.initialize()
    l_rpm5.initialize()
    l_rpm6.initialize()
    l_rpm7.initialize()
    l_rpm8.initialize()
    l_rpm9.initialize()
    l_rpm10.initialize()
    l_rpm11.initialize()
    l_rpm12.initialize()
    l_rpm13.initialize()
    l_rpm14.initialize()
    l_rpm15.initialize()
    l_rpm16.initialize()
    l_rpm17.initialize()
    l_rpm18.initialize()
    l_rpm19.initialize()
    l_rpm20.initialize()
    l_rpm21.initialize()


def initial_setup():
    info = pygame.display.Info()
    print type(info)
    setup_rpm_markers(info)
    pygame.display.update()
    return


def update_rpm(rpm):
    print rpm
    r_rpm1.update(rpm)
    r_rpm2.update(rpm)
    r_rpm3.update(rpm)
    r_rpm4.update(rpm)
    r_rpm5.update(rpm)
    r_rpm6.update(rpm)
    r_rpm7.update(rpm)
    r_rpm8.update(rpm)
    r_rpm9.update(rpm)
    r_rpm10.update(rpm)
    r_rpm11.update(rpm)
    r_rpm12.update(rpm)
    r_rpm13.update(rpm)
    r_rpm14.update(rpm)
    r_rpm15.update(rpm)
    r_rpm16.update(rpm)
    r_rpm17.update(rpm)
    r_rpm18.update(rpm)
    r_rpm19.update(rpm)
    r_rpm20.update(rpm)
    r_rpm21.update(rpm)

    l_rpm1.update(rpm)
    l_rpm2.update(rpm)
    l_rpm3.update(rpm)
    l_rpm4.update(rpm)
    l_rpm5.update(rpm)
    l_rpm6.update(rpm)
    l_rpm7.update(rpm)
    l_rpm8.update(rpm)
    l_rpm9.update(rpm)
    l_rpm10.update(rpm)
    l_rpm11.update(rpm)
    l_rpm12.update(rpm)
    l_rpm13.update(rpm)
    l_rpm14.update(rpm)
    l_rpm15.update(rpm)
    l_rpm16.update(rpm)
    l_rpm17.update(rpm)
    l_rpm18.update(rpm)
    l_rpm19.update(rpm)
    l_rpm20.update(rpm)
    l_rpm21.update(rpm)
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
                    rpm += 250
                    update_rpm(rpm)
                if event.key == K_DOWN:
                    print "Down"
                    rpm -= 250
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
