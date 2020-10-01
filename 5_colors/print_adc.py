import adc  # 別のファイルadc.pyで宣言した関数を使えるようにする。
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
adc.init()

try:
    while True:
        inputVal0 = adc.read(0)
        print(inputVal0)
        sleep(0.2)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
