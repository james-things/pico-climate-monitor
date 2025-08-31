# color is 5-6-5 stored

DarkTheme = {
    'background': 0x04,
    'foreground': 0x7fff,
    'highlight': 0x0088
}

LightTheme = {
    'background': 0x07,
    'foreground': 0x7fff,
    'highlight': 0x1ff0
}

SolidClr = {
    'red': 0x07e0,
    'green': 0x001f,
    'lightblue': 0x000f,
    'blue': 0xf800,
    'darkblue': 0x0e00,
    'white': 0xffff,
    'yellow': 0x07ff,
    'dkyellow': 0x0088,
    'black': 0x0000,
    'gray': 0x1863,
    'darkred': 0x01e0,
    'darkgreen': 0x04,
    'orange': 0x00F8,
    'lightgreen': 0x008F,
    'forestgreen': 0x0068
}

# function to get color by value for sensor readings
def get_color_for_value(value, value_type):
    value = int(float(value))
    if value_type == "temperature":
        if value < 60:
            return SolidClr['lightblue']
        elif 60 <= value < 72:
            return SolidClr['green']
        elif 72 <= value < 80:
            return SolidClr['yellow']
        elif 80 <= value < 90:
            return SolidClr['orange']
        else:
            return SolidClr['red']
    elif value_type == "humidity":
        if value < 20:
            return SolidClr['red']
        elif 20 <= value < 40:
            return SolidClr['orange']
        elif 40 <= value < 60:
            return SolidClr['yellow']
        elif 60 <= value < 80:
            return SolidClr['green']
        else:
            return SolidClr['lightblue']
