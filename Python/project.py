import pyaudio
import wave
import threading
from tkinter import messagebox

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "trial.wav"

# Functions to play, stop, and record audio in Python voice recorder
# The recording is done as a thread to prevent it from being the main process
def threading_rec(x):
    if x == 1:
        # If recording is selected, then the thread is activated
        t1 = threading.Thread(target=record_audio)
        t1.start()
    elif x == 2:
        # To stop, set the flag to false
        global recording
        recording = False
        messagebox.showinfo(message="Recording finished")
    elif x == 3:
        # To play a recording, it must exist
        if file_exists:
            # Read the recording if it exists and play it
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            data = wf.readframes(CHUNK_SIZE)
            while data:
                stream.write(data)
                data = wf.readframes(CHUNK_SIZE)
            stream.stop_stream()
            stream.close()
            p.terminate()
        else:
            # Display an error if none is found
            messagebox.showerror(message="Record something to play")

# Recording function
def record_audio():
    # Declare global variables
    global recording
    # Set to True to record
    recording = True
    global file_exists
    # Create a file to save the audio
    messagebox.showinfo(message="Recording Audio. Speak into the mic")
    frames = []
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)
    while recording:
        data = stream.read(CHUNK_SIZE)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    file_exists = True
