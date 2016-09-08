#encoding:utf-8

import os
import re
import time
from tornado import httpclient

class _config(dict):

    def __getattr__(self, attr):
        if attr in self:
            return self[attr]

        return None

config = _config()
config['width'] = 640
config['top_padding'] = 50
config['left_padding'] = 20
config['right_padding'] = 20
config['bottom_padding'] = 50
config['line_spacing'] = 5
config['save_tmp_text'] = True

def _downloadanswer(url):
    client = httpclient.HTTPClient()
    try:
        response = client.fetch(url)
    except httpclient.HTTPError as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        return None

    if response:
        s = str(response.body, 'utf-8')
        return s

def _gettmpfilename():    
    timestamp = time.strftime(r'%Y%m%d%H%M%S', time.localtime())
    return timestamp + ".txt"

def _saveanswer(filepath, content):
    file = open(filepath, 'w', encoding='utf-8')
    file.write(content)
    file.close()

def _gettmppath():
    if not os.path.exists('/Users/Administrator/Desktop/Tmp'):
        os.mkdir('/Users/Administrator/Desktop/Tmp')

    return '/Users/Administrator/Desktop/Tmp'

config['tmp_dir'] = _gettmppath()
config['outputpath'] = _gettmppath()

def content(url):
    filename = os.path.join(_gettmppath(), _gettmpfilename())
    client = httpclient.HTTPClient()
    try:
        response = client.fetch(url)
        if response.body:
            file = open(filename, 'wb')
            file.write(response.body)
            file.close()
            return response.body
    except httpclient.HTTPError as e:
        print(e)
        return None
    except Exception as e:
        print(e)
        return None
    return None    

def save(answerurl):
    buffer = content(answerurl)
    if buffer:
        c = str(buffer, 'utf-8')
        p = re.compile('<div class="zm-editable-content clearfix">(.+?)</div>', re.S)
        m = p.search(c)
        if m:
            a = m.group().replace('\n', '')
            if a:
                from how_i_save_zhihu_answers.zhihuparsers import AnswerParser
                ans = AnswerParser().parse(a)
                ans.title = re.compile('<title>(.+?)</title>').search(c).group(1)

                from how_i_save_zhihu_answers.draw import AnswerDraw
                from how_i_save_zhihu_answers.builders import ImageBuilder
                AnswerDraw(ans, ImageBuilder(), config).draw()
        

def img(answerurl):
    buffer = content(answerurl)
    if buffer:
        c = str(buffer, 'utf-8')
        p = re.compile('<div class="zm-editable-content clearfix">(.+?)</div>', re.S)
        m = p.search(c)
        if m:
            a = m.group().replace('\n', '')
            if a:
                from how_i_save_zhihu_answers.zhihuparsers import AnswerParser
                ans = AnswerParser().parse(a)

                from how_i_save_zhihu_answers.draw import AnswerImgDownload
                from how_i_save_zhihu_answers.builders import ImageBuilder
                AnswerImgDownload(ans, ImageBuilder(), config).download()


__all__ = ['config', 'saveimage', 'img']
    
