#! /usr/bin/python

# Based on https://cdn.shopify.com/s/files/1/0176/3274/files/iftttpir.py from the PiHut

# Imports
import RPi.GPIO as GPIO
import time
import requests
from dotenv import load_dotenv
import os

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

enable_post = os.getenv("ENABLE_POST")
motion_detected_cooldown = os.getenv("MOTION_DETECTED_COOLDOWN")
read_frequency = os.getenv("READ_FREQUENCY")

try:
	print("Waiting for PIR to settle ...")
	
	# Loop until PIR output is 0
	while GPIO.input(pinpir) == 1:
	
		currentstate = 0

	print("    Ready")
	
	# Loop until users quits with CTRL-C
	while True:
	
		# Read PIR state
		currentstate = GPIO.input(pinpir)

		# If the PIR is triggered
		if currentstate == 1 and previousstate == 0:
		
			print("Motion detected!")

			if enable_post == 'true':
				print("Post enabled")
			else:
				print("Post disabled")
			
			# Your IFTTT URL with event name, key and json parameters (values)
			#r = requests.post(
			#	'https://maker.ifttt.com/trigger/motion_detected/with/key/*INSERT KEY HERE*',
			#	params={"value1":"none","value2":"none","value3":"none"}
			#)
			
			# Record new previous state
			previousstate = 1
			
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