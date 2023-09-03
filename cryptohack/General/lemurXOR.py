#!/usr/local/bin/python3
import numpy as np
from PIL import Image, ImageChops
# Open images
im1 = Image.open("./lemurXORdocs/flag.png")
im2 = Image.open("./lemurXORdocs/lemur.png")

#result = ImageChops.logical_xor(im1,im2)
#result.save('./lemurXORdocs/final_flag.png')

# OR
# Make into Numpy arrays
im1np = np.array(im1)*255
im2np = np.array(im2)*255

# XOR with Numpy
result = np.bitwise_xor(im1np, im2np).astype(np.uint8)
# Convert back to PIL image and save
Image.fromarray(result).save('./lemurXORdocs/final_flag.png')
