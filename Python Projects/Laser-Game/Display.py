import Adafruit_CharLCD as LCD

class Display(object):

    def __init__(self, mux, muxnum):
        self.mux = mux
        self.muxnum = muxnum
        self.mux.channel(self.muxnum)
        self.lcd = LCD.Adafruit_CharLCDPlate()

    def show(self, s):
        self.mux.channel(self.muxnum)
        self.lcd.set_color(0.0, 1.0, 1.0)
        self.lcd.clear()
        self.lcd.message(s)
        
