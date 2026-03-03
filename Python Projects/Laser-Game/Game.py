import random
import time

class Game(object):

    def __init__(self, numships, targets, display):
        self.targets = targets
        self.display = display
        self.numships = numships
        
        
    def play(self):
        for i in range(self.numships):
            self.display.show("Ships Remaining:\n{}".format(self.numships - i))
            time.sleep(random.randrange(1, 2))
            t = random.choice(self.targets)
            t.up()
            t.led_on()
            while not t.hit():
                time.sleep(0.05)
            t.down()
            t.led_off()
        self.display.show("Game Over")
            

    
    
