# application globals
#               MZ Jan 2023
#
# The GlobalObjects dictionary contains loaded and cached stuff but not serialized
#		GlobalObjects() - the set of fonts, and caches
#
# A heavily slimmed-down version of the GlobalPico class from
# https://github.com/MZachmann/PicoPendant
from fonts.fontReader import ParseFontFile
#from fonts.fontCache import FontCache
import gc

# local file name
JsonFile = 'config.json'


def GlobalObjects():
    global _GlobalObjects
    return _GlobalObjects


class PicoObjects(dict):
    ''' Global Data storage of loaded objects '''

    def Initialize(self):
        print("Initializing")
        self['fontList'] = ['fontLucida40', 'fontArial28','fontArial11']
        self.LoadFontFiles()
        # all the really big stuff gets allocated very early...
        try:
            self['dispBuffer'] = bytearray(480 * 32 * 2)
        except Exception as e:
            print(str(e))
        gc.collect()
        print('memory free after output bfr = %d' % (gc.mem_free()))
        #FontCache().AllocateFontCache()

    def LoadFontFiles(self):
        print('memory free before fonts = %d' % (gc.mem_free()))
        for fName in self['fontList']:
            self[fName] = ParseFontFile('fonts/' + fName + '.py')
            gc.collect()
        print('memory free after fonts = %d' % (gc.mem_free()))


_GlobalObjects = PicoObjects()

