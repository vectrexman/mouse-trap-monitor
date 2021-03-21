#! /usr/bin/python

# Based on https://cdn.shopify.com/s/files/1/0176/3274/files/iftttpir.py from the PiHut

# Imports
import RPi.GPIO as GPIO
import time
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

# Set the GPIO naming convention
GPIO.setmode(GPIO.BCM)

# Turn off GPIO warnings
GPIO.setwarnings(False)

# Set a variable to hold the GPIO Pin identity
pinpir = 17

# Set GPIO pin as input
GPIO.setup(pinpir, GPIO.IN)

# Variables to hold the current and last states
currentstate = 0
previousstate = 0

# Load Environment Variables
load_dotenv()
enable_post = bool(os.getenv("ENABLE_POST"))
ifttt_key = str(os.getenv("IFTTT_KEY"))
motion_detected_cooldown = int(os.getenv("MOTION_DETECTED_COOLDOWN"))
read_frequency = float(os.getenv("READ_FREQUENCY"))

print("enable_post loaded as: " + str(enable_post))
print("motion_detected_cooldown loaded as: " + str(motion_detected_cooldown))
print("read_frequency loaded as: " + str(read_frequency))

# Instantiate Program Vars
beganCountDateTime = datetime.now()
beganCountTimeStamp = time.time()
motionDetectedCount = 0
lastOccurenceTimeStamp = 0

beganCountDateTimeFormatted = beganCountDateTime.strftime("%d/%m/%Y %H:%M:%S")
print("Current Date/Time: " + beganCountDateTimeFormatted)

try:
	print("Waiting for PIR to settle ...")
	
	# Loop until PIR output is 0
	while GPIO.input(pinpir) == 1:
	
		currentstate = 0

	print("    Ready. Quit at any time with CTRL-C")
	# Sleep momentarily to allow messages to be read
	time.sleep(1.5)
	
	# Loop until users quits with CTRL-C
	while True:
	
		# Read PIR state
		currentstate = GPIO.input(pinpir)

		# If the PIR is triggered
		if currentstate == 1 and previousstate == 0:
		
			# Make a note
			motionDetectedCount += 1

			# See how long it has been since we started counting
			if lastOccurenceTimeStamp > 0:
				currentTimeStamp = time.time()
				sinceLastOccurence = currentTimeStamp - lastOccurenceTimeStamp

				print("Motion detected! " + str(sinceLastOccurence) + " seconds elapsed since the last occurence")

				if enable_post == 'true':
					print("Post enabled - pushing event to IFTTT")

					# Your IFTTT URL with event name, key and json parameters (values)
					r = requests.post(
						'https://maker.ifttt.com/trigger/motion_detected/with/key/' + ifttt_key,
						params={"value1":"none","value2":"none","value3":"none"}
					)
				else:
					print("Post disabled - nothing sent")
			else:
				print("Motion detected! The first since the last reset")
			
			# Record new previous state
			previousstate = 1
			lastOccurenceTimeStamp = currentTimeStamp
			
			#Wait the specified number of seconds before looping again
			print("    Waiting " + str(motion_detected_cooldown) + " seconds")
			time.sleep(motion_detected_cooldown)
			
		# If the PIR has returned to ready state
		elif currentstate == 0 and previousstate == 1:
		
			print("    Resetting")
			previousstate = 0

		# Wait for the specified number of seconds
		time.sleep(read_frequency)
		print("    Ready")

except KeyboardInterrupt:
	print("    Quit")

	# Reset GPIO settings
	GPIO.cleanup()