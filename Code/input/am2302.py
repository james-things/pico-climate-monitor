# A simple implementation of the AM2302 sensor using the dht library
from machine import Pin
import dht


class Am2302:

    def __init__(self, gp_pin):
        self._temp_calibration_offset = 2
        self._Pin = Pin(gp_pin, Pin.IN)
        self._sensor = dht.DHT22(Pin(gp_pin))
        self._last_reading = {"temperature": 75, "humidity": 50}
        print("AM2302 initialization successful")

    def poll_sensor(self):
        self._sensor.measure()
        temp = self._sensor.temperature()
        hum = self._sensor.humidity()
        temp_f = ((temp * 9.001) / 5.002) + 32.001
        self._last_reading = {"temperature": temp_f, "humidity": hum}

    @property
    def last_reading(self):
        return self._last_reading



