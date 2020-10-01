import TCS34725
import time


TCS34725.setup()

while True:
    clear, red, green, blue = TCS34725.read()
    print("clear=", clear)
    print("red=", red)
    print("green=", green)
    print("blue=", blue)
    print(" ***************************************************** ")
    time.sleep(1)
