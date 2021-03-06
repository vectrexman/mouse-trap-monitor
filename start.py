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
notification_frequency = int(os.getenv("NOTIFICATION_FREQUENCY"))

print("enable_post loaded as: " + str(enable_post))
print("motion_detected_cooldown loaded as: " + str(motion_detected_cooldown))
print("read_frequency loaded as: " + str(read_frequency))
print("notification_frequency loaded as: " + str(notification_frequency))
time.sleep(1)

# Instantiate Program Vars
beganCountDateTime = datetime.now()
beganCountTimeStamp = time.time()
motionDetectedCount = 0
lastOccurenceTimeStamp = 0
connectionTimeout = 60 # How many seconds to wait for IFTTT to respond in secs
retryPostCounter = 0 # Tracks how many attempts to post before giving up

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

			currentTimeStamp = time.time()

			# See how long it has been since we started counting
			if lastOccurenceTimeStamp > 0:
				sinceLastOccurenceSecs = currentTimeStamp - lastOccurenceTimeStamp
				sinceLastOccurenceMins = round(sinceLastOccurenceSecs / 60, 2)
				sinceBeganCount = currentTimeStamp - beganCountTimeStamp

				print(
					"Motion detected! " + str(sinceLastOccurenceMins) + 
					" minutes elapsed since the last occurence. Total since last reset: " + str(motionDetectedCount)
				)

				# If we have passed the notification threshold then send an update if enabled
				if sinceBeganCount > notification_frequency:
					if enable_post:
						print("Post enabled - pushing event to IFTTT")

						sinceBeganCountHours = round((sinceBeganCount / 60) / 60, 2)

						try:
							# Your IFTTT URL with event name, key and json parameters (values)
							# Timeout is how long to wait in seconds in the event of no response or internet dropping
							r = requests.post(
								'https://maker.ifttt.com/trigger/motion_detected/with/key/' + ifttt_key,
								params={"value1":motionDetectedCount,"value2":sinceBeganCountHours,"value3":"none"},
								timeout=connectionTimeout
							)

							retryPostCounter = 0
						except requests.exceptions.ConnectionError:
							retryPostCounter += 1

							if retryPostCounter >= 5:
								raise ValueError("Attempts to contact IFTTT reached threshold. Aborting :(")
							else:
								print("Error pushing to IFTTT - ConnectionError, will try again...")
								time.sleep(connectionTimeout)
						except requests.Timeout:
							retryPostCounter += 1

							if retryPostCounter >= 5:
								raise ValueError("Attempts to contact IFTTT reached threshold. Aborting :(")
							else:
								print("Error pushing to IFTTT - Timeout, will try again...")
								time.sleep(connectionTimeout)
					else:
						print("Post disabled - nothing sent")

					# Reset count
					beganCountTimeStamp = time.time()
					motionDetectedCount = 0
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