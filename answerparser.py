from how_i_save_zhihu_answers.zhihuanswer import ZhihuAns
from how_i_save_zhihu_answers.zhihuanswer import LinkNode
from how_i_save_zhihu_answers.zhihuanswer import ImageNode
from how_i_save_zhihu_answers.zhihuanswer import NodeGroup
from how_i_save_zhihu_answers.zhihuanswer import ErrorNode
from how_i_save_zhihu_answers.zhihuanswer import ChangeLine
from how_i_save_zhihu_answers.zhihuanswer import PlainTextNode
import re

def _replacehtmltransfer(s):
    return s

def _getanswerstr(s):
    if isinstance(s, bytes):
        s = str(s, "utf-8")

    answerArea = re.compile("<div.+?zm-editable-content clearfix.+?>(.+?)</div>", re.S)
        
    match = answerArea.search(s)
    if match:
        return match.group(1).replace("\n", "")

def _parsetextnode(s, nodes):
    if len(nodes) == 1:
        node = nodes[0]
    else:
        node  = NodeGroup()
        node.nodes = nodes 

    p2 = re.compile("^<blockquote>(.*)</blockquote>$")
    if p2.match(s):
        node.addFlag(zhihuanswer.FLAG_QUOTE)
        s = p2.match(s).group(1)
       
    return node    

def _parseimagenode(s, nodes):
    node = ImageNode()
    m = re.compile("^<noscript><img\\s((?:.+?=\".+?\")*)>(.*?)</noscript><img.+?>\\2$").match(s)
    pp = re.compile("([^\\s]+?)=\"(.+?)\"")
    if m:
        node.title = m.group(2)
        if m.group(1):
            for m2 in pp.finditer(m.group(1)):
                node.addProperty(m2.group(1), m2.group(2))
    return node

def _parselinknode(s, nodes):
    node = LinkNode()

    m = re.compile("^<a.+?href=\"//link.zhihu.com/\?target=(.+?)\".*?>(.*?)(?=<).*?</a>$|"
            "^<a.+?href=\"(.+?)\".+?>(.*?)</a>$").match(s)
    if m:
        g = m.groups()
        if g[0]:
            node.url = _replacehtmltransfer(g[0])
            node.text = g[1]
        else:
            node.url = g[2]
            node.text = g[3]
            
    return node

def _parsehtmlnode(s, nodes):
    m = re.compile("^<([pub]|blockquote)>(.*)</\\1>$").match(s)
    flag = 0
    if m:
        tag = m.group(1)

        if tag == "p":
            flag = (flag | zhihuanswer.FLAG_PARAGRAPH)
        elif tag == "u":
            flag = (flag | zhihuanswer.FLAG_UNDERLINED)
        elif tag == "b":
            flag = (flag | zhihuanswer.FLAG_BOLD)
        elif tag == "blockquote":
            flag = (flag | zhihuanswer.FLAG_QUOTE)
        
        nodes[0].addFlag(flag)
    return nodes[0]


def _parseplaintextnode(s, nodes):
    return PlainTextNode(s)

def _parsegroup(s, nodes):
    if len(nodes) == 1:
        return nodes[0]
    node = NodeGroup()
    node.nodes = nodes
    return node

def _groupsplit(s):
    basic = re.compile("<noscript><img.+?>(.*?)</noscript><img.+?>\\1|"
                       "<([puba]|blockquote)(?:\\s.+?)?>.*?</\\2>|"
                       ".+?(?=<[puba]>|<[puba]\\s|<blockquote>|<noscript>)|"
                       ".+$")
    return map(lambda x : x.group(), basic.finditer(s))    

def _func2(s):
    ge = re.compile("<br>|.+?(?=<br>)|.+$")
    return map(lambda x : x.group(), ge.finditer(s))

def _funcn(s):
    m = re.compile("^<([pub]|blockquote)>(.*)</\\1>$").match(s)
    if m:
        return (m.group(2), )
    return ()

_rules = {
    "r0":
    {
        "m":lambda x: True,
        "parser":_parseplaintextnode
        },
    "r_image":
    {        
        "m":lambda x: re.compile(
            "^<noscript><img\\s((?:.+?=\".+?\")*)>(.*?)</noscript><img.+?>\\2$"
            ).match(x) != None,
        "parser":_parseimagenode
        },
    "r_link":
    {        
        "m":lambda x: re.compile(
            "^<a.+?href=\"//link.zhihu.com/\?target=(.+?)\".*?>(.*?)(?=<).*?</a>$|"
            "^<a.+?href=\"(.+?)\".+?>(.*?)</a>$").match(x) != None,   
        "parser":_parselinknode        
        },
    "r_html_node":
    {
        "m":lambda x: re.compile("^<([pub]|blockquote)(?:\\s.+?)?>(.*?)</\\1>$").match(x)!= None and
        re.compile("<([pub]|blockquote)(?:\\s.+?)?>.*?</\\1>.*?</\\1>$").match(x) == None,
        "parser":_parsehtmlnode,
        "g":_funcn,
        "rules":("r_html_node", "r_link", "r1")
        },
    "r_text":
    {
        "m":lambda x: re.compile("^(<br>|[^<]).*$").match(x) != None,
        "rules":("r_br", "r0"),
        "parser":_parsetextnode,
        "g":_func2
        },
    "r1":
    {
        "m":lambda x: True,
        "rules":("r_image", "r_link", "r_html_node", "r_text"),
        "g":_groupsplit,
        "parser":_parsegroup
        },
    "r_br":
    {
        "m":lambda x : x == "<br>",
        "parser":lambda x, y:ChangeLine()
        }
    }

def _conditionprint(s1, s2, s3, i):    
    if i == -1:
        print("parsing:%s using rule:%s, parent:%s"%(s1, s2, s3))

def _parseAnswer(s, rule, depth = 0):
    r = _rules[rule]
    if r:
        if r["m"](s):
            nodes = []
            if "g" in r:                
                for subString in r["g"](s):
                    flag = False
                    for rr in r["rules"]:                
                        if _rules[rr]["m"](subString):
                            _conditionprint(subString, rr, rule, depth + 1)
                            nodes.append(_parseAnswer(subString, rr, depth + 1))
                            flag = True
                            break
                    if not flag:
                        _conditionprint(subString, "r0", rule, depth + 1)                 
                        nodes.append(_parseAnswer(subString, "r0", depth + 1))
                        
            node = r["parser"](s, nodes)
            return node
    return ErrorNode(s)             

def parseAnswer(s):
    s1 = _getanswerstr(s)
    if s1:
        ans = ZhihuAns()
        ans.root = _parseAnswer(s1, "r1")
        return ans
