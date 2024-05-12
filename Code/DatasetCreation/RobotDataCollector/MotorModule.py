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
#!/usr/bin/python3
from operator import le
from turtle import forward
from cairo import Device
from gpiozero import Motor, AngularServo, PWMLED
from time import sleep

#from gpiozero.pins.pigpio import PiGPIOFactory
# Device.pin_factory = PiGPIOFactory()

# leftSpeed   = PWMLED(12)
# rightSpeed  = PWMLED(13)
# servoPin    = 17


class Motors():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B,ServoPin):
        self.servo = AngularServo(ServoPin, initial_angle=0.0, min_angle=-90, max_angle=90, 
                                          min_pulse_width=1/1000, max_pulse_width=2/1000, frame_width=20/1000, pin_factory=None) # 1 /1000 min width
        self.Left  = Motor(forward=In1A, backward=In2A)
        self.Right = Motor(forward=In1B, backward=In2B)
        self.pwmA = PWMLED(EnaA);
        self.pwmB = PWMLED(EnaB);
        self.pwmA.value = 0;
        self.pwmB.value = 0;

    def move(self,speed,turn,t):
        # speed *=100
        # turn *=70
        # leftSpeed = round(speed+(turn*0.5), 2)
        # rightSpeed = round(speed-(turn*0.5), 2)
        steeringAngle = round(turn*90, 2)

        # if leftSpeed>1: leftSpeed = 1
        # elif leftSpeed<-1: leftSpeed = -1
        # if rightSpeed>1: rightSpeed = 1
        # elif rightSpeed<-1: rightSpeed = -1
        # self.pwmA.value = abs(leftSpeed)
        # self.pwmB.value = abs(rightSpeed)
        self.servo.angle = steeringAngle
        
        # leftSpeed = speed+(turn*0.5)
        # rightSpeed = speed-(turn*0.5)
        print('speed,angle:', speed, steeringAngle)
        
        if speed>0:
            self.Left.forward()
            self.Right.forward()
            self.pwmA.value = abs(speed)
            self.pwmB.value = abs(speed)

        elif speed<0:
            self.Left.backward()
            self.Right.backward()
            self.pwmA.value = abs(speed)
            self.pwmB.value = abs(speed)

        else:
            self.stop()
            sleep(t)

    def stop(self,t=0):
        self.pwmA.value = 0;
        self.pwmB.value = 0;
        self.Left.stop()
        self.Right.stop()
        sleep(t)

def main():
    motor.move(0.5,0,2)
    motor.stop(2)
    motor.move(-0.5,0,2)
    motor.stop(2)
    motor.move(0,0.5,2)
    motor.stop(2)
    motor.move(0,-0.5,2)
    motor.stop(2)

if __name__ == '__main__':
    motor= Motors(12,16,19,13,5,6,17)
    # main()


# def main():
#     move(0.5,0,2)
#     stop(2)
#     move(-0.5,0,2)
#     stop(2)
#     move(0,0.5,2)
#     stop(2)
#     move(0,-0.5,2)
#     stop(2)

# if __name__ == '__main__':
#     main()

# while True:
    # servoSteering.angle = 0
    # motorLeft.forward()
    # motorRight.forward()
    # speedLeft.value = 0.25
    # speedRight.value = 0.25
    # sleep(2)
    # servoSteering.angle = 90
    # speedLeft.value = 0.5
    # speedRight.value = 0.5
    # motorLeft.forward()
    # motorRight.forward()
    # sleep(2)
    # servoSteering.angle = 0
    # motorLeft.backward()
    # motorRight.backward()
    # speedLeft.value = 0.90
    # speedRight.value = 0.90
    # sleep(2)
    # servoSteering.angle = -90
    # speedRight.value = 0
    # speedLeft.value = 0
    # motorLeft.stop()
    # motorRight.stop()
    # sleep(2)