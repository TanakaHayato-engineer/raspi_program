import color_code
import RPi.GPIO as GPIO
import time


RED_PIN = 23
BLUE_PIN = 24
GREEN_PIN = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

p0 = GPIO.PWM(RED_PIN, 150)  # 周波数50Hz
p1 = GPIO.PWM(BLUE_PIN, 150)  # 周波数50Hz
p2 = GPIO.PWM(GREEN_PIN, 150)  # 周波数50Hz
p0.start(0)
p1.start(0)
p2.start(0)

code = 0xe6b422
red, green, blue = color_code.get_RGB_percent(code)
print("red=", red, "% ", "green=", green, "% ", "blue=", blue, "%")

try:
    p0.ChangeDutyCycle(red)
    p1.ChangeDutyCycle(blue)
    p2.ChangeDutyCycle(green)
    time.sleep(3)

except KeyboardInterrupt:
    pass

p0.stop()
p1.stop()
p2.stop()
GPIO.cleanup()
