






























from microbit import * 
import music

WORD_LIMIT = 20

EOL = "\n"
WORDS_PER_MINUTE = 10
DOT_TIME = 1200/WORDS_PER_MINUTE
DASH_TIME = DOT_TIME * 3
MARK_SPACE =  DOT_TIME
SIGNAL_SPACE = DOT_TIME * 3
WORD_SPACE = DOT_TIME * 7


DOT_TIME_MIN =  DOT_TIME/4
DOT_TIME_MAX = DASH_TIME/2

DASH_TIME_MIN = DOT_TIME_MAX
DASH_TIME_MAX = DASH_TIME + (DOT_TIME * 2)

SIGNAL_SPACE_MIN = SIGNAL_SPACE * 2
SIGNAL_SPACE_MAX = WORD_SPACE * 2
WORD_SPACE_MIN = SIGNAL_SPACE_MAX


DOT = "."   
DASH = "-"  
SPACE = " "
WORD = "|"


mark_has_begun = False
mark_start_time = running_time()
space_has_begun = False
space_start_time = running_time()
message = list()


is_serial_receive_mode = False

def not_at_max_message_length():
	
 global message
 return message.count(SPACE) < WORD_LIMIT

def clear_extra_space():
	
 global message
 if len(message) == 1 and message[0] == SPACE:
		message.clear()

def display_dot_dash():
	
 mark_interval = running_time() - mark_start_time

 if mark_interval < DOT_TIME_MAX:
		display.show(Image.DIAMOND_SMALL)
 elif mark_interval >= DASH_TIME_MIN and mark_interval < DASH_TIME_MAX:
		display.show(Image.DIAMOND)
 elif mark_interval >= DASH_TIME_MAX:
		display.show(Image.SAD)

def process_mark_time():
	
 global mark_has_begun, mark_start_time
 if not mark_has_begun: return

 clear_extra_space()

 mark_interval = running_time() - mark_start_time

 if mark_interval > DOT_TIME_MIN and mark_interval < DOT_TIME_MAX:
		message.append(DOT)
  space_start_time = running_time()
  space_start_time = running_time() 
 elif mark_interval > DASH_TIME_MIN and mark_interval < DASH_TIME_MAX:
		message.append(DASH)
  space_start_time = running_time() 

 mark_has_begun = False
 
def message_has_first_mark():
	
 return len(message) > 0 and message[0] != SPACE

def process_space_time():
	
 global space_has_begun, space_start_time, mark_start_time
 if not message_has_first_mark(): return

 if not space_has_begun:
		space_start_time = running_time() 
  return  

 space_interval = running_time() - space_start_time
 if space_interval > SIGNAL_SPACE_MIN and space_interval < SIGNAL_SPACE_MAX:

		if len(message) > 0 and not message[len(message)-1] == SPACE and not message[len(message)-1] == SPACE:
			message.append(SPACE)  
 if space_interval > WORD_SPACE_MIN:

		if len(message) > 0 and not message[len(message)-1] == WORD:
			message.append(WORD)

 space_has_begun = False

def encode_keyed_morse_code():
	
 global mark_has_begun, mark_start_time, message, space_start_time, space_has_begun

 button_pressed = button_a.is_pressed()  

 if button_pressed:
		if not mark_has_begun:
			mark_start_time = running_time() 
   mark_has_begun = True

  display_dot_dash()
  music.pitch(800,duration=-1,wait=False)

  if not_at_max_message_length():
			process_space_time()
 else:
		display.clear() 
  music.stop() 

  if not space_has_begun:
			space_start_time = running_time() 
   space_has_begun = True
  if not_at_max_message_length():
			process_mark_time()

def display_character(character):
	
 if character == DASH:
		display.show(Image.DIAMOND)
  music.pitch(800,duration=int(round(DASH_TIME)),wait=True)
  display.clear()
  sleep(MARK_SPACE)

 if character == DOT:
		display.show(Image.DIAMOND_SMALL)
  music.pitch(800,duration=int(round(DOT_TIME)),wait=True)
  display.clear()
  sleep(MARK_SPACE)

 if character == SPACE:
		display.clear() 
  sleep(WORD_SPACE)


def process_incoming_serial_data():
	
 global message, is_serial_receive_mode
 parsed_data = ""
 while uart.any() is True and not parsed_data.endswith('\n'): 
		parsed_data += str(uart.read(), "utf-8", "ignore")
  sleep(10)

 if parsed_data:
		uart.write("parsed {}".format(parsed_data.split(',')) + EOL)
  try:
			is_serial_receive_mode = ("1" == parsed_data.split(',')[0])
   serial_message_str = parsed_data.split(',')[1]

   if parsed_data.split(',')[2]:
				message.clear()

   if serial_message_str and len(serial_message_str) > 0 and is_serial_receive_mode:
				for character in serial_message_str:
					uart.write(character+EOL)
     display_character(character)

  except IndexError:
			return


uart.init(baudrate=9600) 
uart.write(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"+EOL)
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