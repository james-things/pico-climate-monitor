# An original implementation of a brightness button, using momentary button class from
# https://github.com/MZachmann/PicoPendant as a reference. Debounce concept identified
# by querying a modern GPT-based language model for information about methods of mitigating
# repeated button inputs.
from machine import Pin, Timer

class DesiredBrightnessButton:
    '''This class supports a momentary button with brightness control
    gpio pin number = GPxx number
    '''

    def __init__(self, pin_number, lcd_display_controller, use_pullups=False, desired_brightness=50):
        self._button_pin = Pin(pin_number, Pin.IN, Pin.PULL_UP) if use_pullups else Pin(pin_number, Pin.IN)
        self._button_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.handle_interrupt)
        self._clicked = False
        self._state = False
        self._desired_brightness = desired_brightness
        self._debounce_timer = Timer(-1)
        self._debounce_ms = 100
        self._lcd_display_controller = lcd_display_controller

    def handle_interrupt(self, pin):
        '''The interrupt handler for the button pin.
        Update the state and clicked properties based on the button pin state.'''
        self._debounce_timer.init(mode=Timer.ONE_SHOT, period=self._debounce_ms, callback=self.debounce_handler)

    def debounce_handler(self, timer):
        current_state = self._button_pin.value()
        if current_state == 0:
            self._clicked = True
            self.increment_desired_brightness()  # Call the increment function when the button is clicked
            self._lcd_display_controller.set_brightness(self._desired_brightness)
        self._state = current_state == 0
        print(self._clicked)

    @property
    def ButtonClicked(self, reset=True):
        clicked = self._clicked
        if reset:
            self._clicked = False
        return clicked

    @property
    def ButtonState(self):
        return self._state

    @property
    def desired_brightness(self):
        '''Get the current brightness level'''
        return self._desired_brightness

    def increment_desired_brightness(self):
        '''Set a new brightness level'''
        print(f'Desired brightness before: {self._desired_brightness}')
        cur_brightness = self._desired_brightness
        if cur_brightness >= 90:
            self._desired_brightness = 10
        else:
            self._desired_brightness = cur_brightness + 20
        print(f'Desired brightness after: {self._desired_brightness}')
