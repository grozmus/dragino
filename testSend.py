#!/usr/bin/env python3
"""
    Test harness for dragino module - sends hello world out over LoRaWAN 5 times
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
logging.basicConfig(filename="testSend.log", format='%(asctime)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s', level=logLevel)


D = Dragino("dragino.toml", logging_level=logLevel)


try:
    newskey=D.MAC.getNewSKey()
    appskey=D.MAC.getAppSKey()
    lorawan = lorawan_msg(newskey,appskey)

    devaddr=D.MAC.getDevAddr()
    FCntUp=D.MAC.getFCntUp()
    message=[0x00,0x01,0x02,0x04,0x05]

  # get any MAC replies/requests to piggy back on this uplink
    FOpts,FOptsLen= [0x01],1 #D.MAC.getFOpts() # can be an empty bytearray
  

    lorawan.create(MHDR.UNCONF_DATA_UP, {
                'devaddr': devaddr, 
                'fcnt': FCntUp, 
                'data': message,
                'fport=':1,
                'fopts':FOpts})
    
        
    
    # get any MAC replies/requests to piggy back on this uplink
    #FOpts,FOptsLen= bytearray([0x01]),1 #D.MAC.getFOpts() # can be an empty bytearray
            
    #if FOptsLen>0:
        # add the MAC replies FOptsLen is set by this call (see FHDR.py)
    #    lorawan.fhdr().set_fopts(FOpts)    # MAC replies

    lorawan.mac_payload.set_fport(1)

    raw_payload=lorawan.to_raw()

    print(f"raw_payload={raw_payload}")
    logging.info(f"raw_payload={raw_payload}")

except Exception as e:
    logging.exception(f"PROBLEMO: {e}") 
