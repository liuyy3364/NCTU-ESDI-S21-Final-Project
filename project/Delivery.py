import Servo

class Delivery:
    def __init__(self, stock) -> None:
        self.stock = stock
        self.positions = [ServoHook(12), ServoHook(32), ServoHook(33), ServoHook(35)]

    def deliver(self, cart):
        delivery_list = self.get_position(cart)
        for p in delivery_list:
            self.positions[p].deliver()

    def get_position(self, cart):
        delivery_list = []
        for name, num in cart.items():
            for _ in range(num):
                delivery_list.append(self.stock[name].pop())
        return delivery_list

        
class ServoHook:
    def __init__(self, pin) -> None:
        self.servo = Servo.Servo(pin)
        self.servo.start()

    def __del__(self):
        self.servo.stop()

    def deliver(self):
        self.servo.set_angle(0)

    def reset(self):
        self.servo.set_angle(90)
    