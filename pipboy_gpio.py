import RPi.GPIO as GPIO

class PipBoyGpioInput:
    def __init__(self):
        self.rotary1 = RotaryInput(11, 10)
        self.rotary2 = RotaryInput(3, 4)
        self.button1 = ButtonInput(self, 16, 13)
        self.button2 = ButtonInput(self, 20, 19)
        self.button3 = ButtonInput(self, 21, 26)
        self.button1.enable_light()
    
    def btn_pressed(self):
        self.button1.clear_light()
        self.button2.clear_light()
        self.button3.clear_light()

class ButtonInput:
    pressed = False
    
    def __init__(self, pip_gpio, btn_pin, led_pin):
        self.pip_gpio = pip_gpio

        self.BTN_PIN = btn_pin
        self.LED_PIN = led_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.LED_PIN, GPIO.OUT)

        GPIO.add_event_detect(self.BTN_PIN, GPIO.FALLING, callback=self.press_callback, bouncetime=50)

    def press_callback(self, channel):
        if (channel == self.BTN_PIN):
            if (GPIO.input(self.BTN_PIN) == GPIO.LOW):
                self.pressed = True
                self.pip_gpio.btn_pressed()
                GPIO.output(self.LED_PIN, GPIO.HIGH)
    
    def clear_light(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)
    
    def enable_light(self):
        GPIO.output(self.LED_PIN, GPIO.HIGH)

    def get_input(self):
        current_val = self.pressed
        self.pressed = False
        return current_val

class RotaryInput:
    counter = 0
    actual = 0
    clk_pin_state = 0
    dt_pin_state = 0

    def __init__(self, clk_pin, dt_pin):
        self.CLK_PIN = clk_pin
        self.DT_PIN = dt_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.CLK_PIN, GPIO.RISING, callback=self.pulse_callback, bouncetime=None)
        GPIO.add_event_detect(self.DT_PIN, GPIO.BOTH, callback=self.pulse_callback, bouncetime=None)

    def pulse_callback(self, channel):
        if (channel == self.CLK_PIN):
            self.clk_pin_state = GPIO.input(self.CLK_PIN)
            if self.clk_pin_state == GPIO.HIGH:
                if self.dt_pin_state == GPIO.HIGH:
                    self.counter -= 1
                    self.actual -=1
                else:
                    self.counter += 1
                    self.actual += 1
                #print("Rotary Encoder:: direction:", "- count:", self.actual)
        if (channel == self.DT_PIN):
            self.dt_pin_state = GPIO.input(self.DT_PIN)

    def get_input(self):
        current_count = self.counter
        self.counter = 0
        return current_count



