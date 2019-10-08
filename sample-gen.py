import numpy as np
from PIL import Image, ImageDraw, ImageFont

letters = "abcdefg"
size = (16,16)
mode = 'RGBA'
fill = (255,255,255,0)
directory = './samples/'

for letter in [a for a in letters]:
    
    sampleImage = Image.new(mode, size, fill)
    
    draw = ImageDraw.Draw(sampleImage)
    font = ImageFont.truetype("arial.ttf", 16)
    
    draw.text((0,0), letter, font=font, fill="red")
    
    sampleImage.save(directory + letter + "_sample.png")