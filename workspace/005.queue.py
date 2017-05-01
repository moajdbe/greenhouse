#!/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import signal
import sys
import collections

def signal_handler(signal, frame):
	print('Exiting')
	GPIO.cleanup()
        sys.exit(0)

#add more signal handlers here!
signal.signal(signal.SIGINT, signal_handler)



########################
# callbacks per module #
########################

# because these are different values, the LEDs will shift back and forth
# if they were the same, both would blink together
LEDSTATES={
	"led1":False,
	"led2":True
}

def ledToggle(key):
	p = PICONFIG[key]
	LEDSTATES[key] = not LEDSTATES[key]
	GPIO.output( p['io'], LEDSTATES[key] )
	print key+":\t",LEDSTATES[key]


def temperatureCheck(key):
	try:
		p = PICONFIG[key]
		humidity, temperature = Adafruit_DHT.read_retry(11, p['io'])
		print key+":\t",'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
	except:
		print 'Bad input from the temp sensor'


def moistureCheck(key):
	p = PICONFIG[key]
	v = p['valve']
	s=GPIO.input( p['io'] )
	#print '{s}: {b}'.format(key,s)
	if s is MOIST:
		if v not in QUEUE:
			#print "ENQUEUE: ",v
			QUEUE.append( v )
	print key+":\t",s


def pumpCheck(key):
	p = PICONFIG[key]
	s = CURRENTVALVE is not None
	GPIO.output( p['io'], s )
	print key+":\t",s


def valveCheck(key):
	p = PICONFIG[key]
	s = (key == CURRENTVALVE)
	GPIO.output( p['io'], s )
	print key+":\t",s

########################
# end callbacks        #
########################


#setup the GPIO channels as input or output.  Temperature is an exception because the Adafruit library takes care of it
def setup():
	GPIO.setmode(GPIO.BCM)
	for key in PICONFIG:
		if PICONFIG[key]['output'] is True:
			GPIO.setup(PICONFIG[key]['io'],GPIO.OUT)
		if PICONFIG[key]['output'] is False:
			GPIO.setup(PICONFIG[key]['io'],GPIO.IN)
		#skip if 'output' is None, like temperature


#each module's callback is executed per event loop
#the callbacks reference the global variables, in the style of C (not C++)
def eventLoop():
	#try:		#the exception should be uncommented, but it makes it harder to debug
		global CURRENTVALVE, VALVETIME
		while True:

			t = time.time()

			#check if we need to close a valve
			if CURRENTVALVE is not None:
				if t > VALVECLOSE:
					print "Closing valve: ",CURRENTVALVE
					CURRENTVALVE = None
					VALVECLOSE = 0

			#check the queue for more work
			if len(QUEUE):
				if CURRENTVALVE is None:
					CURRENTVALVE = QUEUE.pop(0)
					print "Opening valve: ",CURRENTVALVE
					VALVECLOSE = t + VALVETIME

			#run the callbacks
			for key in PICONFIG:
				#print key
				p = PICONFIG[key]
				if p['callback'] is not None:
					p['callback'](key)

			print '======================================'
			print QUEUE
			print "Current valve: ",CURRENTVALVE
			print '======================================'
			time.sleep( FREQUENCY )
	#except:
	#	print 'An exception occurred'


#any module can be commented out to get rid of it
#the modules work by name/key
#it must be an OrderedDict because the order matters... pump should be last in the chain.  A normal dict does not respect order.
PICONFIG=collections.OrderedDict(
[
#	(	'temp',		{	'io':2,		'output':None,	'callback':temperatureCheck				}	),
	(	'led1',		{	'io':3,		'output':True,	'callback':ledToggle					}	),
	(	'led2',		{	'io':4,		'output':True,	'callback':ledToggle					}	),
	(	'moist1',	{	'io':17,	'output':False,	'callback':moistureCheck,	'valve':'valve1'	}	),
	(	'moist2',	{	'io':27,	'output':False,	'callback':moistureCheck,	'valve':'valve2'	}	),
	(	'moist3',	{	'io':22,	'output':False,	'callback':moistureCheck,	'valve':'valve3'	}	),
	(	'valve1',	{	'io':15,	'output':True,	'callback':valveCheck					}	),
	(	'valve2',	{	'io':18,	'output':True,	'callback':valveCheck					}	),
	(	'valve3',	{	'io':23,	'output':True,	'callback':valveCheck					}	),
	(	'pump',		{	'io':14,	'output':True,	'callback':pumpCheck					}	)
]
)

FREQUENCY=1		#event queue time to sleep
QUEUE=[]		#queue of valves to open
CURRENTVALVE=None	#currently open valve
VALVECLOSE=0		#time in future when valve will close (and get next item in queue)
#VALVETIME=60*1		#number of seconds to keep a valve open
VALVETIME=1		#number of seconds to keep a valve open

MOIST=1			#logical defines
DRY=0			#DRY is unused, but may be useful in the future

setup()
eventLoop()


