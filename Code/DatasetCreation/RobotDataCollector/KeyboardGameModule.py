########### KEYBOARD CONTROL  #################
#
#               UP['w']
# LEFT['a']                 RIGHT['d']
#              DOWN['s']
#
# (1) = START RECORDING
# (3) = STOP RECORDING
###############################################
import sys
import pygame as kb
from time import sleep

from requests import get

buttons = {'steering': 0, 'speed': 0, 'recordctl': 0}

def init():
    kb.init()
    kb.display.set_mode((100,100))
    print("Keyboard Module Initialized...")

def keyEvent(name=''):
    for event in kb.event.get():
        if event.type == kb.KEYDOWN:
            if event.key == kb.K_w or event.key == kb.K_UP:
                # print("forward")
                buttons['speed'] = buttons['speed'] + 1
                if buttons['speed'] > 10: 
                    buttons['speed'] = 10

            elif event.key == kb.K_s or event.key == kb.K_DOWN:
                # print("backward")
                buttons['speed'] = buttons['speed'] - 1
                if buttons['speed'] < -10: 
                    buttons['speed'] = -10

            elif event.key == kb.K_a or event.key == kb.K_LEFT:
                # print("left")
                buttons['steering'] = buttons['steering'] - 1
                if buttons['steering'] < -10: 
                    buttons['steering'] = -10

            elif event.key == kb.K_d or event.key == kb.K_RIGHT:
                # print("right")
                buttons['steering'] = buttons['steering'] + 1
                if buttons['steering'] > 10: 
                    buttons['steering'] = 10

            elif event.key == kb.K_SPACE:
                print("key: SPACE")
                buttons['recordctl'] = 1

            elif event.key == kb.K_0:
                print("key: 0")
                buttons['recordctl'] = 3
                
            elif event.key == kb.K_ESCAPE: # Press 'esc' to exit
                print("closing...")
                kb.quit()
                sys.exit()  
    
    return buttons
    

if __name__ == '__main__':
    init()
    while True:
        sleep(0.001)
