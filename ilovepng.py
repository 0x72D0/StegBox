#!/usr/bin/env python2
#-*- coding:utf-8 -*-
import zlib
import click
from PIL import Image
import struct

COLOR_TYPE = {0 : 'Grayscale', 2 : 'RGB', 3 : 'PLTE', 4 : 'Greyscale + Alpha', 6 : 'RGBA'}
COMPRESSION = {0 : 'Deflate/Inflate'}
FILTER_METHOD = {0 : 'Adaptive filtering'} 
INTERLACE = {0 : 'No interlace', 1 : 'Adam7 interlace'} 
FILTER_TYPE = {0 : 'None', 1 : 'Sub', 2 : 'Up', 3 : 'Average', 4 : 'Paeth'}

# PNG Class. Read meta informations, decompress the pixels data and analyze the filtering.
class PNG:
	def __init__(self, name):
		self.name = name
		self.data = open(name, 'r').read()
		self.header(self.data)
		self.pixelsData = self.decompress(self.data)
		self.filters = self.filter_type()
		# Creates a list with every RGB or RGBA pixels (TEMPORAIRE vu que c'est faux a cause des filter type)
		self.pixels = self.pixel_value()

	# Meta informations from IHDR chunk
	def header(self, data):
		head = data[data.find("IHDR")+4:data.find("IDAT")]
		self.w = struct.unpack("!I", head[0:4])[0]
		self.h = struct.unpack("!I", head[4:8])[0]
		self.bitdepth = ord(head[8])
		self.colortype = COLOR_TYPE[ord(head[9])]
		self.compressionmethod = COMPRESSION[ord(head[10])]
		self.filtermethod = FILTER_METHOD[ord(head[11])]
		self.interlace = INTERLACE[ord(head[12])]
    
	# Decompress pixels data with zlib compression method
	def decompress(self, image):
		# Get the IDATs chunks
		chunks = image[image.find("IDAT"):image.find("IEND")]
		chunks = chunks.split("IDAT")

		# Remove the CRCs and length of IDATs and join the data
		data_compressed = ''.join(chunks[i][:-8] for i in range(len(chunks)))
		
		# Decompress the data
		data = zlib.decompress(data_compressed)
		return data

	# Returns every filters bytes in the PNG pixel data 
	def filter_type(self):
		# Each scanline correspond to the width of the image * 4 (RGBA) + 1 (filter type)
		len_scanline = 1 + self.w * len(self.colortype)
		size = len(self.pixelsData)
		
		# Get the filter type of each scanline
		filters = []
		for s in range(size/len_scanline):
			scanline = self.pixelsData[len_scanline*s:len_scanline*(s+1)]
			filters.append(ord(scanline[0]))
		
		return filters

	# Shows meta informations of the PNG image
	def info(self):
		click.secho('\n [*] %s ' % self.name, fg = 'magenta', bold = True)
		click.secho('     %s x %s, %s-bit/color, %s, %s, %s' % (self.w, self.h, self.bitdepth, self.colortype, self.interlace, self.compressionmethod), fg = 'magenta')
		print "     %d bytes of pixel data " % (len(self.pixelsData))
		print "     %s, filter type(s) : %s " % (self.filtermethod, (', '.join(FILTER_TYPE[i] + "(" + str(i) + ")" for i in list(set(self.filters)))))

	# Returns a 2D array (w x h) of tuple of the real pixels value (RGB, RGBA)
	def pixel_value(self):
		pixels = []
		
		# Remove the filter type byte on every scanlines of the data.
		pixel_data = ''.join(self.pixelsData[i+1:i+self.w] for i in range(0, len(self.pixelsData), self.w))

		psize = len(self.colortype)
		# Create the 2D array of pixels
		for x in xrange(self.w):
			for y in xrange(self.h):
				position = psize * (x + (y * self.w))
				pixels[x][y] = pixel_data[position : position + psize]
		
		return pixels


class StegTool():
    def __init__(self, image, flag):
        self.pixel = image.load()
        self.w, self.h = image.size
        try: self.flagFormat = flag.encode('utf8')
        except: self.flagFormat = ""


    # Basic tests looking for flag in ascii and lsb mode
    def basic(self):
        click.secho('\n[*]ASCII', fg = 'blue', bold = True)
        click.secho('[ By Rows ]', fg = 'magenta', bold = True)
        print " RGB  %s"%self.search(self.ascii(0)[0])
        click.secho(" R    %s"%self.search(self.ascii(1)[0]), fg = 'red')
        click.secho(" G    %s"%self.search(self.ascii(2)[0]), fg = 'green')
        click.secho(" B    %s"%self.search(self.ascii(3)[0]), fg = 'blue')

        click.secho('[ By Columns ]', fg = 'magenta', bold = True)
        print " RGB  %s"%self.search(self.ascii(0)[1])
        click.secho(" R    %s"%self.search(self.ascii(1)[1]), fg = 'red')
        click.secho(" G    %s"%self.search(self.ascii(2)[1]), fg = 'green')
        click.secho(" B    %s"%self.search(self.ascii(3)[1]) , fg = 'blue')

        click.secho('\n[*]LSB', fg = 'blue', bold = True)
        click.secho('[ By Rows ]', fg = 'magenta', bold = True)
        print " RGB  %s"%self.search(self.lsb(0)[0])
        click.secho(" R    %s"%self.search(self.lsb(1)[0]), fg = 'red')
        click.secho(" G    %s"%self.search(self.lsb(2)[0]), fg = 'green')
        click.secho(" B    %s"%self.search(self.lsb(3)[0]), fg = 'blue')

        click.secho('[ By Columns ]', fg = 'magenta', bold = True)
        print " RGB  %s"%self.search(self.lsb(0)[1])
        click.secho(" R    %s"%self.search(self.lsb(1)[1]), fg = 'red')
        click.secho(" G    %s"%self.search(self.lsb(2)[1]), fg = 'green')
        click.secho(" B    %s"%self.search(self.lsb(3)[1]) , fg = 'blue')
    

    def conversion(self, position, equa):
        conv = ""
        conv_tab = []
        for y in xrange(self.h):
            for x in xrange(self.w):
                i = self.pixel[x,y]
                if position == 0: conv+=eval(equa%"(i[0])"+"+"+equa%"(i[1])"+"+"+equa%"(i[2])")
                else: conv+=eval(equa%"(i["+str(position-1)+"])")
                    
        conv_tab.append(conv)
        conv = ""
        for x in xrange(self.w):
            for y in xrange(self.h):
                i = self.pixel[x,y]
                if position == 0: conv+=eval(equa%"(i[0])"+"+"+equa%"(i[1])"+"+"+equa%"(i[2])")
                else: conv+=eval(equa%"(i["+str(position-1)+"])")
        conv_tab.append(conv)
        return conv_tab

    # Message hidden in pixel value as ascii 
    def ascii(self, position):
        row, col = "", ""
        # Rows
        for y in xrange(self.h):
            for x in xrange(self.w):
                if position: row += chr(self.pixel[x,y][position-1])
                else: row += ''.join(chr(self.pixel[x,y][l]) for l in range(3))
        # Columns
        for x in xrange(self.w):
            for y in xrange(self.h):
                if position: col += chr(self.pixel[x,y][position-1])
                else: col += ''.join(chr(self.pixel[x, y][l]) for l in range(3)) 
        return row, col	

    # Message hidden in LSB
    def lsb(self, position):
        row, col = "", ""
        # Rows
        for y in xrange(self.h):
            for x in xrange(self.w):
                if position: row += str(self.pixel[x,y][position-1] & 1)	 
                else: row += ''.join(str(self.pixel[x,y][l] & 1) for l in range(3))  
        row = ''.join(chr(int(row[i:i+8], 2)) for i in range(0, len(row), 8))
        # Columns
        for x in xrange(self.w):
            for y in xrange(self.h):
                if position: col += str(self.pixel[x,y][position-1] & 1) 
                else: col += ''.join(str(self.pixel[x,y][l] & 1) for l in range(3))  
        col = ''.join(chr(int(col[i:i+8], 2)) for i in range(0, len(col), 8))
        return row, col

    def search(self, p):
        return p[p.find(self.flagFormat):p.find(self.flagFormat) + 30]

    def position(self):
        return int(raw_input("\nPosition to make the conversion\n[0]RGB\n[1]R\n[2]G\n[3]B\n[4]A\nEnter a number from 0-4 > "))


    def columns(self, color0, color1, position):
        ascii_text = []
        binary = []
        binaire = ""
        for x in xrange(self.w):
            binary_lines = []
            for y in xrange(self.h):
                if self.pixel[x,y][int(position)] == int(color0): 
                    binary_lines.append("0")
                    binaire += "0"
                elif self.pixel[x,y][int(position)] == int(color1): 
                    binary_lines.append("1")
                    binaire += "1"
            binary.append(binary_lines)
	try: 
            ascii_text.append(''.join((chr(int(binaire[i:i+8], 2)) for i in range(0, len(binaire), 8))))
            ascii_text.append(''.join([ chr(int(''.join(separated),2)) for separated in binary]))
        except: ascii_text.append("Undefined")
        return ascii_text

    def rows(self, color0, color1, position):
        binary = []
        ascii_text = []
        binaire = ""
        for y in xrange(self.h):
            binary_lines = []
	    for x in xrange(self.w):
	        if self.pixel[x,y][int(position)] == int(color0): 
		    binary_lines.append("0")
		    binaire += "0"
                elif self.pixel[x,y][int(position)] == int(color1): 
		    binaire += "1"
                    binary_lines.append("1")
	    binary.append(binary_lines)
	try:
            ascii_text.append(''.join((chr(int(binaire[i:i+8], 2)) for i in range(0, len(binaire), 8))))
            ascii_text.append(''.join([ chr(int(''.join(separated),2)) for separated in binary]))
        except: ascii_text.append("Undefined")
        return ascii_text

    def color2bin(self, b0, b1, pos):
        columns = self.columns(b0, b1, pos)
        rows = self.rows(b0, b1, pos)
        print "\n=========================================================="
        print "pixel->%s"%b0+" = 0   pixel->%s"%b1+" = 1    at position : %s"%pos
        print "=========================================================="
        print "Columns data dump 1 : "
        print columns[0]
        print "\nColumns data dump 2 :"
        print columns[1]
        print "\nRows data dump 1 : "
        print rows[0]
        print "\nRows data dump 2 : "
        print rows[1]+"\n"


@click.command(context_settings = dict(help_option_names = ['-h', '--help']))
@click.option('-f', help="Specify the PNG image to search on")
@click.option('--search', help="Pattern/word to search for (flag format)")
@click.option('-c', '--convert', default=True, help="type")
@click.option('-cb', is_flag = True, help="color to binary value 0 1")
def main(f, search, convert, cb):
	'''Steganography solver for PNG images'''
	if (f):
		
		pf = PNG(f)
		pf.info()
		#pf.pixel
		st = StegTool(Image.open(f, 'r'), search)
		
		if (convert):
			if convert == "ascii": print st.ascii(conv.position())
			elif convert == "lsb": print st.lsb(conv.position())
			else: st.basic()
		
		# color2bin
		if(cb):
			b0  = click.prompt('Pixel value for binary 0', type = int)
			b1 = click.prompt('Pixel value for binary 1', type = int)
			pos  = click.prompt('Position of RGB (R:0, G:1, B:2)', type = int)
			st.color2bin(b0, b1, pos)

	# showing the way
	else:
		click.secho('Please specify a PNG image to perform the test on. See -h/--help', fg = 'yellow', bold = True)

if __name__ == '__main__':
    main()
