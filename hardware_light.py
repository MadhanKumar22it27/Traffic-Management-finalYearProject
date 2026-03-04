from time import sleep
from gpiozero import LED
from RPLCD.i2c import CharLCD

red = [LED(14), LED(17), LED(10), LED(0)]
yellow = [LED(15), LED(27), LED(9), LED(5)]
green = [LED(18), LED(22), LED(11), LED(6)]

lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

def run_hardware(junction, green_time):

    # Safe reset
    for i in range(4):
        green[i].off()
        yellow[i].off()
        red[i].on()

    # Yellow
    yellow[junction].on()
    sleep(3)
    yellow[junction].off()

    # Green
    red[junction].off()
    green[junction].on()

    lcd.clear()
    lcd.write_string(f"Junc {junction+1}")

    for sec in range(green_time, -1, -1):
        lcd.cursor_pos = (1, 0)
        lcd.write_string(" " * 16)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"{sec} sec")
        sleep(1)

    green[junction].off()
    red[junction].on()