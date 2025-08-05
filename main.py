# microcontroller imports
from machine import Pin, unique_id, deepsleep
from utime import sleep
from time import sleep_ms
from ubinascii import hexlify

# sensor importd
from uvSensor import LTR390
from dht import DHT11
import onewire
import ds18x20

# network imports
import env
import network
from mqtt import MQTTClient

SLEEP_TIME = 5

water_temp_F = 0
air_temp_F = 0
humidity = 0
lux = 0
uv = 0

led = Pin("LED", Pin.OUT)
light_sensor = LTR390()
air_sensor = DHT11(Pin(28))

onewire_bus = onewire.OneWire(Pin(27))
water_sensor = ds18x20.DS18X20(onewire_bus)
rom_codes = onewire_bus.scan()

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # print('firmware')
    # sleep(1)      # let wifi firmware finish init
    wlan.connect(env.WIFI_SSID, env.WIFI_PASSWORD)
    attempts = 0
    print('connecting')
    while wlan.isconnected() == False and attempts < 20:
        attempts += 1
        print(f"Connection attempt: {attempts}/10")
        sleep(1)



# collect data from sensors
def gather_data():
    global water_temp_F, air_temp_F, humidity, uv, lux

    water_sensor.convert_temp()
    sleep_ms(750)
    water_temp_F = ( water_sensor.read_temp(rom_codes[0]) * 9.0/5 ) + 32

    air_sensor.measure()
    air_temp_F = ( air_sensor.temperature() * 9.0/5 ) + 32
    humidity = air_sensor.humidity()

    uv = light_sensor.UVS()
    lux = light_sensor.ALS()

    print(f"water temp: {water_temp_F:.2f}, air temp: {air_temp_F:.2F}, humidity: {humidity:.2}, UV: {uv:.2}, Lux: {lux:.2}")


# callback from mqtt
def msg_callback(topic, msg):
    #print('msg received')
    pass



# send collected data with mqtt
def mqtt_send_data():
    client = MQTTClient(hexlify(unique_id()), env.MQTT_BROKER_IP, user=env.MQTT_USERNAME, password=env.MQTT_PASSWD)
    client.set_callback(msg_callback)

    try: 
        client.connect()
        client.subscribe(env.MQTT_TOPIC)
        # client.publish(env.MQTT_TOPIC, b'{hello, my, world }')
        global water_temp_F, air_temp_F, humidity, uv, lux
        msg = f"{{\"wt\":{water_temp_F:.2f},\"at\":{air_temp_F:.2f},\"h\":{humidity:.2f},\"uv\":{uv:.2f},\"l\":{lux:.2f}}}"
        client.publish(env.MQTT_TOPIC, msg)
        client.disconnect()
    except Exception as e:
        print(f"Failed to send {e}")






while 1:
    led.on()
    connect_wifi()
    gather_data()
    mqtt_send_data()
    led.off()
    #sleep(10)
    deepsleep( SLEEP_TIME * 60 * 1000)