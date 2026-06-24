"""
Record your voice for 5 seconds, do some processing on your voice, and plot it.
You can change the duration of the recording.
"""
import pyaudio
import numpy as np
import matplotlib.pyplot as plt


p = pyaudio.PyAudio()

TIME_OF_RECORDING = 5
FORMAT = pyaudio.paInt16
CHUNK = 1024
SAMPLE_RATE = 16000

stream = p.open(
    format=FORMAT,
    channels= 1,
    rate= SAMPLE_RATE,
    input= True,
    frames_per_buffer= CHUNK
)

print ('Start Recording...')
au = np.array([])
for i in range (int(TIME_OF_RECORDING * SAMPLE_RATE/CHUNK)):
    data = np.fromstring(stream.read(CHUNK), dtype= np.int16)
    au = np.append(au, data)
print ('END')

plt.plot(au)
plt.show()

plt.specgram(au, Fs=SAMPLE_RATE)
plt.show()

out_fft = np.fft.fft(au)
out_fft = out_fft[0:SAMPLE_RATE//2]
out_fft = np.abs(out_fft)
plt.plot(out_fft)
plt.show()

stream.stop_stream()
stream.close()
p.terminate()

