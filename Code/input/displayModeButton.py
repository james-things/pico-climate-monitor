# An original implementation of display mode toggling functionality, making use of debounce
# logic from the brightness button class.
from machine import Pin, Timer


class DesiredDisplayButton:

    def __init__(self, pin_number, use_pullups=False, desired_display_state='A'):
        self._button_pin = Pin(pin_number, Pin.IN, Pin.PULL_UP) if use_pullups else Pin(pin_number, Pin.IN)
        self._button_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.handle_interrupt)
        self._clicked = False
        self._state = False
        self._desired_display_state = desired_display_state
        self._debounce_timer = Timer(-1)
        self._debounce_ms = 100

    def handle_interrupt(self, pin):
        self._debounce_timer.init(mode=Timer.ONE_SHOT, period=self._debounce_ms, callback=self.debounce_handler)

    def debounce_handler(self, timer):
        current_state = self._button_pin.value()
        if current_state == 0:
            self._clicked = True
            self.toggle_desired_display_state()  # Call the toggle function when the button is clicked
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
    def desired_display_state(self):
        '''Get the current output state'''
        return self._desired_display_state

    def toggle_desired_display_state(self):
        '''Toggle between output states "A" and "B"'''
        print(f'Desired output state before: {self._desired_display_state}')
        if self._desired_display_state == 'A':
            self._desired_display_state = 'B'
        else:
            self._desired_display_state = 'A'
        print(f'Desired output state after: {self._desired_display_state}')
        