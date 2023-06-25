# Application main
# This file borrows some architecture from the https://github.com/MZachmann/PicoPendant main.py,
# but is heavily modified to fit the needs of this project and bears little resemblance to the original
from input.am2302 import Am2302
import uasyncio as asyncio
from util.globalStorage import GlobalObjects
from input.brightnessButton import DesiredBrightnessButton
from input.displayModeButton import DesiredDisplayButton
from util.wifiTime import set_time
import time
import random

# Returns true if the current hour is different from the last hour
def is_new_hour(current_time, last_time):
    return current_time[3] != last_time[3]

# Returns an offset value of temperature and humidity for generating an initial illustrative graph
def get_offset_value(median, range_size, deviation_size, hour):
    floor = median - (range_size / 2)
    range_middle = median
    actual_floor = median - (range_size / 2)
    offset_value = actual_floor + ((hour * range_size) / 24)
    return offset_value

# Initialize the history dictionary with 24 hours of data (50/0 represents bottom of graph)
def init_history_dict():
    history_dict = {}
    boot_hour = time.localtime()[3]
    start_hour = 0
    
    # apply offset (why does it need -1 and not +1? review logic)
    if boot_hour == 0:
        start_hour = 23
    else:
        start_hour = boot_hour - 1
    
    median_temp = 75
    median_hum = 50
    
    for hour in range(24):
        temperature = get_offset_value(75, 50, 10, hour)
        humidity = get_offset_value(50, 100, 10, hour)
        if start_hour == 23:
            start_hour = 0
        else:
            start_hour += 1

        history_dict[hour] = {"temperature": temperature, "humidity": humidity, "hour": start_hour}
    return history_dict

# Shift the history dictionary one hour to the left
def shift_history_dict(history_dict):
    for hour in range(0, 23):
        history_dict[hour] = history_dict[hour + 1]
    return history_dict

# Store the current reading in the history dictionary
def store_hourly_reading(history_dict, temperature, humidity, hour):
    history_dict = shift_history_dict(history_dict)
    history_dict[23] = {"temperature": temperature, "humidity": humidity, "hour": hour}
    return history_dict


# Initialize the global storage
storage = GlobalObjects()
storage.Initialize()

set_time()


# Import the global objects
from fonts import fontCache
from output.lcdDriver import GlobalLcd
from output.lcdViewManager import LcdViewManager

# Initialize the sensor, LCD, and buttons
sensor = Am2302(2)
lcd_driver_controller = GlobalLcd()
lcd_driver_controller.set_brightness(50)
display_button = DesiredDisplayButton(7, True)
brightness_button = DesiredBrightnessButton(4, lcd_driver_controller, True)

# Initialize the LCD view manager
lcd_view_manager = LcdViewManager(sensor, display_button, lcd_driver_controller)

# Occupy the font cache
fontCache.FontCache().OccupyFontCache(GlobalObjects(), GlobalLcd())

# Clear the screen w/black
lcd_driver_controller.draw_filled_box(0, 0, GlobalLcd().displayWidth, GlobalLcd().displayHeight, 0x0000)

# Initialize the last hour
last_hour = time.localtime()[3] - 1

# Entry to main loop
async def main():
    global last_hour

    # Start the reading screen loop
    asyncio.create_task(lcd_view_manager.refresh_reading_screen())

    # Initialize the history dictionary
    history_dict = init_history_dict()

    # Main loop
    while True:
        current_hour = time.localtime()[3]

        # If the hour has changed, store the current reading in the history dictionary
        if last_hour != current_hour:
            print("Storing hourly reading")
            reading = sensor.last_reading
            history_dict = store_hourly_reading(history_dict, reading["temperature"], reading["humidity"], current_hour)
            last_hour = current_hour

        # If the display button is pressed, switch to the graph screen
        if display_button.ButtonClicked:
            lcd_driver_controller.draw_filled_box(0, 0, GlobalLcd().displayWidth, GlobalLcd().displayHeight, 0x0000)
            await lcd_view_manager.switch_to_graph_screen(history_dict)

        await asyncio.sleep(0.1)

# Run the main loop
asyncio.run(main())

