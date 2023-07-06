import numpy as np
import math
from scipy.fft import fft2
from PIL import Image

def compare_images(file1, file2):
    image1 = np.array(Image.open(file1).resize((200, 200)).convert('L'))
    image2 = np.array(Image.open(file2).resize((200, 200)).convert('L'))

    fft1 = fft2(image1)
    fft2 = fft2(image2)

    diff = np.mean(np.abs(fft1 - fft2))

    return diff < 0.1  # adjust this threshold as needed
