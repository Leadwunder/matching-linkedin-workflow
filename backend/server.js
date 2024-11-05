const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const multer = require('multer');

const app = express();
const PORT = 5000;
app.use(cors());
app.use(express.json());
const upload = multer({ dest: 'uploads/' });

const uploadDir = path.join(__dirname, 'uploads');
let whitelistDownloaded = false;
let blacklistDownloaded = false;

// Upload endpoints for whitelist and blacklist files
app.post('/upload/whitelist', upload.single('file'), (req, res) => {
    if (!req.file) return res.status(400).json({ message: 'No file uploaded' });
    const oldPath = path.join(__dirname, req.file.path);
    const newPath = path.join(uploadDir, 'whitelist.csv');
    fs.renameSync(oldPath, newPath);
    res.json({ message: 'Whitelist uploaded successfully.' });
});

app.post('/upload/blacklist', upload.single('file'), (req, res) => {
    if (!req.file) return res.status(400).json({ message: 'No file uploaded' });
    const oldPath = path.join(__dirname, req.file.path);
    const newPath = path.join(uploadDir, 'blacklist.csv');
    fs.renameSync(oldPath, newPath);
    res.json({ message: 'Blacklist uploaded successfully.' });
});

// Start search endpoint
app.post('/start-search', async (req, res) => {
    const whitelistPath = path.join(uploadDir, 'whitelist.csv');
    const blacklistPath = path.join(uploadDir, 'blacklist.csv');
    const outputWhitelist = path.join(uploadDir, 'whitelist_linkedin.csv');
    const outputBlacklist = path.join(uploadDir, 'blacklist_linkedin.csv');

    try {
        exec(`python openai_imprint_scraper.py ${whitelistPath} ${blacklistPath}`, (error, stdout, stderr) => {
            if (error) {
                console.error('Error with imprint scraper:', stderr);
                return res.status(500).json({ message: 'Error with imprint scraper' });
            }

            const command = `python company_url_bot_optimized_search.py ${whitelistPath} ${outputWhitelist} ${blacklistPath} ${outputBlacklist}`;
            exec(command, (error, stdout, stderr) => {
                if (error) {
                    console.error('Error with LinkedIn search:', stderr);
                    return res.status(500).json({ message: 'Error with LinkedIn search' });
                }

                const whitelistUrl = fs.existsSync(outputWhitelist) ? `/uploads/whitelist_linkedin.csv` : null;
                const blacklistUrl = fs.existsSync(outputBlacklist) ? `/uploads/blacklist_linkedin.csv` : null;

                if (!whitelistUrl && !blacklistUrl) {
                    return res.status(500).json({ message: 'No results found for download.' });
                }

                whitelistDownloaded = false;
                blacklistDownloaded = false;

                res.json({ whitelistUrl, blacklistUrl });
            });
        });
    } catch (error) {
        console.error('Error during search process:', error);
        res.status(500).json({ message: 'Unexpected error during search process' });
    }
});

// Download handling
app.get('/uploads/:file', (req, res) => {
    const filePath = path.join(uploadDir, req.params.file);
    if (fs.existsSync(filePath)) {
        res.download(filePath, (err) => {
            if (err) {
                console.error("Error sending file:", err);
                return res.status(500).json({ message: 'Error sending file' });
            }

            // Mark file as downloaded
            if (req.params.file === 'whitelist_linkedin.csv') {
                whitelistDownloaded = true;
            } else if (req.params.file === 'blacklist_linkedin.csv') {
                blacklistDownloaded = true;
            }

            // Trigger cleanup if both files have been downloaded
            if (whitelistDownloaded && blacklistDownloaded) {
                setTimeout(() => {
                    fs.readdir(uploadDir, (err, files) => {
                        if (err) {
                            console.error('Error during cleanup:', err);
                            return;
                        }

                        files.forEach((file) => {
                            fs.unlink(path.join(uploadDir, file), (err) => {
                                if (err) console.error("Error deleting file:", err);
                            });
                        });

                        console.log("Uploads directory cleared successfully.");
                    });
                }, 10000); // 10-second delay
            }
        });
    } else {
        res.status(404).json({ message: 'File not found' });
    }
});

app.use('/uploads', express.static(uploadDir));

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
