## MicroPython Pico Climate Monitor Application main
from input.am2302 import Am2302
from readings.readingManager import ReadingManager
import uasyncio as asyncio
from input.brightnessButton import DesiredBrightnessButton
from input.displayModeButton import DesiredDisplayButton
from util.wifiTime import WifiTime
import time
from output.lcdDriver import LcdDriver
from output.lcdViewManager import LcdViewManager
from fonts.fontManager import GlobalFontManager


# Initialization sequence
fontManager = GlobalFontManager()
sensor = Am2302(2)
reading_manager = ReadingManager(sensor)
lcd_driver_controller = LcdDriver(fontmanager=fontManager)
lcd_driver_controller.set_brightness(50)
display_button = DesiredDisplayButton(7, True)
brightness_button = DesiredBrightnessButton(4, lcd_driver_controller, True)
lcd_view_manager = LcdViewManager(reading_manager, display_button, lcd_driver_controller,fontManager)
lcd_view_manager.boot_animation()

# Attempt to set the time using the WifiTime class
try:
    wifi_time = WifiTime()
    wifi_time.Initialize()
    print("--time set successfully")
except:
    print("--failure occurred while attempting to set time")

# Clear the screen w/black
lcd_driver_controller.draw_filled_box(0, 0, lcd_driver_controller.displayWidth, lcd_driver_controller.displayHeight, 0x0000)

print("initialization complete")

# Entry to main loop
async def main():
    # Initialize last_hour with the previous hour, making sure to wrap around at midnight
    last_hour = time.localtime()[3] - 1
    if last_hour < 0:
        last_hour = 23

    # Start the reading screen task (refresh loop)
    asyncio.create_task(lcd_view_manager.refresh_reading_screen())

    # Main detection loop
    while True:
        current_hour = time.localtime()[3]

        # If the hour has changed, store the current reading in the history dictionary
        if last_hour != current_hour:
            reading_manager.log_reading()
            last_hour = current_hour

        # If the display button is pressed, switch to the graph screen
        if display_button.ButtonClicked:
            lcd_driver_controller.draw_filled_box(0, 0, lcd_driver_controller.displayWidth, lcd_driver_controller.displayHeight, 0x0000)
            await lcd_view_manager.switch_to_graph_screen(reading_manager.get_history())

        # Note, switching back to reading screen is invoked within the lcd_view_manager, due to a less-than-ideal dependency chain that
        # should be refactored in the future.

        await asyncio.sleep(0.1)

# Run the main loop
asyncio.run(main())
