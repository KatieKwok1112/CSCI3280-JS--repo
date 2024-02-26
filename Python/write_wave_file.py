import struct

def write_wave_file(output_file, audio_data, sample_rate):
    # WAV file format constants
    num_channels = 1  # Mono audio
    bytes_per_sample = 2  # 16-bit audio samples

    # Calculate the size of the audio data and the entire file
    num_frames = len(audio_data)
    subchunk2_size = num_frames * num_channels * bytes_per_sample
    chunk_size = 36 + subchunk2_size

    # Open the output file in binary mode
    with open(output_file, "wb") as file:
        # Write the RIFF chunk descriptor
        file.write(b"RIFF")
        file.write(struct.pack("<I", chunk_size))
        file.write(b"WAVE")

        # Write the fmt subchunk
        file.write(b"fmt ")
        file.write(struct.pack("<I", 16))  # Subchunk1 size
        file.write(struct.pack("<H", 1))  # Audio format (PCM)
        file.write(struct.pack("<H", num_channels))
        file.write(struct.pack("<I", sample_rate))
        file.write(struct.pack("<I", sample_rate * num_channels * bytes_per_sample))
        file.write(struct.pack("<H", num_channels * bytes_per_sample))
        file.write(struct.pack("<H", bytes_per_sample * 8))

        # Write the data subchunk
        file.write(b"data")
        file.write(struct.pack("<I", subchunk2_size))
        
        # Write the audio data
        for sample in audio_data:
            file.write(struct.pack("<h", sample))

    print("Wave file written successfully.")

# Example usage
output_file = "output.wav"
audio_data = [0, 100, 200, 300, 400]  # Example audio data as list of samples (16-bit signed integers)
sample_rate = 44100

write_wave_file(output_file, audio_data, sample_rate)