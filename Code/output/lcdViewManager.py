# An original class which handles the management of the content of the LCD screen
from output.ioBox import IoBox
from util.globalStorage import GlobalObjects
from output.colorSet import SolidClr, get_color_for_value
from fonts.fontDrawer import FontDrawer
import uasyncio as asyncio
import time


class LcdViewManager:

    def __init__(self, sensor, display_button, lcd_driver_controller):
        self._sensor = sensor
        self._display_button = display_button
        self._oled = lcd_driver_controller
        self.lspace = 4
        self.fontArial28 = GlobalObjects()['fontArial28']
        self.fontLucida40 = GlobalObjects()['fontLucida40']
        self.fontArial11 = GlobalObjects()['fontArial11']
        self.curScreen = 1
        self.show_reading = True

    async def refresh_reading_screen(self):
        # first clear the screen before starting the loop
        self._oled.draw_filled_box(0, 0, self._oled.displayWidth, self._oled.displayHeight, 0x0000)
        
        while self.show_reading:
            print("Loading reading screen")
            self._sensor.poll_sensor()
            reading = self._sensor.last_reading
            self.render_reading_screen(reading["temperature"], reading["humidity"])
            await asyncio.sleep(3)
            
        return reading
    
    async def switch_to_graph_screen(self, history_dict):
        self.show_reading = False
        await asyncio.sleep(0.1)  # Give the reading screen loop time to exit
        self.show_graph_screen(history_dict)

        while not self._display_button.ButtonClicked:
            await asyncio.sleep(0.1)

        self.show_reading = True
        asyncio.create_task(self.refresh_reading_screen())  # Restart the reading screen loop
    
    def show_graph_screen(self, history_dict):  # Remove async and change the name
        print("Loading graph screen")
        self.render_graph_screen(history_dict)
        
    def render_reading_screen(self, temp, hum):
        # draw the time
        the_time = time.localtime()
        output_box_hour = IoBox(self._oled, self.fontArial28, 79, 24, True)
        output_box_hour.SetText("{:02d}:{:02d}".format(the_time[3], the_time[4]), SolidClr['white'], SolidClr['black'])
        output_box_hour.Draw(400, 10)
        
        # Initialize some boxes
        output_box_temp_num = IoBox(self._oled, self.fontLucida40, 168, 60, False)
        output_box_temp_symbol = IoBox(self._oled, self.fontLucida40, 42, 60, False)
        output_box_hum_num = IoBox(self._oled, self.fontLucida40, 168, 60, False)
        output_box_hum_symbol = IoBox(self._oled, self.fontLucida40, 42, 60, False)
        
        output_box_temp_label = IoBox(self._oled, self.fontArial28, 300, 48, False)
        output_box_hum_label = IoBox(self._oled, self.fontArial28, 300, 48, False)
        
        # Define some positions
        # temp
        ypos1 = 10
        xpos1 = 10
        # hum
        ypos2 = 160
        xpos2 = 10

        # Set the box text
        temp_color = get_color_for_value(temp, "temperature")
        hum_color = get_color_for_value(hum, "humidity")
        
        output_box_temp_label.SetText('Temperature', SolidClr['white'], SolidClr['black'])
        output_box_temp_num.SetText(f'{round(temp,1)}', temp_color, SolidClr['black'])
        output_box_temp_symbol.SetText(f'F', temp_color, SolidClr['black'])
        
        output_box_hum_label.SetText('Humidity', SolidClr['white'], SolidClr['black'])
        output_box_hum_num.SetText(f'{hum} %', hum_color, SolidClr['black'])
        output_box_hum_symbol.SetText(f'%', hum_color, SolidClr['black'])

        # Draw the boxes
        value_offset = 112
        symbol_offset = 188
        output_box_temp_label.Draw(xpos1, ypos1)
        output_box_temp_num.Draw(xpos1 + value_offset, ypos1 + 62)
        output_box_temp_symbol.Draw(xpos1 + value_offset + symbol_offset, ypos1 + 62)
        
        output_box_hum_label.Draw(xpos2, ypos2)
        output_box_hum_num.Draw(xpos2 + value_offset, ypos2 + 62)
        output_box_hum_symbol.Draw(xpos2 + value_offset + symbol_offset, ypos2 + 62)

    def render_graph_screen(self, history_dict):
        # draw the time
        the_time = time.localtime()
        output_box_hour = IoBox(self._oled, self.fontArial28, 79, 24, True)
        output_box_hour.SetText("{:02d}:{:02d}".format(the_time[3], the_time[4]), SolidClr['white'], SolidClr['black'])
        output_box_hour.Draw(400, 10)

        # Initialize some boxes
        graph_box_temp_label = IoBox(self._oled, self.fontArial28, 300, 48, False)
        graph_box_hum_label = IoBox(self._oled, self.fontArial28, 300, 48, False)

        # Set the box text
        graph_box_temp_label.SetText('Temperature', SolidClr['white'], SolidClr['black'])
        graph_box_hum_label.SetText('Humidity', SolidClr['white'], SolidClr['black'])

        # Define some positions
        # temp
        ypos1 = 10
        xpos1 = 10
        # hum
        ypos2 = 160
        xpos2 = 10

        graph_box_temp_label.Draw(xpos1, ypos1)
        graph_box_hum_label.Draw(xpos2, ypos2)

        y1 = 72
        y2 = 222
        graph_height = 58
        margin = 10
        screen_width = self._oled.displayWidth
        screen_height = self._oled.displayHeight

        # Extract temperature and humidity values from the history dictionary
        temp_values = [value["temperature"] for value in history_dict.values()]
        hum_values = [value["humidity"] for value in history_dict.values()]
        hour_values = [value["hour"] for value in history_dict.values()]

        # Calculate the graph width based on the screen width and margin
        graph_width = screen_width - 2 * margin

        # Log the data values and graph dimensions
        print(f"Temperature values: {temp_values}")
        print(f"Humidity values: {hum_values}")
        print(f"Hour values: {hour_values}")
        print(f"Graph width: {graph_width}, Graph height: {graph_height}")

        # Normalize data to fit in the graph height
        temp_range = 100 - 50
        hum_range = 100 - 0
        temp_vals_normalized = [int((val - 50) / temp_range * graph_height) for val in temp_values]
        hum_vals_normalized = [int(val / hum_range * graph_height) for val in hum_values]

        # Log the normalized data values
        print(f"Data1 normalized: {temp_vals_normalized}")
        print(f"Data2 normalized: {hum_vals_normalized}")
        
        initial_graph_x_margin = 5
        
        # Draw the first graph lines
        for i in range(1, len(temp_vals_normalized)):
            x0 = margin + int((i - 1) * graph_width / len(temp_values)) + initial_graph_x_margin
            x1 = margin + int(i * graph_width / len(temp_values)) + initial_graph_x_margin
            y0 = y1 + graph_height - temp_vals_normalized[i - 1]
            y1_new = y1 + graph_height - temp_vals_normalized[i]

            color = get_color_for_value(temp_values[i], "temperature")
            self._oled.draw_line(x0, y0, x1, y1_new, color, SolidClr['black'])

            # Log the coordinates for each line segment
            print(f"Graph 1 - Line {i}: ({x0}, {y0}) to ({x1}, {y1_new})")

        # Draw the second graph lines
        for i in range(1, len(hum_vals_normalized)):
            x0 = margin + int((i - 1) * graph_width / len(hum_values)) + initial_graph_x_margin
            x1 = margin + int(i * graph_width / len(hum_values)) + initial_graph_x_margin
            y0 = y2 + graph_height - hum_vals_normalized[i - 1]
            y2_new = y2 + graph_height - hum_vals_normalized[i]

            color = get_color_for_value(hum_values[i], "humidity")
            self._oled.draw_line(x0, y0, x1, y2_new, color, SolidClr['black'])

            # Log the coordinates for each line segment
            print(f"Graph 2 - Line {i}: ({x0}, {y0}) to ({x1}, {y2_new})")

        # Draw vertical lines at each point
        def draw_graph_elements(y, graph_height, graph_width, data_values, margin):
            for i in range(len(data_values)):
                # draw vertical lines
                x = margin + int(i * graph_width / len(data_values)) + initial_graph_x_margin
                self._oled.draw_line(x, y, x, y + graph_height, SolidClr['white'], SolidClr['black'])
                
                # draw numbers (every other starting on 0th index, for space)
                if i % 2 is 0:
                    output_box_temp = IoBox(self._oled, self.fontArial11, 24, 24, True)
                    output_box_temp.SetText(f'{hour_values[i]}', SolidClr['white'], SolidClr['black'])
                    if hour_values[i] < 10:
                        output_box_temp.Draw(x - 5, y + graph_height + 5)
                    else:
                        output_box_temp.Draw(x - 8, y + graph_height + 5)
                

        draw_graph_elements(y1, graph_height, graph_width, hour_values, margin)
        draw_graph_elements(y2, graph_height, graph_width, hour_values, margin)
        
        # draw temp scale
        output_tempscale_top = IoBox(self._oled, self.fontArial11, 20, 20, True)
        output_tempscale_top.SetText('50', SolidClr['white'], SolidClr['black'])
        output_tempscale_top.Draw(460, y1 + graph_height - 10)
        
        output_tempscale_top = IoBox(self._oled, self.fontArial11, 20, 20, True)
        output_tempscale_top.SetText('F', SolidClr['white'], SolidClr['black'])
        output_tempscale_top.Draw(460, y1 + ((graph_height - 10) / 2))
        
        output_tempscale_bot = IoBox(self._oled, self.fontArial11, 20, 20, True)
        output_tempscale_bot.SetText('99', SolidClr['white'], SolidClr['black'])
        output_tempscale_bot.Draw(460, y1)
        
        # draw hum scale
        output_humscale_top = IoBox(self._oled, self.fontArial11, 20, 20, True)
        output_humscale_top.SetText('0', SolidClr['white'], SolidClr['black'])
        output_humscale_top.Draw(460, y2 + graph_height - 10)
        
        output_tempscale_top = IoBox(self._oled, self.fontArial11, 20, 20, True)
        output_tempscale_top.SetText('%', SolidClr['white'], SolidClr['black'])
        output_tempscale_top.Draw(460, y2 + ((graph_height - 10) / 2))
        
        output_humscale_bot = IoBox(self._oled, self.fontArial11, 20, 20, True)
        output_humscale_bot.SetText('99', SolidClr['white'], SolidClr['black'])
        output_humscale_bot.Draw(460, y2)

    # Test boot animation
    def boot_animation():
        w = 480
        h = 320
        color = 0x07E0

        w_cur = 0
        h_cur = 0

        while (h_cur + 20) <= h:
            while (w_cur + 20) <= w:
                oled.draw_filled_box(w_cur, h_cur, 20, 20, color)
                w_cur = w_cur + 20
                if color == 0x07E0:
                    color = 0x5800
                else:
                    color = 0x07E0
                print(f'w_cur: {w_cur}, h_cur: {h_cur}')
            h_cur = h_cur + 20
            w_cur = 0
            if color == 0x07E0:
                color = 0x5800
            else:
                color = 0x07E0
            print(f'w_cur: {w_cur}, h_cur: {h_cur}')

