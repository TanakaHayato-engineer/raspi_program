import wave_tool
import math

def sin_wave(frequency, tick):
    tick_mod = tick % wave_tool.sample_rate
    t = tick_mod / wave_tool.sample_rate
    omega = 2.0 * math.pi * frequency
    value = math.sin(omega * t)
    return value


# 以降はメインプログラム
import numpy as np
file = wave_tool.open("sin.wav")

frequency = 440.0
data = [sin_wave(frequency, i) for i in range(wave_tool.sample_rate)]  # リスト内包表記を用いる。1秒間の正弦波をリストとして得る。
print("data[:10]=", data[:10])  # 最初の10個を表示してみる。

wave_tool.write(file, data)  # ファイルに書き込む。
wave_tool.close(file)
