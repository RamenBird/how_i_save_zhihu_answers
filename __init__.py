from how_i_save_zhihu_answers.answerdrawer import AnswerDrawer
from tornado import httpclient
class _config(dict):

    def __getattr__(self, attr):
        if attr in self:
            return self[attr]

        return 0
config = _config()
config['width'] = 640
config['top_padding'] = 50
config['left_padding'] = 20
config['right_padding'] = 20
config['bottom_padding'] = 50
config['line_spacing'] = 5
config['tmp_dir'] = "C:/Users/Administrator/Desktop/tmp_dir"
config['save_tmp_text'] = FALSE

__all__ = ['config', 'save']

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
        if config["save_tmp_text"]:
            _saverawanswer(s)
        return s

def save(url):
    rawstring = _downloadanswer(url)
    drawer = answerdrawer.Answer().default()
