import zhihuanswer
import os

class AnswerDraw(object):
    def __init__(self, answer, builder, config):
        self._ans = answer
        self._builder = builder
        self._config = config
        self._edge = 0
        self.canvas = builder.createcanvas(config.width, 100)
        self._height = 0

    def draw(self):
        config = self._config
        builder = self._builder
        
        self.height = 2000
        self.x = config.left_padding
        self.y = config.top_padding
        self.average_char_width = 0
        self.char_number = 0        

        textpaint = builder.createtextpaint('simsun.ttc', 20)

        for node in self._ans.nodes:
            self.drawnode(node, textpaint)

        self.height = self.edge + config.bottom_padding
        builder.save(self.canvas, os.path.join(os.getcwd(), "a.png"))
    

    @property
    def height(self):
        return self._height      

    @height.setter
    def height(self, value):
        self._height = value
        if self.canvas.height != value:
            self.canvas = self._builder.resizecanvas(self.canvas, self._config.width, value)            

    @property
    def y(self):
        return self._y        

    @y.setter
    def y(self, value):
        self._y = value

        if self.edge < value:
            self.edge = value

    @property
    def edge(self):
        return self._edge

    @edge.setter
    def edge(self, value):
        #print("edge ==> %d"%(value,))
        self._edge = value
        if value + self._config.bottom_padding> self.height:
            self.height = self.height + 1000            

    def measuretext(self, builder, text, paint):
        x, y = builder.measuretext(text, paint)        
        self.average_char_width = (x + self.average_char_width * self.char_number) / (self.char_number + len(text))        
        self.char_number = self.char_number + len(text)
        return x, y

    def drawtext(self, s, paint, fill="black"):
        if len(s) == 0:
            return
        
        builder = self._builder
        config = self._config

        i1 = 0
        l = [0 for i in range(0, len(s) + 1)]
        l[len(s)], height = self.measuretext(builder, s, paint)
                
        while i1 < len(s):
            if l[i1] == 0:
                l[i1], y = self.measuretext(builder, s[0 : i1], paint)
            length = config.width - config.right_padding - self.x
            i2 = min(len(s) - i1, int(length / self.average_char_width))

            while True:
                if i2 == 0:
                    break

                if l[i1 + i2] == 0:
                    l[i1 + i2], y = self.measuretext(builder, s[0 : i1 + i2], paint)
                    
                if l[i1 + i2] - l[i1] <= length:
                    if i1 + i2 == len(s) or l[i1 + i2 + 1] - l[i1] > length:
                        break
                    else:
                        i2 = i2 + 1
                else:
                    i2 = i2 - 1

            if i2 == 0:
                self.x = config.left_padding
                self.y = self.edge + config.line_spacing
            else:                
                builder.drawtext(self.canvas, self.x, self.y, s[i1 : i1 + i2], paint, fill=fill)
                self.x = self.x + l[i1 + i2] - l[i1]
                i1 = i1 + i2
                if self.edge < self.y + height:
                    self.edge = self.y + height

    def drawnode(self, node, paint):
        builder = self._builder
        config = self._config
        
        if isinstance(node, zhihuanswer.ChangeLine):
            self.x = config.left_padding
            self.y = self.edge + config.line_spacing           
            self.edge = self.y
        elif isinstance(node, zhihuanswer.PlainTextNode):
            self.drawtext(str(node), paint)
        elif isinstance(node, zhihuanswer.LinkNode):
            self.drawtext(str(node), paint, fill="blue")
        elif isinstance(node, zhihuanswer.NodeGroup):
            for i in node:
                self.drawnode(i, paint)
        elif isinstance(node, zhihuanswer.ImageNode):
            try:
                url = node.getProperty("data-original")
                img = self._builder.downloadimage(url, config.width - config.left_padding - config.right_padding)

                if self.y + img.height + config.bottom_padding > self.height:
                    self.height = self.y + img.height + config.bottom_padding
                    
                self._builder.drawimage(self.canvas, img, self.x, self.y,
                                        img.width, img.height)          

                self.y = self.y + img.height
                self.x = self._config.left_padding

                self.drawtext(str(node), paint)
            except Exception as e:
                print(e)
