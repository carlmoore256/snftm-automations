import puppeteer from "puppeteer";

export async function downloadPageWithBrowser(url, headless = false) {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });
  const page = await browser.newPage();
  page.setDefaultNavigationTimeout(60000);
  await page.goto(url);
  await page.waitForTimeout(2000);
  const html = await page.evaluate(() => document.documentElement.outerHTML);
  await browser.close();
  return html;
}