# -This module created for Hiwonder 4 wheeles chassis.
# -The motor driver used is the i2c control
# -The base package used is the Rpi GPIO for servo steering
# -The Object Motor needs to be created first
# -Then the move() function can be called to operate the motors
#  move(speed,turn,delay)
# -Speed and turn range from -1 to 1
# -Delay is in seconds.
############################################################################################################
#
#  THIS MODULE WILL WORKING ON RASPBERRY PI 5 ONLY
#
############################################################################################################

#import RPi.GPIO as GPIO
from gpiozero import Motor, AngularServo
from time import sleep

servoSteering = AngularServo(12, min_angle=-90, max_angle=90)
motorLeft = Motor(forward=4, backward=14)
motorRight = Motor(forward=17, backward=18)


def move(motor,speed=0.25,turn=0,t=0):
    speed *=100
    turn *=70
    leftSpeed = speed-turn
    rightSpeed = speed+turn

    #Normalization
    if leftSpeed>1: leftSpeed = 1
    elif leftSpeed<-1: leftSpeed = -1
    if rightSpeed>1: rightSpeed = 1
    elif rightSpeed<-1: rightSpeed = -1
    print('robot speed', leftSpeed,rightSpeed)
        
    #Define steering and direction
    if leftSpeed>0 : 
        motorLeft.forward(leftSpeed)
        motorRight.forward(leftSpeed)
    else:
        motorLeft.forward(leftSpeed)
        motorRight.forward(leftSpeed)

    if rightSpeed>0:
        motorLeft.forward(leftSpeed)
        motorRight.forward(leftSpeed)
    else:
        motorLeft.forward(leftSpeed)
        motorRight.forward(leftSpeed)
        sleep(t)

def stop(self,t=0):
    motorLeft.stop()
    motorRight.stop()
    sleep(t)

def main():
    move(0.5,0,2)
    stop(2)
    move(-0.5,0,2)
    stop(2)
    move(0,0.5,2)
    stop(2)
    move(0,-0.5,2)
    stop(2)

if __name__ == '__main__':
    # motor= Motor(2,3,4,17,22,27)
    main()