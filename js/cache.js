import { readdirSync, readFileSync, writeFileSync } from "fs";
import { downloadPageWithBrowser } from "./browser.js";
import { downloadToDisk, urlToFilename } from "./utils.js";

const CACHE_DIR = "data/web-cache";
const CACHE_FILES = readdirSync(CACHE_DIR);

export async function getCachedHTML(url, requiresBrowser = false) {
    const cacheFilename = urlToFilename(url);
    const cacheFile = CACHE_DIR + "/" + cacheFilename;
    for(const c of CACHE_FILES) {
        if (c.toString().includes(cacheFilename)) {
            console.log("Found cache file: ", cacheFile);
            return readFileSync(cacheFile, "utf8");
        }
    }
    
    if (requiresBrowser) {
        const html = await downloadPageWithBrowser(url);
        writeFileSync(cacheFile, html);
        return html;
    }
    return downloadToDisk(url, cacheFile);
}
