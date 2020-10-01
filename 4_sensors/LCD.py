import smbus
import time

char_table = {
    u' ': [0x20],
    u'　': [0x20],
    u'!': [0x21],
    u'"': [0x22],
    u'#': [0x23],
    u'$': [0x24],
    u'%': [0x25],
    u'&': [0x26],
    u"'": [0x27],
    u'(': [0x28],
    u')': [0x29],
    u'*': [0x2a],
    u'+': [0x2b],
    u',': [0x2c],
    u'-': [0x2d],
    u'.': [0x2e],
    u'/': [0x2f],

    u'0': [0x30],
    u'1': [0x31],
    u'2': [0x32],
    u'3': [0x33],
    u'4': [0x34],
    u'5': [0x35],
    u'6': [0x36],
    u'7': [0x37],
    u'8': [0x38],
    u'9': [0x39],
    u':': [0x3a],
    u';': [0x3b],
    u'<': [0x3c],
    u'=': [0x3d],
    u'>': [0x3e],
    u'?': [0x3f],

    u'@': [0x40],
    u'A': [0x41],
    u'B': [0x42],
    u'C': [0x43],
    u'D': [0x44],
    u'E': [0x45],
    u'F': [0x46],
    u'G': [0x47],
    u'H': [0x48],
    u'I': [0x49],
    u'J': [0x4a],
    u'K': [0x4b],
    u'L': [0x4c],
    u'M': [0x4d],
    u'N': [0x4e],
    u'O': [0x4f],

    u'P': [0x50],
    u'Q': [0x51],
    u'R': [0x52],
    u'S': [0x53],
    u'T': [0x54],
    u'U': [0x55],
    u'V': [0x56],
    u'W': [0x57],
    u'X': [0x58],
    u'Y': [0x59],
    u'Z': [0x5a],
    u'[[': [0x5b],
    u'¥': [0x5c],
    u']]': [0x5d],
    u'^': [0x5e],
    u'_': [0x5f],

    u'`': [0x60],
    u'a': [0x61],
    u'b': [0x62],
    u'c': [0x63],
    u'd': [0x64],
    u'e': [0x65],
    u'f': [0x66],
    u'g': [0x67],
    u'h': [0x68],
    u'i': [0x69],
    u'j': [0x6a],
    u'k': [0x6b],
    u'l': [0x6c],
    u'm': [0x6d],
    u'n': [0x6e],
    u'o': [0x6f],

    u'p': [0x70],
    u'q': [0x71],
    u'r': [0x72],
    u's': [0x73],
    u't': [0x74],
    u'u': [0x75],
    u'v': [0x76],
    u'w': [0x77],
    u'x': [0x78],
    u'y': [0x79],
    u'z': [0x7a],
    u'(': [0x7b],
    u'|': [0x7c],
    u')': [0x7d],
    u'→': [0x7e],
    u'←': [0x7f],

    u'。': [0xa1],
    u'「': [0xa2],
    u'」': [0xa3],
    u'、': [0xa4],
    u'・': [0xa5],
    u'ヲ': [0xa6],
    u"ァ": [0xa7],
    u'ィ': [0xa8],
    u'ゥ': [0xa9],
    u'ェ': [0xaa],
    u'ォ': [0xab],
    u'ャ': [0xac],
    u'ュ': [0xad],
    u'ョ': [0xae],
    u'ッ': [0xaf],

    u'ー': [0xb0],
    u'ア': [0xb1],
    u'イ': [0xb2],
    u'ウ': [0xb3],
    u'エ': [0xb4],
    u'オ': [0xb5],
    u'カ': [0xb6],
    u'キ': [0xb7],
    u'ク': [0xb8],
    u'ケ': [0xb9],
    u'コ': [0xba],
    u'サ': [0xbb],
    u'シ': [0xbc],
    u'ス': [0xbd],
    u'セ': [0xbe],
    u'ソ': [0xbf],

    u'タ': [0xc0],
    u'チ': [0xc1],
    u'ツ': [0xc2],
    u'テ': [0xc3],
    u'ト': [0xc4],
    u'ナ': [0xc5],
    u'ニ': [0xc6],
    u'ヌ': [0xc7],
    u'ネ': [0xc8],
    u'ノ': [0xc9],
    u'ハ': [0xca],
    u'ヒ': [0xcb],
    u'フ': [0xcc],
    u'ヘ': [0xcd],
    u'ホ': [0xce],
    u'マ': [0xcf],

    u'ミ': [0xd0],
    u'ム': [0xd1],
    u'メ': [0xd2],
    u'モ': [0xd3],
    u'ヤ': [0xd4],
    u'ユ': [0xd5],
    u'ヨ': [0xd6],
    u'ラ': [0xd7],
    u'リ': [0xd8],
    u'ル': [0xd9],
    u'レ': [0xda],
    u'ロ': [0xdb],
    u'ワ': [0xdc],
    u'ン': [0xdd],
    u'゛': [0xde],
    u'゜': [0xdf],

    u'ガ': [0xb6, 0xde],
    u'ギ': [0xb7, 0xde],
    u'グ': [0xb8, 0xde],
    u'ゲ': [0xb9, 0xde],
    u'ゴ': [0xba, 0xde],
    u'ザ': [0xbb, 0xde],
    u'ジ': [0xbc, 0xde],
    u'ズ': [0xbd, 0xde],
    u'ゼ': [0xbe, 0xde],
    u'ゾ': [0xbf, 0xde],
    u'ダ': [0xc0, 0xde],
    u'ヂ': [0xc1, 0xde],
    u'ヅ': [0xc2, 0xde],
    u'デ': [0xc3, 0xde],
    u'ド': [0xc4, 0xde],
    u'バ': [0xca, 0xde],
    u'ビ': [0xcb, 0xde],
    u'ブ': [0xcc, 0xde],
    u'ベ': [0xcd, 0xde],
    u'ボ': [0xce, 0xde],
    u'パ': [0xca, 0xdf],
    u'ピ': [0xcb, 0xdf],
    u'プ': [0xcc, 0xdf],
    u'ペ': [0xcd, 0xdf],
    u'ポ': [0xce, 0xdf]
}

bus = smbus.SMBus(1)
addr = 0x3c

def setup(sa0 = 0, cursor = False, blink = False):

    if (sa0 == 0):
        addr = 0x3c
    else:
        addr = 0x3d

    clear()
    move_home()
    display_on(cursor, blink)
    clear()

# 現在の位置に文字を表示させる。
def write_char(c):
    bus.write_byte_data(addr, 0x40, c)

# 現在の位置に文字列を表示させる。
def write_string(s):
    for c in list(s):
        bus.write_byte_data(addr, 0x40, ord(c))

# 現在の位置に、文字コード指定された文字列を表示させる。
def write_string_in_int(s):
    for c in list(s):
        bus.write_byte_data(addr, 0x40, c)

def utf8_to_ascii(str):
    str_tmp = []
    for c in str:
        str_tmp += char_table[c]
    return str_tmp

def write_line(str = '', line = 0, align = 'left'):
    # 文字列が16文字に満たない場合、空白で埋める
    while (len(str) < 16):
        if (align == 'right'):
            str = ' ' + str
        else:
            str = str + ' '
    str_to_int = utf8_to_ascii(str)

    if (line == 1):
        bus.write_byte_data(addr, 0x00, (0x80 + 0x20))
    else:
        bus.write_byte_data(addr, 0x00, 0x80)

    write_string_in_int(str_to_int)

def write_2lines(str_in):
    str = utf8_to_ascii(str_in)
    #print("str=", str)
    str1 = str[0:16]
    bus.write_byte_data(addr, 0x00, 0x80) # 1行目先頭
    write_string_in_int(str1)

    str2 = str[16:32]
    bus.write_byte_data(addr, 0x00, (0x80 + 0x20)) # 2行目先頭
    write_string_in_int(str2)

def clear():
    bus.write_byte_data(addr, 0x00, 0x01)

def move_home():
    bus.write_byte_data(addr, 0x00, 0x02)

def move_2nd_line():
    bus.write_byte_data(addr, 0x00, (0x80 + 0x20)) # 2行目先頭

def move_xy(x, y):
    position = x + y * 0x20
    bus.write_byte_data(addr, 0x00, (0x80 + position))

def display_on(cursor = False, blink = False):
    cmd = 0x0c
    if (cursor):
        cmd += 0x02
    if (blink):
        cmd += 0x01
    bus.write_byte_data(addr, 0x00, cmd)

def display_off():
    bus.write_byte_data(addr, 0x00, 0x08)

# 輝度の変更
def set_contrast(contrast=0x7f):
    bus.write_byte_data(addr, 0x00, 0x2a)
    bus.write_byte_data(addr, 0x00, 0x79)
    bus.write_byte_data(addr, 0x00, 0x81)
    bus.write_byte_data(addr, 0x00, contrast)
    bus.write_byte_data(addr, 0x00, 0x78)
    bus.write_byte_data(addr, 0x00, 0x28)

# 与えた文字cが書き込み可能かを判定する。
# 書き込み可能ならば、その文字を返す。
# そうでなければ、スペース（半角）を返す。
def check_writable(c):
    if c >= 0x06 and c <= 0xff :
        return c
    else:
        return 0x20 # 空白文字
