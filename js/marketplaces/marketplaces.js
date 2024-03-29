import { getCachedHTML } from "../cache.js";
import { JSDOM } from "jsdom";

export const marketplaces = [
    {
        baseURL : "opensea.io",
        alias: "OpenSea",
        requiresBrowser: true,
    },
    {
        baseURL : "foundation.app",
        alias: "Foundation",
        requiresBrowser: false,
    },
    {
        baseURL : "rarible.com",
        alias: "Rarible",
        requiresBrowser: false,
    },
    {
        baseURL : "fxhash.xyz",
        alias: "FxHash",
        requiresBrowser: true,
    },
    {
        baseURL : "objkt.com",
        alias: "Objkt",
        requiresBrowser: true,
    },
    {
        baseURL : "makersplace.com",
        alias: "MakersPlace",
        requiresBrowser: false,
    }
]

export async function getMarketplaceListingPage(url) {
    const marketplaceInfo = marketplaces.find(m => url.includes(m.baseURL));
    if (!marketplaceInfo) {
        console.error(`No marketplace info found for: ${url}`);
        return null;
    }
    console.log(`Getting marketplace listing page for: ${marketplaceInfo.alias} url: ${url}`);
    const html = await getCachedHTML(url, marketplaceInfo.requiresBrowser);
    return new JSDOM(html).window.document;
}