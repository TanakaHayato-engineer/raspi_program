import RPi.GPIO as GPIO

# ピンの名前を変数として定義
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8


def init():
    GPIO.setmode(GPIO.BCM)
    # SPI通信用の入出力を定義
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICS, GPIO.OUT)

# MCP3208からSPI通信で12ビットのデジタル値を取得。0から7の8チャンネル使用可
def read(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1
    GPIO.output(SPICS, GPIO.HIGH)
    GPIO.output(SPICLK, GPIO.LOW)
    GPIO.output(SPICS, GPIO.LOW)

    commandout = adcnum
    commandout |= 0x18  # スタートビット＋シングルエンドビット
    commandout <<= 3    # LSBから8ビット目を送信するようにする
    for i in range(5):
        # LSBから数えて8ビット目から4ビット目までを送信
        if commandout & 0x80:
            GPIO.output(SPIMOSI, GPIO.HIGH)
        else:
            GPIO.output(SPIMOSI, GPIO.LOW)
        commandout <<= 1
        GPIO.output(SPICLK, GPIO.HIGH)
        GPIO.output(SPICLK, GPIO.LOW)
    adcout = 0
    # 13ビット読む（ヌルビット＋12ビットデータ）
    for i in range(13):
        GPIO.output(SPICLK, GPIO.HIGH)
        GPIO.output(SPICLK, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(SPIMISO)==GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(SPICS, GPIO.HIGH)
    return adcout
