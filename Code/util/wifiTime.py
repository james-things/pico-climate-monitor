import network
import socket
import time
import struct
import machine

NTP_DELTA = 2208988800
host = "pool.ntp.org"

# Add your values
val = ['<wifi_ssid>', '<wifi_password>'] 

class WifiTime():

    def Initialize(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(val[0], val[1])
        #wlan.connect(self.deob_str(val[0]), self.deob_str(val[1])) # Example

        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)

        if wlan.status() != 3:
            # raise RuntimeError('network connection failed')
            print('network connection failed')
            self.set_dummy_time()
        else:
            print('connected')
            status = wlan.ifconfig()
            print('ip = ' + status[0])
            self.set_time()
            print(time.localtime())
    
    def deob_str(self, input_string): # Example
        result = ""
        length = len(input_string)
        
        for char in input_string:
            # Increment the ASCII value of the character by the current increment value
            new_char = chr(ord(char) - length)
            result += new_char
            # Decrement the increment value for the next character
            length -= 1
    
        return result    
        
    def set_time(self):
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        addr = socket.getaddrinfo(host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(1)
            res = s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
        finally:
            s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        t = val - NTP_DELTA    
        tm = time.localtime(t)
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
        
    def set_dummy_time(self): 
        machine.RTC().datetime((2025, 1, 1, 0, 0, 0, 0, 0))
