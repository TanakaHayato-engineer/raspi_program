import RPi.GPIO as GPIO
import re
import multiprocessing
import time

PIN0 = 12
PIN1 = 13

TEMPO = 60  # テンポ（1分あたりの四分音符の数）
DURATION_PER_NOTE = 60 / TEMPO  # 4分音符1つあたりの発音時間

# 楽譜（音名と音の分割数からなる。例えば、16は16分音符を意味する。）
# 「エリーゼのために」の上パート（主旋律）の楽譜
UPPER_REPEAT1 = [
    ["e5",16],["e-5",16],
    ["e5",16],["e-5",16],["e5",16],["b4",16],["d5",16],["c5",16],
    ["a4",8],["r",16],["c4",16],["e4",16],["a4",16],
    ["b4",8],["r",16],["e4",16],["a-4",16],["b4",16],
    ["c5",8],["r",16],["e4",16],["e5",16],["e-5",16],
    ["e5",16],["e-5",16],["e5",16],["b4",16],["d5",16],["c5",16], # 第5小節終わり
    ["a4",8],["r",16],["c4",16],["e4",16],["a4",16],
    ["b4",8],["r",16],["e4",16],["c5",16],["b4",16]
]

# 「エリーゼのために」の下パートの楽譜
LOWER_REPEAT1 = [
    ["r",8],
    ["r",8],["r",8],["r",8],
    ["a3",16],["e4",16],["a4",16],["r",16],["r",8],
    ["e3",16],["e4",16],["g+4",16],["r",16],["r",8],
    ["a3",16],["e4",16],["a4",16],["r",16],["r",8],
    ["r",8],["r",8],["r",8], # 第5小節終わり
    ["a3",16],["e4",16],["a4",16],["r",16],["r",8],
    ["e3",16],["e4",16],["g+4",16],["r",16],["r",8],
]

UPPER_sono1_after_REPEAT1 = [ ["a4",4] ]
LOWER_sono1_after_REPEAT1 = [ ["a3",16],["e4",16],["a4",16],["r",16] ]

UPPER_sono2_after_REPEAT1 = [ ["a4",8],["r",16],["b4",16],["c5",16],["d5",16] ]
LOWER_sono2_after_REPEAT1 = [ ["a3",16],["e4",16],["a4",16],["r",16],["r",8] ]

UPPER_REPEAT2 = [
    ["e5",8,"."],["g4",16],["f5",16],["e5",16],
    ["d5",8,"."],["f4",16],["e5",16],["d5",16],
    ["c5",8,"."],["e4",16],["d5",16],["c5",16], # 第13小節終わり
    ["b4",8],["r",16],["e4",16],["e5",16],["r",16],
    ["r",16],["e5",16],["e6",16],["r",16],["r",16],["d+5",16],
    ["e5",16],["r",16],["r",16],["d+5",16],["e5",16],["d+5",16],
    ["e5",16],["d+5",16],["e5",16],["b4",16],["d5",16],["c5",16],
    ["a4",8],["r",16],["c4",16],["e4",16],["a4",16],
    ["b4",8],["r",16],["e4",16],["g+4",16],["b4",16], # 第19小節終わり
    ["c5",8],["r",16],["e4",16],["e5",16],["d+5",16],
    ["e5",16],["d+5",16],["e5",16],["b4",16],["d5",16],["c5",16],
    ["a4",8],["r",16],["c4",16],["e4",16],["a4",16],
    ["b4",8],["r",16],["e4",16],["c5",16],["b4",16],
]

LOWER_REPEAT2 = [
    ["c3",16],["g3",16],["c4",16],["r",16],["r",8],
    ["g2",16],["g3",16],["b3",16],["r",16],["r",8],
    ["a2",16],["e3",16],["a3",16],["r",16],["r",8], # 第13小節終わり
    ["e2",16],["e3",16],["e4",16],["r",16],["r",16],["e4",16],
    ["e5",16],["r",16],["r",16],["d+5",16],["e5",16],["r",16],
    ["r",16],["d+5",16],["e5",16],["r",16],["r",8],
    ["r",8],["r",8],["r",8],
    ["a2",16],["e3",16],["a3",16],["r",16],["r",8],
    ["e2",16],["e3",16],["g+3",16],["r",16],["r",8], # 第19小節終わり
    ["a2",16],["e3",16],["a3",16],["r",16],["r",8],
    ["r",8],["r",8],["r",8],
    ["a2",16],["e3",16],["a3",16],["r",16],["r",8],
    ["e2",16],["e3",16],["g+3",16],["r",16],["r",8],
]

UPPER_sono1_after_REPEAT2 = [ ["a4",8],["r",16],["b4",16],["c5",16],["d5",16] ]
LOWER_sono1_after_REPEAT2 = [ ["a2",16],["e3",16],["a3",16],["r",16],["r",8] ]

UPPER_PART = UPPER_REPEAT1 + UPPER_sono1_after_REPEAT1 + UPPER_REPEAT1 + UPPER_sono2_after_REPEAT1 + UPPER_REPEAT2 + UPPER_sono1_after_REPEAT2
LOWER_PART = LOWER_REPEAT1 + LOWER_sono1_after_REPEAT1 + LOWER_REPEAT1 + LOWER_sono2_after_REPEAT1 + LOWER_REPEAT2 + LOWER_sono1_after_REPEAT2


NOTE_DIFF = {"c":  -9, "c+": -8, "d-": -8, "d":  -7, "d+": -6,
             "e-": -6, "e":  -5, "f":  -4, "f+": -3, "g-": -3,
             "g":  -2, "g+": -1, "a-": -1, "a":   0, "a+":  1,
             "b-": 1, "b": 2, "r": None}

note_pattern = re.compile(r"^([a-gr])(\+|\-)?(\d+)?", re.IGNORECASE)
TUNING = 440  # 基準となるオクターブ4の「ラ」の周波数

def play_tone(p,tone):
    note_match = note_pattern.search(tone[0])
    (note_code, accidential, octave) = note_match.groups()
    #print((note_code, accidential, octave))
    note_acc = note_code + (accidential if accidential else "")  # シャープやフラットの文字を付加
    # 音程の取得と周波数の計算
    if note_code == "r":  # 休符（rest）の場合
        p.start(0)  # デューティ比0%でPWM信号の出力を開始（つまり、PWM信号を止める。）
    else:  # 音符の場合
        note_diff = NOTE_DIFF[note_acc]
        octave = int(octave)  # 文字列を整数に変換
        frequency = TUNING * \
                    (2 ** (octave - 4)) * \
                    ((2 ** note_diff) ** (1 / 12.0))
        p.ChangeFrequency(frequency)
        p.start(0.5)  # デューティ比50%でPWM信号の出力を開始
    duration = 4 * DURATION_PER_NOTE / tone[1]  # 発音（または非発音）時間を計算
    if len(tone) > 2:
        if tone[2] == ".":  # 付点音符（または休符）の場合
            duration *= 1.5
    time.sleep(duration)
    p.stop()

def play(pin, part):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, 440)
    for t in part:
        play_tone(p,t)

def destroy():
    GPIO.cleanup()


# 以降はメインプログラム
p1 = multiprocessing.Process(target=play, args=(PIN0, UPPER_PART))
p2 = multiprocessing.Process(target=play, args=(PIN1, LOWER_PART))

p1.start()
p2.start()

destroy()
