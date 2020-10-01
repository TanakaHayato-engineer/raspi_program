import pigpio
import time

PWM0_PIN = 12

p = pigpio.pi()
frequency = 440  # オクターブ4の「ラ」の周波数
p.hardware_PWM(PWM0_PIN, frequency, 500000)  # 500000はデューティ比50%を意味する。
time.sleep(1.0)
p.hardware_PWM(PWM0_PIN, 0, 0)  # PWMの周波数を0、デューティ比を0とする。（PWMを止める。）
