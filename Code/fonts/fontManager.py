from fonts.fontReader import ParseFontFile
#from fonts.fontCache import FontCache # What is the benefit of this?
import gc

# Todo, review this code and FontCache code in more detail

def GlobalFontManager():
    global _fontManager
    return _fontManager


class FontManager(dict):
    ''' Global Data storage of loaded objects '''

    def __init__(self):
        print("Initializing")
        self.fonts = {}
        self.fontList = ['fontLucida40', 'fontArial28', 'fontArial11']
        self.LoadFontFiles()
        
        # all the really big stuff gets allocated very early...
        try:
            self.dispBuffer = bytearray(480 * 32 * 2)
        except Exception as e:
            print(str(e))
        gc.collect()
        print('memory free after output bfr = %d' % (gc.mem_free()))
        #self.fontCache.AllocateFontCache() # What is the purpose of this?

    def LoadFontFiles(self):
        print('memory free before fonts = %d' % (gc.mem_free()))
        for fName in self.fontList:
            self.fonts[fName] = ParseFontFile('fonts/' + fName + '.py')
            gc.collect()
        print('memory free after fonts = %d' % (gc.mem_free()))

_fontManager = FontManager()
