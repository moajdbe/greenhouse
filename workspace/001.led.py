
import RPi.GPIO as GPIO
import time

p=3
d=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(p, GPIO.OUT)

GPIO.output(p, True)
time.sleep(d)
GPIO.output(p, False)
time.sleep(d)
GPIO.output(p, True)
time.sleep(d)
GPIO.output(p, False)

GPIO.cleanup()

