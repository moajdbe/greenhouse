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

signal.signal(signal.SIGINT, signal_handler)



LEDSTATES={
	"led1":False,
	"led2":False
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
	s=GPIO.input( p['io'] )
	#print '{s}: {b}'.format(key,s)
	print key+":\t",s


def pumpCheck(key):
	p = PICONFIG[key]
	s = CURRENTVALVE is not None
	GPIO.output( p['io'], s )
	print key+":\t",s


def enqueueEvent(key,callback):
	#add tuple to end of array
	QUEUE.append( (key,callback) )


def setup():
	GPIO.setmode(GPIO.BCM)
	for key in PICONFIG:
		if PICONFIG[key]['output'] is True:
			GPIO.setup(PICONFIG[key]['io'],GPIO.OUT)
		if PICONFIG[key]['output'] is False:
			GPIO.setup(PICONFIG[key]['io'],GPIO.IN)
		#skip if 'output' is None

def eventLoop():
	#try:
		while True:
			for key in PICONFIG:
				#print key
				p = PICONFIG[key]
				if p['callback'] is not None:
					p['callback'](key)

			#do queue work here
			#if len(QUEUE

			print '======================================'
			time.sleep( FREQUENCY )
	#except:
	#	print 'An exception occurred'

FREQUENCY=10

PICONFIG=collections.OrderedDict(
[
	(	'temp',		{	'io':2,		'output':None,	'callback':temperatureCheck				}	),
	(	'led1',		{	'io':3,		'output':True,	'callback':ledToggle					}	),
	(	'led2',		{	'io':4,		'output':True,	'callback':ledToggle					}	),
	(	'pump',		{	'io':14,	'output':True,	'callback':pumpCheck					}	),
	(	'moist1',	{	'io':17,	'output':False,	'callback':moistureCheck,	'valve':'valve1'	}	),
	(	'moist2',	{	'io':27,	'output':False,	'callback':moistureCheck,	'valve':'valve2'	}	),
	(	'moist3',	{	'io':22,	'output':False,	'callback':moistureCheck,	'valve':'valve3'	}	)
]
)

QUEUE=[]
CURRENTVALVE=None

setup()
eventLoop()


