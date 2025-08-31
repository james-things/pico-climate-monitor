# ReadingLogger (MicroPython Class)0
# This class handles the logging of temperature and humidity readings.
from time import time


class ReadingLogger:
    def __init__(self, sensor):
        self._sensor = sensor
        self.history = []
        self.last_timestamp = 0
        self.last_temperature = 0
        self.last_humidity = 0  

    def log_hourly_reading(self):
        reading = self._sensor.last_reading
        now = time()
        hour = (now // 3600) % 24  # Get hour from timestamp
        self.last_timestamp = now
        self.last_temperature = reading["temperature"]
        self.last_humidity = reading["humidity"]
        self.history.append({
            "temperature": self.last_temperature,
            "humidity": self.last_humidity,
            "timestamp": now,
            "hour": hour
        })
        if len(self.history) > 24:
            self.history = self.history[-24:]

    def get_new_reading(self):
        self._sensor.poll_sensor()
        reading = self._sensor.last_reading
        self.last_timestamp = time()
        self.last_temperature = reading["temperature"]
        self.last_humidity = reading["humidity"]
        print(reading)
        return {
            "temperature": self.last_temperature,
            "humidity": self.last_humidity,
            "timestamp": self.last_timestamp
        }

    def get_history(self):
        return self.history

    def get_last_reading(self):
        if self.history:
            return self.history[-1]
        return None

    def get_last_timestamp(self):
        return self.last_timestamp

    def get_last_temperature(self):
        return self.last_temperature

    def get_last_humidity(self):
        return self.last_humidity

    def get_last_all(self):
        return {
            "timestamp": self.last_timestamp,
            "temperature": self.last_temperature,
            "humidity": self.last_humidity
        }