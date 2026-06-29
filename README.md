# Python Audio Processing Toolkit

A collection of Python projects demonstrating audio recording, playback, digital signal processing (DSP), and real-time audio visualization. This repository showcases how to capture audio from a microphone, analyze voice signals, visualize waveforms and frequency spectra, and build live audio analyzers using Python.


## Features

- Record audio for a fixed duration
- Record audio using Voice Activity Detection (VAD)
- Save recordings as WAV files
- Playback recorded audio
- Display audio waveforms
- Generate spectrograms
- Perform Fast Fourier Transform (FFT) analysis
- Real-time waveform visualization
- Real-time frequency spectrum analysis
- Combined real-time amplitude and magnitude analyzer


## Technologies Used

- Python 3
- PyAudio
- NumPy
- Matplotlib
- SciPy


## Project Structure

```text
Python-Audio-Processing-Toolkit/
│
├── processing/ 
│   └── voice_processing.py 
│
├── realtime/
│   ├── rtaa_amplitude.py
│   ├── rtaa_magnitude.py
│   └── rtaa_full.py
│
├── recording/
│   ├── fixed_time_recorder.py
│   └── voice_activity_recorder.py
│
├── images/
├── requirements.txt
├── README.md
└── LICENSE
```
---

## Installation

### 1. Clone the repository

``` bash
git clone https://github.com/Matin-python/Python-Audio-Processing-Toolkit.git
cd Python-Audio-Processing-Toolkit
```

### 2. (Optional) Create a virtual environment

``` bash 
python -m venv venv
```

Activate it:

**Windows**

``` bash
venv\Scripts\activate
```

**Linux/macOS**

``` bash
source venv/bin/activate
```

### 3. Install the required packages

``` bash
pip install -r requirements.txt
```


## Modules

### 1. Voice Processing

Records audio and performs several signal-processing operations, including:

- Waveform plotting
- Spectrogram generation
- Fast Fourier Transform (FFT)


### 2. Voice Activity Recorder

Starts recording automatically when speech is detected and stops after several seconds of silence.

Features:

- Voice Activity Detection (VAD)
- Automatic start/stop recording
- Live volume indicator
- Waveform visualization
- FFT analysis
- Audio playback


### 3. Fixed-Time Audio Recorder

Records audio for a specified duration, saves it as a WAV file, plays it back, and visualizes:

- Waveform
- Spectrogram
- Frequency Spectrum (FFT)


### 4. Real-Time Audio Analyzer

Includes three real-time visualization tools:

- Live waveform (Amplitude)
- Live frequency spectrum (Magnitude)
- Combined waveform and spectrum analyzer

The analyzer continuously captures audio from the microphone and updates the graphs in real time.


## Example Output

The toolkit can generate visualizations such as:

- Audio waveform
- Spectrogram
- FFT spectrum
- Live amplitude graph
- Live frequency spectrum

###### Images will upload.


## Future Improvements

- Noise reduction
- Audio filtering
- Pitch detection
- Voice recognition
- Speech-to-text integration
- MFCC feature extraction
- Audio feature extraction
- Real-time audio effects
- Audio classification using Machine Learning

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Author

**Mohammad Reza Bakhshandeh**

Electrical Engineering (Electronics) Graduate

Interested in Python Development, Digital Signal Processing (DSP), Computer Vision, Machine Learning, and Artificial Intelligence.
