# Import libraries
import RPi.GPIO as GPIO
def angle2percent(angle):
    return 2+(angle/18)

class Servo:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BOARD)
        self.pin_num = pin
        GPIO.setup(pin,GPIO.OUT)
        self.pin = GPIO.PWM(self.pin_num,50)
        self.angle = 90

    def __del__(self):
        self.pin.stop()

    def start(self):
        self.pin.start(angle2percent(self.angle))

    def stop(self):
        self.pin.ChangeDutyCycle(0)

    def set_angle(self, angle):
        if angle>180 or angle<0:
            raise "angle out of range(0~180)"
        else:
            self.angle = angle
            self.pin.ChangeDutyCycle(angle2percent(self.angle))
