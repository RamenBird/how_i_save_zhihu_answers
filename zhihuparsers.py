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
    
    def check_stack(self):
        if hasattr(self, work_stack):
            return

        self.work_stack = []
        self.flag = 0


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
        
        if self.flag & flag != 0:
            raise Exception()

        self.flag = self.flag & ~flag
        
    
    def handle_starttag(self, tag, attrs):
        if tag == 'p' or tag == 'b' or tag == 'u' or tag == 'blockquote':
            self.add_flag(tag)
            return
        elif tag == 'img' or tag == 'br' or tag == 'a':
            node = {'tag' : tag, 'attrs' : {}}
        
        for attr in attrs:
            node['attrs'][attr[0]] = attr[1]

        node.flag = self.flag
        self.work_stack.append(node)
            
    def handle_endtag(self, tag):
        print("End tag  :", tag)
        
    def handle_data(self, data):
        print("Data     :", data)
        
    def handle_comment(self, data):
        print("Comment  :", data)
