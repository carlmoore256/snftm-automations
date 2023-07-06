import sharp from 'sharp';
import { fft2d } from 'fft-js';
import { ndarray, ops } from 'ndarray-fft';
import math from 'mathjs';

export async function compareImages(file1, file2) {
  const image1 = await sharp(file1)
    .resize(200, 200)
    .grayscale()
    .toBuffer();
  
  const image2 = await sharp(file2)
    .resize(200, 200)
    .grayscale()
    .toBuffer();

  const fft1 = fft2d(image1);
  const fft2 = fft2d(image2);
  
  const diff = math.mean(math.abs(math.subtract(ndarray(fft1), ndarray(fft2))));
  
  return diff;
}