import Image
import sys
import os



new_size = 1024,1024


for f in sys.argv[1:]:
    old_im = Image.open(f)
    old_size = old_im.size
    new_im = Image.new("RGB", new_size, "white")
    new_im.paste(old_im, ((new_size[0]-old_size[0])/2, 
                        (new_size[1]-old_size[1])/2))
    new_im.show()
    new_im.save(os.path.splitext(f)[0]+ ".bord.jpg", "JPEG")
