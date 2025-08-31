# ReadingManager (MicroPython Class)
# This class manages reading logs and provides access to the last reading.
# In addition, it can be called upon to collect and store new readings.
from readings.readingLogger import ReadingLogger

class ReadingManager:
    def __init__(self, sensor):
        self.logger = ReadingLogger(sensor)

    def log_reading(self):
        self.logger.log_hourly_reading()

    def get_history(self):
        return self.logger.get_history()
    
    def get_new_reading(self):
        return self.logger.get_new_reading()

    def get_last_reading(self):
        return self.logger.get_last_reading()

    def get_last_timestamp(self):
        return self.logger.get_last_timestamp()

    def get_last_temperature(self):
        return self.logger.get_last_temperature()

    def get_last_humidity(self):
        return self.logger.get_last_humidity()

    def get_last_all(self):
        return self.logger.get_last_all()