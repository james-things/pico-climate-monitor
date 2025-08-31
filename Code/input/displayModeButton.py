from machine import Pin, Timer


class DesiredDisplayButton:
    @property
    def ButtonClicked(self, reset=True):
        clicked = self._clicked
        if reset:
            self._clicked = False
        return clicked

    @property
    def ButtonState(self):
        print("button state firing")
        return self._state

    @property
    def desired_display_state(self):
        print("desired display state firing")
        '''Get the current output state'''
        return self._desired_display_state
    
    def __init__(self, pin_number, use_pullups=False, desired_display_state='A'):
        self._button_pin = Pin(pin_number, Pin.IN, Pin.PULL_UP) if use_pullups else Pin(pin_number, Pin.IN)
        self._button_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.handle_interrupt)
        self._clicked = False
        self._state = False
        self._desired_display_state = desired_display_state
        self._debounce_timer = Timer(-1)
        self._debounce_ms = 100
        print("display button initialized")

    def handle_interrupt(self, interrupt_pin):
        print("interrupt-display button (handle_interrupt)")
        self._debounce_timer.init(mode=Timer.ONE_SHOT, period=self._debounce_ms, callback=self.debounce_handler)

    def debounce_handler(self, debounce_timer):
        print("interrupt-display button (debounce_handler)")
        current_state = self._button_pin.value()
        if current_state == 0:
            self._clicked = True
            self.toggle_desired_display_state()  # Call the toggle function when the button is clicked
        self._state = current_state == 0
        print(self._clicked)

    def toggle_desired_display_state(self):
        self._desired_display_state = 'B' if self._desired_display_state == 'A' else 'A'
        