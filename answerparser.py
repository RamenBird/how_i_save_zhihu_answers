import how_i_save_zhihu_answers.parsers as parsers
import re

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
