import { Handler, Router, json } from "express";


export default (parent) => {
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
}