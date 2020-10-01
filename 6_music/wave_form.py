import wave_tool
import math

class sin_wave():
    def __init__(self, frequency=440.0):
        self.frequency = frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.omega = 2.0 * math.pi * self.frequency

    def get(self, tick):
        value = math.sin(self.omega * tick / wave_tool.sample_rate)
        return value


class square_wave():
    def __init__(self, frequency=440.0, duty=0.5):
        self.frequency = frequency
        self.duty = duty

    def set_frequency(self, frequency):
        self.frequency = frequency

    def get(self, tick):
        if self.frequency == 0:
            return 0
        else:
            l = wave_tool.sample_rate / self.frequency
            change_point = l * self.duty

            if (tick % l) <= change_point:
                return 1
            else:
                return -1


class triangular_wave():
    def __init__(self, frequency=440.0):
        self.frequency = frequency

    def set_frequency(self, frequency):
        self.frequency = frequency

    def get(self, tick):
        if self.frequency == 0:
            return 0
        else:
            l = wave_tool.sample_rate / self.frequency
            slope = 1 / (l/4)
            tick_mod = tick % l
            if (tick_mod < l/4):
                value = slope * tick_mod
            elif (l/4 <= tick_mod < 3*l/4):
                value = 1 - slope * (tick_mod-l/4)
            else:  # 3*l/4 <= tick_mod < lの場合
                value = -1 + slope * (tick_mod-3*l/4)
            return value
