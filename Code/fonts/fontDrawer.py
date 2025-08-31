# Modified version of resource from PicoPendant. The FontDrawer 
# has been altered to draw the font at 4x the original size, to
# help in managing memory while drawing large fonts.

# an object for drawing characters created from TrueType
# given a font this creates a lookup table to the character metadata

# a simple struct to convert indexes to names
class Datum() :
    def __init__(self, value) :
        self.TheChar = value[0]     # the character number
        self.Xpos = value[1]        # the X position in the font image
        self.Width = value[2]       # the Width of the glyph in pixels
        self.Offset = value[3]      # the offset of the glyph start in the box
        self.Advance = value[4]     # amount to move after drawing

# the class that draws characters to an Oled output
# on init it creates a lookup table to the font metadata by character
class FontDrawer(object) :
    def __init__(self, font, oled ) :
        self.font = font
        self.oled = oled
        self.chartodata = { }
        numdata = len(font.info)
        for i in range(0, numdata) :
            self.chartodata[font.info[i][0]] = i
        # get N space
        self.emWidth = font.info[self.chartodata[78]][4]
        # print("We have " + str(len(font.data)) + " data points and " + str(len(self.chartodata)) + " datums.")

    # draw a single character to the output
    # this is not optimized at all
    # note theChar is an int (encode('UTF-8'))
    def DrawChar(self, theChar, xpos, ypos, colors, shrink, buffer=None):
        scale_factor = 1 if shrink else 2
        if theChar == 32:  # space character
            return self.emWidth * scale_factor
        if not theChar in self.chartodata.keys():
            print("char not found")
            return 0
        idx = self.chartodata[theChar]
        advance = 0
        if idx:
            c = Datum(self.font.info[idx])  # give the entries names
            width = c.Width
            advance = c.Advance * scale_factor
            for y in range(0, self.font.height):
                # of bits offset (width is in bytes)
                offset = c.Xpos
                starty = ypos + y * scale_factor
                # there are better ways to do this
                for x in range(0, width):
                    uoff = offset + x
                    bittwid = uoff - 8 * int(uoff / 8)
                    bitoff = int(uoff / 8) + y * self.font.width
                    bitv = (self.font.data[bitoff] & (0x80 >> bittwid)) != 0
                    if bitv:
                        startx = xpos + c.Offset * scale_factor + x * scale_factor
                        for dx in range(scale_factor):
                            for dy in range(scale_factor):
                                if buffer == None:
                                    self.oled.draw_point(startx + dx, starty + dy, colors)
                                else:
                                    buffer.pixel(startx + dx, starty + dy, colors)
                                # print('Draw char %s at (%d,%d)' % (theChar, xpos, ypos))
        return advance

    # get the actual pixel width of a string
    def GetStringWidth(self, text) :
        tbt = text.encode('UTF-8')
        total = 0
        for theChar in tbt:
            if theChar == 32 : # space character
                advance = self.emWidth
            elif not theChar in self.chartodata.keys() :
                advance = 0
            else:
                idx = self.chartodata[theChar]
                advance = 0
                if idx :
                    c = Datum(self.font.info[idx])      # give the entries names
                    advance = c.Advance
            total = total + advance
        return total

    # draw a string to the output using the metadata
    # for positioning
    def DrawString(self, text, xpos, ypos, colors, shrink, buffer = None) :
        tbt = text.encode('UTF-8')
        print(tbt)
        print(text)
        xnow = xpos
        ynow = ypos
        for chars in tbt :
            move = self.DrawChar(chars, xnow, ynow, colors, shrink, buffer = buffer)
            xnow += move            


