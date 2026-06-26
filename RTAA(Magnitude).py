"""
Real-time Audio Analyzer(Magnitude)
"""
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

p = pyaudio.PyAudio()

CHUNK = 1024
SAMPLE_RATE = 16000

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    output=False,
    frames_per_buffer=CHUNK
)

# Setup for frequency bars
fig, ax = plt.subplots(figsize=(12, 6))

# Create frequency bands (logarithmic scale for better voice representation)
num_bars = 30
freqs = np.logspace(np.log10(80), np.log10(4000), num_bars)
bar_width = np.diff(np.append([80], freqs))
x_positions = np.arange(num_bars)

bars = ax.bar(x_positions, np.zeros(num_bars), width=0.8)
ax.set_xticks(x_positions[::3])
ax.set_xticklabels([f'{int(freqs[i])}' for i in range(0, len(x_positions), 3)], rotation=45)
ax.set_xlabel('Frequency (Hz) - Logarithmic Scale')
ax.set_ylabel('Magnitude')
ax.set_title('Real-time Voice Frequency Analysis')
ax.set_ylim(0, 1)
ax.grid(True, alpha=0.3, axis='y')

def update(frame):
    try:
        # Read audio data
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Apply window and compute FFT
        window = np.hanning(len(audio_data))
        fft_data = audio_data * window
        fft_vals = np.fft.rfft(fft_data)
        fft_magnitude = np.abs(fft_vals) / CHUNK
        
        # Create frequency vector
        fft_freqs = np.fft.rfftfreq(CHUNK, 1/SAMPLE_RATE)
        
        # Get magnitudes for each frequency band
        band_magnitudes = []
        for freq in freqs:
            # Find closest FFT bin
            idx = np.argmin(np.abs(fft_freqs - freq))
            band_magnitudes.append(fft_magnitude[idx])
        
        # Normalize
        band_magnitudes = np.array(band_magnitudes)
        if np.max(band_magnitudes) > 0:
            band_magnitudes = band_magnitudes / np.max(band_magnitudes)
        
        # Update bars
        for bar, height in zip(bars, band_magnitudes):
            bar.set_height(height)
            
        # Color bars based on typical voice frequency ranges
        for i, bar in enumerate(bars):
            if freqs[i] < 250:  # Bass/Low voice
                bar.set_color('#1f77b4')  # Blue
            elif freqs[i] < 2000:  # Mid voice (main speech range)
                bar.set_color('#ff7f0e')  # Orange
            else:  # High frequencies
                bar.set_color('#2ca02c')  # Green
                
    except Exception as e:
        print(f"Error: {e}")
    
    return bars

print("Live Frequency Display Started!")
print("Speak into your microphone to see real-time frequency analysis...")
print("Close the window to stop.")

ani = FuncAnimation(fig, update, interval=50, blit=False)
plt.tight_layout()
plt.show()

stream.stop_stream()
stream.close()
p.terminate()