import { readFileSync, writeFileSync } from "fs";
import axios from "axios";

export async function downloadToDisk(url, filepath) {
    try {
        const response = await axios.get(url);
        const content = response.data;
        console.log("Saving data to filepath: ", filepath);
        writeFileSync(filepath, content);
        return content;
    } catch (error) {
        console.error("Error downloading url: ", url, + " Error: ", error);
        return null;
    }
}

export function urlToFilename(url) {
    let name = url.replace("https://", "").replace("http://", "").replace(/\//g, "_");
    name = name.replace("?", "_");
    return name + ".html";
}


export function saveJSON(filepath, data) {
    writeFileSync(filepath, JSON.stringify(data, null, 4));
}