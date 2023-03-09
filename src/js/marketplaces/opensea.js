import axios from "axios";
import puppeteer from "puppeteer";
import { JSDOM } from "jsdom";
import { readdirSync, readFileSync, writeFileSync } from "fs";

// try to download an opensea url
const URL = `https://opensea.io/assets/ethereum/0x495f947276749ce646f68ac8c248420045cb7b5e/49627714412250459268020911193636266760001820625666130899906076663685446631425`;
// const URL = `https://makersplace.com/0x494e9B8eF3026dD5f1ca2a7aF111A9D0AbD39DAC/sentient-sun-steel-stella-1-of-1-85961/`;

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