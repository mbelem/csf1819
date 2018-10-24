import sys, struct, numpy, PIL as pillow
from PIL import Image 
from bitstring import *

def extract(imgFile, output, password):
    message = []
     
    displacement = 0
    img = Image.open(imgFile)
    width, height = img.size
    conv = img.convert('RGBA').getdata()
    f = open(output, 'w')
    data_img = img.getdata()
    for h in range(height):
        for w in range(width):
           if displacement < password:
               displacement = displacement + 1
               continue
           r, g, b, a = conv.getpixel((w, h))
           message.append(extractLSB(r))
           message.append(extract2LSB(r))
           message.append(extractLSB(g))
           message.append(extract2LSB(g))
           message.append(extractLSB(b))
           message.append(extract2LSB(b))
    string=''
    str_size=''
    for i in range(4, 0, -1):
        for j in range(1,9):
            str_size += str(message[8*(i-1)+j-1])
    size = int(str_size, 2)
    for i in range(32, 32+size*8):
        string+=str(message[i])
    f.write(bits2a(string))
    f.close()
    
def bits2a(b):
    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)]*8))

def extractLSB(comp):
    lsb = comp & 1
    return lsb

def extract2LSB(comp):
    lsb2 = comp & 2
    lsb2 = lsb2 >> 1
    return lsb2

if __name__ == '__main__':
    password = int(sys.argv[3]) % 13 if len(sys.argv) > 3 else 0
    extract(sys.argv[1], sys.argv[2], password)

