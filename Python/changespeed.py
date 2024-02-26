import struct

def change_audio_speed(input_file, output_file, speed_factor):
    if speed_factor <= 0:
        raise ValueError("Speed factor must be greater than zero.")

    with open(input_file, "rb") as f:
        riff_chunk = f.read(12)
        fmt_chunk_header = f.read(8)
        fmt_chunk = f.read(16)
        data_chunk_header = f.read(8)
        data_chunk_size = struct.unpack("<I", f.read(4))[0]
        audio_data = f.read()

    # Update the sample rate in the fmt-chunk
    sample_rate = struct.unpack("<I", fmt_chunk[4:8])[0]
    new_sample_rate = int(sample_rate * speed_factor)

    # Update the data chunk size
    new_data_chunk_size = int(data_chunk_size / speed_factor)

    # Modify the audio data to change the speed
    if speed_factor == 1:
        modified_audio_data = audio_data
    else:
        modified_audio_data = b""
        step = int(1 / speed_factor)
        for i in range(0, len(audio_data), step):
            modified_audio_data += audio_data[i:i+step]

    # Update the riff chunk size
    new_riff_chunk_size = 36 + new_data_chunk_size

    # Create the modified audio file
    with open(output_file, "wb") as f:
        f.write(riff_chunk)
        f.write(struct.pack("<I", new_riff_chunk_size))
        f.write(fmt_chunk_header)
        f.write(fmt_chunk)
        f.write(data_chunk_header)
        f.write(struct.pack("<I", new_data_chunk_size))
        f.write(modified_audio_data)