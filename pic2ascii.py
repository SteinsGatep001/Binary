#!/usr/bin/python2
#coding:utf-8
from PIL import Image 
import optparse

ascii_list = list(r"$@&%B#=-. ")

# RGB to char
def rgb2char(r, g, b):
    gray = int((19595 * r + 38469 * g + 7472 * b) >> 16)  # ‘RGB－灰度值’转换公式
    unit = 256.0/len(ascii_list)  # ascii_char中的一个字符所能表示的灰度值区间
    return ascii_list[int(gray/unit)]

def prod_ascii(imgfile, outfile, width, height):
    f = open(outfile, 'wr')
    im = Image.open(imgfile)
    
    im = im.resize((width, height), Image.NEAREST)
    str_asc = ""

    for h in xrange(height):
        for w in xrange(width):
            str_asc += rgb2char(*im.getpixel((w, h))[:3])
        str_asc += '\n'
    
    f.write(str_asc)
    f.close()


def main():
    parser = optparse.OptionParser('usage %prog -i <image file name> -o <outfile name> -w <width> -l <height>');
    parser.add_option('-i', dest='imgfile', type='string', help='specify input image file name')
    parser.add_option('-o', dest='outfile', type='string', help='specify output ascii file name')
    parser.add_option('-w', dest='width', type='string', help='specify output width')
    parser.add_option('-l', dest='height', type='string', help='specify output height')
    (options, args) = parser.parse_args()
    imgfile = options.imgfile
    outfile = options.outfile
    width = options.width
    height = options.height
    if (imgfile == None) | (outfile == None) | (width == None) | (height == None):
        print parser.usage
        exit(0)
    width = int(width)
    height = int(height)
    prod_ascii(imgfile, outfile, width, height)


if __name__ == '__main__':
    main()



