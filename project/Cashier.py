#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
#    Copyright 2018 Daniel Perron
#
#    Base on Mario Gomez <mario.gomez@teubi.co>   MFRC522-Python
#
#    This file use part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software:
#    you can redistribute it and/or modify
#    it under the terms of
#    the GNU Lesser General Public License as published by the
#    Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the
#    GNU Lesser General Public License along with MFRC522-Python.
#    If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import mfrc522
import signal 
import time 
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class mem ():
    def __init__(self, token, money):
        self.token = token
        self.money= money

class Cashier:
    def __init__(self, price_sheet):
        # google sheet inform
        self.auth_json_path = 'key.json'
        self.gss_scopes = ['https://spreadsheets.google.com/feeds']

        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.auth_json_path,self.gss_scopes)
        self.gss_client = gspread.authorize(self.credentials)

        self.spreadsheet_key = '1J_Ewl_8pN9WMkNEL1Evb8mC-yTMYnO26lgW10GJWWL4' 

        self.sheet = self.gss_client.open_by_key(self.spreadsheet_key).sheet1

        # Hook the SIGINT
        signal.signal(signal.SIGINT, self.end_read)

        # Create an object of the class MFRC522
        self.MIFAREReader = MFRC522.MFRC522()

        self.member = {}
        self.price_sheet = price_sheet
        self.init_dollar = 1000


    # function to read uid an conver it to a string
    def uidToString(self, uid):
        mystring = ""
        for i in uid:
            mystring = format(i, '02X') + mystring
        return mystring


    # Capture SIGINT for cleanup when the script is aborted
    def end_read(self, signal, frame):
        global continue_reading
        print("Ctrl+C captured, ending read.")
        GPIO.cleanup()

        

    def lineNotifyMessage(self, token, msg):
        headers = { "Authorization": "Bearer " + token,"Content-Type" : "application/x-www-form-urlencoded" }
        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
        return r.status_code  


    def checkout(self, cart):
        # This loop keeps checking for chips.
        # If one is near it will get the UID and authenticate
        while True:

            # Scan for cards
            (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status == self.MIFAREReader.MI_OK:
                print ("Card detected")

                # Get the UID of the card
                (status, uid) = self.MIFAREReader.MFRC522_SelectTagSN()
                # If we have the UID, continue
                if status == self.MIFAREReader.MI_OK:
                    if self.uidToString(uid) in self.member:
                        temp_price = 0
                        string = ""
                        for item, num in cart:
                            if item == self.item1:
                                temp_price += num * self.price_sheet[item]
                                string += str(num) + " " + item + "\n"

                        if self.member[self.uidToString(uid)].money >= temp_price:
                            self.member[self.uidToString(uid)].money -= temp_price
                            string = "you buy:\n" + string + "total: " + str(temp_price) + " dollars\nmoney left: " + str(self.member[self.uidToString(uid)].money)
                            self.lineNotifyMessage(self.member[self.uidToString(uid)].token, string)
                        else:
                            string = "money is not enough!!!\nyou buy:\n" + string + "total: " + str(temp_price) + " dollars\nbut your money left: " + str(self.member[self.uidToString(uid)].money)
                            self.lineNotifyMessage(self.member[self.uidToString(uid)].token, string)
                        return
                    else:
                        for element in self.sheet.get_all_values():
                            if self.uidToString(uid) in element[1]:
                                self.member[self.uidToString(uid)] = mem(element[2], self.init_dollar)
                                temp_price = 0
                                string = ""
                                for item in cart:
                                    num = cart[item]
                                    temp_price += num * self.price_sheet[item]
                                    string += str(num) + " " + item + "\n"

                                if self.member[self.uidToString(uid)].money >= temp_price:
                                    self.member[self.uidToString(uid)].money -= temp_price
                                    string = "you buy:\n" + string + "total: " + str(temp_price) + " dollars\nmoney left: " + str(self.member[self.uidToString(uid)].money)
                                    self.lineNotifyMessage(self.member[self.uidToString(uid)].token, string)
                                else:
                                    string = "money is not enough!!!\nyou buy:\n" + string + "total: " + str(temp_price) + " dollars\nbut your money left: " + str(self.member[self.uidToString(uid)].money)
                                    self.lineNotifyMessage(self.member[self.uidToString(uid)].token, string)
                                return
                            
                    print("you are not member, please scan the QRCode to register, your ID is: " + str(self.uidToString(uid)))
                    return
                else:
                    print("Authentication error")

# p_sheet = {"冷氣卡": 100, "餅乾": 10}
# a = Cashier(p_sheet)
# dic = {"冷氣卡": 1, "餅乾": 1}
# a.checkout(dic)