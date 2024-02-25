const express = require('express');
const multer = require('multer');
const { startRecording, stopRecording,playAudio } = require('./recorder.js');

const app = express()
const upload = multer({dest: 'uploads'});

app.post('/upload', upload.single('audio'),(req,res)=>{
    if(!req.file){
        return res.status(400).send('No audio files provided');
    }

    res.send('File uploaded successfully');
})

app.get('/start-recording', (req, res) => {
    try {
      // Code to start the audio recording
      startRecording();
  
      // Send a response indicating the recording has started
      res.send('Audio recording started');
    } catch (error) {
      console.error('Error starting audio recording:', error);
      res.status(500).send('Error starting audio recording');
    }
  });

let isRecording = false

app.get('/stop-recording', (req, res) => {
    if (isRecording) {
      // Call the stopRecording function from your recording module
      stopRecording()
        .then(() => {
          // Recording stopped successfully
          isRecording = false;
          res.send('Recording stopped');
        })
        .catch((error) => {
          // Failed to stop recording
          console.error('Failed to stop recording:', error);
          res.status(500).send('Failed to stop recording');
        });
    } else {
      // Recording is not in progress
      res.send('No recording in progress');
    }
  });

 // Route to handle the playback recording request
app.get('/playback-recording', async (req, res) => {
    const recordedFilePath = req.query.filePath;
  
    if (!recordedFilePath) {
      res.status(400).send('Please provide a file path for playback');
      return;
    }
  
    try {
      // Call the playbackRecording function from your playback module
      await playbackRecording(recordedFilePath);
  
      // Set the appropriate headers for audio playback
      res.setHeader('Content-Type', 'audio/wav');
      res.setHeader('Content-Disposition', `attachment; filename="${recordedFilePath}"`);
  
      // Send the response
      res.sendFile(recordedFilePath);
    } catch (error) {
      console.error('Failed to playback recording:', error);
      res.status(500).send('Failed to playback recording');
    }
  });



app.listen(3000, ()=>{
    console.log('server is running on port 3000');
})