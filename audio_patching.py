import pyaudio
import numpy as np


CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # 16-bit format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (Hz)
INPUT_DEVICE_INDEX = 4  # Device index found from select_mic.py
OUTPUT_DEVICE_INDEX = 14

SENSITIVITY = 0.1  # Adjust this value (1.0 = normal, > 1.0 = louder, < 1.0 = quieter)

p = pyaudio.PyAudio()


# Open the microphone stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                input_device_index=INPUT_DEVICE_INDEX,   # Select microphone
                output_device_index=OUTPUT_DEVICE_INDEX,
                frames_per_buffer=CHUNK)

print(f"Using microphone: {INPUT_DEVICE_INDEX}, Output: {OUTPUT_DEVICE_INDEX}")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)  # Convert to NumPy array
        audio_data = np.clip(audio_data * SENSITIVITY, -32768, 32767)  # Scale and clip
        stream.write(audio_data.astype(np.int16).tobytes())  # Convert back and play
except KeyboardInterrupt:
    print("\nStopping...")

stream.stop_stream()
stream.close()
p.terminate()
