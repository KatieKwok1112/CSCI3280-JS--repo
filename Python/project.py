import pyaudio
import wave
import threading
from tkinter import messagebox

CHUNK_SIZE = 1024 #1024 audio frames will be read or processed at a time
FORMAT = pyaudio.paInt16 #correspond to 16-bit signed integer PCM encoding
CHANNELS = 1 #1 audio channels
SAMPLE_RATE = 44100 #number of samples per second in the audio stream
RECORD_SECONDS = 5 #duration of recording
WAVE_OUTPUT_FILENAME = "trial.wav"

file_exists = False 

def threading_rec(x): #record
    if x == 1:
        # If recording is selected, then the thread is activated
        t1 = threading.Thread(target=record_audio)
        t1.start()
    elif x == 2: #stop
        # To stop, set the flag to false
        global recording
        recording = False
        messagebox.showinfo(message="Recording finished")
    elif x >= 3:
        # To play a recording, it must exist
        if file_exists:
            speed = 1
            if x == 4:
                speed = 2
            elif x == 5:
                speed = 0.5
            # Read the recording if it exists and play it
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
            p = pyaudio.PyAudio() #initialize PyAudio Library
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=int (wf.getframerate()/speed),
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