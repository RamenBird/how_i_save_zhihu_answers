FLAG_QUOTE = 1 << 0
FLAG_BOLD = 1 << 1
FLAG_UNDERLINED = 1 << 2
FLAG_PARAGRAPH = 1 << 3

class ZhihuAns(object):
    __slot__ = ('root', 'title')

    def __repr__(self):
        return str(self.root)

    @property
    def nodes(self):
        return self.root

class ChangeLine(object):
    def __str__(self):
        return "CL"

class PlainTextNode(object):
    __slot__ = ("text")

    def __init__(self, s):
        self.text = s
        self.flag = 0

    def __str__(self):
        return self.text

    def addFlag(self, f):
        self.flag = self.flag | f

    def hasFlag(self, f):
        return (f & self.flag) == 0

class LinkNode(object):
    __slot__ = ("url", "text")
    
    def __init__(self):
        self.flag = 0

    def __str__(self):
        return self.text

    def addFlag(self, f):
        self.flag = self.flag | f

    def hasFlag(self, f):
        return (f & self.flag) == 0

class ImageNode(object):
    __slot__ = ("title")

    def __init__(self):
        self.__property = {}

    def __str__(self):
        return self.title

    def addProperty(self, k, v):
        self.__property[k] = v

    def getProperty(self, k):
        if k in self.__property:
            return self.__property[k]
        return ""

    @property
    def src(self):
        if self.getProperty("data-original") == "":
            return self.getProperty("src")

        return self.getProperty("data-original")

class NodeGroup(object):    
    def __init__(self):
        self._nodes = []        
        self.flag = 0

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        self._nodes = nodes

    def __str__(self):        
        print("{")
        for node in self._nodes:
            print(node)
        return "}%d nodes, flag:%d"%(len(self._nodes), self.flag)

    def __iter__(self):
        return iter(self._nodes)

    def addFlag(self, f):
        self.flag = self.flag | f

    def hasFlag(self, f):
        return (f & self.flag) == 0

    __slot__ = ()

class ErrorNode(object):
    def __init__(self, s):
        self._s = s

    __slot__ = ()     
