# from RPLCD.i2c import CharLCD
# from time import sleep

# # Try address 0x27 or 0x3F depending on your module
# lcd = CharLCD('PCF8574', 0x27)

# # Clear screen
# lcd.clear()

# # Display message
# lcd.write_string('Hello, World!')
# sleep(3)

# # Clear and write a new message
# lcd.clear()
# lcd.write_string('Raspberry Pi LCD')
# sleep(3)

# lcd.clear()

# from RPLCD.i2c import CharLCD
# from time import sleep

# # Create the LCD object
# lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

# # Green time for each junction
# # green_times = [6, 5, 4]

# # Loop through each junction

# for index, time_value in enumerate(green_times):
#     lcd.clear()
#     lcd.cursor_pos = (0, 0)

#     # Display header line for the junction
#     lcd.write_string(f"Junc {index + 1} Green")

#     # Countdown timer on second row
#     for seconds in range(time_value, -1, -1):
#         lcd.cursor_pos = (1, 0)
#         lcd.write_string(" " * 16)  # Clear line
#         lcd.cursor_pos = (1, 0)
#         lcd.write_string(f"{seconds} sec")
#         sleep(1)

from RPLCD.i2c import CharLCD
from time import sleep

# Initialize LCD
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

# Function to display green time for a given junction
def display_green_time(junction_no, greenlight):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(f"Junc {junction_no} Green")

    for seconds in range(greenlight, -1, -1):
        lcd.cursor_pos = (1, 0)
        lcd.write_string(" " * 16)  # Clear line
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"{seconds} sec")
        sleep(1)

# Example usage
display_green_time(1, 6)
display_green_time(2, 5)
display_green_time(3, 4)
