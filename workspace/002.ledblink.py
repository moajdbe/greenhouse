
import RPi.GPIO as GPIO
import time
import signal
import sys

p=3
d=.5

def signal_handler(signal, frame):
	print('Exiting')
	GPIO.output(p,False)
	GPIO.cleanup()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

GPIO.setmode(GPIO.BCM)
GPIO.setup(p, GPIO.OUT)

while True:
	GPIO.output(p,True)
	time.sleep(d)
	GPIO.output(p,False)
	time.sleep(d)

GPIO.cleanup()

