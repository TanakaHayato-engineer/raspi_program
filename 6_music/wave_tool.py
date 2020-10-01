import wave
import struct

channels = 2
sample_width = 2
sample_rate = 44100
sample_bits = sample_width * 8
max_gain = 2 ** sample_bits / 2 - 1

def open(output_file_name, sampling_rate=44100):
    global sample_rate
    sample_rate = sampling_rate
    output_wave_file = wave.open(output_file_name, "wb")
    output_wave_file.setnchannels(channels)
    output_wave_file.setsampwidth(sample_width)
    output_wave_file.setframerate(sample_rate)
    return output_wave_file

def close(output_wave_file):
    output_wave_file.close()

def write(file, data, gain=max_gain):
    file.writeframesraw(b"".join([struct.pack("h", int(x*gain) ) for x in data]))
