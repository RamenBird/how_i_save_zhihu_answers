import how_i_save_zhihu_answers.parsers as parsers
import re
from html.parser import HTMLParser

class AnswerParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)
    def handle_endtag(self, tag):
        print("End tag  :", tag)
    def handle_data(self, data):
        print("Data     :", data)
    def handle_comment(self, data):
        print("Comment  :", data)

def getanswercode(pagebuff):
    if isinstance(s, bytes):
        s = str(s, "utf-8")

    p = re.compile("<div.+?zm-editable-content clearfix.+?>(.+?)</div>", re.S)
    m = answerArea.search(s)
    if m:
        return m.group(1).replace("\n", "")

def parseanswer(answercontent):
    if answercontent:
        ans = ZhihuAns()
        p = re.compile("<noscript><img.+?>(.*?)</noscript><img.+?>\\1|"
                       "<([puba]|blockquote)(?:\\s.+?)?>.*?</\\2>|"
                       ".+?(?=<[puba]>|<[puba]\\s|<blockquote>|<noscript>)|"
                       ".+$")

        for substring in p.finditer(answercontent):
            node = parsers.parseanswer(substring)
            if node:
                ans.addnode(node)
        return ans
