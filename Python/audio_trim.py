import wave
import pydub


def trim_audio(input_file, output_file, start_time, end_time):
    audio = pydub.AudioSegment.from_wav(input_file)
    start_time_ms = start_time * 1000  # Convert start time to milliseconds
    end_time_ms = end_time * 1000  # Convert end time to milliseconds
    trimmed_audio = audio[start_time_ms:end_time_ms]
    trimmed_audio.export(output_file, format="wav")

# Usage example
input_file = "trial.wav"
output_file = "trimmed_audio.wav"
start_time = 2  # Start trimming from 2 seconds
end_time = 4  # End trimming at 10 seconds

trim_audio(input_file, output_file, start_time, end_time)