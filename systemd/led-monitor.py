#!/usr/bin/python
import RPi.GPIO as GPIO
import time

def check_condition():
    return True

GPIO.setmode(GPIO.BCM)
LED_PIN = 27
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.02)
        if check_condition():
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(3)
finally:
    GPIO.cleanup()
