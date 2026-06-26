"""
Real-time Audio Analyzer(Amplitude & Magnitude)
"""

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib

# Use TkAgg backend for better performance
matplotlib.use('TkAgg')

p = pyaudio.PyAudio()

FORMAT = pyaudio.paInt16
CHUNK = 1024 * 5
SAMPLE_RATE = 16000

stream = p.open(
    format=FORMAT,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    output=False,
    frames_per_buffer=CHUNK
)

# Setup the plot for frequency domain
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle('Real-time Audio Analyzer', fontsize=16)

# Frequency domain (spectrum)
freqs = np.fft.rfftfreq(CHUNK, 1/SAMPLE_RATE)
line_spec, = ax1.plot(freqs, np.random.rand(len(freqs)), 'b-')
ax1.set_xlim(20, 4000)  # Focus on human voice frequency range (20Hz - 4kHz)
ax1.set_ylim(0, 1)
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Magnitude')
ax1.set_title('Frequency Spectrum (Live)')
ax1.grid(True, alpha=0.3)

# Time domain (waveform)
x_time = np.arange(0, CHUNK)
line_time, = ax2.plot(x_time, np.random.rand(CHUNK), 'r-')
ax2.set_xlim(0, CHUNK)
ax2.set_ylim(-30000, 30000)
ax2.set_xlabel('Sample Number')
ax2.set_ylabel('Amplitude')
ax2.set_title('Waveform (Live)')
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# Store audio data
au = np.array([])

# Store dominant frequencies for history
dominant_freqs = []

def update(frame):
    global au, dominant_freqs
    
    try:
        # Read audio data
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Update time domain plot
        line_time.set_ydata(audio_data)
        
        # Calculate FFT for frequency domain
        # Apply Hanning window to reduce spectral leakage
        window = np.hanning(len(audio_data))
        fft_data = audio_data * window
        
        # Compute FFT
        fft_vals = np.fft.rfft(fft_data)
        fft_magnitude = np.abs(fft_vals) / CHUNK
        
        # Normalize
        if np.max(fft_magnitude) > 0:
            fft_magnitude = fft_magnitude / np.max(fft_magnitude)
        
        # Update frequency plot
        line_spec.set_ydata(fft_magnitude)
        
        # Find dominant frequency (excluding very low frequencies)
        # Skip frequencies below 80Hz to avoid DC offset and noise
        min_freq_idx = int(80 / (SAMPLE_RATE / CHUNK))
        if min_freq_idx < len(fft_magnitude):
            dominant_idx = np.argmax(fft_magnitude[min_freq_idx:]) + min_freq_idx
            dominant_freq = freqs[dominant_idx]
            dominant_freqs.append(dominant_freq)
            
            # Keep only last 50 values for average
            if len(dominant_freqs) > 50:
                dominant_freqs.pop(0)
            
            avg_freq = np.mean(dominant_freqs)
            
            # Update title with current dominant frequency
            ax1.set_title(f'Frequency Spectrum - Dominant Frequency: {dominant_freq:.1f} Hz (Avg: {avg_freq:.1f} Hz)', 
                         fontsize=10)
        
        # Update plot limits dynamically for waveform
        max_amp = np.max(np.abs(audio_data))
        if max_amp > 1000:
            ax2.set_ylim(-max_amp*1.1, max_amp*1.1)
        
        # Append to global array (optional - limit to 5 seconds of data)
        au = np.append(au, audio_data)
        if len(au) > SAMPLE_RATE * 5:  # Keep only last 5 seconds
            au = au[-SAMPLE_RATE * 5:]
        
    except Exception as e:
        print(f"Error: {e}")
    
    return line_time, line_spec

# Create animation
ani = FuncAnimation(fig, update, interval=30, blit=False)

print("Live Frequency Spectrum Display Started!")
print("Speak into your microphone to see the frequency response...")
print("Close the plot window to stop.")

plt.show()

# Cleanup when plot is closed
stream.stop_stream()
stream.close()
p.terminate()
print("Recording stopped.")