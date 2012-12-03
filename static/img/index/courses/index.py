import Image
import os
import glob

mergedImg = Image.new("RGBA", (200*(len(glob.glob("*.jpg"))+1), 80), (0,0,0,0))
count = 0
for files in glob.glob("*.jpg"):
	count = count + 1
	img = Image.open(files)
	size = img.size
	ratio = float(size[1])/80
	size = int(round(float(size[0])/ratio, 0)), 80
	img.thumbnail(size, Image.ANTIALIAS)
	w = 200*count - size[0]/2
	mergedImg.paste(img, (w,0))
	print files+': ', 200*count-40

mergedImg.save('image.jpg', quality=90)


