import wave
import numpy as np
import matplotlib.pyplot as plt
import sys

args = sys.argv

if len(args) < 2:
    print("args=", args)
    print("エラー：wavファイルの名前を指定してください。")
    exit()

if len(args) >= 3:
    end_tick = int(args[2])  # コマンドライン引数の2つ目は、描画の終了ティック
    print("end_tick=", end_tick)  # ユーザの確認のため、画面に表示する。

file_name = args[1]  # コマンドライン引数の１つ目はファイル名
wf = wave.open(file_name, "r")
buf = wf.readframes(wf.getnframes())

# バイナリデータを整数型（16bit）に変換
data = np.frombuffer(buf, dtype="int16")
if len(args) >= 3:
    data = data[:end_tick]

# グラフ化
plt.plot(data, linewidth=0.3, marker='o', markersize=1)  # 線は細く、マーカーは小さくする。
plt.grid()
plt.title(file_name)
plt.xlabel("時間（整数値）")
plt.ylabel("値（整数値）")
plt.savefig(file_name + ".png")
plt.show()
