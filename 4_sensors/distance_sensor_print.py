import distance_sensor
import RPi.GPIO as GPIO

# 気温24度の場合の音速[m/s]
v = 331.5 + 0.61 * 24

distance_sensor.init()

distance = distance_sensor.measure(v)
print(distance, "[m]")

GPIO.cleanup()
