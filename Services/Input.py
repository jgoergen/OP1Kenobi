import RPi.GPIO as GPIO

class Input():

    def __init__(self, key1Pin, key2Pin, key3Pin, keyUpPin, keyDownPin, keyLeftPin, keyRightPin, keyPressPin):
        print 'Input:: Starting Init'
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(
            key1Pin, 
            GPIO.IN, 
            pull_up_down = GPIO.PUD_UP)

        GPIO.setup(
            key2Pin, 
            GPIO.IN, 
            pull_up_down = GPIO.PUD_UP)

        GPIO.setup(
            key3Pin, 
            GPIO.IN, 
            pull_up_down = GPIO.PUD_UP)

        GPIO.setup(
            keyUpPin, 
            GPIO.IN, 
            pull_up_down = GPIO.PUD_UP)

        GPIO.setup(
            keyDownPin, 
            GPIO.IN, 
            pull_up_down = GPIO.PUD_UP)

        GPIO.setup(
            keyLeftPin, 
            GPIO.IN, 
            pull_up_down = GPIO.PUD_UP)

        GPIO.setup(
            keyRightPin, 
            GPIO.IN, 
            pull_up_down = GPIO.PUD_UP)

        GPIO.setup(
            keyPressPin, 
            GPIO.IN, 
            pull_up_down = GPIO.PUD_UP)

        GPIO.add_event_detect(
            key1Pin,
            GPIO.FALLING,
            bouncetime = 300)

        GPIO.add_event_detect(
            key2Pin,
            GPIO.FALLING,
            bouncetime = 300)

        GPIO.add_event_detect(
            key3Pin, 
            GPIO.FALLING,
            bouncetime = 300)

        GPIO.add_event_detect(
            keyUpPin, 
            GPIO.FALLING,
            bouncetime = 300)

        GPIO.add_event_detect(
            keyDownPin, 
            GPIO.FALLING,
            bouncetime = 300)

        GPIO.add_event_detect(
            keyLeftPin, 
            GPIO.FALLING,
            bouncetime = 300)

        GPIO.add_event_detect(
            keyRightPin, 
            GPIO.FALLING,
            bouncetime = 300)

        GPIO.add_event_detect(
            keyPressPin, 
            GPIO.FALLING,
            bouncetime = 300)

    def Update(self):
        pass

    def KeyDown(self, keyPin):
        return GPIO.event_detected(keyPin)