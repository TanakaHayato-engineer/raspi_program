def get_RGB_duty(code):  # 引数：HTMLカラーコード（16進数6桁）
    red = (code & 0xFF0000) >> 16
    green = (code & 0xFF00) >> 8
    blue = code & 0xFF
    red = float(red) / 255  # 整数（0〜255）を小数（0〜1）に変換する。
    green = float(green) / 255
    blue = float(blue) / 255
    return red, green, blue

def get_RGB_percent(code):  # 引数：HTMLカラーコード（16進数6桁）
    red = (code & 0xFF0000) >> 16
    green = (code & 0xFF00) >> 8
    blue = code & 0xFF
    red = float(red) * 100 / 255  # 整数（0〜255）をパーセント（0〜100）に変換する。
    green = float(green) * 100 / 255
    blue = float(blue) * 100 / 255
    return red, green, blue

def draw(code):
    import matplotlib.pyplot as plt
    import matplotlib.patches as pat
    # Figureを作成
    fig, ax = plt.subplots()
    # 軸目盛りラベルを消す
    plt.tick_params(labelbottom=False,
                labelleft=False,
                labelright=False,
                labeltop=False)
    # 軸目盛り線を消す
    plt.tick_params(bottom=False,
                left=False,
                right=False,
                top=False)

    red, green, blue = get_RGB_duty(code)
    rect = pat.Rectangle(xy=(0, 0.2), width=1.0, height=1.0, color=[red,green,blue])  # 左下の座標(0,0.2), 横幅1.0, 高さ1.0
    ax.add_patch(rect)  # Axesにrectを追加

    red_per, green_per, blue_per = get_RGB_percent(code)
    str = "red={:2.3f}% green={:2.3f}% blue={:2.3f}%".format(red_per, green_per, blue_per)
    print(str)
    ax.text(0, 0.1, str, size = 10, color = "black")
    plt.savefig("kogane.png")
    plt.show()
