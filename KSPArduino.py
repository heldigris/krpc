#Dont forget to import firmata in the arduino controller.

from pyfirmata import Arduino, util
import pyfirmata
import serial
import krpc
import time

#board = Arduino('COM4')

running = True
server = None
arduino = None
while server is None or arduino is None:
	# We do not know if the server is online, so we want python to try to connect.
	try: 
		# The next line starts the connection with the server. It describes itself to the game as controller.
		server = krpc.connect(name='Controller')
		# Now let's connect to the Arduino
		#arduino = serial.Serial(port='COM4', baudrate=115200, timeout=1)
		arduino = Arduino('COM4')
		#  careful: if u get the baud number wrong, you will only receive garbage.
	except ConnectionRefusedError:  # error raised whe failing to connect to the server.
		print("Server offline")
		time.sleep(5)  # sleep 5 seconds
		server = None
		arduino = None

#	except serial.SerialException:  # error raised when failing to connect to an Arduino
#		# TIP: check if the Arduino serial monitor is off! or any other program using the Arduino
#		print("Arduino Connection Error.")	
#		time.sleep(5)
#		server = None
#		arduino = None

board = arduino
vessel = server.space_center.active_vessel
###########################################Pyfirmata
button_Blue= board.digital[2]
button_Red= board.digital[3]
previous_button_state_Blue = 0
previous_button_state_Red = 0

# Start iterator to receive input data
it = util.Iterator(board)
it.start()

# Setup LEDs and button
button_Blue.mode = pyfirmata.INPUT
button_Red.mode = pyfirmata.INPUT


print("Blue button read:", button_Blue.read())
Autopilot = False
#time.sleep(5)
while True:
        Autopilot
        print("Autopilot",Autopilot)
        # We run the loop at 10Hz
        time.sleep(0.2)
        
        # Get button current state
        button_state_Blue = button_Blue.read()
        button_state_Red = button_Red.read()
        print("button_state_Blue", button_state_Blue)
        print("button_state_Red", button_state_Red)
        # Check if button has been pressed
        if button_state_Blue == True & Autopilot == True:
            print("Look What i pressed, a blue button")
            vessel.control.activate_next_stage()
            time.sleep(0.5)
            print("Blue button pressed", button_state_Blue)

        if button_state_Red == True :
            print("Look What i pressed, a red button")
            if Autopilot == True:
                vessel.auto_pilot.disengage()
                time.sleep(1)
                Autopilot = False
                previous_button_state_Red = button_state_Red
                print("Deactivating autopilot", Autopilot)                
            elif Autopilot == False:
                time.sleep(1)
                Autopilot = True
                print("activating autopilot", Autopilot)
                vessel.auto_pilot.engage()

            
        # Save current button state as previous
        # for the next loop iteration
        #previous_button_state_Blue = button_state_Blue

        #previous_button_state_Red = button_state_Red

        #print("End of loop")
