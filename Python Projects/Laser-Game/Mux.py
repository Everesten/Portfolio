import Adafruit_GPIO.I2C as I2C

class Mux(object):
    def __init__(self, address=0x70):
        self._device = I2C.get_i2c_device(address)

    def _write8(self, reg, value):
        """Write a 8-bit value to a register."""
        self._device.write8(reg, value)

    def channel(self, chan):
        self._write8(0x04, 1<<chan)

if __name__ == '__main__':
    mux = Mux()
    mux.channel(1)
    print "Now run i2cdetect"
