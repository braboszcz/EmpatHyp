import Image
import ImageOps
import os

def mirror(filename, newSide):
	img = Image.open(filename)
	mirror_img = ImageOps.mirror(img)
	mirror_img.save(newSide + '_' + filename)

def flipPict(foldername, flipSide):
	#-------------------------------
	# read pictures name from folder
	#-------------------------------
	
	for root, dirs, files in os.walk(foldername):
		pictList = files
	
	os.chdir(foldername)
	for pictName in pictList:
		mirror(pictName, flipSide)

flipPict('Mains droites', 'L')




