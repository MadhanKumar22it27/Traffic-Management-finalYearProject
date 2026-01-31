from time import sleep
from gpiozero import LED
# Define LEDs
red = LED(4)
yellow = LED(6)
green = LED(2)

try:
    while True:
        # Red Light ON
        red.on()
        yellow.off()
        green.off()
        print("Red Light ON")
        sleep(5)  # Wait 5 seconds

        # Yellow Light ON
        red.off()
        yellow.on()
        green.off()
        print("Yellow Light ON")
        sleep(5)  # Wait 2 seconds

        # Green Light ON
        red.off()
        yellow.off()
        green.on()
        print("Green Light ON")
        sleep(5)  # Wait 5 seconds

except KeyboardInterrupt:
    print("Exiting... Cleaning up GPIO")
    red.off()
    yellow.off()
    green.off() 
