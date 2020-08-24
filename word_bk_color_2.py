import cv2
from PIL import Image,ImageColor, ImageDraw
import numpy as np
import argparse
import sys
import time

def adjust(imgFile, cols, rows):
	global ratio
	image_file = Image.open(f'{imgFile}')

	width, height = image_file.size

	print(f'\noriginal: width:{width}, height:{height}\n')

	if width == height:
		ratio = 1
		cols = int(height * ratio)
		rows = int(width  * ratio)
		print('height == width\n')

	else:
		if cols > height:
			cols == height

		scale = 0.43
		ratio = int(width / cols)

		if rows == None:
			rows = int(height / int( ratio / scale))

	print(f"ratio:{ratio} \
				width: {rows} \
				height: {cols}\n")

	original = image_file.resize((cols,rows)).convert('RGBA')
	grey_img = original.convert("L")

	return grey_img, original, cols, rows

#print(width,hight)
#pixel = [grey_img.getpixel((w,h)) for w in range(width) for h in range(hight)]

def convertToColorAscii(imgFile,original,cols,rows,out_):
	word = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/()1[]?-_+~<>i!lI;:,"^`'.'''
	z = 256 / len(word)
	txt = ''

	base = Image.new('RGBA', (cols*5,rows*5),color=(255,255,255))
	base.save(f'{out_}.png')

	txt_1 = Image.new('RGBA', base.size, (255,255,255,0))
	d = ImageDraw.Draw(txt_1)

	percentage = 0
	
	h2 = 0
	w2 = 0
	for h in range(0,cols,2):
		h2 = h * 5
		for w in range(0,rows,2):
			w2 = w * 5
			percentage = int(((cols-h)/cols)*100)
			print(f'{h}, {w}, {percentage}%',end='\r')
			sys.stdout.flush()

			color = imgFile.getpixel((h,w))
			#r,g,b,a = original.getpixel((h,w))

			if color == 255:
				txt = " "
				r,g,b,a = [0,0,0,0]
			else:
				if color <10:
					r,g,b,a = [0,0,0,0]
				else:
					r,g,b,a = original.getpixel((h,w))
				txt = word[int(color/int(z))]
			d.text((h2,w2), txt, fill=(r,g,b))
	out = Image.alpha_composite(base, txt_1)
	out.save(f'{out_}.png')
	return

def convertToBlackAscii(imgFile,cols,rows,out_):
	word = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/()1[]?-_+~<>i!lI;:,"^`'.'''
	z = 256 / len(word)
	txt = ''

	base = Image.new('RGBA', (cols*10,rows*10),color=(255,255,255))
	base.save(f'{out_}.png')

	txt_1 = Image.new('RGBA', base.size, (255,255,255,0))
	d = ImageDraw.Draw(txt_1)

	percentage = 0
	
	h2 = 0
	w2 = 0
	for h in range(0,cols,2):
		h2 = h * 10
		for w in range(0,rows,2):
			w2 = w * 10
			percentage = int(((cols-h)/cols)*100)
			print(f'{h}, {w}, {percentage}%',end='\r')
			sys.stdout.flush()

			color = imgFile.getpixel((h,w))

			if color == 255:
				txt = " "
			else:
				txt = word[int(color/int(z))]
			d.text((h2,w2), txt, fill=(0,0,0))
	out = Image.alpha_composite(base, txt_1)
	out.save(f'{out_}.png')
	return

def main():
	descStr = "This program converts an image into ASCII art."
	parser = argparse.ArgumentParser(description=descStr)
	parser.add_argument('--photo', dest='imgFile',required=True)
	parser.add_argument('--color', dest='color',required=False)
	parser.add_argument('--out', dest='outFile',required=False)
	parser.add_argument('--cols',dest='cols',required=False)
	parser.add_argument('--rows',dest='rows',required=False)

	args = parser.parse_args()

	img = args.imgFile


	if args.outFile:
		out = args.outFile
	else:
		out = 'out'

	if args.cols:
		cols = int(args.cols)
	else:
		cols = 300

	if args.rows:
		rows = int(args.rows)
	else:
		rows = None

	start = time.time()
	img2,original, cols,rows = adjust(img,cols,rows)
	
	if args.color:
		convertToColorAscii(img2,original,cols,rows,out)
	else:
		convertToBlackAscii(img2,cols,rows,out)
	
	total = time.time()- start
	print(f'total_time: {total}')
	print('\ndone!')
	

if __name__ == '__main__':
	main()
