const fs = require('fs');

const SAMPLE_RATE = 44100;
const BITS_PER_SAMPLE = 16;
const CHANNELS = 1;
const RECORD_SECONDS = 5;
const WAVE_OUTPUT_FILENAME = 'output.wav';

let recording = false;
let fileExists = false;
let audioData = [];

// Function to start recording audio
function startRecording() {
  recording = true;
  fileExists = false;
  audioData = [];

  console.log('Recording audio. Speak into the microphone.');

  setTimeout(() => {
    stopRecording();
  }, RECORD_SECONDS * 1000);
}

// Function to stop recording audio
function stopRecording() {
  recording = false;
  fileExists = true;

  console.log('Recording finished.');

  // Construct the WAV file header and data chunks
  const header = constructWavHeader(audioData.length * 2);
  const fmtChunk = constructFmtChunk();
  const dataChunk = constructDataChunk(audioData);

  // Combine the chunks
  const wavData = Buffer.concat([header, fmtChunk, dataChunk]);

  // Write the WAV data to a file
  fs.writeFileSync(WAVE_OUTPUT_FILENAME, wavData);

  console.log('WAV file saved:', WAVE_OUTPUT_FILENAME);
}

// Function to construct the WAV file header
function constructWavHeader(dataSize) {
  const header = Buffer.alloc(44);

  // Chunk ID (RIFF)
  header.write('RIFF', 0);
  // File size - 8 (total file size minus the first 8 bytes)
  header.writeInt32LE(dataSize + 36, 4);
  // Format (WAVE)
  header.write('WAVE', 8);

  return header;
}

function playAudio() {
    const playProcess = spawn('pcm-play', ['-r', SAMPLE_RATE, '-b', BITS_PER_SAMPLE, '-c', CHANNELS, WAVE_FILE_PATH]);
  
    playProcess.on('error', (err) => {
      console.error('Failed to play audio:', err);
    });
  
    playProcess.on('exit', (code) => {
      if (code !== 0) {
        console.error('Audio playback process exited with code:', code);
      }
    });
  }

// Function to construct the fmt-chunk
function constructFmtChunk() {
  const fmtChunk = Buffer.alloc(24);

  // Subchunk 1 ID (fmt)
  fmtChunk.write('fmt ', 0);
  // Subchunk 1 size (16 for PCM)
  fmtChunk.writeInt32LE(16, 4);
  // Audio format (PCM)
  fmtChunk.writeInt16LE(1, 8);
  // Number of channels (1 for mono, 2 for stereo)
  fmtChunk.writeInt16LE(CHANNELS, 10);
  // Sample rate
  fmtChunk.writeInt32LE(SAMPLE_RATE, 12);
  // Byte rate (Sample rate * Number of channels * Bits per sample / 8)
  fmtChunk.writeInt32LE(SAMPLE_RATE * CHANNELS * (BITS_PER_SAMPLE / 8), 16);
  // Block align (Number of channels * Bits per sample / 8)
  fmtChunk.writeInt16LE(CHANNELS * (BITS_PER_SAMPLE / 8), 20);
  // Bits per sample
  fmtChunk.writeInt16LE(BITS_PER_SAMPLE, 22);

  return fmtChunk;
}

// Function to construct the data-chunk
function constructDataChunk(audioData) {
  const dataSize = audioData.length * 2;
  const dataChunk = Buffer.alloc(8 + dataSize);

  // Subchunk 2 ID (data)
  dataChunk.write('data', 0);
  // Subchunk 2 size (size of audio data in bytes)
  dataChunk.writeInt32LE(dataSize, 4);

  // Write audio data
  for (let i = 0; i < audioData.length; i++) {
    dataChunk.writeInt16LE(audioData[i], 8 + i * 2);
  }

  return dataChunk;
}

// Function to process the recorded audio data
function processAudioData(data) {
  audioData.push(data);
}

module.exports = {startRecording,stopRecording,playAudio}
