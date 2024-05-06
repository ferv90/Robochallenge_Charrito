#!/usr/bin/python3

import sys
import serial
import pigpio
import time
import threading
import RPi.GPIO as GPIO
from smbus2 import SMBus, i2c_msg


if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)
    
print('''
**********************************************************
*******Function: CharritoV2 car routine*******************
*******Official website:https://www.yazaki.com.mx*********
**********************************************************
----------------------------------------------------------
''')

car_speed = 0 # Car speed
car_speed_move = 80   # Car command to move
car_wheel_angle = 90  # Car direction angle, just keep the default
car_wheel_rotate = 0  # Car yaw parameters, just keep the default
car_turn_mode = ['go','back','turn_left','left_back','turn_right','right_back','stop']

# Steering servo control angle
steering_servo_angle_pulse = 1500  # mid position (500 -- 2500)
steering_servo_turn_time = 100  # target angle time

start = True
pin = 12 # The io port of the front steering wheel

pi = pigpio.pi()
pi.set_PWM_range(pin, 20000)# 5 is the IO port to output PWM, 20000 sets the PWM adjustment range,
                            # The control signal of our servo is 50Hz, which is a cycle of 20ms. That�s 20,000us.
                            # Set to 20000, which means the minimum adjustment is 1us
pi.set_PWM_frequency(pin, 50) # Set the frequency of PWM, 5 is the IO port to be set, 50 is the frequency
pi.set_PWM_dutycycle(pin, 1500)

def servo_angle(dc):
    pi.set_PWM_dutycycle(pin, dc) #Set the pulse width of pwm (pin , pulse width)
    time.sleep(0.5)

# Motor controller thread
def motors():
    print(f'{threading.current_thread().name} {threading.get_native_id()}')
    global steering_servo_angle_pulse
    servo_angle(steering_servo_angle_pulse)
    mode = None  # Sport mode
    i = 0
    while True:
        time.sleep(1)
        if i >= 7:
            i = 0
        mode = car_turn_mode[i]
        # car_speed = Indicates the speed of the car
        # steering_servor_angle = Indicates the angle to which the servo rotates
        if mode == 'go':
            car_speed = car_speed_move
            steering_servo_angle_pulse = 1500

        elif mode == 'back':
            car_speed = -car_speed_move
            steering_servo_angle_pulse = 1500

        elif mode == 'turn_left':
            car_speed = car_speed_move
            steering_servo_angle_pulse = 1000

        elif mode == 'left_back':
            car_speed = -car_speed_move
            steering_servo_angle_pulse = 1000

        elif mode == 'turn_right':
            car_speed = car_speed_move
            steering_servo_angle_pulse = 2000

        elif mode == 'right_back':
            car_speed = -car_speed_move
            steering_servo_angle_pulse = 2000

        elif mode == 'stop':
            car_speed = 0
            steering_servo_angle_pulse = 1500
        else:
            print('wait the message')
        
        print("Currently running mode:",mode)
        servo_angle(steering_servo_angle_pulse)
        time.sleep(3)
        i += 1



def aimodel():
    print(f'{threading.current_thread().name} {threading.get_native_id()}')
        # while True:
        # AI main routine implementation

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    thread_motors = threading.Thread(target=motors)
    thread_aimodel = threading.Thread(target=aimodel)

    # Start threads
    thread_motors.start()
    thread_aimodel.start()


    # Wait for thread ends
    thread_motors.join()
    thread_aimodel.join()

    print(f'{threading.current_thread().name} {threading.get_native_id()}')
