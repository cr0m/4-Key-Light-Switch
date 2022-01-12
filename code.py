import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import board

import time
import busio
from secrets import secrets
from adafruit_neokey.neokey1x4 import NeoKey1x4

i2c = busio.I2C(board.SCL1, board.SDA1)
neokey = NeoKey1x4(i2c, addr=0x31)

postheaders = {'Authorization': 'Bearer %s' % secrets["HAToken"]}

JSON_HA_PST_TOGGLE_URL = ("http://%s/api/services/homeassistant/toggle" % secrets["HAIPAddress"])
JSON_HA_PST_ON_URL = ("http://%s/api/services/homeassistant/turn_on" % secrets["HAIPAddress"])

button1_text = "Game Room Off"
button2_text = "Game Room White"
button3_text = "Game Room Blue"
button4_text = "Toggle Droid Cabinet"

button1_color = 0x000000
button2_color = 0xffffff # white
button3_color = 0x0000ff # blue
button4_color = 0xffb000 # yellow

samecolor = 0x00FF00
button1_off_color = samecolor
button2_off_color = samecolor
button3_off_color = samecolor
button4_off_color = samecolor

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
print("ESP32-S2 WebClient Test")

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

print("Available WiFi networks:")
for network in wifi.radio.start_scanning_networks():
    print(
        "\t%s\t\tRSSI: %d\tChannel: %d"
        % (str(network.ssid, "utf-8"), network.rssi, network.channel)
    )
wifi.radio.stop_scanning_networks()

print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4) * 1000))

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

while True:
    if neokey[0]:
        if neokey[0]:
            print(button1_text)
            neokey.pixels[0] = button1_off_color
            datatopost = '{ "entity_id": "scene.game_room_all_off" }'
            responseHA = requests.post(JSON_HA_PST_ON_URL, headers=postheaders, data=datatopost)
            # print(responseHA.text)
            time.sleep(0.01)
    else:
        neokey.pixels[0] = button1_color

    if neokey[1]:
        if neokey[1]:
            print(button2_text)
            neokey.pixels[1] = button2_off_color
            datatopost = '{ "entity_id": "scene.game_room_energize" }'
            responseHA = requests.post(JSON_HA_PST_ON_URL, headers=postheaders, data=datatopost)
            time.sleep(0.01)
    else:
        neokey.pixels[1] = button2_color

    if neokey[2]:

        if neokey[2]:
            print(button3_text)
            neokey.pixels[2] = button3_off_color
            datatopost = '{ "entity_id": "scene.game_room_bluedim" }'
            responseHA = requests.post(JSON_HA_PST_ON_URL, headers=postheaders, data=datatopost)
            time.sleep(0.01)
    else:
        neokey.pixels[2] = button3_color

    if neokey[3]:
        if neokey[3]:
            print(button4_text)
            neokey.pixels[3] = button4_off_color
            datatopost = '{ "entity_id": "switch.droid_case" }'
            responseHA = requests.post(JSON_HA_PST_TOGGLE_URL, headers=postheaders, data=datatopost)
            time.sleep(0.01)
    else:
        neokey.pixels[3] = button4_color

