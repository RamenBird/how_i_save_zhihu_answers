from html.parser import HTMLParser
from how_i_save_zhihu_answers.nodedef import *

FLAG_QUOTE = 1 << 0
FLAG_BOLD = 1 << 1
FLAG_UNDERLINED = 1 << 2
FLAG_PARAGRAPH = 1 << 3

class AnswerParser(HTMLParser):
    def get_stack_top(self):
        self.check_stack()        
        return self.work_stack[len(self.work_stack) - 1]

    def parse(self, s):
        from how_i_save_zhihu_answers.answerdef import ZhihuAns
        ans = ZhihuAns()
        self.feed(s)
        ans.nodes = self.work_stack
        return ans
    
    def check_stack(self):
        if hasattr(self, 'work_stack'):
            return

        self.work_stack = []
        self.flag = 0
        self.ctr_msg = ''


    def add_flag(self, tag):
        if tag == 'p':
            flag = FLAG_PARAGRAPH
        elif tag == 'b':
            flag = FLAG_BOLD
        elif tag == 'blockquote':
            flag = FLAG_QUOTE
        elif tag == 'u':
            flag = FLAG_UNDERLINED
        
        if self.flag & flag != 0:
            raise Exception()

        self.flag = self.flag | flag


    def remove_flag(self, tag):        
        if tag == 'p':
            flag = FLAG_PARAGRAPH
        elif tag == 'b':
            flag = FLAG_BOLD
        elif tag == 'blockquote':
            flag = FLAG_QUOTE
        elif tag == 'u':
            flag = FLAG_UNDERLINED
        
        if self.flag & flag == 0:
            raise Exception()

        self.flag = self.flag & ~flag
        
    
    def handle_starttag(self, tag, attrs):
        #print("Start tag :", tag)
        self.check_stack()
        node = None
        
        if tag == 'p' or tag == 'b' or tag == 'u' or tag == 'blockquote':
            self.add_flag(tag)
            return
        elif tag == 'img':
            if self.ctr_msg == 'img':
                self.ctr_msg = ''
                return
            elif self.ctr_msg == 'noscript':
                node = ImageNode()
                self.work_stack.append(node)
            elif self.ctr_msg == '':
                return
        elif tag == 'br':
            self.work_stack.append(ChangeLine())
            return
        elif tag == 'a':
            node = LinkNode()
            self.work_stack.append(node)
            self.ctr_msg = 'a'
        elif tag == 'noscript':
            self.ctr_msg = 'noscript'
            return
        else:
            return

        if node:        
            for attr in attrs:
                node.addattr(attr[0], attr[1])
            node.flag = self.flag
        else:
            print(tag, self.ctr_msg)
            
    def handle_endtag(self, tag):
        #print("End tag  :", tag)
        if tag == 'p' or tag == 'b' or tag == 'u' or tag == 'blockquote':
            self.remove_flag(tag)
            return
        elif tag == 'a':
            self.ctr_msg = ''
        elif tag == 'noscript':
            self.ctr_msg = 'img'
        else:
            return
        
    def handle_data(self, data):
        #print("Data     :", data)

        if self.ctr_msg == '':
            node = PlainTextNode(data)
            node.flag = self.flag
            self.work_stack.append(node)
        elif self.ctr_msg == 'img':
            node = self.get_stack_top()
            node.text = data
        elif self.ctr_msg == 'a':
            node = self.get_stack_top()
            node.text = data
        else:
            return
        
    def handle_comment(self, data):
        print("Comment  :", data)
