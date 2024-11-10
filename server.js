const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const app = express();
const port = 3000;

app.use(express.json());

app.post('/merge', (req, res) => {
  const { videoUrl, audioUrl, subtitleUrl } = req.body;

  if (!videoUrl || !audioUrl || !subtitleUrl) {
    return res.status(400).send('Missing parameters');
  }

  const outputFile = `output-${Date.now()}.mp4`;

  // Define the path to the shell script
  const scriptPath = path.join(__dirname, 'merge_video_audio_subtitles.sh');

  // Build the shell command to execute the script with the parameters
  const command = `bash ${scriptPath} "${videoUrl}" "${audioUrl}" "${subtitleUrl}" "${outputFile}"`;

  // Execute the command via exec()
  exec(command, (err, stdout, stderr) => {
    if (err) {
      return res.status(500).send(`Error: ${stderr}`);
    }

    // Log output for debugging
    console.log(stdout);

    // Return the merged video file for download
    res.download(outputFile, (err) => {
      if (err) {
        return res.status(500).send('Error downloading file');
      }
    });
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
