FLAG_QUOTE = 1 << 0
FLAG_BOLD = 1 << 1
FLAG_UNDERLINED = 1 << 2
FLAG_PARAGRAPH = 1 << 3

class Node(object):
    def __init__(self):
        self._flag = 0
        self._attrs = {}
    
    def addattr(self, k, v):
        self._attrs[k] = v

    def get_attr(self, k):
        if k in self._attrs:
            return self._attrs[k]
    
    def addflag(self, f):
        self._flag = self._flag | f

    def hasflag(self, f):
        return (f & self._flag) == 0    

class ChangeLine(Node):
    def __str__(self):
        return "CL"

class PlainTextNode(Node):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def __str__(self):
        return self.text

class LinkNode(Node):
    
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'link url:%s'%(self.text,)

class ImageNode(Node):
    def __init__(self):
        super().__init__()
        self.text = ""
    
    def __str__(self):
        return 'image source:%s'%(self.src,)

    @property
    def src(self):
        if self.get_attr("data-original") == "":
            return self.get_attr("src")

        return self.get_attr("data-original")

class NodeGroup(Node):    
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

class ErrorNode(Node):
    def __init__(self, s):
        self._s = s

    __slot__ = ()     
