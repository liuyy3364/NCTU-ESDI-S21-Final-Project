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
import MFRC522
import signal
import time 
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# google sheet inform
auth_json_path = 'key.json'
gss_scopes = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_json_path,gss_scopes)
gss_client = gspread.authorize(credentials)

spreadsheet_key = '1J_Ewl_8pN9WMkNEL1Evb8mC-yTMYnO26lgW10GJWWL4' 

sheet = gss_client.open_by_key(spreadsheet_key).sheet1


continue_reading = True


# function to read uid an conver it to a string

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = format(i, '02X') + mystring
    return mystring


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

def lineNotifyMessage(token, msg):
    headers = { "Authorization": "Bearer " + token,"Content-Type" : "application/x-www-form-urlencoded" }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

member = {}
class mem ():
    def __init__(self, token, money):
        self.token = token
        self.money= money

price1 = 5
price2 = 10
price3 = 15
price4 = 20
price = [price1, price2, price3, price4]
flag = 0
# This loop keeps checking for chips.
# If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_SelectTagSN()
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            if uidToString(uid) in member:
                num = input("number: ")
                if member[uidToString(uid)].money >= price[num - 1]:
                    member[uidToString(uid)].money -= price[num - 1]
                    lineNotifyMessage(member[uidToString(uid)].token, "buy number " + str(num) + "\nmoney left: " + str(member[uidToString(uid)].money))
                    print("get your commodity")
                else:
                    print("money is not enough")
                time.sleep(3)
                continue
            else:
                for element in sheet.get_all_values():
                    if uidToString(uid) in element[1]:
                        member[uidToString(uid)] = mem(element[2], 100)
                        num = input("number: ")
                        if member[uidToString(uid)].money >= price[num - 1]:
                            member[uidToString(uid)].money -= price[num - 1]
                            lineNotifyMessage(member[uidToString(uid)].token, "buy number " + str(num) + "\nmoney left: " + str(member[uidToString(uid)].money))
                            print("get your commodity")
                        else:
                            print("money is not enough")
                        time.sleep(3)
                        flag = 1
                        break
                if flag == 1:
                    flag = 0
                    continue
                    
            print("you are not member, please scan the QRCode to register, your ID is: " + str(uidToString(uid)))
            time.sleep(3)
        else:
            print("Authentication error")

