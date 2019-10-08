import numpy as np 
from PIL import Image
import os
import matplotlib.pyplot as plt
import time
import math

SAMPLE_DIRECTORY = './samples/'
SAMPLE_TYPE = '.png'

def GetSamples():

    ret = []
    
    for filename in os.listdir(SAMPLE_DIRECTORY):
        
        if not filename[-len(SAMPLE_TYPE):] == SAMPLE_TYPE:
            continue
        
        sample = Image.open(SAMPLE_DIRECTORY + filename)
        ret.append(sample)
    
    return ret


def ViewSamples():
    
    samples = GetSamples()
    
    for sample in samples:
        plt.figure()
        plt.imshow(sample)
        
    plt.show()
    
def Generate(size, mode="RGBA", phase=0, color=(255,255,255,0),
             xMarginRange=(0,5), yMarginRange=(0,5), imshow=False):
    
    if type(size) == int:
        print("Integer size parameter selected: " + str(size))
        size = (size, size)
    elif type(size) == tuple:
        print("Tuple size parameter selected: " + str(size))
    else:
        raise(Exception("size parameter must be type int or tuple"))
        
    for value in size:
        if value <= 0:
            raise(Exception("Size must be greater than zero"))
        continue

    phase = np.abs(phase % 180)  # maximum offset is 179 degrees
    phase *= math.pi/180  # convert phase degrees to radians
    print("Phase offset: " + str(phase))
        
    outputImage = Image.new(mode, size, color)
    
    xIndex, yIndex = 0, 0
    
    samples = GetSamples()
    sampleDimensions = samples[0].size
    
    outputHeight, outputWidth = size
    isNewRow = True
    newRowHeight = 0
    phaseOffset = 0
    
    while yIndex < outputHeight:
        #add phase offset as a multiple of the sample size
        if phase:
            phaseOffset += math.sin(phase) * sampleDimensions[0]
            phaseOffset %= sampleDimensions[0]
            xIndex += int(phaseOffset)
        
        while xIndex < outputWidth:
            sample = samples[np.random.randint(0, len(samples))]
            
            if isNewRow:
                newRowHeight = sample.size[1]
                isNewRow = False
            
            if xMarginRange[0] == xMarginRange[1]:
                xIndex += xMarginRange[0]
            else:
                xIndex += np.random.randint(*xMarginRange)
            
            if yMarginRange[0] == yMarginRange[1]:
                cellCoord = (xIndex, yIndex+yMarginRange[0])
            else:
                cellCoord = (xIndex, yIndex+np.random.randint(*yMarginRange))
                
            outputImage.paste(sample, cellCoord, sample)
            xIndex += sample.size[0]
            
        xIndex = 0
        yIndex += newRowHeight
        isNewRow = True
    
    if imshow:
        plt.imshow(outputImage)
    else:
        outputImage.save(str(time.time()) + 'out.png')
    
if __name__ == "__main__":
    Generate(1024, xMarginRange=(5,5), yMarginRange=(5,15), phase=7, imshow=False)
