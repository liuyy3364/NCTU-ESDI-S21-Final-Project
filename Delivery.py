import Servo
import time

class Delivery:
    def __init__(self, stock) -> None:
        self.stock = stock
        self.positions = [ServoHook(12), ServoHook(32), ServoHook(33), ServoHook(35)]

    def deliver(self, cart):
        delivery_list = self.get_position(cart)
        for p in delivery_list:
            self.positions[p].deliver()
            time.sleep(1)
        for p in delivery_list:
            self.positions[p].reset()

    def get_position(self, cart: dict):
        delivery_list = []
        for name, num in cart.items():
            for _ in range(num):
                delivery_list.append(self.stock[name].pop())
        return delivery_list

        
class ServoHook:
    def __init__(self, pin) -> None:
        self.servo = Servo.Servo(pin)
        self.default_angle=120
        self.servo.set_angle(self.default_angle)
        self.servo.start()
        time.sleep(0.35)
        self.servo.stop()

    def deliver(self):
        self.servo.set_angle(0)
        time.sleep(0.35)
        self.servo.stop()

    def reset(self):
        self.servo.set_angle(self.default_angle)
        time.sleep(0.35)
        self.servo.stop()
    