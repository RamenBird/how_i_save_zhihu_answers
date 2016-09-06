class ZhihuAns(object):
    def __init__(self):
        self._nodes = []

    def __repr__(self):
        return str(self.root)

    def addnode(self, node):
        self._nodes.append(node)
