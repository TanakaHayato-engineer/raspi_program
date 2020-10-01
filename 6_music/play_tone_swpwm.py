import RPi.GPIO as GPIO
import time

PIN0 = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN0, GPIO.OUT)
p = GPIO.PWM(PIN0, 440)

p.start(0.5)  # デューティ比50%でPWM信号の出力を開始
time.sleep(1.0)
p.stop()  # PWM信号の出力を停止
