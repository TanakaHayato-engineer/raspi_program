import RPi.GPIO as GPIO
import time

# TRIGとECHOのGPIO番号
TRIG_PIN = 14
ECHO_PIN = 15

def init():
    # ピン番号をGPIOで指定
    GPIO.setmode(GPIO.BCM)
    # TRIG_PINを出力, ECHO_PINを入力
    GPIO.setwarnings(False)
    GPIO.setup(TRIG_PIN,GPIO.OUT)
    GPIO.setup(ECHO_PIN,GPIO.IN)

# PINがHIGHである時間を計測
def pulseIn(PIN):
    t_start = 0
    t_end = 0

    # PINがHIGHに変わった瞬間をt_startに記録する。そのため、PINがLOWである限り、t_startを現在時刻で置き換え続ける。
    while GPIO.input(PIN) == GPIO.LOW:
        t_start = time.time()

    # PINがLOWに変わった瞬間をt_endに記録する。そのため、PINがHIGHである限り、t_startを現在時刻で置き換え続ける。
    while GPIO.input(PIN) == GPIO.HIGH:
        t_end = time.time()

    return t_end - t_start


# 距離計測
def measure(v):
    # TRIGピンを0.3[s]だけLOW
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(0.3)
    # TRIGピンを0.00001[s]だけ出力（超音波発射）
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    # HIGHの時間計測
    t = pulseIn(ECHO_PIN)
    # 距離[m] = 音速[m/s] * 時間[s]/2
    distance = v * t/2
    return distance
