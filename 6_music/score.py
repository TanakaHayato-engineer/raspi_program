import re
import wave_tool

TUNING = 440  # 基準となるオクターブ4の「ラ」の周波数

NOTE_DIFF = {"c":  -9, "c+": -8, "d-": -8, "d":  -7, "d+": -6,
             "e-": -6, "e":  -5, "f":  -4, "f+": -3, "g-": -3,
             "g":  -2, "g+": -1, "a-": -1, "a":   0, "a+":  1,
             "b-": 1, "b": 2, "r": None}

def score_to_sequence(song, tempo=120):
    tick_position = 0

    note_pattern = re.compile(r"^([a-gr])(\+|\-)?(\d+)?", re.IGNORECASE)

    sequence = list()
    for tone in song:
        note_match = note_pattern.search(tone[0])
        (note_code, accidential, octave) = note_match.groups()
        #print((note_code, accidential, octave))
        note_acc = note_code + (accidential if accidential else "")  # シャープやフラットの文字を付加
        #print("note_acc=", note_acc, " octave=", octave)
        # 音程の取得と周波数の計算
        if note_code == "r":  # 休符（rest）の場合
            note_frequency = 0
        else:  # 音符の場合
            note_diff = NOTE_DIFF[note_acc]
            octave = int(octave)  # 文字列を整数に変換
            note_frequency = TUNING * \
              (2 ** (octave - 4)) * \
              ((2 ** note_diff) ** (1 / 12.0))
            #print("note_diff=", note_diff, " note_freq=", note_frequency)

        # 音符（または休符）の長さ
        note_length = tone[1]
        note_on_tick = wave_tool.sample_rate * (60.0 / tempo) * (4.0 / note_length)
        if len(tone) > 2:
            if tone[2] == ".":  # 付点音符（または休符）の場合
                    note_on_tick *= 1.5
                    #print("tone=", tone, "note_on_tick=")

        # 発音の終了ティックを更新する
        tick_position += note_on_tick

        # シーケンス（音楽データ）に追記
        sequence.append((note_frequency, int(tick_position)))

    return sequence


class sequencer(object):
    def __init__(self):
        self.tracks = dict()
        self.volumes = dict()
        self.sequences = dict()

    def add_track(self, track_id, sequence_data, form, volume=1.0):
        self.tracks[track_id] = form
        self.volumes[track_id] = volume
        self.sequences[track_id] = sequence_data

    def get_value(self, tick, stereo=True):
        for (track_id, sequence_data) in self.sequences.items():
            if tick > sequence_data[0][1]:
                #print("sequence_data[0]=", sequence_data[0])
                del sequence_data[0]

            if len(sequence_data) == 0:
                return None

            (frequency, off_tick) = sequence_data[0]
            form = self.tracks[track_id]
            form.set_frequency(frequency)

        if stereo:
            return [ self.tracks[0].get(tick) * self.volumes[0] , self.tracks[1].get(tick) * self.volumes[1] ]  # [ 左チャンネル, 右チャンネル ]
        else:
            result = 0
            for (track_id, form) in self.tracks.items():
                result += form.get(tick) * self.volumes[track_id]
            result = result / len(self.tracks)  # 正規化して、足し込み
            return [result, result]


def render(file_name, sequencer, stereo=True, gain=wave_tool.max_gain):
    file = wave_tool.open(file_name)

    tick = 0
    while True:
        data = sequencer.get_value(tick, stereo)
        if data is None:
            break
        wave_tool.write(file, data, gain)

        tick += 1

        if (tick % 50000) == 0:
            print("{:8d} ticks ... ".format(tick))

    wave_tool.close(file)
