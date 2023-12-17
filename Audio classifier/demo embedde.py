from machine import Pin, ADC
import utime
import rp2

# Configure the Pico's onboard LED
led_pin = Pin(25, Pin.OUT)

# Configure the microphone input pins
microphone_pin = 32  # AUD pin
adc_pin = 36  # VCC pin

# Define thresholds for sound detection
threshold = 500

# Function to check if the sound is a "yes"
def is_yes_sound():
    return adc.read_u16() > threshold

# Initialize the ADC (Analog to Digital Converter) for the microphone
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def get_adc():
    pull()
    mov(x, osr)
    mov(y, isr)
    label("loop")
    jmp(x_dec, "loop")
    jmp(y_dec, "loop")

# Create a Pin object for the microphone_pin
microphone_pin = Pin(26)

# Create an ADC object using ADC0
adc = ADC(Pin(microphone_pin))

def turn_on_led():
    led_pin.on()

def turn_off_led():
    led_pin.off()

# Main loop
while True:
    # Wait for the "yes" command
    while not is_yes_sound():
        pass

    # Turn on the LED
    print("Sound detected! Turning on the LED...")
    turn_on_led()

    # Wait for the "no" command to turn off the LED
    while is_yes_sound():
        pass

    # Turn off the LED
    print("Sound detected! Turning off the LED.")
    turn_off_led()
    utime.sleep(5)  # Add a delay to prevent rapid toggling
