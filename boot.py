#-------------------------
#smartmeter Programm for the esp32 
#programm by: lars jelschen
#-------------------------

#import the needed libraries
from machine import UART
from machine import Pin
import time
import network
import socket
import urequests as requests
import json


#settings
#---------WIFI----------------
SSID = "WIFI NAME"
PASS = "WIFI PASS"
#---------Homeassistant----------------
SENSOR_NAME = "house"
HA_IP = ""
HA_TOKEN = ""
#---------UART----------------
TX = 32
RX = 33

#connect to the wifi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(SSID, PASS)
p2 = Pin(2, Pin.OUT)

#wait for the connection
while not sta_if.isconnected():
    time.sleep(0.5)
    

#show the ip
print(sta_if.ifconfig())
p2.off()

#update the value in homeassistant
def updateValue(variable, typ, value):
    #connect to the api of homeassistant
    url = f"http://{HA_IP}/api/states/{variable}"
    headers = {
        "Authorization":f"Bearer {HA_TOKEN}",
        "content-type": "application/json",
    }
    try:
        if typ:
            #convert the value to the right format
            val = float(str(value).replace("'",'').split(' ')[0])
            response = requests.post(url, headers=headers, json={"state": val, "attributes":{"state_class":"total_increasing","unit_of_measurement":"kWh","device_class":"energy","icon":"mdi:calendar-clock"}})
            response.close()
        else:
            #convert the value to the right format
            val = float(str(value).replace("'",'').split(' ')[0])*1000
            response = requests.post(url, headers=headers, json={"state": val, "attributes":{"state_class":"measurement","unit_of_measurement":"W","device_class":"power","icon":"mdi:gauge"} })
            response.close()
        print(f"update: {variable} with {val} | status {response.status_code}")
    except Exception as e:
        print("could not update value")
        print(str(e))

   




while True:
    #connect to the uart
    ser = UART(1,300, parity=0, bits=7, timeout=1, rx=RX, tx=TX, stop=1)
    print("reading...")
    p2.on()
    #send the request to the uart
    ser.write(b"/?!\x0D\x0A")
    time.sleep(1)


    endline = 0
    power = ""
    powermeter_count = ""
    startTime = time.time()
    isPowerMeter = False
    while True:
        if (time.time() - startTime) >= 20:
            break
            
        line = ser.readline()
        if line.__class__.__name__ != "NoneType":
            #powermeter found
            if b'5MT174-0001\r\n' in line:
                time.sleep(1)
                print("powermeter found")
                p2.off()
                isPowerMeter = True

                #change the baudrate
                ser.write(b"\x06050\x0D\x0A")
                print("change baudrate")
                time.sleep(0.5)
                #ser.write(b"\x06050\x0D\x0A")
                #print("change b audrate")
                ser = UART(1,9600, parity=0, bits=7, timeout=1, rx=32, tx=33, stop=1)
            if b'1-0:1.7.0*255' in line:
                power = str(line).split('(')[1]
                power = power.split('*')[0]
            if b'1-0:1.8.0*255' in line:
                powermeter_count = str(line).split('(')[1]
                powermeter_count = powermeter_count.split('*')[0]
            if b'53.5*255' in line or b'1.8.4*15' in line:
                break

    
    if isPowerMeter:
        updateValue("sensor.house_power", False, power)
        time.sleep(1)
        updateValue("sensor.house_powermeter_count", True, powermeter_count)
        time.sleep(1)

        print("end")
        time.sleep(10)
    else:
        p2.off()
        time.sleep(2.5)
        print("no powermeter found")
