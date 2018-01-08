# encoding: utf-8
from cook.common.Curl import Curl
from bs4 import BeautifulSoup
import time
import sys


def wordInfo(word):
    url = 'https://baike.baidu.com/item/' + word
    request_res = {'status': 0, 'body': ''}
    while (1):
        request_res = Curl().get(url)

        try:
            location = request_res['header']['Location']
        except KeyError:
            location = ''

        if location:
            url = 'https://baike.baidu.com' + location
        else:
            break

    # print request_res
    if request_res['status'] == 200:
        body = request_res['body']

        soup = BeautifulSoup(body, "html5lib")  # pip install html5lib
        names = soup.find_all("dt", class_="basicInfo-item name")

        values = soup.find_all("dd", class_="basicInfo-item value")

        value_list = {}
        if len(names) == len(values):
            for index, name in enumerate(names):
                name = name.get_text().replace(u'\xa0', '')
                value = values[index].get_text().replace(u'\xa0', '').replace(u'\n', '')
                value_list[name] = value

        result = {'wubi': '', 'pinyin': '', 'bihua': ''}

        for name, value in value_list.items():
            # print name, value
            if name.find(u'\u4e94\u7b14') >= 0:
                result['wubi'] = value
            elif name == u'\u62fc\u97f3':
                result['pinyin'] = value
            elif name.find(u'\u603b\u7b14\u753b') >= 0:
                result['bihua'] = value

        return result


file_obj = open('chinese.txt')
words = file_obj.read().splitlines()
for word in words:
    word_info = wordInfo(word[0:3])
    print word[0:3], word_info
    # break
    time.sleep(3)
