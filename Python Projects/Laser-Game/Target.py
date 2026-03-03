import time
import Adafruit_GPIO.I2C as I2C
import Adafruit_PCA9685
import Mux
import Adafruit_TCS34725
import RPi.GPIO as GPIO

servo_min = 150 # 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
servo_mid = 350

class Target(object):
    def __init__(self, mux, muxnum, servo, servonum, lednum):
        self.mux = mux
        self.muxnum = muxnum
        self.servo = servo
        self.servonum = servonum

        self.mux.channel(self.muxnum)
        self.sensor = Adafruit_TCS34725.TCS34725(address=0x29, busnum=1)

        self.lednum = lednum
        GPIO.setup(lednum, GPIO.OUT)

    def led_on(self):
        GPIO.output(self.lednum, True)
        
    def led_off(self):
        GPIO.output(self.lednum, False)
        
    def reading(self):
        self.mux.channel(self.muxnum)
        r, g, b, c = self.sensor.get_raw_data()
        return r, g, b, c

    def up(self):
        self.servo.set_pwm(self.servonum, 0, servo_mid)

    def down(self):
        self.servo.set_pwm(self.servonum, 0, servo_min)

    def hit(self):
        r1, g1, b1, c1 = self.reading()
        return b1 >= 1000
