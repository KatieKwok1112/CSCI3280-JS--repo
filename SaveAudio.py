import pyaudio
import wave

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 44100

# Function to save audio file
def save_audio(filename, frames):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Create PyAudio object
p = pyaudio.PyAudio()

# Define the number of audio files you want to save
num_files = 5

for i in range(num_files):
    # Create a new filename for each iteration
    filename = f"audio_{i}.wav"
    frames = []

    # Start recording
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)

    print(f"Recording {filename}...")

    # Record audio for a specified duration
    for _ in range(int(SAMPLE_RATE / CHUNK_SIZE * RECORD_SECONDS)):
        data = stream.read(CHUNK_SIZE)
        frames.append(data)

    # Stop recording
    stream.stop_stream()
    stream.close()

    # Save the audio file
    save_audio(filename, frames)

    print(f"Saved {filename}")

# Terminate PyAudio object
p.terminate()