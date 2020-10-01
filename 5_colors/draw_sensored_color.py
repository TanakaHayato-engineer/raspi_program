import matplotlib.pyplot as plt
import matplotlib.patches as pat

def set_color(R_in, G_in, B_in, C_in):
    R_duty = float(R_in) / 65535
    G_duty = float(G_in) / 65535
    B_duty = float(B_in) / 65535
    C_duty = float(C_in) / 65535
    rect = pat.Rectangle(xy=(0,0.2), width=1.0, height=1.0, color=[R_duty,G_duty,B_duty,C_duty])
    ax.add_patch(rect)  # 長方形rectを置き換える。

    red_per = float(R_in) * 100 / 65535
    green_per = float(G_in) * 100/ 65535
    blue_per = float(B_in) * 100 / 65535
    clear_per = float(C_in) * 100 / 65535
    str = "red={:2.3f}% green={:2.3f}% blue={:2.3f}% clear={:2.3f}%".format(red_per, green_per, blue_per, clear_per)
    print(str)
    color_text.set_text(str)
    plt.draw()
    plt.savefig("sensored_color.png")
    plt.pause(0.01)  # この間にdrawが実行される。


# 以降はメインプログラム
import TCS34725

TCS34725.setup()

# Figureを作成
fig, ax = plt.subplots() # figureとaxesを作成
plt.ion() # インタラクティブモードにする。
color_text = plt.text(0, 0.1, "", size = 10, color = "black")

try:
    while True:
        clear, red, green, blue = TCS34725.read()
        print("clear={}, red={}, green={}, blue={}".format(clear, red, green, blue) )
        set_color(red, green, blue, clear)

except KeyboardInterrupt:
    pass
