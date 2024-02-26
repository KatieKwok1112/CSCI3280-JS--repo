import struct

def change_audio_speed(input_file, output_file, speed_factor):
    with open(input_file, "rb") as f:
        riff_chunk = f.read(12)
        fmt_chunk_header = f.read(8)
        fmt_chunk = f.read(16)
        data_chunk_header = f.read(8)
        data_chunk_size = struct.unpack("<I", f.read(4))[0]
        audio_data = f.read()

    # Update the sample rate in the fmt-chunk
    sample_rate = struct.unpack("<I", fmt_chunk[4:8])[0]
    new_sample_rate = round(sample_rate * speed_factor)
    new_fmt_chunk = fmt_chunk[:4] + struct.pack("<I", new_sample_rate) + fmt_chunk[8:]

    # Update the duration in the data-chunk
    num_samples = data_chunk_size // 2  # Assuming 16-bit audio
    new_num_samples = round(num_samples / speed_factor)
    new_data_chunk_size = new_num_samples * 2
    new_data_chunk_header = data_chunk_header[:4] + struct.pack("<I", new_data_chunk_size)

    # Calculate the modified audio data
    step = int(speed_factor)
    modified_audio_data = audio_data[::step]

    # Write the modified audio to the output file
    with open(output_file, "wb") as f:
        f.write(riff_chunk)
        f.write(fmt_chunk_header)
        f.write(new_fmt_chunk)
        f.write(data_chunk_header)
        f.write(new_data_chunk_header)
        f.write(struct.pack("<I", new_data_chunk_size))
        f.write(modified_audio_data)

# Usage example
input_file = "trial.wav"
output_file = "modified_audio.wav"
speed_factor = 1.5  # Increase the speed by 1.5 times

change_audio_speed(input_file, output_file, speed_factor)