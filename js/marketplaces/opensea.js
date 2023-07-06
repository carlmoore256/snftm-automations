import puppeteer from "puppeteer";
import { JSDOM } from "jsdom";

export async function getOpenSeaImage(url) {
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  await page.goto(url);
  
  const x = await page.evaluate(() => document.body.innerHTML);
  const dom = new JSDOM(x);
  const body = dom.window.document.body;
  const images = body.getElementsByTagName("img");

  for(const image of images) {
    if (image.classList.contains("Image--image")) {
      await browser.close();
      return image.src;
    }
  }

  await browser.close();
  return null;
}


export function isOpenSea(url) {
  return url.includes("opensea.io");
}