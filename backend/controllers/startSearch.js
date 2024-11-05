const { exec } = require('child_process');
const path = require('path');

const startSearch = async () => {
  const inputFilePath = path.join(__dirname, '..', 'uploads', 'whitelist.csv');
  const outputFilePath = path.join(__dirname, '..', 'output', 'extracted_data.csv');

  return new Promise((resolve, reject) => {
    const command = `python openai_imprint_scraper.py ${inputFilePath} ${outputFilePath}`;
    
    exec(command, (error, stdout, stderr) => {
      if (error) return reject(`Error: ${error.message}`);
      if (stderr) return reject(`stderr: ${stderr}`);

      console.log(`stdout: ${stdout}`);
      resolve(stdout);
    });
  });
};

module.exports = startSearch;
