import Image
import os
import glob

mergedImg = Image.new("RGBA", (300*(len(glob.glob("*.jpg"))+1), 100), (0,0,0,0))
count = 0
for files in glob.glob("*.jpg"):
	count = count + 1
	img = Image.open(files)
	size = img.size
	ratio = float(size[1])/100
	size = int(round(float(size[0])/ratio, 0)), 100
	img.thumbnail(size, Image.ANTIALIAS)
	w = 300*count - size[0]/2
	mergedImg.paste(img, (w,0))
	print files+': ', 300*count-50

mergedImg.save('image.jpg', 'JPEG')


