
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import signal
import sys

def signal_handler(signal, frame):
	print('Exiting')
	GPIO.cleanup()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


GPIO.setmode(GPIO.BCM)


def ledToggle(key):
	if "state" not in ledToggle.__dict__: ledToggle.state=False
	p = PICONFIG[key]
	ledToggle.state = not ledToggle.state
	GPIO.output( p['io'], ledToggle.state )
	print key+": ",ledToggle.state

def temperatureCheck(key):
	try:
		p = PICONFIG[key]
		humidity, temperature = Adafruit_DHT.read_retry(11, p['io'])
		print key+": ",'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
	except:
		print 'Bad input from the temp sensor'

def moistureCheck(key):
	p = PICONFIG[key]
	s=GPIO.input( p['io'] )
	#print '{s}: {b}'.format(key,s)
	print key+": ",s


def setup():
	for key in PICONFIG:
		if PICONFIG[key]['output'] is True:
			GPIO.setup(PICONFIG[key]['io'],GPIO.OUT)
		if PICONFIG[key]['output'] is False:
			GPIO.setup(PICONFIG[key]['io'],GPIO.IN)
		#skip if 'output' is None

def eventLoop():
	try:
		while True:
			for key in PICONFIG:
				#print key
				PICONFIG[key]['callback'](key)

			time.sleep( FREQUENCY )
	except:
		print 'An exception occurred'

FREQUENCY=1

PICONFIG={
	'temp':		{	'io':2,		'output':None,	'callback':temperatureCheck	},
	'led':		{	'io':3,		'output':True,	'callback':ledToggle		},
	'moist1':	{	'io':17,	'output':False,	'callback':moistureCheck	},
	'moist2':	{	'io':27,	'output':False,	'callback':moistureCheck	},
	'moist3':	{	'io':22,	'output':False,	'callback':moistureCheck	}
}

setup()
eventLoop()


