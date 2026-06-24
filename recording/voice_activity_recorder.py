"""
Record your voice since you start speaking until you stop speaking for 3 seconds.
Then it playback
"""
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Configuration
CHUNK = 1024
SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 1000
SILENCE_DURATION = 50

def record_with_vad():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    
    print("Voice Activity Detection Ready 🎤")
    print("Speak into the microphone...")
    
    audio_data = np.array([], dtype=np.int16)
    is_recording = False
    silence_counter = 0
    
    try:
        while True:
            # Read audio
            data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            peak = np.average(np.abs(data)) * 2
            
            # Visual feedback
            bars = "█" * int(50 * min(1.0, peak / 30000))
            print(f"\rVolume: [{bars:<50}] {int(peak):5d}", end="", flush=True)
            
            # Voice detection
            if peak > SILENCE_THRESHOLD and not is_recording:
                is_recording = True
                audio_data = np.array([], dtype=np.int16)
                print("\n🔴 Recording started...")
            
            if is_recording:
                audio_data = np.append(audio_data, data)
                
                if peak < SILENCE_THRESHOLD:
                    silence_counter += 1
                else:
                    silence_counter = 0
                
                if silence_counter > SILENCE_DURATION:
                    print("\n🟢 Recording stopped")
                    break
                    
    except KeyboardInterrupt:
        print("\n⚠️ Stopped by user")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return audio_data

# Record audio
audio = record_with_vad()

if len(audio) > 0:
    # Plot results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Waveform
    time = np.arange(len(audio)) / SAMPLE_RATE
    ax1.plot(time, audio)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title(f'Recorded Audio ({len(audio)/SAMPLE_RATE:.2f}s)')
    ax1.grid(True)
    
    # FFT
    n = len(audio)
    freqs = fftfreq(n, 1/SAMPLE_RATE)[:n//2]
    fft_vals = np.abs(fft(audio))[:n//2]
    ax2.semilogx(freqs[freqs <= 4000], fft_vals[freqs <= 4000])
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    ax2.set_title('Frequency Spectrum')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()
else:
    print("No audio recorded!")



p = pyaudio.PyAudio()
output = p.open(
    format=pyaudio.paInt16,
    channels= 1,
    rate= SAMPLE_RATE,
    output= True,
    frames_per_buffer= CHUNK
)

data_out = np.chararray.tostring(audio.astype(np.int16))
output.write(data_out)
