const express = require('express');
const multer = require('multer');

const app = express()
const upload = multer({dest: 'uploads'});

app.post('/upload', upload.single('audio'),(req,res)=>{
    if(!req.file){
        return res.status(400).send('No audio files provided');
    }

    res.send('File uploaded successfully');
})

app.get('/', (req,res)=>{
    if(Error){
        return res.status(404).json({success:"False", msg:"Error"})
    }
    res.status(200).json({success:"True", msg:"Welcome!"})
})

app.listen(3000, ()=>{
    console.log('server is running on port 3000');
})