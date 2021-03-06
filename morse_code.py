# ------------__ Hacking STEM – morse_code.py – micro:bit __-----------
# For use with the Harnessing Electricity to Communicate Lesson plan
# from Microsoft Education Workshop at https://www.microsoft.com/en-us/education/education-workshop/telegraph.aspx
# http://aka.ms/hackingSTEM
#
#  This project uses a speaker across Pin 0 and GND as well as the 
#  left built in button. Using short and long button presses, up to 
#  20 dots, dashes, and spaces will be transmitted to Excel, which can
#  be used to decode messages.
#  
#   * Short button hold will display a dot on LED grid and tone 
#   * Long button hold will display a dash on LED grid and tone 
#   * Extra long button hold will display an X on LED grid and no 
#  character will transmitted to Excel
#   * Pause between button presses will result in a space.
#   * If all 20 slots are filled, button pressed will display an X on LED
#  grid and no data will be transmitted to Excel
#   * Serial messages sent from excel will display on LED matrix and make
#  tones via speaker
#
#  This project uses a BBC micro:bit microcontroller, information at:
#  https://microbit.org/
#
#  Comments, contributions, suggestions, bug reports, and feature
#  requests are welcome! For source code and bug reports see:
#  https://github.com/microsoft/hackingstem-morsecode-microbit
#
#  Copyright 2018, Jeremy Franklin-Ross
#  Microsoft EDU Workshop - HackingSTEM
#  MIT License terms detailed in LICENSE.txt
# ===---------------------------------------------------------------===

from microbit import * 
import music

WORD_LIMIT = 20

EOL = "\n"
WORDS_PER_MINUTE = 10             # Scaler to adjust all time
DOT_TIME = 1200/WORDS_PER_MINUTE  # Duration of ideal dot moark
DASH_TIME = DOT_TIME * 3          # Duration of ideal dash mark
MARK_SPACE =  DOT_TIME            # Time between marks
SIGNAL_SPACE = DOT_TIME * 3       # Time between letters
WORD_SPACE = DOT_TIME * 7         # Time between words

""" Following thresholds are used to detect input """
DOT_TIME_MIN =  DOT_TIME/4         # Minimum dot duration
DOT_TIME_MAX = DASH_TIME/2         # Maximum dot duration

DASH_TIME_MIN = DOT_TIME_MAX                # Min dash duration
DASH_TIME_MAX = DASH_TIME + (DOT_TIME * 2)  # Max dash duration

SIGNAL_SPACE_MIN = SIGNAL_SPACE * 2  # Max duration between marks
SIGNAL_SPACE_MAX = WORD_SPACE * 2    # Max duration between letters
WORD_SPACE_MIN = SIGNAL_SPACE_MAX    # Min duration between words

# Characters for dot, dash, space
DOT = "."   
DASH = "-"  
SPACE = " "
WORD = "|"

''' State and timers to derive button input '''
mark_has_begun = False             # State when key pressed
mark_start_time = running_time()   # Used to derive dot or dash
space_has_begun = False            # State when key let up
space_start_time = running_time()  # Used to derive space
message = list()  # List accumulates Dots, Dashes, and Spaces 

# state switch, prevents keying when excel sending messages
is_serial_receive_mode = False

def not_at_max_message_length():
    """ Indicates if we have room left in message """
    global message
    return message.count(SPACE) < WORD_LIMIT

def clear_extra_space():
    """ remove extra space at list front """
    global message
    if len(message) == 1 and message[0] == SPACE:
        message.clear()

def display_dot_dash():
    """ based on time interval, display appropriate image """
    mark_interval = running_time() - mark_start_time

    if mark_interval < DOT_TIME_MAX:
        display.show(Image.DIAMOND_SMALL)  # Dot Image
    elif mark_interval >= DASH_TIME_MIN and mark_interval < DASH_TIME_MAX:
        display.show(Image.DIAMOND)        # Dash Image
    elif mark_interval >= DASH_TIME_MAX:
        display.show(Image.SAD)            # Overtime Image

def process_mark_time():
    """ Determine if DOT or DASH timing has elapsed """
    global mark_has_begun, mark_start_time
    if not mark_has_begun: return

    clear_extra_space()

    mark_interval = running_time() - mark_start_time

    if mark_interval > DOT_TIME_MIN and mark_interval < DOT_TIME_MAX:
        message.append(DOT)
        space_start_time = running_time() 
    elif mark_interval > DASH_TIME_MIN and mark_interval < DASH_TIME_MAX:
        message.append(DASH)
        space_start_time = running_time() 

    mark_has_begun = False
    
def message_has_first_mark():
    """ Message list contains at lease one dot or dash """
    return len(message) > 0 and message[0] != SPACE

def process_space_time():
    """ Determines if enough time has elapsed to generate a space """
    global space_has_begun, space_start_time, mark_start_time
    if not message_has_first_mark(): return

    if not space_has_begun:
        space_start_time = running_time() 
        return  

    space_interval = running_time() - space_start_time
    if space_interval > SIGNAL_SPACE_MIN and space_interval < SIGNAL_SPACE_MAX:
        # Don't put two spaces in a row
        if len(message) > 0 and not message[len(message)-1] == SPACE and not message[len(message)-1] == SPACE:
            message.append(SPACE)        
    if space_interval > WORD_SPACE_MIN:
        # Don't put two spaces in a row
        if len(message) > 0 and not message[len(message)-1] == WORD:
            message.append(WORD)

    space_has_begun = False

def encode_keyed_morse_code():
    """ Depending on button state, encode keys to marks """
    global mark_has_begun, mark_start_time, message, space_start_time, space_has_begun

    button_pressed = button_a.is_pressed() or (pin1.read_digital() == 1)
    if len(message) == 0: space_has_begun = False

    if button_pressed:
        if not mark_has_begun:
            mark_start_time = running_time() 
            mark_has_begun = True

        display_dot_dash()
        music.pitch(800,duration=-1,wait=False)

        if not_at_max_message_length():
            process_space_time()
    else:  # not button_pressed
        display.clear() 
        music.stop() 

        if not space_has_begun:
            space_start_time = running_time() 
            space_has_begun = True
        if not_at_max_message_length():
            process_mark_time()

def display_character(character):
    """ Display Dot, Dash, or Space images on LED Matrix """
    if character == DASH:
        display.show(Image.DIAMOND)        # Dot image
        music.pitch(800,duration=int(round(DASH_TIME)),wait=True)
        display.clear()
        sleep(MARK_SPACE)

    if character == DOT:
        display.show(Image.DIAMOND_SMALL)  # Dash image
        music.pitch(800,duration=int(round(DOT_TIME)),wait=True)
        display.clear()
        sleep(MARK_SPACE)

    if character == SPACE:
        display.clear() 
        sleep(WORD_SPACE)


def process_incoming_serial_data():
    """ gets comma delimited data from serial applies changes appropriately """
    global message, is_serial_receive_mode, mark_has_begun
    parsed_data = ""
    
    while uart.any() is True and not "\n" in parsed_data: 
        parsed_data += str(uart.readline(), "utf-8", "ignore")
        sleep(10)

    if parsed_data:
        process_message_list = parsed_data.rstrip('\n').split(',')
        try:
            is_serial_receive_mode = ("1" == process_message_list[0])
            if not is_serial_receive_mode or ("1" == process_message_list[2]):
                mark_has_begun = False

            if process_message_list[2]:
                message.clear()

            if (process_message_list[1] == "1") and is_serial_receive_mode:
                saw_word = False

                for message_string in process_message_list[3:]:
                    if "\n" in message_string:
                        break

                    if len(message_string) == 0:
                        if not saw_word: display_character(WORD)
                        saw_word = True
                    else:
                        for character in message_string:
                            display_character(character)
                            saw_word = False

                        display_character(SPACE)


        except IndexError:
            return

# Initialization
uart.init(baudrate=9600) 
uart.write(EOL+",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"+EOL)
last_message_length = 0

while True: 
    if not is_serial_receive_mode: encode_keyed_morse_code()
    process_incoming_serial_data()
    if last_message_length != len(message) and not is_serial_receive_mode:
        for character in message:
            if character == SPACE:
                uart.write(",")
            elif character == WORD:
                uart.write(", ,")
            else:
                uart.write(character)

        uart.write(EOL)         
        last_message_length = len(message)