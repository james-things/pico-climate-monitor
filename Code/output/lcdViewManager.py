# An original class which handles the management of the content of the LCD screen
from output.ioBox import IoBox
from output.colorSet import SolidClr, get_color_for_value
import uasyncio as asyncio
import time


class LcdViewManager:

    def __init__(self, reading_manager, display_button, lcd_driver_controller, font_manager):
        self._font_manager = font_manager
        self._reading_manager = reading_manager
        self._display_button = display_button
        self._oled = lcd_driver_controller
        self.lspace = 4
        self.fontArial28 = self._font_manager.fonts['fontArial28']
        self.fontLucida40 = self._font_manager.fonts['fontLucida40']
        self.fontArial11 = self._font_manager.fonts['fontArial11']
        self.curScreen = 1
        self.show_reading = True

    async def refresh_reading_screen(self):
        # first clear the screen before starting the loop
        self._oled.draw_filled_box(0, 0, self._oled.displayWidth, self._oled.displayHeight, 0x0000)
        
        while self.show_reading:
            reading = self._reading_manager.get_new_reading()
            self.render_reading_screen(reading["temperature"], reading["humidity"])
            await asyncio.sleep(5)
            
        return reading
    
    def render_reading_screen(self, temp, hum):
        temp = "{:.1f}".format(temp)
        hum = "{:.1f}".format(hum)
        # draw the time
        the_time = time.localtime()
        output_box_hour = IoBox(self._oled, self.fontArial28, 79, 24, True)
        output_box_hour.SetText("{:02d}:{:02d}".format(the_time[3], the_time[4]), SolidClr['white'], SolidClr['black'])
        output_box_hour.Draw(400, 10)
        
        temp = float(temp)
        hum = float(hum)
        
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
        output_box_temp_num.SetText(f'{temp}', temp_color, SolidClr['black'])
        output_box_temp_symbol.SetText(f'F', temp_color, SolidClr['black'])
        
        output_box_hum_label.SetText('Humidity', SolidClr['white'], SolidClr['black'])
        output_box_hum_num.SetText(f'{hum}', hum_color, SolidClr['black'])
        output_box_hum_symbol.SetText(f'%', hum_color, SolidClr['black'])

        # Draw the boxes
        value_xoffset = 112
        symbol_xoffset = 188
        yoffset = 62
        output_box_temp_label.Draw(xpos1, ypos1)
        print("debug A")
        output_box_temp_num.Draw(xpos1 + value_xoffset, ypos1 + yoffset)
        print("debug B")
        output_box_temp_symbol.Draw(xpos1 + value_xoffset + symbol_xoffset, ypos1 + yoffset)
        
        output_box_hum_label.Draw(xpos2, ypos2)
        output_box_hum_num.Draw(xpos2 + value_xoffset, ypos2 + yoffset)
        output_box_hum_symbol.Draw(xpos2 + value_xoffset + symbol_xoffset, ypos2 + yoffset)
    
    async def switch_to_graph_screen(self, reading_array):
        self.show_reading = False
        await asyncio.sleep(0.1)  # Give the reading screen loop time to exit
        self.render_graph_screen(reading_array)

        while not self._display_button.ButtonClicked:
            await asyncio.sleep(0.1)

        self.show_reading = True
        asyncio.create_task(self.refresh_reading_screen())  # Restart the reading screen loop
        
    # Draw vertical lines at each point
    def draw_graph_elements(self, y, graph_height, graph_width, data_values, margin, initial_graph_x_margin):
        for i in range(len(data_values)):
            # draw vertical lines
            x = margin + int(i * graph_width / len(data_values)) + initial_graph_x_margin
            self._oled.draw_line(x, y, x, y + graph_height, SolidClr['white'], SolidClr['black'])
            
            # draw numbers (every other starting on 0th index, for space)
            if i % 2 is 0:
                output_box_temp = IoBox(self._oled, self.fontArial11, 24, 24, True)
                output_box_temp.SetText(f'{data_values[i]}', SolidClr['white'], SolidClr['black'])
                if data_values[i] < 10:
                    output_box_temp.Draw(x - 5, y + graph_height + 5)
                else:
                    output_box_temp.Draw(x - 8, y + graph_height + 5)

    def render_graph_screen(self, reading_array):
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
        # screen_height = self._oled.displayHeight

        # Extract temperature and humidity values from the history dictionary
        temp_values = [value["temperature"] for value in reading_array]
        hum_values = [value["humidity"] for value in reading_array]
        hour_values = [value["hour"] for value in reading_array]
         # Fill missing hours so hour_values always represents a 24-hour time-scale (0-23)
        missing_count = 24 - len(hour_values)
        last_hour = hour_values[-1] if hour_values else -1
        for i in range(missing_count):
            hour_values.append((last_hour + i + 1) % 24)
    
        # Check if less than 24 hours were logged; if so, append dummy values for
        # as many hours as necessary. Values: temperature=75, humidity=50
        while len(temp_values) < 24:
            temp_values.append(75)
            hum_values.append(50)
           
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

        self.draw_graph_elements(y1, graph_height, graph_width, hour_values, margin, initial_graph_x_margin)
        self.draw_graph_elements(y2, graph_height, graph_width, hour_values, margin, initial_graph_x_margin)

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
    def boot_animation(self):
        self.display_boot_animation('A')
    
    # Experimental animation, no purpose
    def display_boot_animation(self, variant):
        w = 480
        h = 320
        color = 0x07E0 if variant is 'A' else 0x5800

        w_cur = 0 #if variant is 'A' else w - 20
        h_cur = 0 #if variant is 'A' else h - 20

        while (h_cur + 20) <= h:
            while (w_cur + 20) <= w:
                self._oled.draw_filled_box(w_cur, h_cur, 20, 20, color)
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
        
