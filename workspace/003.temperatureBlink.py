
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import signal
import sys

pins={
	'temp':2,
	'led':3
}

p=3
d=.5
T=True

def signal_handler(signal, frame):
	print('Exiting')
	GPIO.output(pins['led'],False)
	GPIO.cleanup()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pins['led'], GPIO.OUT)
GPIO.output(pins['led'],T)

while True:

	humidity, temperature = Adafruit_DHT.read_retry(11, pins['temp'])
	print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)

	T = not T
	GPIO.output(pins['led'],T)

	time.sleep(d)

GPIO.cleanup()


