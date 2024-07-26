from PIL import Image
import os.path
import sys

def blend(color, base=[234,237,222]):
    out = [int(round((color[3]/255 * color[i]) + ((1 - color[3]/255) * base[i]))) for i in range(3)]
    return out
    
def to_hex(color):
    return ''.join(["%02x" % e for e in color])
    
def colorToBlock(color,count):
    blocks=''
    for i in range(count):
        blocks=blocks+'█'
    return '[color=#'+to_hex(color)+']'+blocks+'[/color]'

fileName = sys.argv[1]
#im = Image.open('plushie_lizard.png') # Can be many different formats.
im = Image.open(fileName) # Can be many different formats.

rgb_im = im.convert('RGBA')
pix = rgb_im.load()
width,height = rgb_im.size
#print(rgb_im.size)  # Get the width and hight of the image for iterating over
#print(colorToBlock(blend(pix[8,8])))
#[color=#ffffff]█[/color]

outputFileName = fileName +'_output.txt'

if os.path.exists(outputFileName):
    f = open(outputFileName, 'w', encoding='utf-8')
else:
    f = open(outputFileName, 'x', encoding='utf-8')

for x in range(height):
    line = ''
    lastColor = blend(pix[0, x])
    lastHex = to_hex(lastColor)
    sameHexBlock = 1
    for y in range(width):
        if y == 0: continue
        thisColor = blend(pix[y, x])
        thisHex = to_hex(thisColor)
        
        if lastHex==thisHex:
            sameHexBlock= sameHexBlock+1
            if y==width-1:
                line = line + colorToBlock(thisColor,sameHexBlock)
        else:
            line = line + colorToBlock(lastColor,sameHexBlock)
            sameHexBlock=1
            if y==width-1:
                line = line + colorToBlock(thisColor,sameHexBlock)
        lastHex = thisHex
        lastColor = thisColor
    f.write(line+'\n')
    #print(line)

f.close()