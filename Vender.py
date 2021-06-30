from GraphicAndDetect_debug import Camera
from TextToSpeech import TTS
import Clerk
import Cashier
import Delivery
import time

class Vender:
    def __init__(self, graphic: Camera) -> None:
        self.graphic = graphic
        self.audio = TTS()
        self.products = {"冷氣卡":600,"餅乾":10}
        self.stock = {"冷氣卡": [1,3], "餅乾": [0,2]}
        self.clerk = Clerk.Clerk(self.graphic, self.audio, self.products, self.stock)
        self.cashier = Cashier.Cashier(self.graphic, self.audio, self.products)
        self.delivery = Delivery.Delivery(self.stock)
    
    def check_presence(self) -> int:
        return self.graphic.face_num

    def return_idle(self):
        self.graphic.update_msg("IDLE")

    def run(self) -> None:
        while 1:
            # Idle
            self.return_idle()
            # -DEBUG BEGIN
            self.graphic.face_detector_switch(True)
            while self.check_presence() == 0:
                continue
            time.sleep(0.5)
            while self.check_presence() == 0:
                continue
            # Transaction start
            self.graphic.face_detector_switch(False)
            # -DEBUG END
            try:
                info = self.clerk.take_order()
                if self.cashier.checkout(info):
                    continue
                self.delivery.deliver(info.cart)
            except Exception as e:
                print(str(e))
                pass
