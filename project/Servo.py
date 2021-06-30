# Import libraries
import RPi.GPIO as GPIO

class PWM_Pin:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BOARD)
        self.pin_num = pin
        GPIO.setup(pin,GPIO.OUT)
        self.pin = GPIO.PWM(self.pin_num,50)
        self.percetage = 50

    def __del__(self):
        self.stop()

    def start(self, val=0):
        self.pin.start(val)

    def stop(self):
        self.pin.stop()

    def set_pwm(self, percentage):
        if percentage>100 or percentage<0:
            raise "percentage out of range(0~100)"
        else:
            self.percetage = percentage
            self.pin.ChangeDutyCycle(percentage)

class Servo:
    def __init__(self, pin):
        self.pin = PWM_Pin(pin)
        self.angle = 90

    def __del__(self):
        self.stop()

    def start(self, val=0):
        self.pin.start(val)
        self.set_angle(self.angle)

    def stop(self):
        self.pin.stop()

    def set_angle(self, angle):
        if angle>180 or angle<0:
            raise "angle out of range(0~180)"
        else:
            self.pin.set_pwm(2+(angle/18))


# PWM_PIN = 12

# # Set GPIO numbering mode
# GPIO.setmode(GPIO.BOARD)

# PWM_PIN = 12


# # Set pin 11 as an output, and define as servo1 as PWM pin
# GPIO.setup(PWM_PIN,GPIO.OUT)
# servo1 = GPIO.PWM(PWM_PIN,50) # pin 11 for servo1, pulse 50Hz

# # Start PWM running, with value of 0 (pulse off)
# servo1.start(1)

# # Loop to allow user to set servo angle. Try/finally allows exit
# # with execution of servo.stop and GPIO cleanup :)

# try:
#     while True:
#         #Ask user for angle and turn servo to it
#         angle = float(input('Enter angle between 0 & 180: '))%181
#         servo1.ChangeDutyCycle(2+(angle/18))
#         time.sleep(1)

# finally:
#     #Clean things up at the end
#     servo1.stop()
#     GPIO.cleanup()
#     print("Goodbye!")