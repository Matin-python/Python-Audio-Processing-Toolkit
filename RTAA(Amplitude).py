"""
Real-time Audio Analyzer(Amplitude)
"""
import pyaudio
import numpy as np
import matplotlib.pyplot as plt


p = pyaudio.PyAudio()

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

plt.ion()       # Interactive mode ON
fig, ax = plt.subplots(figsize=(7, 4))
x = np.arange(0, 2*CHUNK, 2)
line, = ax.plot (x, np.random.rand(CHUNK), 'r')
ax.set_xlim(0, CHUNK)
ax.set_ylim(-30000,30000)
ax.set_xlabel('Sample Number')
ax.set_ylabel('Amplitude')
ax.set_title('Waveform (Live)')
ax.grid(True, alpha=0.2)        # Visual only

fig.show()

au = np.array([])

running = True
def on_close(event):
    global running
    running = False

fig.canvas.mpl_connect('close_event', on_close)

try:
    while running:
        # Read audio data
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
            
        # Update time domain plot
        line.set_ydata(audio_data)

        max_amp = np.max(np.abs(audio_data))
        if max_amp > 1000:
            ax.set_ylim(-max_amp*1.1, max_amp*1.1)

        # Refresh plot
        fig.canvas.draw()
        fig.canvas.flush_events()

        au = np.append(au, audio_data)
        if len(au) > SAMPLE_RATE * 5:  # Keep only last 5 seconds
            au = au[-SAMPLE_RATE * 5:]

except KeyboardInterrupt:
    print("\nStopped by user")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    plt.ioff()

