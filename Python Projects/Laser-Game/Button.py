import RPi.GPIO as GPIO

class Button(object):

    def __init__(self, num):
        self.num = num
        GPIO.setup(num, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def state(self):
        return GPIO.input(self.num)

    def pressed(self):
        return GPIO.input(self.num) == 0
    

