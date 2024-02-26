import pyaudio
# Function to save audio file
import wave

def save_audio(filename, frames, p):
    num_frames = len(frames)
    num_channels = CHANNELS
    sample_width = p.get_sample_size(FORMAT)
    sample_rate = SAMPLE_RATE

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    file_exists = True

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