const fs = require('fs');
const path = require('path');
const wav = require('wav');
const moment = require('moment');

function listAllAudio(directory) {
  const audioList = [];

  fs.readdirSync(directory).forEach((filename) => {
    if (filename.endsWith('.wav')) {
      const filepath = path.join(directory, filename);
      const audioInfo = {};

      try {
        const wavFile = new wav.Reader();
        wavFile.on('format', (format) => {
          const durationSeconds = format.subchunk2Size / (format.sampleRate * format.channels * (format.bitDepth / 8));
          const durationStr = moment.utc(durationSeconds * 1000).format('HH:mm:ss');
          const modTime = fs.statSync(filepath).mtime;
          const modTimeStr = moment(modTime).format('YYYY-MM-DD');

          audioInfo.filename = filename;
          audioInfo.durationStr = durationStr;
          audioInfo.modTimeStr = modTimeStr;
        });

        fs.createReadStream(filepath).pipe(wavFile);
      } catch (error) {
        console.error(`Could not process file ${filename}: ${error.message}`);
      }

      audioList.push(audioInfo);
    }
  });

  return audioList;
}

// Example usage
const directory = '/path/to/audio/files';
const audioInfoList = listAllAudio(directory);
audioInfoList.forEach((audioInfo) => {
  const { filename, durationStr, modTimeStr } = audioInfo;
  console.log(`File: ${filename}`);
  console.log(`Duration: ${durationStr}`);
  console.log(`Last modified: ${modTimeStr}`);
  console.log('---');
});