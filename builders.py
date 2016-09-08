from PIL import Image, ImageFont, ImageDraw
from urllib import request
import time
import os
import io

class ImageBuilder(object):
    def __init__(self):
        self.i = 0
    
    def createcanvas(self, width, height):
        img = Image.new('RGB', (width, height), "white")
        return img

    def resizecanvas(self, canvas, width, height):
        img2 = Image.new('RGB', (width, height), "white")
        img2.paste(canvas, (0, 0, canvas.width, canvas.height))
        return img2
        
    def createtextpaint(self, font, fontsize):
        return ImageFont.truetype("C:/Windows/Fonts/" + font, fontsize)

    def measuretext(self, text, textpaint):
        return textpaint.getsize(text)

    def drawtext(self, canvas, x, y, text, paint, fill="black"):
        draw = ImageDraw.Draw(canvas)
        draw.text((x, y), text, font=paint, fill=fill)
        if False:
            print("%d,%d, write:%s"%(x, y, text))
        del draw

    def save(self, canvas, file):
        canvas.save(file)

    def drawimage(self, canvas, image, x, y, width, height):
        canvas.paste(image, (x, y, x + width, y + height))

    def downloadimage(self, url, width, path = None):
        name = url[url.rfind("/") : len(url)]
        
        file = io.BytesIO(request.urlopen(url).read())
        img = Image.open(file)        
        if path != None:
            img.save(path + name)

        if width == 0:
            width = img.width

        img2 = img.resize((width, int(img.height * width / img.width)))
        file.close()
        return img2

        

