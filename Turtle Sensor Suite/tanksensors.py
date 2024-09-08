from picozero import pico_led
import time
import math
from machine import Pin, I2C
from uvSensor import LTR390
from dht import DHT11
import onewire, ds18x20
import network
import urequests

ssid = ""
password = ""
api_key = ''
base_url = 'https://api.thingspeak.com/update'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid)
while wlan.isconnected() == False:
    print("waiting connection")
    time.sleep(1)


lightSensor = LTR390()
airSensor = DHT11(Pin(28))

data = Pin(22)
waterSensor = ds18x20.DS18X20(onewire.OneWire(data))
roms = waterSensor.scan()	#gives list of all onewire devices

pico_led.on()

try:
    while True:
        waterSensor.convert_temp()	# must wait minimum 750ms to read temp
        time.sleep(30)
        airSensor.measure()
        waterTemp = (waterSensor.read_temp(roms[0]) * 9/5) + 32
        airTemp = (airSensor.temperature() * 9/5) + 32
        humidity = airSensor.humidity()
        uvs = lightSensor.UVS()
        als = lightSensor.ALS()
        '''
        print(f'Water Temp: {waterTemp}')
        print(f'Air Temp: {airTemp}')
        print(f'Humidity: {humidity}')
        print(f'UVS: {uvs}')
        print(f'ALS: {als}')
        '''
        url = f"{base_url}?api_key={api_key}&field1={airTemp}&field2={humidity}&field3={waterTemp}&field4={uvs}&field5={als}&field6={10}"
        response = urequests.get(url)
        print(response.text)
        
except KeyboardInterrupt:
    pico_led.off()