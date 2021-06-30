import collections
from SpeechToText import STT
from TextToSpeech import TTS
from typing import Callable, Any
from TransactionInfo import Info
import time
import threading as Thread
from ChtToDigit import trans
from GraphicAndDetect_debug import Camera
import speech_recognition as sr

class Clerk:
    def __init__(self, graphic: Camera, products: dict, stock: dict) -> None:
        self.graphic = graphic
        self.tts = TTS()
        self.stt = STT()
        self.products = products
        self.stock = stock

    def update_msg(self, msg):
        self.graphic.update_msg(msg)

    def check_presence(self):
        return self.graphic.face_num
        

    def face_detector_switch(self, val):
        self.graphic.face_detector_switch(val)


    def take_order(self) -> Info:
        info = Info(self.products)
        audio = None
        msg_wrapper = [""]
        self.update_msg(msg_wrapper[0])

        # record_reporter_sem = Thread.Semaphore(0)
        # calibarate_sem = Thread.Semaphore(0)
        # record_reporter_stop = False
        # def record_reporter()->None:
        #     while 1:
        #         record_reporter_sem.acquire()
        #         self.update_msg(msg_wrapper[0] + "麥克風校正中...")
        #         # self.update_msg(info.print_cart() + "麥克風校正中...")
        #         calibarate_sem.acquire()
        #         self.update_msg(msg_wrapper[0] + "收音中...")
        #         # self.update_msg(info.print_cart() + "收音中...")
        #         if record_reporter_stop:
        #             return

        # # t_record_reporter = Thread.Thread(target=record_reporter, args=([]))
        # # t_record_reporter.daemon = True
        # # t_record_reporter.start()
        while 1:
            tutorial =  "語音指令:\n購買: [數量]商品名稱 例：餅乾和兩張冷氣卡\n移除: 移除[數量]商品名稱\n取消並離開: 取消\n清空購物車: 清空\n結帳: 結帳\n\n"
            cart = info.print_cart()
            print("cart : ", cart)
            msg_wrapper[0] = tutorial +  cart + "你好!\n請說出要購買的商品\n先說數量再說品項，例：餅乾和三張冷氣卡\n若要結帳請說結帳\n"
            self.update_msg(msg_wrapper[0])
            self.tts.say("你好!請說出要購買的商品",lang='zh')
            # record_reporter_sem.release() # tell record_reporter it's about to record
            try:
                audio = (self.stt.record(timeout=5, logger=self.update_msg, msg=tutorial+cart)) # 20s to timeout)
                # #DEBUG BEGIN
                # while 1:
                #     try:
                #         audio = (self.stt.from_file(input())) # from file
                #         break
                #     except:
                #         pass
                # #DEBUG END
                self.update_msg("辨識中")
                self.tts.say("辨識中", lang='zh')
                sentence = ""
                err, sentence = self.stt.recognize(audio)
                print("sentence: ", sentence)
                if err[0]==1:
                    self.tts.say("Google Speech Recognition could not understand audio", lang='en')
                elif err[0]==2:
                    self.tts.say("No response from Google Speech Recognition service: {0}", lang='en')
                else:
                    if("取消" in sentence):
                        raise Exception("Transaction canceled.")
                    elif("清空購物車" in sentence):
                        info.reset()
                    elif("移除" in sentence):
                        info.cart_remove(info.parse_shopping_list(sentence))
                    else:
                        info.cart_add(info.parse_shopping_list(sentence))
                cart = info.print_cart()
                if("結帳" in sentence):
                    self.update_msg(cart)
                    info = self.check_stock(info)
                    if self.ensure_checkout(info):
                        break

            except sr.WaitTimeoutError as e:
                # Timeout! Let's check if customer is still there.
                print(str(e))
                self.face_detector_switch(True)
                if not self.check_presence():
                    time.sleep(0.5)
                    if not self.check_presence():
                        # customer leave
                        self.face_detector_switch(False)
                        raise Exception("Customer left.")
                self.face_detector_switch(False)
                pass
        return info

    def check_stock(self, info: Info):
        cart_d = collections.defaultdict(int)
        for name, num in info.cart.items():
            if len(self.stock[name]) < num:
                cart_d[name] = len(self.stock[name])
        info.cart.update(cart_d)
        
        return info

    def ensure_checkout(self, info: Info) ->bool:
        print("stop")
        # print("確定要結帳嗎?", "確定要結帳嗎? (是/否)\n"+info.print_cart()+"內容可能因實際存貨而有變動\n")
        while 1:
            err, sentence = self.ask("確定要結帳嗎?", "確定要結帳嗎? (確定/取消)\n"+info.print_cart()+"內容可能因實際存貨而有變動\n")
            if err[0]==1:
                self.tts.say("Google Speech Recognition could not understand audio", lang='en')
                continue
            elif err[0]==2:
                self.tts.say("No response from Google Speech Recognition service: {0}", lang='en')
                continue
            for keyword in ["確定","是"]:
                if keyword in sentence:
                    return True
            for keyword in ["取消","否"]:
                if keyword in sentence:
                    return True

    def ask(self, question, display_text="")->Info:
        while 1:
            self.tts.say(question)
            self.update_msg(display_text)
            try:
                audio = (self.stt.record(timeout=5, logger=self.update_msg, msg=tutorial+cart)) # 20s to timeout)
                # #DEBUG BEGIN
                # while 1:
                #     try:
                #         audio = (self.stt.from_file(input())) # from file
                #         break
                #     except:
                #         pass
                # #DEBUG END
                
                self.update_msg("辨識中")
                # self.tts.say("辨識中", lang='zh')
                sentence = ""
                err, sentence = self.stt.recognize(audio)
                return err, sentence
            except sr.WaitTimeoutError as e:
                # Timeout! Let's check if customer is still there.
                print(str(e))
                self.face_detector_switch(True)
                if not self.check_presence():
                    time.sleep(0.5)
                    if not self.check_presence():
                        # customer leave
                        self.face_detector_switch(False)
                        raise Exception("Customer left.")
                self.face_detector_switch(False)
                pass
