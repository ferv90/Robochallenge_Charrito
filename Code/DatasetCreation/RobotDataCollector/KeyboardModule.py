########### KEYBOARD CONTROL  #################
#
#               UP['w']
# LEFT['a']                 RIGHT['d']
#              DOWN['s']
#
# (1) = START RECORDING
# (3) = STOP RECORDING
###############################################

import keyboard as kb
from time import sleep

buttons = {'steering': 0, 'speed': 0, 'recordctl': 0}

def keyEvent(name=''):
    global buttons
    event = kb.read_event()
    if event.event_type == kb.KEY_DOWN:
        if event.name == 'w' or event.name == '8':
            print("forward")
            buttons['speed'] = round(buttons['speed']+0.1, 2)
            if buttons['speed'] > 1: 
                buttons['speed'] = 1

        elif event.name == 's' or event.name == '2':
            print("backward")
            buttons['speed'] = round(buttons['speed']-0.1, 2)
            if buttons['speed'] < -1: 
                buttons['speed'] = -1

        elif event.name == 'a' or event.name == '4':
            print("left")
            buttons['steering'] = round(buttons['steering']-0.1, 2)
            if buttons['steering'] < -1: 
                buttons['steering'] = -1

        elif event.name == 'd' or event.name == '6':
            print("right")
            buttons['steering'] = round(buttons['steering']+0.1, 2)
            if buttons['steering'] > 1: 
                buttons['steering'] = 1

        elif event.name == '1':
            print("key:1")
            buttons['recordctl']=1
        elif event.name == '3':
            print("key:3")
            buttons['recordctl']=3
                
        elif event.name == 'esc': # Press 'esc' to exit
            print("closing...")
            kb.unhook_all()
            exit()  
    
    return buttons
    
def main():
    # print(keyEvent('recordCtl'))  # To get a single value
    sleep(0.05)


if __name__ == '__main__':
    while True:
        main()
