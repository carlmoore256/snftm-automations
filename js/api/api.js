import express, { json } from 'express';
import multer from 'multer';
import { resolveNFTContent } from '../parsing.js';

const PORT = 62116;
const app = express();

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'data/uploads');
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    }
});

const upload = multer({ 
    storage: storage 
});

const imgEquivalentFields = upload.fields([{ name: 'img1', maxCount: 1 }, { name: 'img2', maxCount: 1 }])
app.post('/api/images/is-equivalent', imgEquivalentFields, (req, res) => {
    res.send('Hello World!');
});

// resolve the image, video, audio, or html of the NFT given
// a link to the marketplace listing
app.post('/api/nft/resolve-content', json(), async (req, res) => {
    if (!req.body.link) {
        res.status(400).send('No link provided');
        return;
    }
    const link = req.body.link;
    console.log(`Resolving content for ${link}`);
    const fileURL = await resolveNFTContent(link);
    if (fileURL == null) {
        res.status(400).send('No content found');
        return;
    }
    res.send(fileURL);
})

app.listen(PORT);
console.log(`API listening on port ${PORT}`)
