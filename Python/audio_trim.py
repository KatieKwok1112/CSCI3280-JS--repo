import struct


    # Example usage
input_file = "trial.wav"
output_file = "output.wav"
start_time = 1  # Start time in seconds
end_time = 2  # End time in seconds
new_audio_data = [500, 600, 700]  # New audio data to overwrite the trimmed section
sample_rate = 44100



def audio_trim(input_file, output_file, start_time, end_time, new_audio_data, sample_rate):
    # Read the input wave file
    with open(input_file, "rb") as file:
        riff = file.read(4)  # RIFF chunk descriptor
        file_size = struct.unpack("<I", file.read(4))[0]  # File size
        wave = file.read(4)  # WAVE format

        # Find the "fmt " subchunk
        fmt = file.read(4)
        fmt_chunk_size = struct.unpack("<I", file.read(4))[0]
        audio_format = struct.unpack("<H", file.read(2))[0]
        num_channels = struct.unpack("<H", file.read(2))[0]
        sample_rate = struct.unpack("<I", file.read(4))[0]
        byte_rate = struct.unpack("<I", file.read(4))[0]
        block_align = struct.unpack("<H", file.read(2))[0]
        bits_per_sample = struct.unpack("<H", file.read(2))[0]

        # Find the "data" subchunk
        data = file.read(4)
        data_chunk_size = struct.unpack("<I", file.read(4))[0]

        # Calculate the start and end positions in the audio data
        bytes_per_sample = bits_per_sample // 8
        frames_per_second = sample_rate * num_channels
        start_position = int(start_time * frames_per_second * bytes_per_sample)
        end_position = int(end_time * frames_per_second * bytes_per_sample)

        # Adjust the data chunk size based on the trimmed audio
        new_data_chunk_size = end_position - start_position
        new_file_size = file_size - data_chunk_size + new_data_chunk_size

        # Open the output file in binary mode
        with open(output_file, "wb") as output:
            # Write the RIFF chunk descriptor
            output.write(riff)
            output.write(struct.pack("<I", new_file_size))
            output.write(wave)

            # Write the fmt subchunk
            output.write(fmt)
            output.write(struct.pack("<I", fmt_chunk_size))
            output.write(struct.pack("<H", audio_format))
            output.write(struct.pack("<H", num_channels))
            output.write(struct.pack("<I", sample_rate))
            output.write(struct.pack("<I", byte_rate))
            output.write(struct.pack("<H", block_align))
            output.write(struct.pack("<H", bits_per_sample))

            # Write the data subchunk
            output.write(data)
            output.write(struct.pack("<I", new_data_chunk_size))

            # Skip to the start position in the input file
            file.seek(44 + start_position)

            # Write the trimmed audio data from the input file
            output.write(file.read(new_data_chunk_size))

            # Adjust the file size and data chunk size
            file_size = new_file_size
            data_chunk_size = new_data_chunk_size

            # Write the new audio data at the start position
            for sample in new_audio_data:
                output.write(struct.pack("<h", sample))

    print("Audio trimmed and overwritten successfully.")

audio_trim(input_file, output_file, start_time, end_time, new_audio_data, sample_rate)

