import { resolveNFTContent } from "./parsing.js";
import { saveJSON } from "./utils.js";
import fs from "fs";


export async function parseArtistWorks() {

    const artistWorksFile = "data/artist-works-feb.json";
    const artistWorks = JSON.parse(fs.readFileSync(artistWorksFile, "utf8"));

    for(const work of artistWorks) {
        if (!work.link) continue;
        if (work.file_url) continue;
    
        const fileURL = await resolveNFTContent(work.link);

        if (fileURL != null) {
            work['file_url'] = fileURL;
            console.log("Success: ", fileURL);
        }
    }

    saveJSON(artistWorksFile, artistWorks);
}

console.clear();
parseArtistWorks();