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
                                          min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, frame_width=20/1000, pin_factory=None) # 1 /1000 min width
        self.Left  = Motor(forward=In1A, backward=In2A)
        self.Right = Motor(forward=In1B, backward=In2B)
        self.pwmA = PWMLED(EnaA);
        self.pwmB = PWMLED(EnaB);
        self.pwmA.value = 0;
        self.pwmB.value = 0;
        self.lastAngle = 0;

    def move(self,speed,turn,t):
        offsetMiddle = 10
        turn = (turn*90)+offsetMiddle  # Offset to make the servo straight
        # leftSpeed = round(speed+(turn*0.5), 2)
        # rightSpeed = round(speed-(turn*0.5), 2)
        if turn>90: turn = 90
        steeringAngle = round(turn, 2)

        if(steeringAngle != self.lastAngle):
            self.lastAngle = steeringAngle
            self.servo.angle = steeringAngle
            sleep(0.5)
        
        # leftSpeed = speed+(turn*0.5)
        # rightSpeed = speed-(turn*0.5)
        print('speed,angle:', speed, steeringAngle-offsetMiddle)
        
        if speed>0:
            self.Left.forward()
            self.Right.forward()
            self.pwmA.value = abs(speed)
            self.pwmB.value = abs(speed*0.9)

        elif speed<0:
            self.Left.backward()
            self.Right.backward()
            self.pwmA.value = abs(speed)
            self.pwmB.value = abs(speed*0.9)

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