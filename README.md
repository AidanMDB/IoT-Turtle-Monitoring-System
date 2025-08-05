# IoT-Turtle-Monitoring-System

Used a Raspberry Pi Pico W to collect sensor readings and communicate them over wi-fi to personal server using MQTT protocol.

# Micropython Flow Chart
 ________
|       ↓
|    Boot Up
|    Connect to Wi-Fi
|    Collect sensor readings
|    Connect to MQTT broker and send data
|    deepsleep for 5 minutes     
|_______|


personal dashboard for viewing data can be found here (work in progress)
https://github.com/AidanMDB/turtle_iot_project 


Written in MicroPython this system reads data from
 - DHT11 for air temperature and humidity
 - Adafruit LTR390 for UV and ambient light
 - DS18B20 for water temperature.

Plans to add in a liquid level sensor for measuring amount of evaporation




The adafruit LTR390 does not have a built in micropython module so I used code from here
https://forums.pimoroni.com/t/ltr390-micropython-code/22314 
With some personal modifications to get it working better. My modified code is listed in this respository as well.




# Personal Reminders
for micropython press the run button at the bottom to test code
to actually flash to controller use ctrl+shift+P -> Micropico: upload file to raspberry pi