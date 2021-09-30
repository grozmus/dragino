#!/usr/bin/env python3
"""
    test to add a MAC command to an uplink FOpts field

    It logs the response from the server
"""
import logging
from time import sleep,time
import RPi.GPIO as GPIO
from dragino import Dragino
from dragino.LoRaWAN import new as lorawan_msg
from dragino.LoRaWAN.MHDR import MHDR

GPIO.setwarnings(False)

# add logfile
logLevel=logging.DEBUG
logging.basicConfig(filename="testMAC.log", format='%(asctime)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s', level=logLevel)


D = Dragino("dragino.toml", logging_level=logLevel)

D.join()
while not D.registered():
    sleep(0.1)

try:
    newskey=D.MAC.getNewSKey()
    appskey=D.MAC.getAppSKey()
    lorawan = lorawan_msg(newskey,appskey)

    devaddr=D.MAC.getDevAddr()
    FCntUp=D.MAC.getFCntUp()
    message=[0x00,0x01,0x02,0x04,0x05]

    # linkCheck request. Server should respond with a demodulation margin and gateway count
    # see LoRaWAN MAC specification
    # During join it is possible the server sent us a statusReq. The reply to that will be added
    # to the FOpts field

    FOpts=[0x02]+D.MAC.getFOpts() # linkCheckReq + any other replies

    lorawan.create(MHDR.UNCONF_DATA_UP, {
                'devaddr': devaddr,
                'fcnt': FCntUp,
                'data': message,
                'fport=':1,
                'fopts':FOpts})

    raw_payload=lorawan.to_raw()

    print(f"raw_payload={raw_payload}")
    logging.info(f"raw_payload={raw_payload}")
    D.send_bytes(raw_payload)

except Exception as e:
    logging.exception(f"PROBLEMO: {e}")

print("testMAC finished - check the log file")
