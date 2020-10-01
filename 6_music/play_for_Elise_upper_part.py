import pigpio
import re
import time


PWM0_PIN = 12

TEMPO = 60  # テンポ（1分あたりの四分音符の数）
DURATION_PER_NOTE = 60 / TEMPO  # 4分音符1つあたりの発音時間

# 楽譜（音名と音の分割数からなる。例えば、16は16分音符を意味する。）
# 「エリーゼのために」の上パート（主旋律）の楽譜
UPPER_PART = [
    ["e5",16],["e-5",16],
    ["e5",16],["e-5",16],["e5",16],["b4",16],["d5",16],["c5",16],
    ["a4",8],["r",16],["c4",16],["e4",16],["a4",16],
    ["b4",8],["r",16],["e4",16],["a-4",16],["b4",16],
    ["c5",8],["r",16],["e4",16],["e5",16],["e-5",16],
    ["e5",16],["e-5",16],["e5",16],["b4",16],["d5",16],["c5",16],
    ["a4",8],["r",16],["c4",16],["e4",16],["a4",16],
    ["b4",8],["r",16],["e4",16],["c5",16],["b4",16],
    ["a4",4]
]

NOTE_DIFF = {"c":  -9, "c+": -8, "d-": -8, "d":  -7, "d+": -6,
             "e-": -6, "e":  -5, "f":  -4, "f+": -3, "g-": -3,
             "g":  -2, "g+": -1, "a-": -1, "a":   0, "a+":  1,
             "b-": 1, "b": 2, "r": None}

note_pattern = re.compile(r"^([a-gr])(\+|\-)?(\d+)?", re.IGNORECASE)
TUNING = 440  # 基準となるオクターブ4の「ラ」の周波数

def play_tone(p, pin, tone):
    note_match = note_pattern.search(tone[0])
    (note_code, accidential, octave) = note_match.groups()
    #print((note_code, accidential, octave))
    note_acc = note_code + (accidential if accidential else "")  # シャープやフラットの文字を付加
    #print("note_acc=", note_acc, " octave=", octave)
    # 音程の取得と周波数の計算
    if note_code == "r":  # 休符（rest）の場合
        frequency = 0
    else:  # 音符の場合
        note_diff = NOTE_DIFF[note_acc]
        octave = int(octave)  # 文字列を整数に変換
        frequency = TUNING * \
                    (2 ** (octave - 4)) * \
                    ((2 ** note_diff) ** (1 / 12.0))
    #print("note_diff=", note_diff, " note_freq=", note_frequency)

    duration = 4 * DURATION_PER_NOTE / tone[1]  # 発音（または非発音）時間を計算
    if len(tone) > 2:
        if tone[2] == ".":  # 付点音符（または休符）の場合
            duration *= 1.5
    p.hardware_PWM(pin, int(frequency), 500000)  # デューティ比50%
    time.sleep(duration)

def play(p, pin, song):
    p.set_mode(pin, pigpio.OUTPUT)
    try:
        for t in song:
            play_tone(p, pin, t)
    except KeyboardInterrupt:
        pass

    p.hardware_PWM(pin, 0, 0)  # PWMの周波数を0、デューティ比を0とする。（PWMを止める。）
    p.set_mode(pin, pigpio.INPUT)


# 以降はメインプログラム
p = pigpio.pi()
play(p, PWM0_PIN, UPPER_PART)
