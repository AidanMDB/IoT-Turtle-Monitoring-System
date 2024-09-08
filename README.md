# IoT-Turtle-Monitoring-System

Used a Raspberry Pi Pico W to get sensor readings and send them over Wi-Fi to Thingspeak.

ThingSpeak is a cloud based data collection service with free tiers for personal projects and home labs.
https://thingspeak.com/ 

Written in MicroPython this system reads data from
 - DHT11 for air temperature and humidity
 - Adafruit LTR390 for UV and ambient light
 - DS18B20 for water temperature.

Have plans to add in an ultrasonic distance sensor for measuring the level of water in the tank.

The adafruit LTR390 does not have a built in micropython module so I used code from here
https://forums.pimoroni.com/t/ltr390-micropython-code/22314 
With some personal modifications to get it working better. My modified code is listed in this respository as well.
