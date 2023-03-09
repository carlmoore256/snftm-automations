import axios from "axios";
import { getMarketplaceListingPage } from "./marketplaces/marketplaces.js";

function IPFSPinURL(ipfsHash) {
    ipfsHash = ipfsHash.replace("ipfs://", "");
    return `https://ipfs.io/ipfs/${ipfsHash}`;
}

const isIPFS = (url) => url.startsWith("ipfs://");

function resolveBlockchainMetadata(url) {
    if (url.startsWith("https://")) {
        return url;
    }
    if (url.startsWith("ipfs://")) {
        return IPFSPinURL(url);
    }
    if (url.includes("gateway")) {
        return url;
    }

    return null;
}

async function queryMetadataJSON(document) {
    const metadataLinks =  document.querySelectorAll("a[href*='metadata.json']");
    for (const metadataLink of metadataLinks) {
        console.log("metadataLink", metadataLink.href);
        const response = await axios.get(metadataLink.href);
        const metadata = response.data;
        const contentURL = resolveBlockchainMetadata(metadata.image);
        return contentURL;
    }
    return null;
}

// find an 'a' tag where the text reads "View metadata", get the json by loading the link, and return the source to "image"
async function queryAnchorTagsWithText(document, text) {
    const anchors =  document.querySelectorAll("a");
    for (const anchor of anchors) {
        if (anchor.text.includes(text)) {
            return anchor.href;
        }
    }
    return null;
}


async function tryGetMetadataMedia(url, mediaType) {
    try {
        const response = await axios.get(url);
        const metadata = response.data;
        if (metadata[mediaType] == null) {
            return null;
        }

        return resolveBlockchainMetadata(metadata[mediaType]);
    } catch (error) {
        console.log("Error getting metadata: ", error.message);
        return null;
    }
}

function searchAllImages(document) {
    const images = document.querySelectorAll("img");
    const imageSources = [];
    for (const image of images) {
        const url = resolveBlockchainMetadata(image.src);
        if (url) {
            return url;
        }
    }
    return imageSources;
}

function tagsWithPartialClassMatch(document, tag, partialString) {
    const divs = document.querySelectorAll(`${tag}[class*="${partialString}"]`);
    return Array.from(divs);
}


export const MARKETPLACE_PARSERS = [
    {
        baseURL: "makersplace.com",
        mediaType: "image",
        func: async function(document) {
            console.log("parsing makersplace.com");
            const imagePreview = tagsWithPartialClassMatch(document, "div", "image-preview");
            for (const element of imagePreview) {
                const img = Array.from(element.getElementsByTagName("img"));
                if (img.length > 0) {
                    return img[0].src;
                }
            }
        }
    },
    {
        baseURL: "makersplace.com",
        mediaType: "video",
        func: async function(document) {
            console.log("paring makersplace.com for VIDEO");
            const imagePreview = tagsWithPartialClassMatch(document, "div", "image-preview");
            for (const element of imagePreview) {
                const video = Array.from(element.getElementsByTagName("video"));
                if (video.length > 0) {
                    const source = Array.from(video[0].getElementsByTagName("source"));
                    if (source.length > 0) {
                        return source[0].src;
                    }
                }
            }
        }
    },
    {
        baseURL: "objkt.com",
        mediaType: "image",
        func: async function(document) {
            console.log("Doing objkt.com!");
            const artWrapper = tagsWithPartialClassMatch(document, "div", "art-wrapper");
            for(const wrapper of artWrapper) {
                const image = Array.from(wrapper.getElementsByTagName("img"));
                if (image.length > 0) {
                    return image[0].src;
                }
            }
            return null;
        }
    },
    {
        baseURL: "opensea.io",
        mediaType: "image",
        func: async function(document) {
            const image = document.querySelector(".Image--image");
            if (image) {
                return image.src;
            }
            return null;
        }
    },
    {
        baseURL : "fxhash.xyz",
        mediaType: "image",
        func: async function(document) {
            const artworkFrames = tagsWithPartialClassMatch(document, "div", "ArtworkFrame");
            for(const artworkFrame of artworkFrames) {
                const image = artworkFrame.querySelector("img");
                if (image) {
                    return image.src;
                }
            }
            return null;
        }
    },
    {
        baseURL : "opensea.io",
        mediaType: "image",
        func: async function(document) {
            const image = document.querySelector(".Image--image");
            if (image) {
                return image.src;
            }
            return null;
        }
    },
    {
        baseURL : "foundation.app",
        mediaType: "video",
        func: async function(document) {
            var url = await queryAnchorTagsWithText(document, "View metadata");
            if (!url) {
                return null;
            }
            if (isIPFS(url)) {
                url = IPFSPinURL(url);
            }
            return tryGetMetadataMedia(url, "video");
        }
    },
    {
        baseURL : "foundation.app",
        mediaType: "video",
        func: async function(document) {
            return queryMetadataJSON(document);
        }
    },
    {
        baseURL : "foundation.app",
        mediaType: "image",
        func: async function(document) {
            // find a div with the class "fullscreen" and return the image src of the first child image
            const fullscreenDiv = document.querySelector(".fullscreen");
            console.log("fullscreenDiv", fullscreenDiv);
            if (fullscreenDiv) {
                const image = fullscreenDiv.querySelector("img");
                if (image) {
                    return image.src;
                }
            }
            return null;
        }
    }
]

export async function runParser(parser, document) {
    return await parser.func(document);
}

// attempts to get the main nft content, whether it be an image, video, or html content
// handles different marketplaces, as defined in marketplaces.js
export async function resolveNFTContent(url) {
    const document = await getMarketplaceListingPage(url);
    if (document == null) {
        console.error("No document found for url: ", url);
        return;
    }

    const candidateParsers = MARKETPLACE_PARSERS.filter(p => url.includes(p.baseURL));

    
    if (candidateParsers == null) {
        console.error("No parser found for url: ", url);
        return;
    }

    for (const parser of candidateParsers) {
        console.log("Using parser: ", parser.baseURL, parser.mediaType);
        const res = await parser.func(document);
        if (res) {
            return res;
        }
    
        console.log("Found nothing :(");

    }
    return null;
}

export function anyParserResult(document) {

    for (const parser of MARKETPLACE_PARSERS) {
        const res = parser.func(document);
        if (res) {
            return res;
        }
    }
    return null;
}