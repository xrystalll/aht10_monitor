from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from aht10 import AHT10
import sys, time

SDA = Pin(10)
SCL = Pin(11)
AHT_ADDRESS = 0x38
ENTER_BTN = Pin(16, Pin.IN, Pin.PULL_DOWN)
DOWN_BTN = Pin(17, Pin.IN, Pin.PULL_DOWN)

pix_res_x = 128 # horizontal resolution
pix_res_y = 32  # vertical resolution

i2c = I2C(1, scl = SCL, sda = SDA, freq=200000)  # start I2C on I2C1 (GPIO 10/11)
i2c_addr = [hex(i) for i in i2c.scan()] # get I2C address in hex format
if i2c_addr == []:
    print('No I2C Devices Found') 
    sys.exit() # exit routine if no dev found
else:
    print("I2C Devices      : {}".format(i2c_addr))
    print("I2C Configuration: {}".format(i2c))

display = SSD1306_I2C(pix_res_x, pix_res_y, i2c)
sensor = AHT10(i2c, 0, AHT_ADDRESS)


display.fill(0)
menu = ["Temperature", "Humidity", "About"]
height = 12
active = 1
saved_active = 1
curr_screen = 0


def draw_menu():
    global curr_screen
    curr_screen = 0
    display.fill(0)
    for i, item in enumerate(menu):
        text = ""

        if i == active - 1:
            text = ">" + item
        else:
            text = " " + item

        if i == 0:
            display.text(text, 0, 1)
        display.text(text, 0, height * i + 1)
    display.show()

draw_menu()

def temp_screen():
    display.fill(0)
    temp = sensor.temperature()
    display.text("<Back", 0, 1)
    display.text(" Temperature:", 0, height + 1)
    display.text(" {}C".format(round(temp, 1)), 0, height * 2 + 1)
    display.show()

def hum_screen():
    display.fill(0)
    hum = sensor.humidity()
    display.text("<Back", 0, 1)
    display.text(" Humidity:", 0, height + 1)
    display.text(" {}%".format(round(hum, 1)), 0, height * 2 + 1)
    display.show()

def about_screen():
    display.fill(0)
    display.text("<Back", 0, 1)
    display.text(" Home air sensor", 0, height + 1)
    display.text(" by xrystalll", 0, height * 2 + 1)
    display.show()

while True:
    if ENTER_BTN.value():
        if active == 1:
            saved_active = active
            active = 0
            curr_screen = 1
        elif active == 2:
            saved_active = active
            active = 0
            curr_screen = 2
        elif active == 3:
            saved_active = active
            active = 0
            curr_screen = 3
            about_screen()
        else:
            active = saved_active
            draw_menu()

    if DOWN_BTN.value():
        if active == 0:
            active = saved_active
        else:
            active += 1
        if active > len(menu):
            active = 1
        draw_menu()

    if curr_screen == 1:
        temp_screen()
    elif curr_screen == 2:
        hum_screen()

    time.sleep(0.25)
